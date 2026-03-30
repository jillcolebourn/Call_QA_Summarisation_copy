"""
Simple configuration loader - loads config.yml once at module import.

Usage:
    from src.config.config_loader import POLICIES, PATHS, LLM_CONFIG

    ltv_max = POLICIES['pre_qualification']['ltv_max']
    customer_data_path = PATHS['customer_data']
    model = LLM_CONFIG['model']
"""
import yaml
from pathlib import Path
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Load config once when module is imported
_config_path = Path("config.yml")

try:
    with open(_config_path, 'r') as f:
        CONFIG = yaml.safe_load(f)

    # Direct access to main sections for convenience
    POLICIES = CONFIG.get('policies', {})
    PATHS = CONFIG.get('paths', {})
    LLM_CONFIG = CONFIG.get('llm', {})
    WORKFLOW = CONFIG.get('workflow', {})

    logger.info(f"✅ Configuration loaded from {_config_path}")

except FileNotFoundError:
    logger.error(f"❌ Config file not found: {_config_path}")
    # Provide empty defaults to avoid crashes
    CONFIG = {}
    POLICIES = {}
    PATHS = {}
    LLM_CONFIG = {}
    WORKFLOW = {}

except yaml.YAMLError as e:
    logger.error(f"❌ Error parsing config.yml: {e}")
    CONFIG = {}
    POLICIES = {}
    PATHS = {}
    LLM_CONFIG = {}
    WORKFLOW = {}


def reload_config():
    """
    Reload configuration from file.
    Useful for testing or hot-reloading config changes.
    """
    global CONFIG, POLICIES, PATHS, LLM_CONFIG, WORKFLOW

    with open(_config_path, 'r') as f:
        CONFIG = yaml.safe_load(f)

    POLICIES = CONFIG.get('policies', {})
    PATHS = CONFIG.get('paths', {})
    LLM_CONFIG = CONFIG.get('llm', {})
    WORKFLOW = CONFIG.get('workflow', {})

    logger.info(f"🔄 Configuration reloaded from {_config_path}")


def get_nested(dictionary: dict, *keys, default=None):
    """
    Safely get nested dictionary value.

    Example:
        get_nested(CONFIG, 'policies', 'pre_qualification', 'ltv_max', default=0.95)
    """
    value = dictionary
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
            if value is None:
                return default
        else:
            return default
    return value
