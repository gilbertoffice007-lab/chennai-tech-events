from supabase import create_client

from .config import (
    SUPABASE_URL,
    SUPABASE_KEY
)


_supabase = None


def get_supabase():
    """Return the singleton Supabase client, creating it on first use."""
    global _supabase
    if _supabase is None:
        if not SUPABASE_URL:
            raise ValueError("SUPABASE_URL is missing.")
        if not SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY is missing.")
        _supabase = create_client(
            SUPABASE_URL,
            SUPABASE_KEY
        )
    return _supabase


# Backwards-compatible alias — modules that do
# ``from .supabase_client import supabase`` will get a proxy
# that lazily resolves to the real client.
class _SupabaseProxy:
    """Lazily delegate every attribute access to the real client."""

    def _client(self):
        return get_supabase()

    def __getattr__(self, name):
        # Re-raise a clear error if credentials are missing
        return getattr(self._client(), name)


supabase = _SupabaseProxy()
