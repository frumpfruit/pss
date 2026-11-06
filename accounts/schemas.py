from ninja import Schema


class UserOut(Schema):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool


class UserMessage(Schema):
    detail: str