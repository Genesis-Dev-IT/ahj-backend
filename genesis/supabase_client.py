import os
from supabase import create_client, Client

URL: str = os.getenv("SUPABASE_URL")
KEY: str = os.getenv("SERVICE_KEY")

# Singleton for the Supabase client
_supabase_client: Client | None = None


def get_supabase_client():
    # Initializing and returning the Supabase client singleton.
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(URL, KEY)
    return _supabase_client
