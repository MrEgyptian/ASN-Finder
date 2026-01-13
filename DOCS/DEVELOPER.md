# Developer Guide

API documentation and development guide for ASN-Finder.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Core Functions](#core-functions)
3. [Utility Modules](#utility-modules)
4. [Extending ASN-Finder](#extending-asn-finder)
5. [Development Setup](#development-setup)
6. [Testing](#testing)
7. [Contributing](#contributing)

## Project Structure

```
ASN-Finder/
├── main.py                 # Main script and entry point
├── config_example.ini      # Configuration template
├── requirements.txt        # Python dependencies
├── README.md              # Project README
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
├── data/
│   └── vpn_hosts.txt     # VPN ASN database
├── exports/              # Output directory (generated)
└── utils/                # Utility modules
    ├── __init__.py
    ├── csv_exporter.py
    ├── json_exporter.py
    ├── html_exporter.py
    ├── sql_exporter.py
    ├── cloudflare_exporter.py
    ├── format_detector.py
    ├── file_handler.py
    ├── vpn_detector.py
    ├── config_reader.py
    └── data_filter.py
```

## Core Functions

### main.py

#### `query_asn_whois(ip)`

Query ASN information using ipwhois library.

**Parameters**:
- `ip` (str): IP address to query

**Returns**:
- `dict`: Dictionary with ASN information:
  - `asn`: ASN number (str)
  - `as_name`: AS name/description (str)
  - `country`: Country code (str)
  - `ip_block`: IP block/CIDR (str)
  - `registry`: Regional Internet Registry (str)
  - `error`: Error message (str, empty if successful)

#### `process_single_ip(ip, index, total, full_details=False, vpn_asns_set=None)`

Process a single IP address and return the result.

**Parameters**:
- `ip` (str): IP address to process
- `index` (int): Index in the IP list
- `total` (int): Total number of IPs
- `full_details` (bool): Include full details
- `vpn_asns_set` (set, optional): Set of VPN ASNs for detection

**Returns**:
- `tuple`: (index, ip, result_dict, is_success)

#### `save_results(results, filename, output_format='csv', ...)`

Save ASN lookup results to file in specified format.

**Parameters**:
- `results` (list): List of result dictionaries
- `filename` (str): Output filename
- `output_format` (str): Output format
- `exports_dir` (str): Exports directory
- `cloudflare_action` (str): Cloudflare rule action
- `columns` (list, optional): Columns to include
- `separate_by` (str, optional): Column to separate by
- `config` (ConfigParser, optional): Configuration object
- Additional format-specific parameters

**Returns**:
- None (saves file directly)

## Utility Modules

### utils/csv_exporter.py

#### `export_to_csv(df, filename, config_dict=None)`

Export DataFrame to CSV file.

**Parameters**:
- `df` (pandas.DataFrame): DataFrame to export
- `filename` (str): Output filename
- `config_dict` (dict, optional): CSV configuration

**Returns**:
- `tuple`: (success: bool, message: str)

### utils/json_exporter.py

#### `export_to_json(df, filename, config_dict=None)`

Export DataFrame to JSON file.

**Parameters**:
- `df` (pandas.DataFrame): DataFrame to export
- `filename` (str): Output filename
- `config_dict` (dict, optional): JSON configuration

**Returns**:
- `tuple`: (success: bool, message: str)

### utils/html_exporter.py

#### `export_to_html(df, filename, config_dict=None)`

Export DataFrame to HTML file.

**Parameters**:
- `df` (pandas.DataFrame): DataFrame to export
- `filename` (str): Output filename
- `config_dict` (dict, optional): HTML configuration

**Returns**:
- `tuple`: (success: bool, message: str)

### utils/sql_exporter.py

#### `export_to_sql(df, filename, config_dict=None)`

Export DataFrame to SQL file.

**Parameters**:
- `df` (pandas.DataFrame): DataFrame to export
- `filename` (str): Output filename
- `config_dict` (dict, optional): SQL configuration

**Returns**:
- `tuple`: (success: bool, message: str, table_name: str)

### utils/cloudflare_exporter.py

#### `export_to_cloudflare(df, filename, action='block', description='...')`

Export DataFrame to Cloudflare firewall rules format.

**Parameters**:
- `df` (pandas.DataFrame): DataFrame to export
- `filename` (str): Output filename
- `action` (str): Rule action ('block' or 'allow')
- `description` (str): Rule description

**Returns**:
- `tuple`: (success: bool, message: str)

### utils/vpn_detector.py

#### `load_vpn_asns(data_dir='data', filename='vpn_hosts.txt')`

Load VPN ASN database from file.

**Parameters**:
- `data_dir` (str): Data directory
- `filename` (str): VPN database filename

**Returns**:
- `set`: Set of VPN ASN numbers (strings)

#### `is_vpn_asn(asn, vpn_asns_set)`

Check if ASN is a VPN ASN.

**Parameters**:
- `asn` (str): ASN to check
- `vpn_asns_set` (set): Set of VPN ASNs

**Returns**:
- `bool`: True if VPN ASN, False otherwise

### utils/config_reader.py

#### `load_config(config_file='config.ini')`

Load configuration from INI file.

**Parameters**:
- `config_file` (str): Config file path

**Returns**:
- `ConfigParser` or `None`: Configuration object

#### `get_config_value(config, section, key, default_value)`

Get configuration value with fallback.

**Parameters**:
- `config` (ConfigParser): Config object
- `section` (str): Section name
- `key` (str): Key name
- `default_value`: Default value

**Returns**:
- Configuration value or default

#### `get_config_int(config, section, key, default_value)`

Get integer configuration value.

#### `get_config_bool(config, section, key, default_value)`

Get boolean configuration value.

#### `get_section_dict(config, section)`

Get all options from a section as a dictionary.

## Extending ASN-Finder

### Adding New Export Format

1. Create new exporter in `utils/`:
   ```python
   # utils/xml_exporter.py
   def export_to_xml(df, filename, config_dict=None):
       # Implementation
       return True, "Success message"
   ```

2. Add to `utils/__init__.py`:
   ```python
   from .xml_exporter import export_to_xml
   __all__ = [..., 'export_to_xml']
   ```

3. Add format detection in `utils/format_detector.py`

4. Add handler in `main.py` `save_results()` function

5. Add command-line option if needed

### Adding New Configuration Options

1. Add to `config_example.ini`

2. Add parsing in `main.py` or relevant utility

3. Add command-line argument if needed

4. Update documentation

### Adding New Data Sources

1. Create new data loader in `utils/`

2. Integrate in `main.py`

3. Add configuration options

4. Update documentation

## Development Setup

### Prerequisites

- Python 3.7+
- Git
- Virtual environment (recommended)

### Setup Steps

1. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd ASN-Finder
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install development dependencies** (optional):
   ```bash
   pip install pytest black flake8
   ```

### Code Style

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions
- Keep functions focused and small

## Testing

### Manual Testing

Test with sample IPs:

```bash
# Create test file
echo "8.8.8.8" > test_ips.txt
echo "1.1.1.1" >> test_ips.txt

# Run tests
python main.py test_ips.txt
python main.py test_ips.txt --full
python main.py test_ips.txt --detect-vpn
```

### Unit Testing

Create test files in `tests/` directory:

```python
# tests/test_vpn_detector.py
import unittest
from utils.vpn_detector import is_vpn_asn

class TestVPNDetector(unittest.TestCase):
    def test_is_vpn_asn(self):
        vpn_asns = {'12345', '67890'}
        self.assertTrue(is_vpn_asn('AS12345', vpn_asns))
        self.assertFalse(is_vpn_asn('AS99999', vpn_asns))
```

Run tests:
```bash
pytest tests/
```

## Contributing

### Contribution Process

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Update documentation
6. Submit pull request

### Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Keep commits focused
- Write clear commit messages

## Next Steps

- See [User Guide](USER_GUIDE.md) for usage
- Check [Configuration Reference](CONFIGURATION.md) for config details
- Review code comments for implementation details
