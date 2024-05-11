from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashingMixin:

    @staticmethod
    def hasher(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)