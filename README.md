# GazeHum

GazeHum is a Streamlit-based attendance platform that combines face recognition, voice enrollment, and Supabase-backed persistence to support classroom attendance workflows. The project is structured for teacher and student journeys, with shareable class links and QR-based onboarding.

Live app: [https://intelligentaiattendancesystem-fav7ycvbcme4zvjltrgjjx.streamlit.app](https://intelligentaiattendancesystem-fav7ycvbcme4zvjltrgjjx.streamlit.app)

## Key Capabilities

- Separate student and teacher interfaces
- Face-based student enrollment and login
- Optional voice enrollment for attendance support
- Subject creation, sharing, and attendance tracking
- QR code generation for class join links
- Supabase storage for application data

## Technology Stack

- [Streamlit](https://streamlit.io/)
- [Supabase](https://supabase.com/)
- [scikit-learn](https://scikit-learn.org/)
- [dlib](http://dlib.net/) and `face_recognition_models`
- [Pillow](https://python-pillow.org/)
- [segno](https://segno.readthedocs.io/)
- [librosa](https://librosa.org/)
- [resemblyzer](https://github.com/resemble-ai/Resemblyzer)

## Application Overview

The application starts in `app.py`, where Streamlit configures the page title and app icon from `asserts/image.png`. Navigation is driven by session state and query parameters, allowing teachers and students to move through dedicated flows and enabling join links like `?join-code=INT354` for quick class enrollment.

## Getting Started

### Prerequisites

- Python 3.10 or newer
- A virtual environment tool such as `venv`
- A Supabase project with credentials

### Installation

1. Clone the repository and open the project directory.
2. Create and activate a virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

Create `.streamlit/secrets.toml` and add your Supabase credentials plus the deployed app URL used for generated join links:

```toml
SUPABASE_URL="https://your-project-id.supabase.co"
SUPABASE_KEY="your-supabase-anon-key"
APP_BASE_URL="https://intelligentaiattendancesystem-fav7ycvbcme4zvjltrgjjx.streamlit.app"
```

`APP_BASE_URL` is especially important because class share links are generated from that value.

### Run Locally

```bash
streamlit run app.py
```

## Project Structure

- `app.py` - Streamlit entry point and page configuration
- `src/screens/` - Home, teacher, and student screens
- `src/components/` - Shared UI elements, dialogs, and page sections
- `src/database/` - Supabase configuration and database helpers
- `src/pipelines/` - Face and voice processing pipelines
- `src/ui/` - Shared layout and styling utilities
- `asserts/` - Local static images and branding assets

## Sharing Class Links

Teachers can generate shareable class links and QR codes from the teacher flow. Links are built from `APP_BASE_URL` and the subject join code, for example:

```text
https://intelligentaiattendancesystem-fav7ycvbcme4zvjltrgjjx.streamlit.app/?join-code=INT354
```

If you move the deployment to a new Streamlit app URL, update `APP_BASE_URL` so all new links point to the correct location.

## Troubleshooting

- If the app cannot connect to Supabase, verify `SUPABASE_URL` and `SUPABASE_KEY` in `.streamlit/secrets.toml`.
- If join links open the wrong deployment, confirm `APP_BASE_URL` matches the active Streamlit app.
- If the browser shows an access error, verify the Streamlit deployment is public and that the correct app URL is being used.
- If face recognition startup feels slow, the first run may take longer while models and dependencies initialize.

## Notes

- Keep `.streamlit/secrets.toml` out of version control.
- The app icon and branding image are stored in `asserts/image.png`.
- The project uses Streamlit session state to manage login and navigation.