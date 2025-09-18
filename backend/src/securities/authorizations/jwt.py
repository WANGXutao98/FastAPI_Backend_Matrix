import datetime

from jose import jwt as jose_jwt
from src.config.manager import settings
from src.models.schemas.jwt import JWToken


class JWTGenerator:
    @staticmethod
    def __init__():
        pass

    @staticmethod
    def _generate_jwt_token(*, jwt_data: dict[str, str], expires_delta: datetime.timedelta | None = None) -> str:
        to_encode = jwt_data.copy()

        if expires_delta:
            expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta

        else:
            expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=settings.JWT_MIN)
        to_encode.update(JWToken(exp=expire, sub=settings.JWT_SUBJECT).model_dump())
        return jose_jwt.encode(to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()
