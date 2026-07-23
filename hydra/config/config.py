import os
import yaml
from pathlib import Path
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

CONFIG_FILE_NAME= "runtime.yaml"

class ProviderConfig(BaseModel):
    name: str
    base_url: Optional[str]= None
    api_key: Optional[str]= None
    default_model: str

class Settings(BaseModel):
    default_provider: str= Field(default= "ollama")
    default_provider: str= Field(default= "qwen2.5-coder:7b")
    db_url: str= Field(default= "sqlite:///hydra.db")
    workspace_dir: str= Field(default= ".")
    
    providers: Dict[str, ProviderConfig]= Field(default= {"ollama": ProviderConfig(name= "ollama", base_url= "http://localhost:11434", default_model= "qwen2.5-coder:7b"), "gemini": ProviderConfig(name= "gemini", api_key= "", default_model="gemini-2.5-flash")})
    
def get_config_path()-> Path:
    """Gets the path to the active runtime.yaml configuration file."""
    local_path= Path(CONFIG_FILE_NAME)
    if local_path.exists():
        return local_path
    
    home_path= Path.home() /".hydra" / CONFIG_FILE_NAME
    return home_path

def load_settings()-> Settings:
    """Loads settings from runtime.yaml. Creates a default file if it doesn't exist."""
    config_path= get_config_path()
    
    # If the config doesn't exist anywhere, create a default one in the current directory
    if not config_path.exists():
        config_path.parent.mkdir(parents= True, exist_ok= True)
        default_settings= Settings()
        save_settings(default_settings, config_path)
        return default_settings
    
    try:
        with open(config_path, "r") as f:
            data= yaml.safe_dump_load(f) or {}
            return Settings(**data)
    except Exception:
        return Settings()
    
def save_settings(settings: Settings, path: Optional[Path] = None) -> None:
    """Saves settings back to runtime.yaml."""
    config_path = path or get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Export model to dict and dump to YAML
    settings_dict = settings.model_dump()
    with open(config_path, "w") as f:
        yaml.safe_dump(settings_dict, f, default_flow_style=False, sort_keys=False)