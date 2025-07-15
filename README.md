# Reddit User Persona Generator

## 🛠️ Project Setup & Run Instructions

 1. Clone the Repository
```bash
git clone <your-repo-url>
cd BeyondChats-Assignment-Generative-AI-
```

 2. Create a Virtual Environment (Recommended)
```bash
python -m venv venv
# Activate the virtual environment:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

 3. Install Dependencies
```bash
pip install -r requirements.txt
```

 4. (Optional) Set Up API Keys
- For OpenAI persona generation, set your API key:
  ```bash
  set OPENAI_API_KEY=your_openai_api_key  # On Windows
  export OPENAI_API_KEY=your_openai_api_key  # On Mac/Linux
  ```

 5. Apply Database Migrations
```bash
python manage.py migrate
```

 6. Run the Development Server
```bash
python manage.py runserver
```
- Open your browser and go to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

 7. (Optional) Create a Superuser for Admin
```bash
python manage.py createsuperuser
```

---

**Notes:**
- Requires Python 3.7 or higher.
- You may need Reddit API credentials for full access (see PRAW documentation).
- Output persona files (if any) will be saved in the `personas/` directory.

## Example: Running the Django Server

When you run the server with:
```sh
python manage.py runserver
```
You should see output similar to this:

```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
July 15, 2025 - 21:35:06
Django version 4.2.7, using settings 'redditpersona_web.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
[15/Jul/2025 21:35:11] "GET / HTTP/1.1" 200 6073
Not Found: /favicon.ico
[15/Jul/2025 21:35:13] "GET /favicon.ico HTTP/1.1" 404 2244
[15/Jul/2025 21:46:35] "GET / HTTP/1.1" 200 6073
[15/Jul/2025 21:49:08] "POST / HTTP/1.1" 200 40819
[15/Jul/2025 21:49:29] "POST / HTTP/1.1" 200 53352
[15/Jul/2025 22:16:20] "GET / HTTP/1.1" 200 6073
[15/Jul/2025 22:19:10] "POST / HTTP/1.1" 200 40819
[15/Jul/2025 22:19:19] "POST / HTTP/1.1" 200 58102
[15/Jul/2025 22:20:40] "POST / HTTP/1.1" 200 59042
[15/Jul/2025 22:22:17] "POST / HTTP/1.1" 200 58822
[15/Jul/2025 22:26:57] "POST / HTTP/1.1" 200 57742
```

This means your server is running successfully and is receiving requests from your browser.
