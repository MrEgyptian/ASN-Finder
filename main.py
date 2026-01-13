import argparse
import configparser
import csv
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from ipaddress import ip_address, AddressValueError

# Try to import pandas for multiple output formats
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# Try to import ipwhois for ASN lookup
try:
    from ipwhois import IPWhois
    IPWHOIS_AVAILABLE = True
except ImportError:
    IPWHOIS_AVAILABLE = False


def query_asn_whois(ip):
    """
    Query ASN information using ipwhois library.
    Returns dict with ASN information or error.
    """
    if not IPWHOIS_AVAILABLE:
        return {
            'asn': 'N/A',
            'as_name': 'N/A',
            'country': 'N/A',
            'ip_block': 'N/A',
            'registry': 'N/A',
            'error': 'ipwhois not installed. Install with: pip install ipwhois'
        }
    
    try:
        # Create IPWhois object and perform lookup
        obj = IPWhois(ip)
        result = obj.lookup_whois()
        
        # Extract ASN information from the result
        asn = result.get('asn', 'N/A')
        asn_description = result.get('asn_description', 'N/A')
        asn_country_code = result.get('asn_country_code', 'N/A')
        asn_cidr = result.get('asn_cidr', 'N/A')
        asn_registry = result.get('asn_registry', 'N/A')
        
        # Format ASN (remove 'AS' prefix if present, or add it if it's just a number)
        if asn and asn != 'N/A':
            if isinstance(asn, str) and asn.upper().startswith('AS'):
                asn = asn.upper()
            elif isinstance(asn, (str, int)):
                asn = f"AS{asn}"
        
        return {
            'asn': asn if asn else 'N/A',
            'as_name': asn_description if asn_description else 'N/A',
            'country': asn_country_code if asn_country_code else 'N/A',
            'ip_block': asn_cidr if asn_cidr else 'N/A',
            'registry': asn_registry if asn_registry else 'N/A',
            'error': ''
        }
        
    except Exception as e:
        return {
            'asn': 'N/A',
            'as_name': 'N/A',
            'country': 'N/A',
            'ip_block': 'N/A',
            'registry': 'N/A',
            'error': f'Whois error: {str(e)}'
        }


def is_valid_ip(ip_str):
    """Validate IP address format."""
    try:
        ip_address(ip_str.strip())
        return True
    except (AddressValueError, ValueError):
        return False




def ensure_exports_dir(exports_dir='exports'):
    """Ensure exports directory exists, create if it doesn't."""
    try:
        if not os.path.exists(exports_dir):
            os.makedirs(exports_dir)
            print(f"Created exports directory: {exports_dir}/")
    except Exception as e:
        print(f"Warning: Could not create exports directory '{exports_dir}': {e}")


