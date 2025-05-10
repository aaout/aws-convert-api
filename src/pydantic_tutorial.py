from pydantic import BaseModel
from pydantic import ValidationError


class User(BaseModel):
    name: str
    age: int
    email: str


# 正しいデータの場合
valid_data = {"name": "Alice", "age": 25, "email": "alice@example.com"}
user = User(**valid_data)
print(user)

# 間違ったデータの場合
# invalid_data = {"name": "Bob", "age": "not a number", "email": "bob@example.com"}
# try:
#     user = User(**invalid_data)
# except ValidationError as e:
#     print("Validation Error:")
#     print(e)
