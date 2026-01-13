# Output Formats

Detailed documentation for all supported output formats in ASN-Finder.

## Supported Formats

ASN-Finder supports five output formats:

1. **CSV** - Comma-Separated Values (default)
2. **JSON** - JavaScript Object Notation
3. **HTML** - HyperText Markup Language
4. **SQL** - Structured Query Language
5. **Cloudflare** - Cloudflare firewall rules (JSON)

## Format Selection

Select format using the `-f` or `--format` option:

```bash
python main.py ips.txt -f csv -o results.csv
python main.py ips.txt -f json -o results.json
python main.py ips.txt -f html -o results.html
python main.py ips.txt -f sql -o results.sql
python main.py ips.txt -f cloudflare -o rules.json
```

Format is auto-detected from file extension if `-f` is not specified:
- `.csv` → CSV
- `.json` → JSON (or Cloudflare if `-f cloudflare` is used)
- `.html` → HTML
- `.sql` → SQL

## CSV Format

### Overview

CSV (Comma-Separated Values) is the default format, suitable for spreadsheet applications and data analysis.

### Usage

```bash
python main.py ips.txt -f csv -o results.csv
```

### Configuration Options

Configure CSV output in `config.ini`:

```ini
[csv]
cols = IP, ASN, Country
line_separator = \n
quote_character = "
```

#### cols

- **Description**: Comma-separated list of columns to include
- **Default**: All columns
- **Example**: `cols = IP, ASN, Country, Type`

#### line_separator

- **Description**: Line separator character(s)
- **Default**: `\n` (Unix/Linux/macOS)
- **Options**: `\n` (Unix), `\r\n` (Windows), `\r` (old Mac)
- **Example**: `line_separator = \r\n`

#### quote_character

- **Description**: Character used to quote fields
- **Default**: `"` (double quote)
- **Example**: `quote_character = '`

### Example Output

```csv
IP,ASN,Error
8.8.8.8,AS15169,
1.1.1.1,AS13335,
```

### Use Cases

- Import into Excel, Google Sheets, or other spreadsheet applications
- Data analysis with pandas, R, or other tools
- Simple data exchange format
- Log file analysis

## JSON Format

### Overview

JSON (JavaScript Object Notation) provides structured data in a human-readable format, ideal for APIs and programming.

### Usage

```bash
python main.py ips.txt -f json -o results.json
```

### Configuration Options

Configure JSON output in `config.ini`:

```ini
[json]
cols = IP, ASN, Country
indent = 2
```

#### cols

- **Description**: Comma-separated list of columns to include
- **Default**: All columns
- **Example**: `cols = IP, ASN, "AS Name", Country`

#### indent

- **Description**: Indentation level (0 = compact, 2 = readable, 4 = very readable)
- **Default**: `2`
- **Range**: 0-10
- **Example**: `indent = 4`

**Command-line override**: `--json-indent`

```bash
python main.py ips.txt -f json --json-indent 4 -o results.json
```

### Example Output

```json
[
  {
    "IP": "8.8.8.8",
    "ASN": "AS15169",
    "Error": ""
  },
  {
    "IP": "1.1.1.1",
    "ASN": "AS13335",
    "Error": ""
  }
]
```

### Use Cases

- API responses
- Web applications
- Programmatic data processing
- Configuration files
- Data exchange between systems

## HTML Format

### Overview

HTML format produces web-ready output with embedded CSS styling, perfect for viewing in browsers.

### Usage

```bash
python main.py ips.txt -f html -o results.html
```

### Configuration Options

Configure HTML output in `config.ini`:

```ini
[html]
cols = IP, ASN, Country, Type
table_class = table table-striped
```

#### cols

- **Description**: Comma-separated list of columns to include
- **Default**: All columns
- **Example**: `cols = IP, ASN, "AS Name", Country`

#### table_class

- **Description**: CSS class(es) for the HTML table
- **Default**: `table table-striped`
- **Example**: `table_class = table table-bordered table-hover`

**Command-line override**: `--html-table-class`

```bash
python main.py ips.txt -f html --html-table-class "table table-bordered" -o results.html
```

### Styling

The HTML output includes embedded CSS with:
- Responsive table design
- Striped rows for readability
- Hover effects
- Professional color scheme

### Example Output Structure

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>ASN Lookup Results</title>
    <style>...</style>
</head>
<body>
    <h1>ASN Lookup Results</h1>
    <p>Total records: 100</p>
    <table class="table table-striped" id="asn_results">
        <!-- Table content -->
    </table>
