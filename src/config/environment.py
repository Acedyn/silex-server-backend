########################################
## Config classes to store configuration variables according to the environment
########################################

from dataclasses import dataclass, field
import os


@dataclass
class Config:
    DB_HOST: str = field(default="localhost")
    DB_PORT: str = field(default="5432")
    DB_USER: str = field(default="pipeline")
    DB_PASSWORD: str = field(default="pipeline")
    DB_NAME: str = field(default="silex")


@dataclass
class ConfigDev(Config):
    DB_HOST: str = field(default="silex-db-dev")


@dataclass
class ConfigBeta(Config):
    DB_HOST: str = field(default="silex-db-prod")


@dataclass
class ConfigProd(Config):
    DB_HOST: str = field(default="silex-db-prod")


# Get the environment variable SILEX_BACKEND_CONFIG to set the right config
environment_config = str(os.environ.get("SILEX_BACKEND_CONFIG")).lower()

if environment_config == "dev" or environment_config == "development":
    config = ConfigDev()
elif environment_config == "beta":
    config = ConfigBeta()
elif environment_config == "prod" or environment_config == "production":
    config = ConfigProd()
else:
    config = Config()
