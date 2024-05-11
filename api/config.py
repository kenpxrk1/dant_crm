from dataclasses import dataclass
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict



dotenv_path = Path(__file__).parent.parent.joinpath(".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

@dataclass
class DBConfig():

    """ Database config class"""  
    def __init__(self) -> None:
        self.__DB_HOST: str = os.getenv("DB_HOST")
        self.__DB_PORT: str = os.getenv("DB_PORT")
        self.__DB_USER: str = os.getenv("DB_USER")
        self.__DB_PASS: str = os.getenv("DB_PASS")
        self.__DB_NAME: str = os.getenv("DB_NAME")

    @property
    def DB_HOST(self):
        return self.__DB_HOST
    
    @property 
    def DB_PORT(self):
        return self.__DB_PORT
    
    @property
    def DB_USER(self):        
        return self.__DB_USER
    
    @property
    def DB_PASS(self):
        return self.__DB_PASS
    
    @property
    def DB_NAME(self):
        return self.__DB_NAME
    


    @property
    def DATABASE_URL(self) -> str:
        """
        Returns a string for bd connection
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

 
db_settings = DBConfig() # DBConfig object. ! Must be single


@dataclass
class AuthConfig():

    """ Authorization config class """

    def __init__(self):
        self.__SECRET_KEY: str = os.getenv("SECRET_KEY")
        self.__ALGORITHM: str = os.getenv("ALGORITHM")
        self.__ACCESS_TOKEN_EXPIRE_MINUTES: str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

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


