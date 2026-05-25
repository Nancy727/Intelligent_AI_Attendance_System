# ai-attendance-project-app

## Streamlit UI setup

The app now expects a local icon at `assets/Screenshot 2026-05-15 152619.png` and uses a shared custom CSS layer for the academic theme.

If you add or replace configuration files, keep these in sync:

1. Create `.streamlit/config.toml` to define the Streamlit theme colors and default font.
2. Keep the shared CSS injection in `src/ui/base_layout.py` imported from every screen so the portal styling stays consistent.
3. If you rename or replace the icon asset, update `app.py` and `src/components/header.py` to point to the new local file.

The existing ML pipelines and Supabase database functions are unchanged.