"""Data filtering and separation utilities."""

import pandas as pd
import os


def filter_columns(df, columns):
    """
    Filter DataFrame to include only specified columns.
    
    Args:
        df: pandas DataFrame
        columns: List of column names to include (must include 'IP' if present)
    
    Returns:
        Filtered DataFrame
    """
    if not columns:
        return df
    
    # Ensure IP column is always included if it exists
    available_columns = list(df.columns)
    columns_to_include = []
    
    for col in columns:
        if col in available_columns:
            columns_to_include.append(col)
    
    # Always include IP if it exists and columns are specified
    if 'IP' in available_columns and 'IP' not in columns_to_include:
        columns_to_include.insert(0, 'IP')
    
    if columns_to_include:
        return df[columns_to_include]
    else:
        return df


def separate_data(df, separate_by, exports_dir='exports', base_filename='results', output_format='csv'):
    """
    Separate data based on a column and save to different files.
    
    Args:
        df: pandas DataFrame
        separate_by: Column name to separate by (e.g., 'Type', 'Country', 'Registry')
        exports_dir: Directory to save separated files
        base_filename: Base filename for separated files
        output_format: Output format (csv, json, html, sql)
    
    Returns:
        List of tuples (filename, count) for separated files
    """
    separated_files = []
    
    if separate_by not in df.columns:
        return separated_files
    
    # Get unique values in the separation column
    unique_values = df[separate_by].dropna().unique()
    
    for value in unique_values:
        # Filter data for this value
        filtered_df = df[df[separate_by] == value]
        
        # Create safe filename from value
        safe_value = str(value).replace('/', '_').replace('\\', '_').replace(' ', '_')
        safe_value = ''.join(c for c in safe_value if c.isalnum() or c in ('_', '-'))
        
        # Create filename
        name, ext = os.path.splitext(base_filename)
        if ext:
            filename = f"{name}_{safe_value}{ext}"
        else:
            # Add extension based on format
            ext_map = {'csv': '.csv', 'json': '.json', 'html': '.html', 'sql': '.sql'}
            ext = ext_map.get(output_format, '.csv')
            filename = f"{name}_{safe_value}{ext}"
        
        filepath = os.path.join(exports_dir, filename)
        
        # Save filtered data
        try:
            if output_format == 'csv':
                filtered_df.to_csv(filepath, index=False, encoding='utf-8')
            elif output_format == 'json':
                filtered_df.to_json(filepath, orient='records', indent=2, force_ascii=False)
            elif output_format == 'html':
                # Use pandas to_html for HTML export
                html_content = filtered_df.to_html(index=False, escape=False, classes='table table-striped')
                html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ASN Lookup Results - {value}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        h1 {{ color: #333; }}
        .table {{ border-collapse: collapse; width: 100%; background-color: white; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .table th {{ background-color: #4CAF50; color: white; padding: 12px; text-align: left; font-weight: bold; }}
        .table td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        .table tr:hover {{ background-color: #f5f5f5; }}
    </style>
</head>
<body>
    <h1>ASN Lookup Results - {value}</h1>
    <p>Total records: {len(filtered_df)}</p>
    {html_content}
</body>
</html>"""
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(html_template)
            elif output_format == 'sql':
                # SQL export for separated data
                table_name = safe_value.lower().replace('-', '_').replace('.', '_')
                if not table_name.replace('_', '').isalnum():
                    table_name = f'table_{safe_value}'
                
                sql_statements = []
                sql_statements.append(f"-- ASN Lookup Results - {value}\n")
                sql_statements.append(f"-- Total records: {len(filtered_df)}\n\n")
                sql_statements.append(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
                sql_statements.append("    id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
                for col in filtered_df.columns:
                    col_name = col.replace(' ', '_')
                    sql_statements.append(f"    {col_name} TEXT,\n")
                sql_statements.append(");\n\n")
                
                # Generate INSERT statements
                for _, row in filtered_df.iterrows():
                    values = []
                    col_names = []
                    for col in filtered_df.columns:
                        col_names.append(col.replace(' ', '_'))
                        val = str(row[col]) if pd.notna(row[col]) else 'NULL'
                        if val != 'NULL':
                            val = val.replace("'", "''")
                            values.append(f"'{val}'")
                        else:
                            values.append('NULL')
                    
                    sql_statements.append(f"INSERT INTO {table_name} ({', '.join(col_names)}) VALUES ({', '.join(values)});\n")
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(''.join(sql_statements))
            
            separated_files.append((filepath, len(filtered_df), value))
        except Exception as e:
            print(f"Warning: Could not save separated file for {value}: {e}")
    
    return separated_files
