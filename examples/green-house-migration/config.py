import os

from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


def get_required_env(key: str) -> str:
     """Obtener variable de entorno requerida."""
     value = os.getenv(key)
     if not value:
         raise ValueError(f"Variable de entorno {key} es requerida")
     return value


def get_optional_env(key: str, default: str = "") -> str:
     """Obtener variable de entorno opcional."""
     return os.getenv(key, default)


# Configuración de la API
GREENHOUSE_API_KEY = get_required_env("GREENHOUSE_API_KEY")
GREENHOUSE_API_URL = get_optional_env(
     "GREENHOUSE_API_URL", "https://harvest.greenhouse.io/v1"
)

# Configuración de la aplicación
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = get_optional_env("LOG_LEVEL", "INFO")

# Configuración de almacenamiento
DATA_DIR = get_optional_env("DATA_DIR", "data")
BATCH_SIZE = int(get_optional_env("BATCH_SIZE", "100"))
