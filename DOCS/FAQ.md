# Frequently Asked Questions (FAQ)

Common questions and answers about ASN-Finder.

## General Questions

### What is ASN-Finder?

ASN-Finder is a Python tool for querying ASN (Autonomous System Number) information for IP addresses using WHOIS data. It supports multiple export formats, VPN detection, and Cloudflare firewall rule generation.

### What is an ASN?

ASN (Autonomous System Number) is a unique identifier assigned to networks on the internet. It helps identify which organization or company owns a particular IP address or IP range.

### What Python version do I need?

Python 3.7 or higher is required. Check your version with:
```bash
python --version
```

### Is ASN-Finder free to use?

Yes, ASN-Finder is licensed under the MIT License and is free to use, modify, and distribute.

## Installation Questions

### How do I install ASN-Finder?

See the [Installation Guide](INSTALLATION.md) for detailed instructions. Basic steps:
1. Download/clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py ips.txt`

### Do I need to install anything besides Python?

You need to install the dependencies listed in `requirements.txt`:
- `ipwhois>=1.2.0`
- `pandas>=2.0.0`

Install with: `pip install -r requirements.txt`

### Can I use a virtual environment?

Yes, using a virtual environment is recommended. See [Installation Guide](INSTALLATION.md) for details.

## Usage Questions

### How do I use ASN-Finder?

Basic usage:
```bash
python main.py ips.txt
```

See [User Guide](USER_GUIDE.md) for comprehensive usage instructions.

### What format should my input file be in?

Input file should contain one IP address per line:
```
8.8.8.8
1.1.1.1
192.168.1.1
```

Comments (lines starting with `#`) and empty lines are ignored.

### Where are output files saved?

All output files are saved in the `exports/` directory by default. You can change this in `config.ini`.

### Can I specify a custom output directory?

Yes, set `exports_dir` in `config.ini`:
```ini
[DEFAULT]
exports_dir = my_output
```

## Configuration Questions

### Do I need a configuration file?

No, configuration files are optional. The script works with defaults, but using a config file is recommended for persistent settings.

### How do I create a configuration file?

Copy the example:
```bash
cp config_example.ini config.ini
```

Then edit `config.ini` with your preferences.

### Do command-line arguments override the config file?

Yes, command-line arguments always override configuration file settings.

## Output Format Questions

### What output formats are supported?

ASN-Finder supports:
- CSV (default)
- JSON
- HTML
- SQL
- Cloudflare (firewall rules)

See [Output Formats](OUTPUT_FORMATS.md) for details.

### How do I change the output format?

Use the `-f` or `--format` option:
```bash
python main.py ips.txt -f json -o results.json
```

### Can I customize the output format?

Yes, format-specific options are available. See [Output Formats](OUTPUT_FORMATS.md) and [Configuration Reference](CONFIGURATION.md).

## VPN Detection Questions

### What is VPN detection?

VPN detection identifies IP addresses belonging to VPN providers, hosting services, and datacenters using a database of known ASNs.

### How do I enable VPN detection?

Use the `--detect-vpn` flag:
```bash
python main.py ips.txt --detect-vpn
```

Or set in `config.ini`:
```ini
[DEFAULT]
detect_vpn = true
```

### How accurate is VPN detection?

VPN detection uses a comprehensive database but has limitations:
- May flag legitimate hosting/datacenter ASNs
- New VPN providers may not be in the database
- Some VPN services use residential IPs (not detected)

See [VPN Detection](VPN_DETECTION.md) for details.

### Can I update the VPN database?

Yes, replace `data/vpn_hosts.txt` with an updated version. The database format is documented in [VPN Detection](VPN_DETECTION.md).

## Performance Questions

### How fast is ASN-Finder?

Performance depends on:
- Number of IPs
- Thread count
- Network speed
- WHOIS service response times

Typical performance: 10-50 IPs per second with default settings (10 threads).

### How many threads should I use?

