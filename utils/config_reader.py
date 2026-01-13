"""Configuration file reader utility."""

import configparser
import os


def load_config(config_file='config.ini'):
    """
    Load configuration from INI file.
    
    Args:
        config_file: Path to configuration file
    
    Returns:
        ConfigParser object with loaded configuration, or None if file doesn't exist
    """
    config = configparser.ConfigParser()
    
    # Check if config file exists
    if not os.path.exists(config_file):
        return None
    
    try:
        config.read(config_file, encoding='utf-8')
        return config
    except Exception as e:
        print(f"Warning: Error reading config file '{config_file}': {e}")
        return None


def get_config_value(config, section, key, default_value):
    """
    Get configuration value with fallback to default.
    
    Args:
        config: ConfigParser object (can be None)
        section: Configuration section name
        key: Configuration key name
        default_value: Default value if not found
    
    Returns:
        Configuration value or default
    """
    if config is None:
        return default_value
    
    try:
        if section == 'DEFAULT':
            return config.get(section, key, fallback=default_value)
        else:
            if config.has_section(section) and config.has_option(section, key):
                return config.get(section, key, fallback=default_value)
            return default_value
    except Exception:
        return default_value


def get_config_int(config, section, key, default_value):
    """Get integer configuration value."""
    value = get_config_value(config, section, key, str(default_value))
    try:
        return int(value)
    except (ValueError, TypeError):
        return default_value


def get_config_bool(config, section, key, default_value):
    """Get boolean configuration value."""
    value = get_config_value(config, section, key, str(default_value)).lower()
    return value in ('true', '1', 'yes', 'on')


def get_section_dict(config, section):
    """
    Get all options from a section as a dictionary.
    
    Args:
        config: ConfigParser object (can be None)
        section: Configuration section name
    
    Returns:
        Dictionary with section options, or empty dict if section doesn't exist
    """
    if config is None:
        return {}
    
    try:
        if config.has_section(section):
            return dict(config.items(section))
        return {}
    except Exception:
        return {}
