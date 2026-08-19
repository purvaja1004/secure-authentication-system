import jwt
import datetime
from config import SECRET_KEY

def generate_token(email):
    return jwt.encode(
        {
            "email": email,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )


def verify_token(token):
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"]
    )