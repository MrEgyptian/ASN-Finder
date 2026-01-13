"""VPN ASN detection utility."""

import os


def load_vpn_asns(data_dir='data', filename='vpn_hosts.txt'):
    """
    Load VPN ASN numbers from the data file.
    
    Args:
        data_dir: Directory containing the VPN data file
        filename: Name of the VPN data file
    
    Returns:
        Set of VPN ASN numbers (as strings, without 'AS' prefix)
    """
    vpn_asns = set()
    filepath = os.path.join(data_dir, filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Extract ASN (number before the first space or #)
                parts = line.split(None, 1)  # Split on whitespace, max 1 split
                if parts:
                    asn_str = parts[0].strip()
                    # Remove 'AS' prefix if present
                    if asn_str.upper().startswith('AS'):
                        asn_str = asn_str[2:]
                    if asn_str.isdigit():
                        vpn_asns.add(asn_str)
        
        return vpn_asns
    except FileNotFoundError:
        print(f"Warning: VPN data file '{filepath}' not found. VPN detection will be disabled.")
        return set()
    except Exception as e:
        print(f"Warning: Error loading VPN data file '{filepath}': {e}. VPN detection will be disabled.")
        return set()


def is_vpn_asn(asn, vpn_asns_set):
    """
    Check if an ASN is a VPN ASN.
    
    Args:
        asn: ASN string (can be "AS12345" or "12345")
        vpn_asns_set: Set of VPN ASN numbers (as strings, without 'AS' prefix)
    
    Returns:
        True if ASN is a VPN, False otherwise
    """
    if not asn or asn == 'N/A' or not vpn_asns_set:
        return False
    
    # Remove 'AS' prefix if present and convert to string
    asn_str = str(asn).upper()
    if asn_str.startswith('AS'):
        asn_str = asn_str[2:]
    
    return asn_str in vpn_asns_set
