# Reddit User Persona Generator

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. (Optional) Set up OpenAI API key for LLM persona generation:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

## Usage

Run the script with a Reddit user profile URL:

```bash
python reddit_user_persona.py https://www.reddit.com/user/kojied/
```

- Output persona files will be saved in the `personas/` directory.
- Each persona will cite the posts/comments used for extracting information.

## Notes
- Requires Python 3.7 or higher.
- You may need Reddit API credentials for full access (see PRAW documentation).
