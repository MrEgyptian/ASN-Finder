"""JSON export functionality for ASN lookup results."""

import pandas as pd


def export_to_json(df, filename, config_dict=None):
    """
    Export DataFrame to JSON file.
    
    Args:
        df: pandas DataFrame containing the results
        filename: Output filename
        config_dict: Optional dictionary with JSON configuration:
            - indent: Indentation level (default: 2)
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        if config_dict is None:
            config_dict = {}
        
        # Parse JSON configuration
        indent = 2
        try:
            indent = int(config_dict.get('indent', '2'))
        except (ValueError, TypeError):
            indent = 2
        
        # Use orient='records' for JSON array format
        df.to_json(filename, orient='records', indent=indent, force_ascii=False)
        return True, f"\n✓ ASN lookup completed! Results saved to '{filename}' (JSON format)"
    except Exception as e:
        return False, f"Error saving JSON file: {e}"
