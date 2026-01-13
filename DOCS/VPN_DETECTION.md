# VPN Detection

Documentation for the VPN ASN detection feature in ASN-Finder.

## Overview

ASN-Finder can identify VPN (Virtual Private Network) ASNs using a comprehensive database of known VPN providers, hosting services, and datacenter ASNs.

## Enabling VPN Detection

### Command-Line

```bash
python main.py ips.txt --detect-vpn
```

### Configuration File

```ini
[DEFAULT]
detect_vpn = true
```

## VPN Database

The VPN detection uses a database file containing ASN numbers of known VPN providers, hosting services, datacenters, and transit providers.

### Database Location

- **Default**: `data/vpn_hosts.txt`
- **Configurable**: Set `vpn_data_file` in `config.ini`

### Database Format

The database file uses a simple format:
```
ASN # Provider Name
```

Example:
```
210558 # 1337 Services GmbH
28716 # AirVPN
21859 # VyprVPN
```

Comments (lines starting with `#`) and empty lines are ignored.

### Database Source

The VPN database is based on the global ASN list maintained by @githubcom13:
- Source: [global-asn-providers-vps-dedicated-colo-transit](https://gist.github.com/githubcom13/2e0a0ab3c130024fe25920854e3120eb)
- Updated regularly with new VPN and hosting providers
- Includes VPS, dedicated servers, colocation, and transit providers

## Output Fields

When VPN detection is enabled, results include a `Type` field:

| Value | Description |
|-------|-------------|
| `VPN` | ASN is in the VPN database (VPN/hosting provider) |
| `Normal` | ASN is not in the VPN database (regular ISP/network) |
| `N/A` | Error occurred or ASN lookup failed |

## Usage Examples

### Basic VPN Detection

```bash
# Detect VPN ASNs
python main.py ips.txt --detect-vpn -o results.csv
```

Output includes `Type` column:
```csv
IP,ASN,Type,Error
8.8.8.8,AS15169,Normal,
1.1.1.1,AS13335,Normal,
123.45.67.89,AS28716,VPN,
```

### VPN Detection with Full Details

```bash
python main.py ips.txt --detect-vpn --full -o results.csv
```

### Separate VPN from Normal

```bash
python main.py ips.txt --detect-vpn --separate-by Type -o results.csv
```

This creates separate files:
- `results_VPN.csv` - VPN ASNs
- `results_Normal.csv` - Normal ASNs

### Filter Only VPN ASNs

After running with `--separate-by Type`, use the `_VPN.csv` file, or filter programmatically:

```bash
# Separate by Type to get VPN-only file
python main.py ips.txt --detect-vpn --separate-by Type
# Use exports/results_VPN.csv
```

## Use Cases

### Security Analysis

Identify VPN connections in security logs:

```bash
python main.py security_log_ips.txt --detect-vpn --full -o security_analysis.csv
```

### Access Control

Generate lists for firewall rules:

```bash
# Get VPN ASNs only
python main.py ip_list.txt --detect-vpn --separate-by Type
# Use the VPN file for blocking rules
```

### Network Monitoring

Analyze network traffic:

```bash
python main.py network_traffic_ips.txt --detect-vpn --full -o network_analysis.csv
```

### Compliance

Identify potential policy violations:

```bash
python main.py user_connection_ips.txt --detect-vpn -o compliance_report.csv
```

## Database Management

### Updating the Database

1. Download the latest database from the source
2. Replace `data/vpn_hosts.txt`
3. Verify format is correct

### Custom Database

Create a custom database file:

1. Create a text file with ASN entries:
   ```
   12345 # Custom Provider 1
   67890 # Custom Provider 2
   ```

2. Update `config.ini`:
   ```ini
   [DEFAULT]
   vpn_data_file = data/custom_vpn_list.txt
   ```

3. Use the custom database:
   ```bash
   python main.py ips.txt --detect-vpn
   ```

### Database Format Requirements

- One ASN per line
- Format: `ASN # Description` (description is optional)
- ASN can be with or without "AS" prefix
- Comments (lines starting with `#`) are ignored
- Empty lines are ignored

Valid formats:
```
210558
AS210558
210558 # Provider Name
AS210558 # Provider Name
```

## Limitations

### Detection Accuracy

- **False Positives**: Legitimate hosting/datacenter ASNs may be flagged as VPN
- **False Negatives**: New VPN providers may not be in the database
- **Generic ASNs**: Some ASNs are used for both VPN and regular services

### Database Coverage

The database includes:
- ✅ Major VPN providers
- ✅ VPS and hosting providers
- ✅ Datacenters and colocation
- ✅ Transit providers
- ❌ Residential VPN services (often use residential IPs)
- ❌ New or obscure VPN providers (may not be in database)

### Performance Impact

VPN detection adds minimal overhead:
- Database is loaded once at startup
- Lookup is O(1) using Python sets
- No significant performance impact

## Troubleshooting

### VPN Detection Not Working

**Issue**: `Type` field shows `N/A` for all entries

**Solutions**:
1. Verify `data/vpn_hosts.txt` exists
2. Check file permissions (must be readable)
3. Verify file format is correct
4. Check for errors in console output

### Database Not Found

**Issue**: Warning message about database file

**Solutions**:
1. Ensure `data/vpn_hosts.txt` exists
2. Check file path in `config.ini`
3. Verify path is relative to script directory
4. Check file permissions

### No VPN ASNs Detected

**Issue**: All entries show `Normal`

**Possible Reasons**:
1. IP list doesn't contain VPN ASNs
2. Database is outdated
3. VPN provider uses residential IPs (not in database)

**Solutions**:
1. Test with known VPN IPs
2. Update database file
3. Verify database format

## Best Practices

1. **Keep Database Updated**: Regularly update `data/vpn_hosts.txt` for new providers
2. **Verify Results**: Manually verify critical detections
3. **Use with Full Details**: Enable `--full` for comprehensive analysis
4. **Separate for Analysis**: Use `--separate-by Type` for easier filtering
5. **Combine with Other Filters**: Use field selection and other options for refined results

## Statistics

After processing, the script shows VPN statistics:

```
Summary:
  Successful queries: 95
  Errors/Invalid: 5
  VPN ASNs: 12
  Normal ASNs: 83
```

## Integration with Other Features

### Field Selection

Select only relevant fields:

```bash
python main.py ips.txt --detect-vpn --fields IP ASN Type -o vpn_only.csv
```

### Cloudflare Integration

Generate Cloudflare rules for VPN ASNs:

```bash
# Block VPN ASNs
python main.py ips.txt --detect-vpn --separate-by Type
# Use the VPN file for Cloudflare rules
python main.py exports/results_VPN.csv -f cloudflare --cloudflare-action block -o block_vpn.json
```

### Data Separation

Separate by Type for different processing:

```bash
python main.py ips.txt --detect-vpn --separate-by Type
# Process VPN and Normal files separately
```

## Next Steps

- See [User Guide](USER_GUIDE.md) for usage examples
- Check [Examples](EXAMPLES.md) for real-world scenarios
- Review [Cloudflare Integration](CLOUDFLARE.md) for firewall rules
