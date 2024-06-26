from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import EmailStr




dotenv_path = Path(__file__).parent.parent.joinpath(".env-prod")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@dataclass
class DBConfig:
    """Database config class"""

    def __init__(self) -> None:
        self.__DB_HOST: str = os.getenv("DB_HOST")
        self.__DB_PORT: str = os.getenv("DB_PORT")
        self.__DB_USER: str = os.getenv("DB_USER")
        self.__DB_PASS: str = os.getenv("DB_PASS")
        self.__DB_NAME: str = os.getenv("DB_NAME")

    @property
    def DATABASE_URL(self) -> str:
        """
        Returns a string for bd connection
        """
        return f"postgresql+asyncpg://{self.__DB_USER}:{self.__DB_PASS}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DB_NAME}"


db_settings = DBConfig()  # DBConfig object. ! Must be single


@dataclass
class TestDBConfig:
    def __init__(self) -> None:
        self.__DB_HOST: str = os.getenv("TEST_DB_HOST")
        self.__DB_PORT: str = os.getenv("TEST_DB_PORT")
        self.__DB_USER: str = os.getenv("TEST_DB_USER")
        self.__DB_PASS: str = os.getenv("TEST_DB_PASS")
        self.__DB_NAME: str = os.getenv("TEST_DB_NAME")

    @property
    def TEST_DATABASE_URL(self) -> str:
        """
        Returns a string for test bd connection
        """
        print(f"postgresql+asyncpg://{self.__DB_USER}:{self.__DB_PASS}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DB_NAME}")
        return f"postgresql+asyncpg://{self.__DB_USER}:{self.__DB_PASS}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DB_NAME}"


test_db_settings = TestDBConfig()


@dataclass
class AuthConfig:
    """Authorization config class"""

    def __init__(self):
        self.__SECRET_KEY: str = os.getenv("SECRET_KEY")
        self.__ALGORITHM: str = os.getenv("ALGORITHM")
        self.__ACCESS_TOKEN_EXPIRE_MINUTES: str = os.getenv(
            "ACCESS_TOKEN_EXPIRE_MINUTES"
        )

    @property
    def SECRET_KEY(self):
        return self.__SECRET_KEY

    @property
    def ALGORITHM(self):
        return self.__ALGORITHM

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self):
        return self.__ACCESS_TOKEN_EXPIRE_MINUTES


auth_config = AuthConfig()


@dataclass
class SuperUserConfig:
    def __init__(self):
        self.__login: EmailStr = os.getenv("login")
        self.__password: str = os.getenv("password")
        self.__name: str = os.getenv("name")
        self.__surname: str = os.getenv("surname")
        self.__role: str = os.getenv("role")

    @property
    def super_user_data(self):
        """returns super_user_data from .env"""

        return {
            "login": self.__login,
            "password": self.__password,
            "name": self.__name,
            "surname": self.__surname,
            "role": self.__role,
        }


super_user = SuperUserConfig()


@dataclass
class RabbitConfig:
    def __init__(self):
        self.__RABBIT_URL = os.getenv("RABBIT_URL")

    @property
    def RABBITMQ_URL(self):
        return self.__RABBIT_URL


rabbit_config = RabbitConfig()


@dataclass
class EmailConfig:
    def __init__(self):
        self.__APP_EMAIL: EmailStr = os.getenv("APP_EMAIL")
        self.__SECRET_EMAIL: str = os.getenv("SECRET_EMAIL")

    @property
    def APP_EMAIL(self):
        return self.__APP_EMAIL

    @property
    def SECRET_MAIL(self):
        return self.__SECRET_EMAIL


email_config = EmailConfig()
