from datetime import datetime, timedelta

from fastapi import status
from jose import ExpiredSignatureError, JWTError, jwt
from starlette.status import HTTP_401_UNAUTHORIZED

from core.config import config
from core.exceptions import CustomException
from core.utils.clean_str import clean_string


class JWTDecodeError(CustomException):
    status = HTTP_401_UNAUTHORIZED
    error_code = HTTP_401_UNAUTHORIZED
    message = "Invalid token"


class JWTExpiredError(CustomException):
    status = HTTP_401_UNAUTHORIZED
    error_code = HTTP_401_UNAUTHORIZED
    message = "Token expired"


class JWTHandler:
    secret_key = clean_string(config.SECRET_KEY)
    algorithm = clean_string(config.JWT_ALGORITHM)
    expire_minutes = config.JWT_EXPIRE_MINUTES

    @staticmethod
    def encode(payload: dict, expires: bool = True) -> str:
        """
        Encode a payload into a JWT token.
        :param payload: The data to encode into the token.
        :param expires: Whether the token should expire. If False, no expiration is added.
        :return: Encoded JWT token as a string.
        """
        if expires:
            expire = datetime.utcnow() + timedelta(minutes=JWTHandler.expire_minutes)
            payload.update({"exp": expire})
        return jwt.encode(
            payload, JWTHandler.secret_key, algorithm=JWTHandler.algorithm
        )

    @staticmethod
    def decode(token: str) -> dict:
        """
        Decode a JWT token and validate its expiration.
        :param token: The JWT token to decode.
        :return: Decoded payload as a dictionary.
        :raises JWTExpiredError: If the token is expired.
        :raises JWTDecodeError: If the token is invalid.
        """
        try:
            decoded_payload = jwt.decode(
                clean_string(token),
                JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
            )
            return decoded_payload
        except ExpiredSignatureError as exception:
            raise JWTExpiredError() from exception
        except JWTError as exception:
            raise JWTDecodeError() from exception

    @staticmethod
    def decode_expired(token: str) -> dict:
        """
        Decode a JWT token without verifying its expiration.
        :param token: The JWT token to decode.
        :return: Decoded payload as a dictionary.
        :raises JWTDecodeError: If the token is invalid.
        """
        try:
            decoded_payload = jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
                options={"verify_exp": False},
            )
            return decoded_payload
        except JWTError as exception:
            raise JWTDecodeError() from exception