Recommendations:
- Small lists (< 100 IPs): 10 threads (default)
- Medium lists (100-1000 IPs): 20-30 threads
- Large lists (> 1000 IPs): 30-50 threads

Higher thread counts may hit rate limits.

### Can I process very large IP lists?

Yes, but consider:
- Using high thread count: `-t 30`
- Processing in batches
- Using ASN-only mode (not `--full`)
- Monitoring for rate limits

## Cloudflare Questions

### How do I generate Cloudflare rules?

Use the Cloudflare format:
```bash
python main.py ips.txt -f cloudflare --cloudflare-action block -o rules.json
```

See [Cloudflare Integration](CLOUDFLARE.md) for details.

### How do I apply Cloudflare rules?

Use the Cloudflare Dashboard or API. See [Cloudflare Integration](CLOUDFLARE.md) for instructions.

### Can I generate allow rules?

Yes, use `--cloudflare-action allow`:
```bash
python main.py ips.txt -f cloudflare --cloudflare-action allow -o allow_rules.json
```

## Troubleshooting Questions

### The script is slow. What can I do?

- Increase thread count: `-t 20` or `-t 30`
- Use ASN-only mode (don't use `--full`)
- Check network connectivity
- Process in smaller batches

### I'm getting many errors. Why?

Common causes:
- Invalid IP addresses in input file
- Network connectivity issues
- WHOIS service rate limiting (reduce thread count)
- Temporary service unavailability

See [Troubleshooting](TROUBLESHOOTING.md) for solutions.

### VPN detection isn't working. Why?

- Ensure `--detect-vpn` flag is used
- Verify `data/vpn_hosts.txt` exists
- Check file permissions
- Review console output for errors

See [Troubleshooting](TROUBLESHOOTING.md) for details.

### Configuration file isn't being read. Why?

- Verify `config.ini` exists in script directory
- Check file syntax (INI format)
- Use `-c` to specify custom config file
- Review console for error messages

## Advanced Questions

### Can I use ASN-Finder programmatically?

Yes, you can import and use functions from the modules. See [Developer Guide](DEVELOPER.md) for API documentation.

### Can I add custom export formats?

Yes, see [Developer Guide](DEVELOPER.md) for extension instructions.

### Can I customize the VPN database?

Yes, create a custom database file and update `config.ini`. See [VPN Detection](VPN_DETECTION.md) for format details.

### Can I process IPs from stdin?

Not directly, but you can pipe to a file:
```bash
cat ips.txt | python main.py -  # Not supported
cat ips.txt > temp.txt && python main.py temp.txt  # Use file instead
```

### Can I filter results by country or ASN?

Use field selection and data separation:
```bash
# Separate by country
python main.py ips.txt --full --separate-by Country

# Filter specific fields
python main.py ips.txt --fields IP ASN Country
```

Then process the separated files or filter programmatically.

## License and Legal Questions

### What license is ASN-Finder under?

MIT License. See [LICENSE](../LICENSE) file for details.

### Can I use ASN-Finder commercially?

Yes, the MIT License allows commercial use.

### Can I modify ASN-Finder?

Yes, the MIT License allows modification.

### Do I need to credit ASN-Finder?

The MIT License requires including the license and copyright notice. See [LICENSE](../LICENSE) for details.

## Getting Help

### Where can I get more help?

- Review the documentation in `DOCS/`
- Check [Troubleshooting](TROUBLESHOOTING.md) for common issues
- Review [Examples](EXAMPLES.md) for usage scenarios
- Check the main [README.md](../README.md)

### How do I report bugs or request features?

Check the repository's issue tracker or contribution guidelines.

### Can I contribute to ASN-Finder?

Yes, contributions are welcome! See [Developer Guide](DEVELOPER.md) for contribution guidelines.

## Next Steps

- See [User Guide](USER_GUIDE.md) for usage instructions
- Check [Examples](EXAMPLES.md) for real-world scenarios
- Review [Troubleshooting](TROUBLESHOOTING.md) if you have issues
