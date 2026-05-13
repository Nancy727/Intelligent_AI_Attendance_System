# GazeHum

GazeHum is an AI-powered attendance system built with Streamlit, face recognition, voice enrollment, and Supabase.

## Features

- Student and teacher login flows
- FaceID-based student login and enrollment
- Voice enrollment for optional attendance support
- Subject management and attendance tracking
- Shareable class links and QR codes

## Tech Stack

- Streamlit
- Supabase
- dlib / face_recognition_models
- scikit-learn
- Pillow
- segno

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your Supabase credentials in `.streamlit/secrets.toml`:

```toml
SUPABASE_URL="https://your-project-id.supabase.co"
SUPABASE_KEY="your-supabase-anon-key"
APP_BASE_URL="https://your-deployed-app.streamlit.app"
```

4. Run the app:

```bash
streamlit run app.py
```

## Notes

- Keep `.streamlit/secrets.toml` out of git.
- If you deploy the app on Streamlit Cloud, set `APP_BASE_URL` to the deployed public URL so share links open the correct app.
- The app uses Supabase for teacher, student, subject, and attendance data.

## Project Structure

- `app.py` - Streamlit entry point
- `src/screens/` - Student and teacher screens
- `src/components/` - Dialogs, headers, footers, cards, and shared UI pieces
- `src/database/` - Supabase configuration and database helpers
- `src/pipelines/` - Face and voice processing logic
- `src/ui/` - Global styling helpers

## Troubleshooting

- If login fails, verify your Supabase URL and key in `.streamlit/secrets.toml`.
- If share links show access errors, confirm the deployed Streamlit app is public or that the viewer has access.
- If the UI feels slow, the first FaceID load may take longer because the models are initialized on demand.