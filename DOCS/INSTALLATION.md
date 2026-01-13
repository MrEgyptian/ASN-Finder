# Installation Guide

This guide covers installation of ASN-Finder and all its dependencies.

## System Requirements

- **Python**: 3.7 or higher
- **Operating System**: Windows, macOS, or Linux
- **pip**: Python package installer (usually included with Python)
- **Internet Connection**: Required for downloading dependencies and performing ASN lookups

## Installation Methods

### Method 1: Standard Installation (Recommended)

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd ASN-Finder
   ```

   Or download and extract the ZIP file, then navigate to the directory.

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `ipwhois>=1.2.0` - For ASN lookup via WHOIS
   - `pandas>=2.0.0` - For data manipulation and export

3. **Verify installation**
   ```bash
   python main.py --help
   ```

   You should see the help message with all available options.

### Method 2: Virtual Environment (Recommended for Development)

Using a virtual environment isolates the project dependencies:

1. **Create a virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Deactivate when done** (optional)
   ```bash
   deactivate
   ```

### Method 3: Using pip directly

If you prefer not to use a requirements file:

```bash
pip install ipwhois>=1.2.0 pandas>=2.0.0
```

## Post-Installation Setup

1. **Create configuration file** (optional but recommended)
   ```bash
   cp config_example.ini config.ini
   ```

   Then edit `config.ini` to customize settings.

2. **Verify VPN data file exists**
   The VPN detection feature requires `data/vpn_hosts.txt`. This file should be included in the repository. If it's missing, VPN detection will be disabled with a warning.

3. **Create exports directory** (optional)
   The script will create the `exports/` directory automatically, but you can create it manually:
   ```bash
   mkdir exports
   ```

## Verification

Test the installation with a simple command:

```bash
# Create a test file with one IP
echo "8.8.8.8" > test_ip.txt

# Run ASN lookup
python main.py test_ip.txt

# Check the output
cat exports/asn_results.csv
```

You should see ASN information for 8.8.8.8 (Google's DNS server).

## Troubleshooting Installation

### Issue: `pip: command not found`

**Solution**: Install pip or use `python -m pip` instead:
```bash
python -m pip install -r requirements.txt
```

### Issue: Permission denied during pip install

**Solution**: 
- On Linux/macOS: Use `sudo` (not recommended) or use a virtual environment
- On Windows: Run command prompt as administrator, or use a virtual environment

### Issue: `ipwhois` installation fails

**Solution**: 
- Ensure you have internet connectivity
- Try upgrading pip: `pip install --upgrade pip`
- Install dependencies separately: `pip install ipwhois`

### Issue: `pandas` installation fails

**Solution**:
- Ensure you have Python 3.7+
- Try: `pip install --upgrade pip setuptools wheel`
- Then: `pip install pandas`

### Issue: Python version too old

**Solution**: 
- Install Python 3.7 or higher
- Check version: `python --version` or `python3 --version`
- Download from [python.org](https://www.python.org/downloads/)

## Optional Dependencies

The following are not required but may be useful:

- **Development tools**:
  - `pytest` - For running tests
  - `black` - For code formatting
  - `flake8` - For linting

## Updating

To update ASN-Finder:

1. **Update the code** (if using git):
   ```bash
   git pull
   ```

2. **Update dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

## Uninstallation

To remove ASN-Finder:

1. **Remove the directory**:
   ```bash
   # Delete the ASN-Finder directory
   rm -rf ASN-Finder  # Linux/macOS
   # or delete the folder manually on Windows
   ```

2. **Remove dependencies** (if not used by other projects):
   ```bash
   pip uninstall ipwhois pandas
   ```

   **Note**: Only uninstall if these packages aren't used by other projects. If using a virtual environment, simply delete the virtual environment directory.

## Next Steps

After installation:
1. Read the [User Guide](USER_GUIDE.md) to learn how to use ASN-Finder
2. Check the [Configuration Reference](CONFIGURATION.md) to customize settings
3. See [Examples](EXAMPLES.md) for usage scenarios
