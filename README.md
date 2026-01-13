# ASN-Finder

A powerful Python tool for querying ASN (Autonomous System Number) information for IP addresses using WHOIS data. Supports multiple export formats, VPN detection, multithreading, and Cloudflare firewall rule generation.

## Features

- 🔍 **ASN Lookup**: Query ASN information for IP addresses using the `ipwhois` library
- 🚀 **Multithreading**: Process multiple IPs concurrently for faster performance
- 🎯 **VPN Detection**: Identify VPN ASNs using a comprehensive database
- 📊 **Multiple Export Formats**: CSV, JSON, HTML, SQL, and Cloudflare rules
- ⚙️ **Configuration File Support**: Customize settings via INI configuration files
- 📁 **Organized Exports**: All exports are automatically saved to the `exports/` directory
- 🌐 **Cloudflare Integration**: Generate firewall rules for Cloudflare (block/allow)
- 📈 **Detailed Results**: Optional full details mode (ASN, AS Name, Country, IP Block, Registry)

## Installation

### Requirements

- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install -r requirements.txt
```

The required packages are:
- `ipwhois>=1.2.0` - For ASN lookup via WHOIS
- `pandas>=2.0.0` - For data manipulation and export

## Quick Start

### Basic Usage

```bash
# Query ASNs for IPs in a file (default: ASN only, CSV output)
python main.py ips.txt

# Specify output file
python main.py ips.txt -o results.csv

# Use multiple threads for faster processing
python main.py ips.txt -t 20
```

### Input File Format

Create a text file with one IP address per line:

```
1.2.3.4
5.6.7.8
9.10.11.12
```

Lines starting with `#` are treated as comments and ignored.

## Configuration

### Configuration File

Copy `config_example.ini` to `config.ini` and customize settings:

```ini
[DEFAULT]
# Default number of threads for concurrent queries
threads = 10

# Default output format (csv, json, html, sql, cloudflare)
output_format = csv

# Show full details by default (true/false)
full_details = false

# Enable VPN detection by default (true/false)
detect_vpn = false

# Output directory for exported files
exports_dir = exports

# VPN data file location
vpn_data_file = data/vpn_hosts.txt

[CLOUDFLARE]
# Cloudflare rule action (block or allow)
rule_action = block

# Cloudflare rule description
rule_description = ASN-based firewall rule
```

### Using Configuration File

```bash
# Use default config.ini
python main.py ips.txt

# Use custom config file
python main.py ips.txt -c my_config.ini
```

**Note**: Command-line arguments override configuration file settings.

## Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output filename | `asn_results.csv` |
| `--format` | `-f` | Output format (csv, json, html, sql, cloudflare, auto) | `auto` |
| `--threads` | `-t` | Number of threads for concurrent queries | `10` |
| `--full` | | Show full details (ASN, AS Name, Country, etc.) | `false` |
| `--detect-vpn` | | Enable VPN ASN detection | `false` |
| `--config` | `-c` | Configuration file path | `config.ini` |
| `--cloudflare-action` | | Cloudflare rule action (block/allow) | `block` |

## Usage Examples

### Basic Examples

```bash
# Simple ASN lookup (ASN only, CSV format)
python main.py ips.txt

# Full details mode
python main.py ips.txt --full

# JSON output
python main.py ips.txt -o results.json -f json

# HTML output with full details
python main.py ips.txt --full -o results.html -f html

# SQL output
python main.py ips.txt -o results.sql -f sql
```

### Advanced Examples

```bash
# VPN detection with full details
python main.py ips.txt --detect-vpn --full -o vpn_results.csv

# High-performance processing (20 threads)
python main.py large_ip_list.txt -t 20 -o results.csv

# Cloudflare firewall rules (block)
python main.py ips.txt -f cloudflare --cloudflare-action block -o cloudflare_block.json

# Cloudflare firewall rules (allow)
python main.py ips.txt -f cloudflare --cloudflare-action allow -o cloudflare_allow.json

# Custom configuration file
python main.py ips.txt -c production_config.ini -o results.csv
```

