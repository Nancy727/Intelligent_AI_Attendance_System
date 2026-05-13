import streamlit as st


from supabase import create_client, Client

supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


@st.cache_data(ttl=300)
def test_supabase_connection():
    """Test if Supabase is reachable and return diagnostic info."""
    try:
        # Try a simple query
        response = supabase.table('teachers').select('count', count='exact').limit(0).execute()
        return True, "Connected successfully"
    except Exception as e:
        error_msg = str(e)
        if 'getaddrinfo' in error_msg or 'ConnectError' in error_msg:
            return False, f"Network/DNS error: Cannot reach Supabase. Check internet connection or Supabase URL: {st.secrets.get('SUPABASE_URL', 'N/A')}"
        elif 'timeout' in error_msg.lower():
            return False, "Supabase connection timeout. The server is not responding."
        else:
            return False, f"Supabase error: {error_msg}"
