"""Cloudflare firewall rules export functionality for ASN lookup results."""

import pandas as pd


def export_to_cloudflare(df, filename, action='block', description='ASN-based firewall rule'):
    """
    Export DataFrame to Cloudflare firewall rules format.
    
    Args:
        df: pandas DataFrame containing the results
        filename: Output filename
        action: Rule action ('block' or 'allow')
        description: Rule description
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Extract unique ASNs (excluding errors and N/A)
        asns = set()
        for asn in df['ASN'].dropna():
            asn_str = str(asn).strip().upper()
            if asn_str and asn_str != 'N/A':
                # Remove 'AS' prefix if present
                if asn_str.startswith('AS'):
                    asn_str = asn_str[2:]
                if asn_str.isdigit():
                    asns.add(asn_str)
        
        if not asns:
            return False, "No valid ASNs found to export"
        
        # Create Cloudflare rule expression
        # Format: (ip.geoip.asnum in {ASN1 ASN2 ASN3 ...})
        asn_list = ' '.join(sorted(asns))
        expression = f"(ip.geoip.asnum in {{{asn_list}}})"
        
        # Create rule JSON format
        rule = {
            "action": action,
            "expression": expression,
            "description": description
        }
        
        # Write to file (JSON format for Cloudflare API)
        import json
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(rule, f, indent=2, ensure_ascii=False)
        
        return True, f"\n✓ ASN lookup completed! Cloudflare rule saved to '{filename}' ({action} action, {len(asns)} ASNs)"
    except Exception as e:
        return False, f"Error saving Cloudflare rule file: {e}"
