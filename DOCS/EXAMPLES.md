# Examples

Real-world usage examples and use cases for ASN-Finder.

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Security Analysis](#security-analysis)
3. [Network Monitoring](#network-monitoring)
4. [Access Control](#access-control)
5. [Data Analysis](#data-analysis)
6. [Cloudflare Integration](#cloudflare-integration)
7. [Batch Processing](#batch-processing)
8. [Reporting](#reporting)

## Basic Examples

### Quick ASN Lookup

Simple lookup for a few IPs:

```bash
# Create input file
echo "8.8.8.8" > test_ips.txt
echo "1.1.1.1" >> test_ips.txt

# Run lookup
python main.py test_ips.txt

# View results
cat exports/asn_results.csv
```

### Full Details Lookup

Get comprehensive information:

```bash
python main.py ips.txt --full -o detailed_results.csv
```

### JSON Output

Get structured JSON output:

```bash
python main.py ips.txt -f json -o results.json
```

## Security Analysis

### Analyze Security Logs

Identify VPN connections in security logs:

```bash
# Extract IPs from log file
grep "failed login" auth.log | awk '{print $NF}' | sort -u > suspicious_ips.txt

# Analyze with VPN detection
python main.py suspicious_ips.txt --detect-vpn --full -o security_analysis.csv

# Separate VPN from normal
python main.py suspicious_ips.txt --detect-vpn --separate-by Type
```

### Block VPN Traffic

Generate Cloudflare rules to block VPN ASNs:

```bash
# Detect VPN ASNs
python main.py access_log_ips.txt --detect-vpn --separate-by Type

# Generate block rules
python main.py exports/results_VPN.csv -f cloudflare \
  --cloudflare-action block \
  --cloudflare-description "Block VPN ASNs from access logs" \
  -o block_vpn_rules.json
```

### Identify Hosting Providers

Find hosting/datacenter ASNs:

```bash
python main.py ip_list.txt --detect-vpn --full -o analysis.csv

# Filter for VPN/hosting ASNs
grep "VPN" exports/analysis.csv > hosting_asns.csv
```

## Network Monitoring

### Monitor Network Traffic

Analyze network traffic by ASN:

```bash
# Extract unique IPs from network logs
cat netflow.log | awk '{print $3}' | sort -u > network_ips.txt

# Analyze with full details
python main.py network_ips.txt --full --separate-by Country -o network_analysis.json -f json
```

### Country-Based Analysis

Analyze traffic by country:

```bash
python main.py ip_list.txt --full --separate-by Country -o by_country.csv
```

This creates files like:
- `by_country_US.csv`
- `by_country_GB.csv`
- `by_country_CN.csv`
- etc.

### Registry Analysis

Analyze by Regional Internet Registry:

```bash
python main.py ip_list.txt --full --separate-by Registry -o by_registry.csv
```

## Access Control

### Generate Allow Lists

Generate allow rules for trusted ASNs:

```bash
# Analyze trusted IPs
python main.py trusted_ips.txt --full -o trusted_asns.csv

# Generate allow rules
python main.py trusted_ips.txt -f cloudflare \
  --cloudflare-action allow \
  --cloudflare-description "Allow trusted ASNs" \
  -o allow_trusted.json
```

### Generate Block Lists

Generate block rules for suspicious ASNs:

```bash
# Analyze suspicious IPs
python main.py suspicious_ips.txt --detect-vpn --full -o suspicious_asns.csv

# Generate block rules
python main.py suspicious_ips.txt -f cloudflare \
  --cloudflare-action block \
  --cloudflare-description "Block suspicious ASNs" \
  -o block_suspicious.json
```

## Data Analysis

### Custom Field Selection

Select specific fields for analysis:

```bash
# Only IP, ASN, and Country
python main.py ips.txt --full --fields IP ASN Country -o simplified.csv
```

### Combine with Other Tools

Use with command-line tools:

```bash
# Count unique ASNs
python main.py ips.txt --full -o results.csv
cut -d',' -f2 exports/results.csv | sort -u | wc -l

# Find most common ASNs
cut -d',' -f2 exports/results.csv | sort | uniq -c | sort -rn | head -10

# Filter by country
python main.py ips.txt --full -o results.csv
grep ",US," exports/results.csv > us_ips.csv
```

### Export for Analysis

Export in analysis-friendly formats:

```bash
# JSON for programmatic analysis
python main.py ips.txt -f json --json-indent 4 -o analysis.json

# SQL for database analysis
python main.py ips.txt -f sql -o analysis.sql
```

## Cloudflare Integration

### Complete Cloudflare Workflow

```bash
# 1. Collect IPs from access logs
cat access.log | awk '{print $1}' | sort -u > ip_list.txt

# 2. Detect VPN ASNs
python main.py ip_list.txt --detect-vpn --separate-by Type

# 3. Generate block rules for VPN ASNs
python main.py exports/results_VPN.csv -f cloudflare \
  --cloudflare-action block \
  --cloudflare-description "Block VPN ASNs - $(date +%Y-%m-%d)" \
  -o block_vpn_$(date +%Y%m%d).json

# 4. Apply to Cloudflare (manually or via API)
```

### Multiple Rule Sets

Generate different rule sets:

```bash
# Block VPN ASNs
python main.py vpn_ips.txt -f cloudflare --cloudflare-action block \
  -o block_vpn.json

# Allow trusted ASNs
python main.py trusted_ips.txt -f cloudflare --cloudflare-action allow \
  -o allow_trusted.json

# Block hosting providers
python main.py hosting_ips.txt -f cloudflare --cloudflare-action block \
  --cloudflare-description "Block hosting providers" \
  -o block_hosting.json
```

## Batch Processing

### Process Large Lists

For very large IP lists:

```bash
# Split into chunks (Linux/macOS)
split -l 1000 huge_list.txt chunk_

# Process each chunk
for file in chunk_*; do
  python main.py "$file" -o "results_${file}.csv" -t 30
done

# Combine results (if needed)
cat exports/results_chunk_*.csv > combined_results.csv
```

### Scheduled Processing

Use with cron (Linux/macOS) or Task Scheduler (Windows):

```bash
# Example cron job (daily at 2 AM)
0 2 * * * cd /path/to/ASN-Finder && python main.py daily_ips.txt -o daily_$(date +\%Y\%m\%d).csv
```

## Reporting

### Generate HTML Reports

Create web-ready reports:

```bash
python main.py ips.txt --full --detect-vpn -f html \
  --html-table-class "table table-striped table-bordered" \
  -o report_$(date +%Y%m%d).html
```

### Custom Reports

Generate reports with specific fields:

```bash
# Security report
python main.py security_ips.txt --detect-vpn --full \
  --fields IP ASN "AS Name" Country Type \
  -f html -o security_report.html

# Network report
python main.py network_ips.txt --full \
  --fields IP ASN Country Registry \
  --separate-by Country \
  -f json -o network_report.json
```

## Advanced Examples

### Configuration-Based Workflow

1. Create `config.ini`:
   ```ini
   [DEFAULT]
   threads = 20
   full_details = true
   detect_vpn = true
   output_format = json
   exports_dir = reports
   ```

2. Run with config:
   ```bash
   python main.py ips.txt -o report.json
   ```

### Multi-Step Analysis

```bash
# Step 1: Initial analysis
python main.py ip_list.txt --full -o initial_analysis.csv

# Step 2: Identify VPN ASNs
python main.py ip_list.txt --detect-vpn --separate-by Type

# Step 3: Analyze VPN ASNs separately
python main.py exports/results_VPN.csv --full \
  --separate-by Country -o vpn_by_country.csv

# Step 4: Generate Cloudflare rules
python main.py exports/results_VPN.csv -f cloudflare \
  --cloudflare-action block -o block_vpn.json
```

### Integration Scripts

Create wrapper scripts for common tasks:

```bash
#!/bin/bash
# analyze_and_block.sh

INPUT_FILE=$1
OUTPUT_DIR="reports/$(date +%Y%m%d)"

mkdir -p "$OUTPUT_DIR"

# Analyze
python main.py "$INPUT_FILE" --detect-vpn --full \
  -o "$OUTPUT_DIR/analysis.csv"

# Separate
python main.py "$INPUT_FILE" --detect-vpn --separate-by Type

# Generate rules
python main.py exports/results_VPN.csv -f cloudflare \
  --cloudflare-action block \
  --cloudflare-description "Block VPN ASNs - $(date +%Y-%m-%d)" \
  -o "$OUTPUT_DIR/block_rules.json"

echo "Analysis complete. Results in $OUTPUT_DIR"
```

## Next Steps

- See [User Guide](USER_GUIDE.md) for more usage details
- Check [Configuration Reference](CONFIGURATION.md) for configuration examples
- Review [Troubleshooting](TROUBLESHOOTING.md) if you encounter issues