def save_results(results, filename, output_format='csv', exports_dir='exports', cloudflare_action='block'):
    """Save ASN lookup results to file in specified format using pandas."""
    if not PANDAS_AVAILABLE:
        print("Error: pandas library is required for saving results.")
        print("Install it with: pip install pandas")
        sys.exit(1)
    
    try:
        # Ensure exports directory exists
        ensure_exports_dir(exports_dir)
        
        # Import exporter functions
        from utils import (
            export_to_csv,
            export_to_json,
            export_to_html,
            export_to_sql,
            export_to_cloudflare,
            detect_format
        )
        
        # Create DataFrame from results
        df = pd.DataFrame(results)
        
        # Detect format
        format_type = detect_format(filename, output_format)
        
        # Ensure filename is in exports directory
        if not os.path.dirname(filename):
            # No directory specified, use exports directory
            filename = os.path.join(exports_dir, filename)
        elif not os.path.abspath(filename).startswith(os.path.abspath(exports_dir)):
            # Directory specified but not exports, prepend exports
            basename = os.path.basename(filename)
            filename = os.path.join(exports_dir, basename)
        
        # Save based on format
        if format_type == 'csv':
            success, message = export_to_csv(df, filename)
            if not success:
                print(message)
                sys.exit(1)
            print(message)
        
        elif format_type == 'json':
            success, message = export_to_json(df, filename)
            if not success:
                print(message)
                sys.exit(1)
            print(message)
        
        elif format_type == 'html':
            success, message = export_to_html(df, filename)
            if not success:
                print(message)
                sys.exit(1)
            print(message)
        
        elif format_type == 'sql':
            success, message, table_name = export_to_sql(df, filename)
            if not success:
                print(message)
                sys.exit(1)
            print(message)
        
        elif format_type == 'cloudflare':
            success, message = export_to_cloudflare(df, filename, action=cloudflare_action)
            if not success:
                print(message)
                sys.exit(1)
            print(message)
        
        else:
            print(f"Error: Unsupported output format '{format_type}'")
            print("Supported formats: csv, json, html, sql, cloudflare")
            sys.exit(1)
        
        print(f"  Total IPs processed: {len(results)}")
        
    except ImportError as e:
        print(f"Error importing exporter modules: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error saving results: {e}")
        sys.exit(1)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="ASN Finder - Query ASN information for IP addresses using ipwhois",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py ips.txt
  python main.py ips.txt -o results.csv
  python main.py ips.txt -o results.json -f json
  python main.py tor.txt --output my_results.html --format html
  python main.py ips.txt -o results.sql -f sql
  python main.py ips.txt -t 10  # Use 10 threads
  python main.py ips.txt --detect-vpn  # Detect VPN ASNs
  python main.py ips.txt --detect-vpn --full -o results.csv  # Full details with VPN detection
        """
    )
    parser.add_argument(
        'input_file',
        help='Input file containing IP addresses (one per line)'
    )
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        default='asn_results.csv',
        help='Output file (default: asn_results.csv). Format is auto-detected from extension or use --format'
    )
    parser.add_argument(
        '-f', '--format',
        dest='output_format',
        choices=['csv', 'json', 'html', 'sql', 'cloudflare', 'auto'],
        default='auto',
        help='Output format: csv, json, html, sql, cloudflare, or auto (detect from file extension). Default: auto'
    )
    parser.add_argument(
        '-c', '--config',
        dest='config_file',
        default='config.ini',
        help='Configuration file path (default: config.ini)'
    )
    parser.add_argument(
        '--cloudflare-action',
        dest='cloudflare_action',
        choices=['block', 'allow'],
        default='block',
        help='Cloudflare rule action: block or allow (default: block)'
    )
    parser.add_argument(
        '-t', '--threads',
        dest='threads',
        type=int,
        default=10,
        help='Number of threads to use for concurrent queries (default: 10)'
    )
    parser.add_argument(
        '--full',
        dest='full_details',
        action='store_true',
        default=False,
        help='Show full details (ASN, AS Name, Country, IP Block, Registry). Default: ASN only'
    )
    parser.add_argument(
        '--detect-vpn',
        dest='detect_vpn',
        action='store_true',
        default=False,
        help='Detect and separate VPN ASNs from normal ones using data/vpn_hosts.txt'
    )
    return parser.parse_args()


def process_single_ip(ip, index, total, full_details=False, vpn_asns_set=None):
    """
    Process a single IP address and return the result.
    
    Args:
        ip: IP address to query
        index: Index of the IP in the list (for progress tracking)
        total: Total number of IPs to process
        full_details: If True, include all fields. If False, only ASN.
        vpn_asns_set: Set of VPN ASN numbers for detection (optional)
    
    Returns:
        Tuple of (index, ip, result_dict, is_success)
    """
    if not is_valid_ip(ip):
        result_base = {
            'IP': ip,
            'ASN': 'N/A',
            'Error': 'Invalid IP format'
        }
        if full_details:
            result_base.update({
                'AS Name': 'Invalid IP',
                'Country': 'N/A',
                'IP Block': 'N/A',
                'Registry': 'N/A'
            })
        if vpn_asns_set is not None:
            result_base['Type'] = 'N/A'
        return (index, ip, result_base, False)
    
    # Query ASN
    asn_data = query_asn_whois(ip)
    asn = asn_data.get('asn', 'N/A')
    
    # Determine VPN status
    type_value = 'Normal'
    if vpn_asns_set is not None:
        from utils import is_vpn_asn
        type_value = 'VPN' if is_vpn_asn(asn, vpn_asns_set) else 'Normal'
    
    if full_details:
        result = {
            'IP': ip,
            'ASN': asn,
            'AS Name': asn_data.get('as_name', 'N/A'),
            'Country': asn_data.get('country', 'N/A'),
            'IP Block': asn_data.get('ip_block', 'N/A'),
            'Registry': asn_data.get('registry', 'N/A'),
            'Error': asn_data.get('error', '')
        }
    else:
        result = {
            'IP': ip,
            'ASN': asn,
            'Error': asn_data.get('error', '')
        }
    
    if vpn_asns_set is not None:
        result['Type'] = type_value
    
    is_success = not bool(asn_data.get('error'))
    return (index, ip, result, is_success)


def main():
    """Main function to orchestrate ASN lookup process."""
    args = parse_arguments()
    
    # Load configuration file
    from utils.config_reader import load_config, get_config_int, get_config_bool, get_config_value
    config = load_config(args.config_file)
    
    # Apply configuration (command line args override config file)
    input_file = args.input_file
    output_file = args.output_file if args.output_file != 'asn_results.csv' else get_config_value(config, 'DEFAULT', 'output_file', 'asn_results.csv')
    output_format = args.output_format if args.output_format != 'auto' else get_config_value(config, 'DEFAULT', 'output_format', 'auto')
    threads = args.threads if args.threads != 10 else get_config_int(config, 'DEFAULT', 'threads', 10)
    full_details = args.full_details if args.full_details else get_config_bool(config, 'DEFAULT', 'full_details', False)
    detect_vpn = args.detect_vpn if args.detect_vpn else get_config_bool(config, 'DEFAULT', 'detect_vpn', False)
    exports_dir = get_config_value(config, 'DEFAULT', 'exports_dir', 'exports')
    cloudflare_action = args.cloudflare_action if args.cloudflare_action != 'block' else get_config_value(config, 'CLOUDFLARE', 'rule_action', 'block')
    
    # Check for required libraries
    if not IPWHOIS_AVAILABLE:
        print("Error: ipwhois library is required.")
        print("Install it with: pip install ipwhois")
        sys.exit(1)
    
    if not PANDAS_AVAILABLE:
        print("Error: pandas library is required.")
        print("Install it with: pip install pandas")
        sys.exit(1)
    
    # Load VPN ASNs if detection is enabled
    vpn_asns_set = None
    vpn_data_file = get_config_value(config, 'DEFAULT', 'vpn_data_file', 'data/vpn_hosts.txt')
    if detect_vpn:
        from utils import load_vpn_asns
        print("Loading VPN ASN database...")
        vpn_asns_set = load_vpn_asns(data_dir=os.path.dirname(vpn_data_file) if os.path.dirname(vpn_data_file) else 'data',
                                     filename=os.path.basename(vpn_data_file))
        if vpn_asns_set:
            print(f"Loaded {len(vpn_asns_set)} VPN ASNs from {vpn_data_file}\n")
        else:
            print("Warning: No VPN ASNs loaded. VPN detection will be disabled.\n")
            detect_vpn = False
    
    # Read IPs from file
    from utils import read_ips_from_file
    print(f"Reading IP addresses from '{input_file}'...")
    ip_list = read_ips_from_file(input_file)
    
    if not ip_list:
        print("No IP addresses found in the input file.")
        return
    
    print(f"Found {len(ip_list)} IP address(es) to process.")
    print(f"Using {threads} thread(s) for concurrent queries.")
    if full_details:
        print("Mode: Full details (ASN, AS Name, Country, IP Block, Registry)")
    else:
        print("Mode: ASN only (default)")
    if detect_vpn:
        print("VPN Detection: Enabled")
    else:
        print("VPN Detection: Disabled")
    print(f"Exports directory: {exports_dir}\n")
    
    # Thread-safe progress tracking
    print_lock = threading.Lock()
    completed_count = [0]  # Use list to allow modification in nested function
    success_count = [0]
    error_count = [0]
    vpn_count = [0]
    normal_count = [0]
    
    # Store results with index to maintain order
    results_dict = {}
    
    def update_progress(index, ip, result, is_success):
        """Thread-safe progress update function."""
        with print_lock:
            completed_count[0] += 1
            results_dict[index] = result
            
            if is_success:
                success_count[0] += 1
                asn = result.get('ASN', 'N/A')
                type_value = result.get('Type', '')
                
                # Update VPN/Normal counts
                if detect_vpn:
                    if type_value == 'VPN':
                        vpn_count[0] += 1
                    elif type_value == 'Normal':
                        normal_count[0] += 1
                
                # Format progress message
                type_str = f" [{type_value}]" if detect_vpn and type_value else ""
                
                if full_details:
                    as_name = result.get('AS Name', 'N/A')
                    print(f"[{completed_count[0]}/{len(ip_list)}] {ip}: ✓ ASN: {asn} ({as_name}){type_str}")
                else:
                    print(f"[{completed_count[0]}/{len(ip_list)}] {ip}: ✓ ASN: {asn}{type_str}")
            else:
                error_count[0] += 1
                error_msg = result.get('Error', 'Unknown error')
                print(f"[{completed_count[0]}/{len(ip_list)}] {ip}: ✗ {error_msg}")
    
    # Process IPs using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # Submit all tasks
        futures = {
            executor.submit(process_single_ip, ip, i, len(ip_list), full_details, vpn_asns_set): (i, ip)
            for i, ip in enumerate(ip_list)
        }
        
        # Process completed tasks as they finish
        for future in as_completed(futures):
            try:
                index, ip, result, is_success = future.result()
                update_progress(index, ip, result, is_success)
            except Exception as e:
                index, ip = futures[future]
                with print_lock:
                    completed_count[0] += 1
                    error_count[0] += 1
                    if full_details:
                        error_result = {
                            'IP': ip,
                            'ASN': 'N/A',
                            'AS Name': 'Error',
                            'Country': 'N/A',
                            'IP Block': 'N/A',
                            'Registry': 'N/A',
                            'Error': f'Exception: {str(e)}'
                        }
                    else:
                        error_result = {
                            'IP': ip,
                            'ASN': 'N/A',
                            'Error': f'Exception: {str(e)}'
                        }
                    if detect_vpn:
                        error_result['Type'] = 'N/A'
                    results_dict[index] = error_result
                    print(f"[{completed_count[0]}/{len(ip_list)}] {ip}: ✗ Exception: {str(e)}")
    
    # Convert results dict to list maintaining original order
    results = [results_dict[i] for i in range(len(ip_list))]
    
    # Get final counts
    final_success_count = success_count[0]
    final_error_count = error_count[0]
    
    # Save results in specified format
    save_results(results, output_file, output_format, exports_dir, cloudflare_action)
    
    # Summary
    print(f"\nSummary:")
    print(f"  Successful queries: {final_success_count}")
    print(f"  Errors/Invalid: {final_error_count}")
    if detect_vpn:
        print(f"  VPN ASNs: {vpn_count[0]}")
        print(f"  Normal ASNs: {normal_count[0]}")


if __name__ == "__main__":
    main()
