"""SQL export functionality for ASN lookup results."""

import os
import pandas as pd


def export_to_sql(df, filename, config_dict=None):
    """
    Export DataFrame to SQL file with CREATE TABLE and INSERT statements.
    
    Args:
        df: pandas DataFrame containing the results
        filename: Output filename
        config_dict: Optional dictionary with SQL configuration:
            - create_table: Whether to include CREATE TABLE statement (default: True)
            - insert_into: Whether to include INSERT statements (default: True)
    
    Returns:
        Tuple of (success: bool, message: str, table_name: str)
    """
    try:
        if config_dict is None:
            config_dict = {}
        
        # Parse SQL configuration
        create_table = config_dict.get('create_table', 'true').lower() in ('true', '1', 'yes', 'on')
        insert_into = config_dict.get('insert_into', 'true').lower() in ('true', '1', 'yes', 'on')
        
        # Generate table name from filename
        table_name = os.path.splitext(os.path.basename(filename))[0].replace('-', '_').replace('.', '_')
        if not table_name.replace('_', '').isalnum():
            table_name = 'asn_results'
        
        sql_statements = []
        sql_statements.append(f"-- ASN Lookup Results\n")
        sql_statements.append(f"-- Total records: {len(df)}\n\n")
        
        # Generate CREATE TABLE statement if enabled
        if create_table:
            sql_statements.append(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
            sql_statements.append("    id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
            
            # Add columns based on DataFrame columns
            for col in df.columns:
                col_name = col.replace(' ', '_').replace('-', '_')
                sql_statements.append(f"    {col_name} TEXT,\n")
            
            sql_statements.append(");\n\n")
        
        # Generate INSERT statements if enabled
        if insert_into:
            for _, row in df.iterrows():
                values = []
                columns = []
                for col in df.columns:
                    col_name = col.replace(' ', '_').replace('-', '_')
                    columns.append(col_name)
                    value = str(row[col]) if pd.notna(row[col]) else 'NULL'
                    if value != 'NULL':
                        value = value.replace("'", "''")  # Escape single quotes
                        values.append(f"'{value}'")
                    else:
                        values.append('NULL')
                
                columns_str = ', '.join(columns)
                values_str = ', '.join(values)
                sql_statements.append(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});\n")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(''.join(sql_statements))
        
        message = f"\n✓ ASN lookup completed! Results saved to '{filename}' (SQL format)\n  Table name: {table_name}"
        return True, message, table_name
    except Exception as e:
        return False, f"Error saving SQL file: {e}", None
