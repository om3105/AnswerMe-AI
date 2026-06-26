"""
User Repository — Data Access for User Entity

Methods:
    get_by_id(user_id: UUID) → User | None
    get_by_email(email: str) → User | None
    create(user_data: dict) → User
    update(user_id: UUID, update_data: dict) → User | None
    delete(user_id: UUID) → bool
    list_users(skip: int, limit: int) → list[User]

All methods are async and receive an AsyncSession via constructor injection.
"""
