# Command-Line Reference

Complete reference for all ASN-Finder command-line arguments.

## Syntax

```bash
python main.py <input_file> [options]
```

## Required Arguments

### input_file

- **Description**: Input file containing IP addresses (one per line)
- **Type**: File path
- **Example**: `ips.txt`, `data/ip_list.txt`, `/path/to/ips.txt`

## Optional Arguments

### Output Options

#### `-o`, `--output`

- **Description**: Output filename
- **Type**: String (filename)
- **Default**: `asn_results.csv`
- **Example**: `-o results.csv`, `--output my_results.json`
- **Notes**: 
  - File is saved in the `exports/` directory
  - Format is auto-detected from extension unless `-f` is specified

#### `-f`, `--format`

- **Description**: Output format
- **Type**: Choice
- **Choices**: `csv`, `json`, `html`, `sql`, `cloudflare`, `auto`
- **Default**: `auto`
- **Example**: `-f json`, `--format html`
- **Notes**:
  - `auto` detects format from file extension
  - Overrides config file `output_format` setting

### Configuration Options

#### `-c`, `--config`

- **Description**: Configuration file path
- **Type**: File path
- **Default**: `config.ini`
- **Example**: `-c my_config.ini`, `--config /path/to/config.ini`
- **Notes**: 
  - Uses default `config.ini` if not specified
  - File must exist (script won't create it)

### Performance Options

#### `-t`, `--threads`

- **Description**: Number of threads for concurrent queries
- **Type**: Integer
- **Default**: `10`
- **Example**: `-t 20`, `--threads 50`
- **Notes**:
  - Higher values = faster processing but more resource usage
  - Recommended: 10-50 for most use cases
  - Overrides config file `threads` setting

### Output Mode Options

#### `--full`

- **Description**: Show full details (ASN, AS Name, Country, IP Block, Registry)
- **Type**: Flag (no value)
- **Default**: `False` (ASN only mode)
- **Example**: `--full`
- **Notes**:
  - Without `--full`: Shows only IP, ASN, Error, Type
  - With `--full`: Shows all available fields
  - Overrides config file `full_details` setting

#### `--detect-vpn`

- **Description**: Enable VPN ASN detection
- **Type**: Flag (no value)
- **Default**: `False` (disabled)
- **Example**: `--detect-vpn`
- **Notes**:
  - Adds `Type` field with VPN/Normal values
  - Requires `data/vpn_hosts.txt` file
  - Overrides config file `detect_vpn` setting

### Field Selection Options

#### `--fields`

- **Description**: Select specific fields to export
- **Type**: Space-separated list
- **Default**: All fields (or columns from config)
- **Example**: `--fields IP ASN Country`, `--fields IP ASN "AS Name" Type`
- **Available fields**:
  - `IP` - IP address (always included)
  - `ASN` - Autonomous System Number
  - `AS Name` - AS name/description (full details mode)
  - `Country` - Country code (full details mode)
  - `IP Block` - IP address block/CIDR (full details mode)
  - `Registry` - Regional Internet Registry (full details mode)
  - `Error` - Error message
  - `Type` - VPN/Normal (if VPN detection enabled)
- **Notes**:
  - Field names are case-sensitive
  - Use quotes for fields with spaces: `"AS Name"`
  - `IP` is always included even if not specified
  - Overrides config file `cols` settings

#### `--separate-by`

- **Description**: Separate data into different files based on column value
- **Type**: Choice
- **Choices**: `Type`, `Country`, `Registry`, `ASN`
- **Default**: `None` (no separation)
- **Example**: `--separate-by Type`, `--separate-by Country`
- **Notes**:
  - Creates multiple output files, one per unique value
  - File names include the value (e.g., `results_VPN.csv`)
  - Useful for filtering VPN vs Normal, or by country/registry

### Cloudflare Options

#### `--cloudflare-action`

- **Description**: Cloudflare rule action
- **Type**: Choice
- **Choices**: `block`, `allow`
- **Default**: `block`
- **Example**: `--cloudflare-action allow`
- **Notes**:
  - Only used with `-f cloudflare` format
  - Overrides config file `rule_action` setting

#### `--cloudflare-description`

- **Description**: Cloudflare rule description
- **Type**: String
- **Default**: From config or "ASN-based firewall rule"
- **Example**: `--cloudflare-description "Block VPN ASNs"`
- **Notes**:
  - Only used with `-f cloudflare` format
  - Overrides config file `rule_description` setting

### Format-Specific Options

#### `--json-indent`

- **Description**: JSON output indentation level
- **Type**: Integer
- **Default**: `2` (or from config)
- **Example**: `--json-indent 4`
- **Notes**:
  - Only used with `-f json` format
  - `0` = compact (no indentation)
  - `2` or `4` = readable
  - Overrides config file `indent` setting

#### `--sql-no-create-table`

- **Description**: Exclude CREATE TABLE statement from SQL output
- **Type**: Flag (no value)
- **Default**: `False` (CREATE TABLE included)
- **Example**: `--sql-no-create-table`
- **Notes**:
  - Only used with `-f sql` format
  - Use when you only want INSERT statements
  - Overrides config file `create_table` setting

#### `--sql-no-insert`

- **Description**: Exclude INSERT statements from SQL output
- **Type**: Flag (no value)
- **Default**: `False` (INSERT statements included)
- **Example**: `--sql-no-insert`
- **Notes**:
  - Only used with `-f sql` format
  - Use when you only want CREATE TABLE statement
  - Overrides config file `insert_into` setting

#### `--html-table-class`

- **Description**: HTML table CSS class
- **Type**: String
- **Default**: `table table-striped` (or from config)
- **Example**: `--html-table-class "table table-bordered"`
- **Notes**:
  - Only used with `-f html` format
  - Can specify multiple classes separated by spaces
  - Overrides config file `table_class` setting

## Examples

### Basic Examples

```bash
# Simple ASN lookup
python main.py ips.txt

# Specify output file
python main.py ips.txt -o results.csv

# Use JSON format
python main.py ips.txt -f json -o results.json

# Use 20 threads
python main.py ips.txt -t 20
```

### Advanced Examples

```bash
# Full details with VPN detection, JSON output
python main.py ips.txt --full --detect-vpn -f json -o results.json

# Custom fields, HTML output
python main.py ips.txt --fields IP ASN Country -f html -o results.html

# Separate by Type (VPN vs Normal)
python main.py ips.txt --detect-vpn --separate-by Type

# Cloudflare rules with custom description
python main.py ips.txt -f cloudflare --cloudflare-action block \
  --cloudflare-description "Block VPN ASNs" -o rules.json

# SQL format without CREATE TABLE
python main.py ips.txt -f sql --sql-no-create-table -o inserts.sql

# JSON with custom indentation
python main.py ips.txt -f json --json-indent 4 -o results.json
```

### Combined Options

```bash
# Full workflow: VPN detection, full details, custom fields, HTML output, 30 threads
python main.py ips.txt --full --detect-vpn --fields IP ASN "AS Name" Country Type \
  -f html --html-table-class "table table-striped table-bordered" -t 30 -o results.html
```

## Argument Precedence

Command-line arguments override configuration file settings in this order:

1. Configuration file values (lowest priority)
2. Command-line arguments (highest priority)

## Getting Help

Display help message with all options:

```bash
python main.py --help
python main.py -h
```

## Common Patterns

### Pattern 1: Quick Scan (ASN Only)

```bash
python main.py ips.txt
```

### Pattern 2: Detailed Analysis

```bash
python main.py ips.txt --full -t 20 -o detailed_results.csv
```

### Pattern 3: VPN Analysis

```bash
python main.py ips.txt --detect-vpn --full --separate-by Type -o vpn_analysis.csv
```

### Pattern 4: Country Analysis

```bash
python main.py ips.txt --full --separate-by Country -f json -o by_country.json
```

### Pattern 5: Cloudflare Block List

```bash
python main.py ips.txt --detect-vpn -f cloudflare --cloudflare-action block \
  --cloudflare-description "Block VPN ASNs" -o block_rules.json
```

## Tips

1. **Start simple**: Begin with basic options, add complexity as needed
2. **Use help**: Run `python main.py --help` to see all options
3. **Test first**: Test with a small IP list before processing large files
4. **Combine wisely**: Not all option combinations make sense (e.g., `--separate-by` with Cloudflare format)
5. **Check output**: Verify output format and content before processing large datasets

## Next Steps

- See [User Guide](USER_GUIDE.md) for usage examples
- Check [Configuration Reference](CONFIGURATION.md) for config file options
- Review [Output Formats](OUTPUT_FORMATS.md) for format-specific details
