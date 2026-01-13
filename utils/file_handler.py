"""File handling utilities for reading IP addresses from files."""

import sys


def read_ips_from_file(filename):
    """
    Read IP addresses from file with validation.
    
    Args:
        filename: Path to file containing IP addresses (one per line)
    
    Returns:
        List of IP addresses as strings
    
    Raises:
        SystemExit: If file is not found or cannot be read
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            ips = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
        return ips
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when reading file '{filename}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)
