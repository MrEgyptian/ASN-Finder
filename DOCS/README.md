# ASN-Finder Documentation

Welcome to the comprehensive documentation for ASN-Finder. This documentation covers installation, usage, configuration, and advanced features.

## Documentation Index

1. **[Installation Guide](INSTALLATION.md)** - Step-by-step installation instructions
2. **[User Guide](USER_GUIDE.md)** - Comprehensive usage instructions and examples
3. **[Configuration Reference](CONFIGURATION.md)** - Detailed configuration file documentation
4. **[Command-Line Reference](COMMAND_LINE.md)** - Complete command-line options reference
5. **[Output Formats](OUTPUT_FORMATS.md)** - Documentation for all supported output formats
6. **[VPN Detection](VPN_DETECTION.md)** - VPN detection feature documentation
7. **[Cloudflare Integration](CLOUDFLARE.md)** - Cloudflare firewall rules documentation
8. **[Examples](EXAMPLES.md)** - Real-world usage examples and use cases
9. **[Troubleshooting](TROUBLESHOOTING.md)** - Common issues and solutions
10. **[Developer Guide](DEVELOPER.md)** - API documentation and extension guide
11. **[FAQ](FAQ.md)** - Frequently asked questions

## Quick Links

- **Getting Started**: See [Installation Guide](INSTALLATION.md) and [User Guide](USER_GUIDE.md)
- **Configuration**: Check [Configuration Reference](CONFIGURATION.md) for all settings
- **Output Formats**: Learn about formats in [Output Formats](OUTPUT_FORMATS.md)
- **Problems?**: Check [Troubleshooting](TROUBLESHOOTING.md) for solutions

## Overview

ASN-Finder is a powerful Python tool for querying ASN (Autonomous System Number) information for IP addresses using WHOIS data. It supports:

- ✅ Multiple export formats (CSV, JSON, HTML, SQL, Cloudflare rules)
- ✅ Multithreading for fast processing
- ✅ VPN ASN detection
- ✅ Configuration file support
- ✅ Cloudflare firewall rule generation
- ✅ Detailed and concise output modes

## Basic Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Basic ASN lookup
python main.py ips.txt

# Full details with VPN detection
python main.py ips.txt --full --detect-vpn -o results.csv
```

For more information, see the [User Guide](USER_GUIDE.md).

## Contributing

Contributions are welcome! Please see the main [README.md](../README.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

Copyright (c) 2026 MrEgyptian
