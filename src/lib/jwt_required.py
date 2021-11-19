from quart import request, current_app, g
from src.lib.api_error import APIError
from functools import wraps
from dataclasses import dataclass
from datetime import datetime
import jwt


@dataclass
class User:
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    hashed_password: str
    created_at: datetime


async def get_user_by_id(id: int):
    """
    Fake get_user_by_id function
    """
    return User(
        id,
        "test@example.com",
        "John",
        "Doe",
        True,
        "3748shfjdhsajdkhfkajsdf",
        datetime.now(),
    )


def decode_token(token) -> dict:
    try:
        decoded = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            issuer="api",
            algorithms=["HS256"],
        )
        return decoded
    except jwt.ExpiredSignatureError:
        raise APIError(401, "TOKEN_EXPIRED")
    except jwt.InvalidIssuerError:
        raise APIError(401, "TOKEN_INVALID_ISSUER")
    except jwt.DecodeError:
        raise APIError(401, "TOKEN_INVALID")


# JWT required decorator
def jwt_required(f):
    """
    This function will make sure the request headers contains a valid JWT.
    Headers:
        Authorization: Bearer <token>
    """

    @wraps(f)
    async def decorated_function(*args, **kwargs):
        # Check if the headers contain a valid Authorization header
        if "Authorization" in request.headers:
            if "Bearer" in request.headers.get("Authorization"):
                token = request.headers.get("Authorization").split()[
                    1
                ]  # The format expected is Bearer <token>
                decoded = decode_token(token)
                result = await get_user_by_id(decoded["id"])
                # Throws an error if the user doesn't exist or isn't active
                if result is None:
                    raise APIError(401, "USER_NOT_FOUND")
                if not result.active:
                    return APIError(401, "USER_NOT_ACTIVE")
                g.user = result
            else:
                raise APIError(401, "INVALID_AUTHORIZATION_SCHEME")
        else:
            raise APIError(401, "MISSING_JWT_TOKEN")
        return f(*args, **kwargs)

    return decorated_function
