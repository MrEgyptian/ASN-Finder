# Configuration Reference

Complete reference for ASN-Finder configuration files.

## Configuration File Format

ASN-Finder uses INI format configuration files. The default configuration file is `config.ini`, but you can specify a custom file with `-c` or `--config`.

### Creating a Configuration File

1. Copy the example configuration:
   ```bash
   cp config_example.ini config.ini
   ```

2. Edit `config.ini` with your preferred settings

3. The configuration is automatically loaded when running the script

## Configuration Sections

### [DEFAULT] Section

Global settings that apply to all operations.

#### threads
- **Type**: Integer
- **Default**: `10`
- **Description**: Number of threads for concurrent ASN queries
- **Example**: `threads = 20`
- **Command-line override**: `-t` or `--threads`

#### output_format
- **Type**: String
- **Default**: `csv`
- **Valid values**: `csv`, `json`, `html`, `sql`, `cloudflare`, `auto`
- **Description**: Default output format
- **Example**: `output_format = json`
- **Command-line override**: `-f` or `--format`

#### full_details
- **Type**: Boolean
- **Default**: `false`
- **Description**: Show full details (ASN, AS Name, Country, etc.) instead of ASN only
- **Example**: `full_details = true`
- **Command-line override**: `--full`

#### detect_vpn
- **Type**: Boolean
- **Default**: `false`
- **Description**: Enable VPN ASN detection
- **Example**: `detect_vpn = true`
- **Command-line override**: `--detect-vpn`

#### exports_dir
- **Type**: String (directory path)
- **Default**: `exports`
- **Description**: Directory for exported files (created automatically if missing)
- **Example**: `exports_dir = my_exports`
- **Command-line override**: None (set in config only)

#### vpn_data_file
- **Type**: String (file path)
- **Default**: `data/vpn_hosts.txt`
- **Description**: Path to VPN ASN database file
- **Example**: `vpn_data_file = data/custom_vpn_list.txt`
- **Command-line override**: None (set in config only)

### [CLOUDFLARE] Section

Settings specific to Cloudflare firewall rule generation.

#### rule_action
- **Type**: String
- **Default**: `block`
- **Valid values**: `block`, `allow`
- **Description**: Action for Cloudflare firewall rules
- **Example**: `rule_action = allow`
- **Command-line override**: `--cloudflare-action`

#### rule_description
- **Type**: String
- **Default**: `ASN-based firewall rule`
- **Description**: Description for Cloudflare firewall rules
- **Example**: `rule_description = Block VPN ASNs`
- **Command-line override**: `--cloudflare-description`

### [csv] Section

Settings for CSV export format.

#### cols
- **Type**: String (comma-separated list)
- **Default**: Not set (all columns)
- **Description**: Comma-separated list of columns to include
- **Example**: `cols = IP, ASN, Country`
- **Note**: Column names must match exactly (spaces are significant)
- **Command-line override**: `--fields`

#### line_separator
- **Type**: String
- **Default**: `\n`
- **Description**: Line separator character(s)
- **Example**: `line_separator = \r\n` (Windows line endings)
- **Note**: Use `\n` for Unix, `\r\n` for Windows

#### quote_character
- **Type**: Character
- **Default**: `"`
- **Description**: Character used to quote fields
- **Example**: `quote_character = '`

### [json] Section

Settings for JSON export format.

#### cols
- **Type**: String (comma-separated list)
- **Default**: Not set (all columns)
- **Description**: Comma-separated list of columns to include
- **Example**: `cols = IP, ASN, Country`
- **Command-line override**: `--fields`

#### indent
- **Type**: Integer
- **Default**: `2`
- **Description**: JSON indentation level (0 = compact, 2 = readable, 4 = very readable)
- **Example**: `indent = 4`
- **Command-line override**: `--json-indent`

### [html] Section

Settings for HTML export format.

#### cols
- **Type**: String (comma-separated list)
- **Default**: Not set (all columns)
- **Description**: Comma-separated list of columns to include
- **Example**: `cols = IP, ASN, Country`
- **Command-line override**: `--fields`

#### table_class
- **Type**: String (CSS class names)
- **Default**: `table table-striped`
- **Description**: CSS class(es) for the HTML table
- **Example**: `table_class = table table-bordered table-hover`
- **Command-line override**: `--html-table-class`

### [sql] Section

Settings for SQL export format.

#### cols
- **Type**: String (comma-separated list)
- **Default**: Not set (all columns)
- **Description**: Comma-separated list of columns to include
- **Example**: `cols = IP, ASN, Country`
- **Command-line override**: `--fields`