## Export Formats

### CSV (Comma-Separated Values)
Standard CSV format, suitable for Excel, Google Sheets, and data analysis tools.

```bash
python main.py ips.txt -o results.csv -f csv
```

### JSON (JavaScript Object Notation)
Structured JSON format, perfect for APIs and programming integrations.

```bash
python main.py ips.txt -o results.json -f json
```

### HTML (HyperText Markup Language)
Beautiful styled HTML table with professional formatting.

```bash
python main.py ips.txt -o results.html -f html
```

### SQL (Structured Query Language)
SQL INSERT statements with CREATE TABLE schema.

```bash
python main.py ips.txt -o results.sql -f sql
```

### Cloudflare Rules
JSON format compatible with Cloudflare Firewall Rules API.

```bash
python main.py ips.txt -f cloudflare --cloudflare-action block -o cloudflare_rules.json
```

**Cloudflare Output Format**:
```json
{
  "action": "block",
  "expression": "(ip.geoip.asnum in {12345 67890 11111})",
  "description": "ASN-based firewall rule"
}
```

## VPN Detection

The tool includes a database of known VPN ASNs. Enable VPN detection to categorize ASNs as VPN or Normal.

```bash
# Enable VPN detection
python main.py ips.txt --detect-vpn

# VPN detection with full details
python main.py ips.txt --detect-vpn --full
```

When enabled, the output includes a `Type` field:
- **VPN**: ASN is in the VPN database
- **Normal**: ASN is not in the VPN database
- **N/A**: Error or invalid IP

The summary shows separate counts for VPN and Normal ASNs.

## Output Structure

### ASN Only Mode (Default)
- `IP`: IP address
- `ASN`: Autonomous System Number
- `Error`: Error message (if any)
- `Type`: VPN/Normal (if VPN detection enabled)

### Full Details Mode (`--full`)
- `IP`: IP address
- `ASN`: Autonomous System Number
- `AS Name`: Autonomous System name/description
- `Country`: Country code
- `IP Block`: IP address block/CIDR
- `Registry`: Regional Internet Registry
- `Error`: Error message (if any)
- `Type`: VPN/Normal (if VPN detection enabled)

## Output Directory

All exports are automatically saved to the `exports/` directory. The directory is created automatically if it doesn't exist.

**Example**:
```bash
python main.py ips.txt -o results.csv
# Output: exports/results.csv
```

## Project Structure

```
ASN-Finder/
├── main.py                 # Main script
├── config_example.ini      # Configuration file template
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── data/
│   └── vpn_hosts.txt      # VPN ASN database
├── exports/               # Output directory (auto-created)
└── utils/                 # Utility modules
    ├── __init__.py
    ├── csv_exporter.py
    ├── json_exporter.py
    ├── html_exporter.py
    ├── sql_exporter.py
    ├── cloudflare_exporter.py
    ├── format_detector.py
    ├── file_handler.py
    ├── vpn_detector.py
    └── config_reader.py
```

## Performance Tips

1. **Multithreading**: Increase threads for faster processing of large IP lists
   ```bash
   python main.py ips.txt -t 20  # Use 20 threads
   ```

2. **ASN Only Mode**: Use default mode (without `--full`) for faster processing and smaller output files

3. **Batch Processing**: Process IPs in batches if you have a very large list (>10,000 IPs)

## Troubleshooting

### Common Issues

**Issue**: `ipwhois not installed`
```bash
pip install ipwhois
```

**Issue**: `pandas not installed`
```bash
pip install pandas
```

**Issue**: VPN detection not working
- Ensure `data/vpn_hosts.txt` exists
- Check file permissions
- Verify the file format is correct

**Issue**: Exports directory permission error
- Check write permissions in the current directory
- The script will attempt to create the `exports/` directory automatically

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2026 MrEgyptian

## Contributing

Contributions, issues, and feature requests are welcome!

## Acknowledgments

- Uses `ipwhois` library for ASN lookups
- VPN ASN database compiled from various sources
- Cloudflare firewall rules format based on Cloudflare API documentation
