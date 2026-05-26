from utils.jwt_handler import generate_token

token = generate_token(
    1,
    "nimisha@gmail.com",
    "citizen"
)

print(token)