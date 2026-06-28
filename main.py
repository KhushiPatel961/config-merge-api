import os
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

defaults = {
    "port": 8000,
    "workers": 1,
    "debug": False,
    "log_level": "info",
    "api_key": "default-secret-000",
}

config = defaults.copy()

# YAML layer
with open("config.development.yaml") as f:
    config.update(yaml.safe_load(f))

# .env layer
env_map = {
    "APP_PORT": "port",
    "APP_LOG_LEVEL": "log_level",
    "APP_API_KEY": "api_key",
    "NUM_WORKERS": "workers",
}

for env_key, cfg_key in env_map.items():
    if env_key in os.environ:
        config[cfg_key] = os.environ[env_key]

# OS env layer
os_env = {
    "APP_WORKERS": "workers",
    "APP_LOG_LEVEL": "log_level",
}

for env_key, cfg_key in os_env.items():
    if env_key in os.environ:
        config[cfg_key] = os.environ[env_key]


def to_bool(v):
    return str(v).lower() in ("true", "1", "yes", "on")


@app.get("/effective-config")
def effective_config(set: list[str] = Query(default=[])):
    result = config.copy()

    for item in set:
        if "=" not in item:
            continue
        k, v = item.split("=", 1)
        result[k] = v

    result["port"] = int(result["port"])
    result["workers"] = int(result["workers"])
    result["debug"] = to_bool(result["debug"])
    result["log_level"] = str(result["log_level"])
    result["api_key"] = "****"

    return result
