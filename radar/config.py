from pydantic import BaseModel
import yaml
from .paths import CONFIG_DIR

class AppConfig(BaseModel):
    name: str
    region_name: str
    latitude: float
    longitude: float
    hazards: list[str]

class DataConfig(BaseModel):
    refresh_minutes: int

class SourceConfig(BaseModel):
    openweather: dict

class Config(BaseModel):
    app: AppConfig
    data: DataConfig
    sources: SourceConfig

def load_config(path: str | None = None) -> Config:
    cfg_path = CONFIG_DIR / "defaults.yaml" if path is None else path
    with open(cfg_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    return Config(**raw)