#### create_table
- **Type**: Boolean
- **Default**: `true`
- **Description**: Include CREATE TABLE statement
- **Example**: `create_table = false`
- **Command-line override**: `--sql-no-create-table`

#### insert_into
- **Type**: Boolean
- **Default**: `true`
- **Description**: Include INSERT statements
- **Example**: `insert_into = false`
- **Command-line override**: `--sql-no-insert`

## Example Configuration File

```ini
[DEFAULT]
# Performance settings
threads = 20

# Default output format
output_format = csv

# Show full details by default
full_details = false

# Enable VPN detection
detect_vpn = true

# Output directory
exports_dir = exports

# VPN data file
vpn_data_file = data/vpn_hosts.txt

[CLOUDFLARE]
# Cloudflare rule action
rule_action = block

# Cloudflare rule description
rule_description = Block VPN and hosting provider ASNs

[csv]
# CSV columns to include
cols = IP, ASN, Country, Type

# CSV formatting
line_separator = \n
quote_character = "

[json]
# JSON columns
cols = IP, ASN, AS Name, Country, Type

# JSON indentation
indent = 2

[html]
# HTML columns
cols = IP, ASN, AS Name, Country, Type

# HTML table styling
table_class = table table-striped table-bordered

[sql]
# SQL columns
cols = IP, ASN, AS Name, Country, Type

# SQL options
create_table = true
insert_into = true
```

## Configuration Precedence

Settings are applied in this order (later overrides earlier):

1. **Configuration file defaults** - Values in `config.ini`
2. **Command-line arguments** - Override config file settings

### Examples

**Example 1**: Config file sets `threads = 20`, command-line uses `-t 10`
- **Result**: Uses 10 threads (command-line overrides)

**Example 2**: Config file sets `full_details = false`, no command-line flag
- **Result**: Uses false (ASN-only mode)

**Example 3**: Config file sets `output_format = csv`, command-line uses `-f json`
- **Result**: Uses JSON format (command-line overrides)

## Column Names Reference

When using `cols` in format sections, use these exact column names:

| Column Name | Description | Available In |
|-------------|-------------|--------------|
| `IP` | IP address | Always |
| `ASN` | Autonomous System Number | Always |
| `AS Name` | AS name/description | Full details mode |
| `Country` | Country code | Full details mode |
| `IP Block` | IP address block/CIDR | Full details mode |
| `Registry` | Regional Internet Registry | Full details mode |
| `Error` | Error message | Always (if error) |
| `Type` | VPN/Normal | VPN detection enabled |

**Important**: 
- Column names are case-sensitive
- Spaces are significant (`AS Name` not `ASName`)
- `IP` is always included even if not in `cols` list

## Boolean Values

Boolean settings accept these values (case-insensitive):
- **True**: `true`, `1`, `yes`, `on`
- **False**: `false`, `0`, `no`, `off`

## File Paths

File paths in configuration can be:
- **Relative paths**: Relative to the script's working directory
  - Example: `data/vpn_hosts.txt`
- **Absolute paths**: Full system path
  - Example: `/path/to/vpn_hosts.txt` (Linux/macOS)
  - Example: `C:\path\to\vpn_hosts.txt` (Windows)

## Validation

The script validates configuration values:
- Invalid values fall back to defaults
- Errors are logged but don't stop execution
- Missing sections use default values

## Tips

1. **Start with defaults**: Copy `config_example.ini` and modify only what you need
2. **Use comments**: Add comments (lines starting with `#`) to document your settings
3. **Test changes**: Test configuration changes with a small IP list first
4. **Backup config**: Keep backups of working configurations
5. **Version control**: Consider excluding `config.ini` from version control (it's in `.gitignore`)

## Troubleshooting Configuration

### Config file not found
- **Symptom**: Settings not applied, using defaults
- **Solution**: Ensure `config.ini` exists in the script directory, or use `-c` to specify path

### Invalid values
- **Symptom**: Settings ignored, using defaults
- **Solution**: Check value format (boolean, integer, string) and valid options

### Column names not working
- **Symptom**: `cols` setting ignored
- **Solution**: Verify exact column names (case-sensitive, spaces matter)

### Thread count not working
- **Symptom**: Always uses 10 threads
- **Solution**: Ensure integer value, check command-line override with `-t`

## Next Steps

- See [Command-Line Reference](COMMAND_LINE.md) for all options
- Check [User Guide](USER_GUIDE.md) for usage examples
- Review [Output Formats](OUTPUT_FORMATS.md) for format-specific settings