</body>
</html>
```

### Use Cases

- Viewing results in web browsers
- Sharing results with non-technical users
- Generating reports
- Embedding in web pages
- Email attachments

## SQL Format

### Overview

SQL format generates SQL statements for database import, including CREATE TABLE and INSERT statements.

### Usage

```bash
python main.py ips.txt -f sql -o results.sql
```

### Configuration Options

Configure SQL output in `config.ini`:

```ini
[sql]
cols = IP, ASN, Country
create_table = true
insert_into = true
```

#### cols

- **Description**: Comma-separated list of columns to include
- **Default**: All columns
- **Example**: `cols = IP, ASN, "AS Name", Country`

#### create_table

- **Description**: Include CREATE TABLE statement
- **Default**: `true`
- **Options**: `true`, `false`

**Command-line override**: `--sql-no-create-table`

```bash
python main.py ips.txt -f sql --sql-no-create-table -o inserts.sql
```

#### insert_into

- **Description**: Include INSERT statements
- **Default**: `true`
- **Options**: `true`, `false`

**Command-line override**: `--sql-no-insert`

```bash
python main.py ips.txt -f sql --sql-no-insert -o schema.sql
```

### Example Output

```sql
-- ASN Lookup Results
-- Total records: 2

CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    IP TEXT,
    ASN TEXT,
    Error TEXT
);

INSERT INTO results (IP, ASN, Error) VALUES ('8.8.8.8', 'AS15169', '');
INSERT INTO results (IP, ASN, Error) VALUES ('1.1.1.1', 'AS13335', '');
```

### Database Compatibility

The SQL output is compatible with:
- SQLite (primary target)
- MySQL (with minor modifications)
- PostgreSQL (with minor modifications)

### Table Structure

- **Primary Key**: `id` (auto-incrementing integer)
- **Column Types**: All TEXT (for compatibility)
- **Table Name**: Derived from filename (sanitized)

### Use Cases

- Database import
- Data persistence
- Data analysis in databases
- Integration with database workflows
- Backup and restore operations

## Cloudflare Format

### Overview

Cloudflare format generates JSON firewall rules compatible with Cloudflare's API for blocking or allowing traffic based on ASNs.

### Usage

```bash
python main.py ips.txt -f cloudflare --cloudflare-action block -o rules.json
```

### Configuration Options

Configure Cloudflare output in `config.ini`:

```ini
[CLOUDFLARE]
rule_action = block
rule_description = ASN-based firewall rule
```

#### rule_action

- **Description**: Action for the firewall rule
- **Default**: `block`
- **Options**: `block`, `allow`

**Command-line override**: `--cloudflare-action`

```bash
python main.py ips.txt -f cloudflare --cloudflare-action allow -o allow_rules.json
```

#### rule_description

- **Description**: Description for the firewall rule
- **Default**: `ASN-based firewall rule`
- **Type**: String

**Command-line override**: `--cloudflare-description`

```bash
python main.py ips.txt -f cloudflare --cloudflare-description "Block VPN ASNs" -o rules.json
```

### Example Output

```json
{
  "action": "block",
  "expression": "(ip.geoip.asnum in {15169 13335 32934})",
  "description": "ASN-based firewall rule"
}
```

### Cloudflare Integration

To use the generated rules:

1. **Copy the JSON** from the output file
2. **Use Cloudflare API** or **Dashboard** to create firewall rules
3. **Apply the rule** to your zone

### Expression Format

The expression uses Cloudflare's expression syntax:
```
(ip.geoip.asnum in {ASN1 ASN2 ASN3 ...})
```

ASNs are automatically extracted and formatted (numbers only, no "AS" prefix).

### Use Cases

- Blocking VPN traffic
- Allowing specific ASNs
- Security policy enforcement
- Traffic filtering
- DDoS protection rules

## Format Comparison

| Format | Readability | File Size | Use Case | Programmatic Access |
|--------|-------------|-----------|----------|---------------------|
| CSV | Medium | Small | Spreadsheets, analysis | Easy |
| JSON | High | Medium | APIs, programming | Very Easy |
| HTML | High (visual) | Medium | Viewing, reports | Difficult |
| SQL | Medium | Medium | Database import | Easy |
| Cloudflare | Medium | Small | Firewall rules | Easy |

## Choosing a Format

- **CSV**: For spreadsheet analysis, simple data exchange
- **JSON**: For APIs, web applications, programmatic processing
- **HTML**: For viewing in browsers, sharing with non-technical users
- **SQL**: For database import, data persistence
- **Cloudflare**: For Cloudflare firewall rule generation

## Next Steps

- See [User Guide](USER_GUIDE.md) for usage examples
- Check [Configuration Reference](CONFIGURATION.md) for format-specific settings
- Review [Examples](EXAMPLES.md) for real-world usage
