"""Format detection utility for output files."""

import os


def detect_format(filename, output_format='auto'):
    """
    Detect output format from file extension or use provided format.
    
    Args:
        filename: Output filename
        output_format: Format string ('auto', 'csv', 'json', 'html', 'sql', 'cloudflare')
    
    Returns:
        Detected format string (csv, json, html, sql, or cloudflare)
    """
    if output_format != 'auto':
        return output_format.lower()
    
    ext = os.path.splitext(filename)[1].lower()
    filename_lower = filename.lower()
    
    if ext == '.csv':
        return 'csv'
    elif ext == '.json':
        # Check if it's cloudflare rule (could be .json but we'll check filename)
        if 'cloudflare' in filename_lower or 'cf' in filename_lower:
            return 'cloudflare'
        return 'json'
    elif ext == '.html' or ext == '.htm':
        return 'html'
    elif ext == '.sql' or ext == '.db':
        return 'sql'
    elif 'cloudflare' in filename_lower or ext == '.cf':
        return 'cloudflare'
    else:
        return 'csv'  # default
