import yaml
import os
from pathlib import Path

# -- Defaults 
DEFAULTS = {
    "hotkey_accept":  "tab",
    "hotkey_cancel":  "esc",
    "model":          "gemma4",
    "temperature":    0.3,
    "max_tokens":     15,
    "is_running":     True,
    "ollama_url":     "http://localhost:11434",
    "context_limit":  500,
    "profile_path":   "config/profile.md",
}

CONFIG_PATH = Path("config/config.yaml")

# -- Loader 
def load_config(path: str = None) -> dict:
    """
    1. Load config from yaml file.
    2. Missing keys fall back to DEFAULTS.
    3. If no file exists, create one from DEFAULTS.
    """
    config_path = Path(path) if path else CONFIG_PATH

    if not config_path.exists():
        print(f"[config] No config found, creating defaults at {config_path}")
        save_config(DEFAULTS, config_path)
        return DEFAULTS.copy()

    with open(config_path, "r") as f:
        loaded = yaml.safe_load(f) or {}

    # Merge with defaults so missing keys are always present
    config = {**DEFAULTS, **loaded}

    print(f"[config] Loaded from {config_path}")
    return config


def save_config(config: dict, path: Path = CONFIG_PATH) -> None:
    """Save config dict to yaml file, creating dirs if needed."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"[config] Saved to {path}")


def load_profile(config: dict) -> str:
    """
    Load the user's personal system prompt from profile.md.
    Returns empty string if file doesn't exist.
    """
    profile_path = Path(config.get("profile_path", DEFAULTS["profile_path"]))

    if not profile_path.exists():
        print(f"[config] No profile found at {profile_path}, using empty profile")
        return ""

    with open(profile_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    print(f"[config] Profile loaded ({len(content)} chars)")
    return content

if __name__ == "__main__":
    load_config()