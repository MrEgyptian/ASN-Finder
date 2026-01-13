"""CSV export functionality for ASN lookup results."""

import pandas as pd


def export_to_csv(df, filename):
    """
    Export DataFrame to CSV file.
    
    Args:
        df: pandas DataFrame containing the results
        filename: Output filename
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        return True, f"\n✓ ASN lookup completed! Results saved to '{filename}' (CSV format)"
    except Exception as e:
        return False, f"Error saving CSV file: {e}"
