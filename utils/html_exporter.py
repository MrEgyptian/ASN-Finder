"""HTML export functionality for ASN lookup results."""

import pandas as pd


def export_to_html(df, filename):
    """
    Export DataFrame to HTML file with styling.
    
    Args:
        df: pandas DataFrame containing the results
        filename: Output filename
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Create HTML table with styling
        html_content = df.to_html(index=False, escape=False, classes='table table-striped', table_id='asn_results')
        
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ASN Lookup Results</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
        }}
        .table {{
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .table th {{
            background-color: #4CAF50;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}
        .table td {{
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }}
        .table tr:hover {{
            background-color: #f5f5f5;
        }}
    </style>
</head>
<body>
    <h1>ASN Lookup Results</h1>
    <p>Total records: {len(df)}</p>
    {html_content}
</body>
</html>"""
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        return True, f"\n✓ ASN lookup completed! Results saved to '{filename}' (HTML format)"
    except Exception as e:
        return False, f"Error saving HTML file: {e}"
