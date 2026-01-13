# Troubleshooting

Common issues and solutions for ASN-Finder.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Runtime Errors](#runtime-errors)
3. [Output Issues](#output-issues)
4. [Performance Issues](#performance-issues)
5. [VPN Detection Issues](#vpn-detection-issues)
6. [Configuration Issues](#configuration-issues)
7. [Network Issues](#network-issues)

## Installation Issues

### pip: command not found

**Symptom**: `pip: command not found` error

**Solutions**:
- Use `python -m pip` instead: `python -m pip install -r requirements.txt`
- Install pip: `python -m ensurepip --upgrade`
- On Linux: `sudo apt-get install python3-pip`

### Permission denied during installation

**Symptom**: Permission errors when installing packages

**Solutions**:
- Use virtual environment (recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  venv\Scripts\activate     # Windows
  pip install -r requirements.txt
  ```
- Use `--user` flag: `pip install --user -r requirements.txt`
- On Linux/macOS: Use `sudo` (not recommended)

### ipwhois installation fails

**Symptom**: Error installing `ipwhois`

**Solutions**:
- Upgrade pip: `pip install --upgrade pip`
- Install dependencies: `pip install ipwhois`
- Check internet connection
- Verify Python version (3.7+): `python --version`

### pandas installation fails

**Symptom**: Error installing `pandas`

**Solutions**:
- Upgrade pip and setuptools: `pip install --upgrade pip setuptools wheel`
- Install pandas: `pip install pandas`
- On Windows: May need Visual C++ Build Tools
- Check Python version compatibility

## Runtime Errors

### ModuleNotFoundError: No module named 'utils'

**Symptom**: `ModuleNotFoundError: No module named 'utils'`

**Solutions**:
- Ensure you're running from the correct directory
- Verify `utils/` directory exists
- Check `utils/__init__.py` exists
- Run from project root: `python main.py ips.txt`

### FileNotFoundError: config.ini

**Symptom**: Warning about missing config file

**Solutions**:
- This is normal if you haven't created `config.ini`
- Create from example: `cp config_example.ini config.ini`
- Or ignore the warning (defaults will be used)

### FileNotFoundError: data/vpn_hosts.txt

**Symptom**: VPN detection warning about missing database

**Solutions**:
- Verify `data/vpn_hosts.txt` exists
- Check file path in `config.ini`
- VPN detection will be disabled (this is expected if file is missing)

### Invalid IP address format

**Symptom**: Errors about invalid IP addresses

**Solutions**:
- Check input file format (one IP per line)
- Remove invalid entries from input file
- Verify IP addresses are valid IPv4 format
- Check for hidden characters or encoding issues

## Output Issues

### Empty output file

**Symptom**: Output file is empty or missing

**Solutions**:
- Check input file has valid IPs
- Verify write permissions in exports directory
- Check for errors in console output
- Ensure at least one IP was processed successfully

### Wrong format in output

**Symptom**: Output format doesn't match expected format

**Solutions**:
- Check format selection: `-f csv`, `-f json`, etc.
- Verify file extension matches format
- Use explicit format: `-f json` instead of relying on extension

### Missing columns in output

**Symptom**: Expected columns are missing

**Solutions**:
- Use `--full` for full details mode
- Check `--fields` selection includes desired columns
- Verify column names are correct (case-sensitive, spaces matter)
- Check config file `cols` settings

### CSV encoding issues

**Symptom**: Special characters appear incorrectly in CSV

**Solutions**:
- CSV uses UTF-8 encoding (should handle most characters)
- Open CSV in text editor with UTF-8 encoding
- Use JSON format for better Unicode support

## Performance Issues

### Slow processing

**Symptom**: Processing is very slow

**Solutions**:
- Increase thread count: `-t 20` or `-t 30`
- Use ASN-only mode (don't use `--full` for initial scans)
- Check network connectivity
- Reduce thread count if hitting rate limits
- Process in smaller batches

### High memory usage

**Symptom**: High memory consumption

**Solutions**:
- Process in smaller batches
- Don't use `--full` for very large lists
- Reduce thread count
- Close other applications

### Rate limiting / timeouts

**Symptom**: Many errors, timeouts, or rate limit messages

**Solutions**:
- Reduce thread count: `-t 5` or `-t 10`
- Add delays between requests (not configurable, but reducing threads helps)
- Process in smaller batches
- Wait and retry later

## VPN Detection Issues

### VPN detection not working

**Symptom**: `Type` field shows `N/A` for all entries

**Solutions**:
- Verify `data/vpn_hosts.txt` exists
- Check file permissions (must be readable)
- Verify `--detect-vpn` flag is used
- Check console for error messages
- Verify file format is correct

### All entries show "Normal"

**Symptom**: No VPN ASNs detected

**Possible Reasons**:
- IP list doesn't contain VPN ASNs (this is normal)
- Database is outdated
- VPN provider uses residential IPs

**Solutions**:
- Test with known VPN IPs
- Update `data/vpn_hosts.txt`
- Verify database format

### Database file not found

**Symptom**: Warning about missing VPN database

**Solutions**:
- Ensure `data/vpn_hosts.txt` exists
- Check path in `config.ini`
- Verify file permissions
- VPN detection will be disabled (expected behavior)

## Configuration Issues

### Config file not being read

**Symptom**: Settings from config file not applied

**Solutions**:
- Verify `config.ini` exists in script directory
- Check file syntax (INI format)
- Use `-c` to specify config file path
- Check for syntax errors in config file

### Invalid configuration values

**Symptom**: Settings ignored, using defaults

**Solutions**:
- Verify value formats (boolean, integer, string)
- Check valid options for each setting
- Review config file syntax
- Check console for warnings

### Column names not working

**Symptom**: `cols` setting in config not working

**Solutions**:
- Verify exact column names (case-sensitive)
- Check for spaces: `AS Name` not `ASName`
- Use quotes for multi-word names in command-line
- Check available columns for your output mode

## Network Issues

### Connection errors

**Symptom**: Many connection errors or timeouts

**Solutions**:
- Check internet connectivity
- Verify firewall isn't blocking connections
- Try reducing thread count
- Check WHOIS service availability
- Retry later (temporary network issues)

### DNS resolution failures

**Symptom**: DNS-related errors

**Solutions**:
- Check DNS settings
- Verify internet connectivity
- Try different DNS servers
- Check for proxy settings

### WHOIS service unavailable

**Symptom**: WHOIS lookup failures

**Solutions**:
- Wait and retry (temporary service issues)
- Check WHOIS service status
- Verify IP addresses are valid
- Some IPs may not have WHOIS data available

## General Tips

### Debugging

1. **Start simple**: Test with a small IP list first
2. **Check console output**: Error messages provide clues
3. **Verify inputs**: Check input file format and content
4. **Test options**: Try with minimal options first
5. **Check logs**: Review error messages carefully

### Getting Help

1. **Check documentation**: Review relevant docs
2. **Verify setup**: Ensure installation is correct
3. **Test with examples**: Try examples from documentation
4. **Check versions**: Verify Python and library versions
5. **Review error messages**: Read error messages carefully

### Common Mistakes

1. **Wrong directory**: Not running from project root
2. **Invalid IP format**: IPs must be valid IPv4 format
3. **Missing dependencies**: Not installing requirements
4. **Wrong options**: Using incompatible option combinations
5. **File permissions**: Insufficient permissions for files/directories

## Next Steps

- See [Installation Guide](INSTALLATION.md) for installation help
- Check [User Guide](USER_GUIDE.md) for usage examples
- Review [Configuration Reference](CONFIGURATION.md) for config help
- Check [FAQ](FAQ.md) for common questions
