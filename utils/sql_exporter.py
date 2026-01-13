"""SQL export functionality for ASN lookup results."""

import os
import pandas as pd


def export_to_sql(df, filename):
    """
    Export DataFrame to SQL file with CREATE TABLE and INSERT statements.
    
    Args:
        df: pandas DataFrame containing the results
        filename: Output filename
    
    Returns:
        Tuple of (success: bool, message: str, table_name: str)
    """
    try:
        # Generate table name from filename
        table_name = os.path.splitext(os.path.basename(filename))[0].replace('-', '_').replace('.', '_')
        if not table_name.replace('_', '').isalnum():
            table_name = 'asn_results'
        
        sql_statements = []
        sql_statements.append(f"-- ASN Lookup Results\n")
        sql_statements.append(f"-- Total records: {len(df)}\n\n")
        sql_statements.append(f"CREATE TABLE IF NOT EXISTS {table_name} (\n")
        sql_statements.append("    id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
        sql_statements.append("    IP TEXT NOT NULL,\n")
        sql_statements.append("    ASN TEXT,\n")
        sql_statements.append("    AS_Name TEXT,\n")
        sql_statements.append("    Country TEXT,\n")
        sql_statements.append("    IP_Block TEXT,\n")
        sql_statements.append("    Registry TEXT,\n")
        sql_statements.append("    Error TEXT\n")
        sql_statements.append(");\n\n")
        
        for _, row in df.iterrows():
            values = []
            for col in df.columns:
                value = str(row[col]) if pd.notna(row[col]) else 'NULL'
                if value != 'NULL':
                    value = value.replace("'", "''")  # Escape single quotes
                    values.append(f"'{value}'")
                else:
                    values.append('NULL')
            
            sql_statements.append(f"INSERT INTO {table_name} (IP, ASN, AS_Name, Country, IP_Block, Registry, Error) VALUES ({', '.join(values)});\n")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(''.join(sql_statements))
        
        message = f"\n✓ ASN lookup completed! Results saved to '{filename}' (SQL format)\n  Table name: {table_name}"
        return True, message, table_name
    except Exception as e:
        return False, f"Error saving SQL file: {e}", None
