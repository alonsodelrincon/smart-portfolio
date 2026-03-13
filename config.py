import pathlib
import tomllib

BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / ".streamlit/config.toml"

with open(CONFIG_DIR, "rb") as f:
    tomlib_config = tomllib.load(f)

DEFAULT_ASSETS_DB = tomlib_config["assets_databases"]