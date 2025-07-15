from django.shortcuts import render
from django import forms
import praw
import requests
import os
from collections import Counter
import re
import openai
from dotenv import load_dotenv
import json

class RedditProfileForm(forms.Form):
    profile_url = forms.CharField(label='Reddit Profile URL', max_length=200)


def extract_username(profile_url):
    match = re.search(r"reddit.com/user/([A-Za-z0-9_\-]+)/?", profile_url)
    if match:
        return match.group(1)
    else:
        return None


def fetch_user_data(username, limit=10):
    reddit = praw.Reddit(
        client_id="-2PWxzDgJLpLmOcUCjnl3A",
        client_secret="ZpRU680ehbNejdKpcZbsMsXN14o6dA",
        user_agent="user_persona_script"
    )
    user = reddit.redditor(username)
    posts = []
    comments = []
    try:
        for submission in user.submissions.new(limit=limit):
            posts.append({
                'title': submission.title,
                'selftext': submission.selftext,
                'subreddit': str(submission.subreddit),
                'permalink': f"https://www.reddit.com{submission.permalink}"
            })
        for comment in user.comments.new(limit=limit):
            comments.append({
                'body': comment.body,
                'subreddit': str(comment.subreddit),
                'permalink': f"https://www.reddit.com{comment.permalink}"
            })
        profile_pic = getattr(user, 'icon_img', None)
    except Exception as e:
        return [], [], None, str(e)
    return posts, comments, profile_pic, None


def rule_based_persona(posts, comments, username, profile_pic=None):
    # Collect all text
    all_text = ' '.join([p['title'] + ' ' + p['selftext'] for p in posts] + [c['body'] for c in comments])
    words = re.findall(r'\w+', all_text.lower())
    stopwords = set(['the','and','to','a','of','in','is','it','for','on','that','this','with','as','was','but','are','be','at','by','an','or','from','so','if','not','have','has','i','you','my','me','we','they','he','she','his','her','their','our','your','just','do','did','can','will','would','should','could'])
    filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
    word_counts = Counter(filtered_words)
    top_words = word_counts.most_common(7)

    # Subreddit stats
    subreddits = [p['subreddit'] for p in posts] + [c['subreddit'] for c in comments]
    subreddit_counts = Counter(subreddits)
    top_subreddits = subreddit_counts.most_common(3)

    # Activity
    total_posts = len(posts)
    total_comments = len(comments)
    avg_post_len = sum(len(p['selftext']) for p in posts) / total_posts if total_posts else 0
    avg_comment_len = sum(len(c['body']) for c in comments) / total_comments if total_comments else 0

    # Simple interests/traits
    interests = ', '.join([w[0] for w in top_words])
    active_subs = ', '.join([f"{s[0]} ({s[1]})" for s in top_subreddits])
    writing_style = "Long-form" if avg_post_len > 200 else "Short-form"
    comment_style = "Detailed" if avg_comment_len > 100 else "Brief"

    # Persona fields (heuristics and placeholders)
    persona = {
        "name": username.capitalize(),
        "photo_url": profile_pic or "https://www.redditstatic.com/avatars/avatar_default_02_24A0ED.png",  # Use Reddit profile pic if available
        "age": 28,  # Placeholder or could be guessed
        "occupation": "Redditor",  # Placeholder
        "status": "Active",
        "location": "Internet",  # Placeholder
        "tier": "Enthusiast",  # Placeholder
        "archetype": "The Explorer",  # Placeholder
        "traits": ["Practical", "Adaptable", writing_style, comment_style],
        "motivations": {
            "Convenience": 80,
            "Wellness": 60,
            "Speed": 70,
            "Preferences": 50,
            "Comfort": 40,
            "Dietary Needs": 90,
        },
        "personality": {
            "Introvert-Extrovert": 40,
            "Intuition-Sensing": 60,
            "Feeling-Thinking": 50,
            "Perceiving-Judging": 70,
        },
        "behaviour_habits": [
            f"Frequently posts about {interests.split(',')[0] if interests else 'varied topics'}.",
            f"Most active in {', '.join([s[0] for s in top_subreddits])}.",
            f"{writing_style} posts, {comment_style} comments.",
            f"Posts per fetch: {total_posts}, Comments per fetch: {total_comments}.",
        ],
        "frustrations": [
            "Sometimes struggles to find relevant discussions.",
            "Wishes for more engagement on posts.",
            "Occasional difficulty navigating subreddit rules.",
        ],
        "goals_needs": [
            "To connect with like-minded individuals.",
            "To share and gain knowledge on favorite topics.",
            "To have a positive and engaging Reddit experience.",
        ],
        "quote": f"I want to spend more time discussing {interests.split(',')[0] if interests else 'interesting topics'} and less time searching for good conversations.",
    }
    return persona


def openai_persona(posts, comments, username, profile_pic=None):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompt = f"""
    Analyze the following Reddit posts and comments and generate a persona in this JSON format:
    {{
        "name": "",
        "age": "",
        "occupation": "",
        "status": "",
        "location": "",  # If possible, infer from content; else 'Unknown'
        "tier": "",
        "archetype": "",
        "traits": [],
        "photo_url": "{profile_pic or 'https://randomuser.me/api/portraits/men/1.jpg'}",
        "quote": "",
        "motivations": {{}},
        "personality": {{}},
        "behaviour_habits": [],
        "frustrations": [],
        "goals_needs": []
    }}
    If possible, infer the user's likely location from their posts, comments, or flair. If not clear, use 'Unknown'.
    Posts: {posts}
    Comments: {comments}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a UX researcher and persona generator."},
                {"role": "user", "content": prompt}
            ]
        )
        persona = json.loads(response.choices[0].message['content'])
        persona["photo_url"] = profile_pic or persona.get("photo_url")
        return persona
    except Exception as e:
        return None


def reddit_profile_view(request):
    posts = comments = error = persona = profile_pic = None
    if request.method == 'POST':
        form = RedditProfileForm(request.POST)
        if form.is_valid():
            profile_url = form.cleaned_data['profile_url']
            username = extract_username(profile_url)
            if not username:
                error = 'Invalid Reddit profile URL.'
            else:
                posts, comments, profile_pic, fetch_error = fetch_user_data(username)
                if fetch_error:
                    error = fetch_error
                elif 'generate_persona' in request.POST:
                    persona = openai_persona(posts, comments, username, profile_pic)
                    if not persona:
                        persona = rule_based_persona(posts, comments, username, profile_pic)
    else:
        form = RedditProfileForm()
    return render(request, 'redditpersona/profile.html', {
        'form': form,
        'posts': posts,
        'comments': comments,
        'persona': persona,
        'error': error,
    })
