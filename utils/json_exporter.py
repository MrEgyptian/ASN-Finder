"""JSON export functionality for ASN lookup results."""

import pandas as pd


def export_to_json(df, filename):
    """
    Export DataFrame to JSON file.
    
    Args:
        df: pandas DataFrame containing the results
        filename: Output filename
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Use orient='records' for JSON array format
        df.to_json(filename, orient='records', indent=2, force_ascii=False)
        return True, f"\n✓ ASN lookup completed! Results saved to '{filename}' (JSON format)"
    except Exception as e:
        return False, f"Error saving JSON file: {e}"
