"""
User Model — Core Entity

Columns:
    id          : UUID (primary key, server-generated)
    email       : str (unique, indexed, not null)
    hashed_password : str (bcrypt hash, not null)
    full_name   : str (optional)
    is_active   : bool (default True, for soft-delete)
    is_superuser: bool (default False)
    created_at  : datetime (server-generated UTC)
    updated_at  : datetime (auto-updated UTC)
"""
