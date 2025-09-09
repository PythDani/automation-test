import os
from dotenv import load_dotenv

load_dotenv() 

# URLs disponibles
AVAILABLE_URLS = {
    "nuxqa4": "https://nuxqa4.avtest.ink/",
    "nuxqa5": "https://nuxqa5.avtest.ink/",
    "default": "https://nuxqa4.avtest.ink/"
}

# Configuración principal
HOME_URL = os.getenv("HOME_URL", AVAILABLE_URLS["default"])
CURRENT_ENVIRONMENT = os.getenv("CURRENT_ENVIRONMENT", "nuxqa4")

# Credenciales
USER_NAME = os.getenv("USER_NAME")
USER_PASSWORD = os.getenv("USER_PASSWORD")

# Datos de tarjeta de crédito
CARD_CREDIT_NUMBER = os.getenv("CARD_CREDIT_NUMBER")
CARD_CREDIT_PIN = os.getenv("CREDIT_PIN")

# Configuraciones de video
ENABLE_VIDEO_RECORDING = os.getenv("ENABLE_VIDEO_RECORDING", "false").lower() == "true"
MAX_VIDEO_SIZE_MB = int(os.getenv("MAX_VIDEO_SIZE_MB", "50"))
VIDEO_QUALITY = os.getenv("VIDEO_QUALITY", "medium")
VIDEO_FPS = int(os.getenv("VIDEO_FPS", "15"))

# Configuraciones de navegador
BROWSER_HEADLESS = os.getenv("BROWSER_HEADLESS", "false").lower() == "true"
BROWSER_TIMEOUT = int(os.getenv("BROWSER_TIMEOUT", "30"))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

# Configuraciones de memoria
ENABLE_MEMORY_MONITORING = os.getenv("ENABLE_MEMORY_MONITORING", "false").lower() == "true"
MEMORY_CLEANUP_INTERVAL = int(os.getenv("MEMORY_CLEANUP_INTERVAL", "5"))

# Configuraciones de testing
PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "2"))
RETRY_COUNT = int(os.getenv("RETRY_COUNT", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))

def get_url_for_environment(env: str = None) -> str:
    """
    Obtiene la URL para un entorno específico
    
    Args:
        env (str): Nombre del entorno (nuxqa4, nuxqa5, etc.)
    
    Returns:
        str: URL del entorno
    """
    if env is None:
        env = CURRENT_ENVIRONMENT
    
    return AVAILABLE_URLS.get(env, AVAILABLE_URLS["default"])

def switch_environment(env: str) -> str:
    """
    Cambia el entorno actual
    
    Args:
        env (str): Nombre del entorno
    
    Returns:
        str: URL del nuevo entorno
    """
    global HOME_URL, CURRENT_ENVIRONMENT
    
    if env in AVAILABLE_URLS:
        HOME_URL = AVAILABLE_URLS[env]
        CURRENT_ENVIRONMENT = env
        return HOME_URL
    else:
        raise ValueError(f"Environment '{env}' not found. Available: {list(AVAILABLE_URLS.keys())}")

def get_current_config() -> dict:
    """
    Retorna la configuración actual
    
    Returns:
        dict: Configuración actual
    """
    return {
        "home_url": HOME_URL,
        "current_environment": CURRENT_ENVIRONMENT,
        "available_environments": list(AVAILABLE_URLS.keys()),
        "video_recording": ENABLE_VIDEO_RECORDING,
        "video_quality": VIDEO_QUALITY,
        "video_fps": VIDEO_FPS,
        "browser_headless": BROWSER_HEADLESS,
        "parallel_workers": PARALLEL_WORKERS,
        "memory_monitoring": ENABLE_MEMORY_MONITORING
    }

def validate_config() -> bool:
    """
    Valida que la configuración sea correcta
    
    Returns:
        bool: True si la configuración es válida
    """
    required_vars = [
        "USER_NAME",
        "USER_PASSWORD", 
        "CARD_CREDIT_NUMBER",
        "CARD_CREDIT_PIN"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    if HOME_URL not in AVAILABLE_URLS.values():
        print(f"Invalid HOME_URL: {HOME_URL}")
        return False
    
    print("Configuration is valid")
    return True

if __name__ == "__main__":
    print("Current Configuration:")
    config = get_current_config()
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    print(f"\nAvailable URLs:")
    for env, url in AVAILABLE_URLS.items():
        marker = "👉" if env == CURRENT_ENVIRONMENT else "  "
        print(f"  {marker} {env}: {url}")
    
    print(f"\nConfiguration validation: {'PASSED' if validate_config() else 'FAILED'}")
