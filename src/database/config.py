import os

import streamlit as st
from supabase import Client, create_client
from streamlit.errors import StreamlitSecretNotFoundError


def _get_secret(name: str) -> str:
    value = os.getenv(name)
    if value:
        return value

    try:
        if name in st.secrets:
            return st.secrets[name]
    except StreamlitSecretNotFoundError:
        pass

    raise RuntimeError(
        f"Missing required Supabase secret: {name}. Add it to .streamlit/secrets.toml or set an environment variable."
    )


supabase: Client = create_client(
    _get_secret("SUPABASE_URL"),
    _get_secret("SUPABASE_KEY"),
)