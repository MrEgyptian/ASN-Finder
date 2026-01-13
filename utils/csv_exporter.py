"""CSV export functionality for ASN lookup results."""

import pandas as pd


def export_to_csv(df, filename, config_dict=None):
    """
    Export DataFrame to CSV file.
    
    Args:
        df: pandas DataFrame containing the results
        filename: Output filename
        config_dict: Optional dictionary with CSV configuration:
            - line_separator: Line separator (default: '\n')
            - quote_character: Quote character (default: '"')
            - escape_character: Escape character (default: '\\')
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        if config_dict is None:
            config_dict = {}
        
        # Parse CSV configuration
        lineterminator = config_dict.get('line_separator', '\n').replace('\\n', '\n').replace('\\r', '\r')
        quotechar = config_dict.get('quote_character', '"').strip('"').strip("'")
        escapechar = config_dict.get('escape_character', '\\').replace('\\\\', '\\')
        
        # Set pandas CSV parameters
        csv_params = {
            'index': False,
            'encoding': 'utf-8',
            'lineterminator': lineterminator,
            'quotechar': quotechar if quotechar else '"',
        }
        
        # Only set escapechar if provided and not empty
        if escapechar and escapechar != '\\':
            csv_params['escapechar'] = escapechar
        
        df.to_csv(filename, **csv_params)
        return True, f"\n✓ ASN lookup completed! Results saved to '{filename}' (CSV format)"
    except Exception as e:
        return False, f"Error saving CSV file: {e}"
