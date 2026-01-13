# User Guide

Comprehensive guide to using ASN-Finder for ASN lookups and data export.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Input File Format](#input-file-format)
3. [Output Formats](#output-formats)
4. [Output Modes](#output-modes)
5. [VPN Detection](#vpn-detection)
6. [Field Selection](#field-selection)
7. [Data Separation](#data-separation)
8. [Multithreading](#multithreading)
9. [Configuration Files](#configuration-files)
10. [Advanced Usage](#advanced-usage)

## Basic Usage

### Simple ASN Lookup

The most basic usage queries ASNs for IP addresses in a file:

```bash
python main.py ips.txt
```

This will:
- Read IP addresses from `ips.txt`
- Query ASN information for each IP
- Save results to `exports/asn_results.csv` (default)
- Use 10 threads (default)
- Show only ASN information (default mode)

### Specify Output File

```bash
python main.py ips.txt -o my_results.csv
```

### Specify Output Format

```bash
# JSON format
python main.py ips.txt -o results.json -f json

# HTML format
python main.py ips.txt -o results.html -f html

# SQL format
python main.py ips.txt -o results.sql -f sql

# Cloudflare rules
python main.py ips.txt -f cloudflare -o rules.json
```

Format is auto-detected from file extension if `-f` is not specified.

## Input File Format

### Standard Format

Create a text file with one IP address per line:

```
1.2.3.4
5.6.7.8
9.10.11.12
192.168.1.1
```

### Comments

Lines starting with `#` are treated as comments and ignored:

```
# This is a comment
1.2.3.4
5.6.7.8
# Another comment
9.10.11.12
```

### Empty Lines

Empty lines are ignored automatically.

### Example Input File

```
# List of IPs to check
8.8.8.8
8.8.4.4
1.1.1.1
# More IPs
208.67.222.222
208.67.220.220
```

## Output Formats

ASN-Finder supports multiple output formats. See [Output Formats](OUTPUT_FORMATS.md) for detailed documentation.

### CSV (Comma-Separated Values)

Default format, suitable for spreadsheet applications:

```bash
python main.py ips.txt -f csv -o results.csv
```

### JSON (JavaScript Object Notation)

Structured data format, suitable for APIs and programming:

```bash
python main.py ips.txt -f json -o results.json
```

### HTML (HyperText Markup Language)

Web-ready format with styling:

```bash
python main.py ips.txt -f html -o results.html
```

### SQL (Structured Query Language)

SQL statements for database import:

```bash
python main.py ips.txt -f sql -o results.sql
```

### Cloudflare Rules

JSON format for Cloudflare firewall rules:

```bash
python main.py ips.txt -f cloudflare -o rules.json
```

## Output Modes

### ASN Only Mode (Default)

Shows minimal information: IP address and ASN.

**Fields**: `IP`, `ASN`, `Error`, `Type` (if VPN detection enabled)

```bash
python main.py ips.txt
```

### Full Details Mode

Shows comprehensive ASN information.

**Fields**: `IP`, `ASN`, `AS Name`, `Country`, `IP Block`, `Registry`, `Error`, `Type` (if VPN detection enabled)

```bash
python main.py ips.txt --full
```

## VPN Detection

Enable VPN ASN detection to identify VPN providers:

```bash
python main.py ips.txt --detect-vpn
```

When enabled, results include a `Type` field with values:
- `VPN` - Identified as VPN ASN
- `Normal` - Not a VPN ASN
- `N/A` - Error or unknown

See [VPN Detection](VPN_DETECTION.md) for detailed documentation.

## Field Selection

Select specific fields to export:

```bash
python main.py ips.txt --fields IP ASN Country
```

Available fields:
- `IP` - IP address
- `ASN` - Autonomous System Number
- `AS Name` - AS name/description
- `Country` - Country code
- `IP Block` - IP address block/CIDR
- `Registry` - Regional Internet Registry
- `Error` - Error message (if any)
- `Type` - VPN/Normal (if VPN detection enabled)

**Note**: `IP` is always included even if not specified.

## Data Separation

Separate results into multiple files based on a column value:

```bash
# Separate by Type (VPN vs Normal)
python main.py ips.txt --detect-vpn --separate-by Type

# Separate by Country
python main.py ips.txt --full --separate-by Country

# Separate by Registry
python main.py ips.txt --full --separate-by Registry

# Separate by ASN
python main.py ips.txt --full --separate-by ASN
```

Separated files are saved in the `exports/` directory with descriptive names.

## Multithreading

Control the number of concurrent queries for better performance:

```bash
# Use 20 threads
python main.py ips.txt -t 20

# Use 50 threads (for very large lists)
python main.py large_list.txt -t 50
```

**Recommendations**:
- Small lists (< 100 IPs): 10 threads (default)
- Medium lists (100-1000 IPs): 20-30 threads
- Large lists (> 1000 IPs): 30-50 threads
- Very large lists (> 10000 IPs): 50-100 threads (be mindful of rate limits)

Higher thread counts process faster but may hit rate limits or use more resources.

## Configuration Files

Use configuration files for persistent settings. See [Configuration Reference](CONFIGURATION.md) for details.

### Basic Configuration

1. Copy the example config:
   ```bash
   cp config_example.ini config.ini
   ```

2. Edit `config.ini` with your preferences

3. Use it:
   ```bash
   python main.py ips.txt  # Uses config.ini automatically
   ```

### Custom Configuration File

```bash
python main.py ips.txt -c my_config.ini
```

**Note**: Command-line arguments override configuration file settings.

## Advanced Usage

### Combining Options

Combine multiple options for powerful queries:

```bash
# Full details, VPN detection, JSON output, 20 threads
python main.py ips.txt --full --detect-vpn -f json -o results.json -t 20

# Custom fields, HTML output, separate by country
python main.py ips.txt --fields IP ASN Country -f html --separate-by Country
```

### Cloudflare Integration

Generate firewall rules for Cloudflare:

```bash
# Block VPN ASNs
python main.py ips.txt --detect-vpn -f cloudflare --cloudflare-action block -o block_rules.json

# Allow specific ASNs
python main.py ips.txt -f cloudflare --cloudflare-action allow -o allow_rules.json --cloudflare-description "Allowed ASNs"
```

See [Cloudflare Integration](CLOUDFLARE.md) for detailed documentation.

### Format-Specific Options

Some formats support additional options:

```bash
# JSON with custom indentation
python main.py ips.txt -f json --json-indent 4

# SQL without CREATE TABLE
python main.py ips.txt -f sql --sql-no-create-table

# SQL without INSERT statements
python main.py ips.txt -f sql --sql-no-insert

# HTML with custom CSS class
python main.py ips.txt -f html --html-table-class "my-table"
```

### Processing Large Lists

For very large IP lists (>10,000 IPs):

1. **Use high thread count**:
   ```bash
   python main.py huge_list.txt -t 50
   ```

2. **Process in batches** (split your file first):
   ```bash
   # Split file into chunks (example for Linux/macOS)
   split -l 1000 huge_list.txt chunk_
   
   # Process each chunk
   python main.py chunk_aa -o results_aa.csv
   python main.py chunk_ab -o results_ab.csv
   # ... etc
   ```

3. **Use ASN-only mode** for faster processing:
   ```bash
   python main.py huge_list.txt  # Don't use --full
   ```

## Output Directory

All exports are automatically saved to the `exports/` directory. The directory is created automatically if it doesn't exist.

You can change the output directory in `config.ini`:
```ini
[DEFAULT]
exports_dir = my_exports
```

## Progress Tracking

The script shows real-time progress:
```
[1/100] 8.8.8.8: ✓ ASN: AS15169 (Google LLC)
[2/100] 8.8.4.4: ✓ ASN: AS15169 (Google LLC)
...
```

## Error Handling

Errors are handled gracefully:
- Invalid IP addresses are skipped with error messages
- Network errors are logged in the `Error` field
- Processing continues even if some queries fail

Check the `Error` field in results to see any issues.

## Best Practices

1. **Start with a small test file** to verify settings
2. **Use appropriate thread counts** - not too high to avoid rate limits
3. **Use ASN-only mode** for initial scans, then use `--full` for detailed analysis
4. **Enable VPN detection** when analyzing security-related IP lists
5. **Use configuration files** for repeated workflows
6. **Save important results** - exports are overwritten if using the same filename

## Next Steps

- See [Examples](EXAMPLES.md) for real-world usage scenarios
- Check [Configuration Reference](CONFIGURATION.md) for advanced settings
- Read [Output Formats](OUTPUT_FORMATS.md) for format-specific details
- Review [Troubleshooting](TROUBLESHOOTING.md) if you encounter issues
