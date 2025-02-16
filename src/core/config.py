"""
Configuration module for the application.

This module defines the Settings class using pydantic for managing
application configuration through environment variables.
"""

from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Settings class to manage application configuration using environment variables.

    This class uses pydantic to define and validate configuration settings.
    It loads values from environment variables, with some having default values.

    Attributes:
        SONAR_QUBE_URL: str = Field(..., env="SONAR_QUBE_URL")
        SONAR_QUBE_AUTH_TOKEN: str = Field(..., env="SONAR_QUBE_AUTH_TOKEN")
        SONAR_QUBE_PROJECT_KEY: str = Field(..., env="SONAR_QUBE_PROJECT_KEY")
    """

    SONAR_QUBE_URL: str = Field(..., env="SONAR_QUBE_URL")
    SONAR_QUBE_AUTH_TOKEN: str = Field(..., env="SONAR_QUBE_AUTH_TOKEN")
    SONAR_QUBE_PROJECT_KEY: str = Field(..., env="SONAR_QUBE_PROJECT_KEY")

    class Config:
        """Configuration for the Settings class."""

        env_file = ".env"
        env_file_encoding = "utf-8"


# Instantiate the settings
settings = Settings()
