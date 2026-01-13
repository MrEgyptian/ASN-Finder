# Cloudflare Integration

Documentation for generating Cloudflare firewall rules with ASN-Finder.

## Overview

ASN-Finder can generate Cloudflare firewall rules in JSON format that can be imported into Cloudflare's firewall rules system to block or allow traffic based on ASNs.

## Basic Usage

### Generate Block Rules

```bash
python main.py ips.txt -f cloudflare --cloudflare-action block -o block_rules.json
```

### Generate Allow Rules

```bash
python main.py ips.txt -f cloudflare --cloudflare-action allow -o allow_rules.json
```

## Output Format

The output is a JSON file compatible with Cloudflare's firewall rules API:

```json
{
  "action": "block",
  "expression": "(ip.geoip.asnum in {15169 13335 32934})",
  "description": "ASN-based firewall rule"
}
```

### Fields

- **action**: `block` or `allow`
- **expression**: Cloudflare expression syntax matching ASNs
- **description**: Human-readable description

## Configuration

### Configuration File

```ini
[CLOUDFLARE]
rule_action = block
rule_description = ASN-based firewall rule
```

### Command-Line Options

```bash
# Set action
--cloudflare-action block
--cloudflare-action allow

# Set description
--cloudflare-description "Block VPN ASNs"
```

## Expression Format

The expression uses Cloudflare's `ip.geoip.asnum` field:

```
(ip.geoip.asnum in {ASN1 ASN2 ASN3 ...})
```

ASNs are automatically:
- Extracted from results
- Formatted as numbers only (no "AS" prefix)
- Sorted for readability
- Deduplicated

## Use Cases

### Block VPN ASNs

Generate rules to block known VPN providers:

```bash
# Detect VPN ASNs
python main.py ips.txt --detect-vpn --separate-by Type

# Generate block rules for VPN ASNs only
python main.py exports/results_VPN.csv -f cloudflare \
  --cloudflare-action block \
  --cloudflare-description "Block VPN ASNs" \
  -o block_vpn.json
```

### Allow Specific ASNs

Generate allow rules for trusted ASNs:

```bash
python main.py trusted_ips.txt -f cloudflare \
  --cloudflare-action allow \
  --cloudflare-description "Allow trusted ASNs" \
  -o allow_trusted.json
```

### Block Hosting Providers

Generate rules to block hosting/datacenter ASNs:

```bash
python main.py hosting_ips.txt -f cloudflare \
  --cloudflare-action block \
  --cloudflare-description "Block hosting providers" \
  -o block_hosting.json
```

## Applying Rules to Cloudflare

### Method 1: Cloudflare Dashboard

1. Log in to Cloudflare Dashboard
2. Select your domain
3. Go to **Security** → **WAF** → **Custom Rules**
4. Click **Create rule**
5. Use the expression from the JSON file
6. Set the action (block/allow)
7. Add the description
8. Save the rule

### Method 2: Cloudflare API

Use the Cloudflare API to create rules programmatically:

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/{zone_id}/firewall/rules" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  --data @block_rules.json
```

**Note**: You may need to adapt the JSON format to match Cloudflare's API requirements.

### Method 3: Terraform

Use Terraform to manage Cloudflare firewall rules:

```hcl
resource "cloudflare_firewall_rule" "asn_block" {
  zone_id = var.zone_id
  description = "Block VPN ASNs"
  action = "block"
  filter_id = cloudflare_filter.asn_filter.id
  priority = 100
}

resource "cloudflare_filter" "asn_filter" {
  zone_id = var.zone_id
  expression = "(ip.geoip.asnum in {15169 13335 32934})"
}
```

## Advanced Usage

### Combining with VPN Detection

Generate rules specifically for VPN ASNs:

```bash
# Step 1: Identify VPN ASNs
python main.py ip_list.txt --detect-vpn --separate-by Type

# Step 2: Generate rules for VPN ASNs only
python main.py exports/results_VPN.csv -f cloudflare \
  --cloudflare-action block \
  --cloudflare-description "Block VPN providers" \
  -o block_vpn_rules.json
```

### Multiple Rule Sets

Generate different rule sets for different purposes:

```bash
# Block VPN ASNs
python main.py vpn_ips.txt -f cloudflare --cloudflare-action block \
  --cloudflare-description "Block VPN ASNs" -o block_vpn.json

# Allow trusted ASNs
python main.py trusted_ips.txt -f cloudflare --cloudflare-action allow \
  --cloudflare-description "Allow trusted ASNs" -o allow_trusted.json
```

### Custom Descriptions

Add descriptive information:

```bash
python main.py ips.txt -f cloudflare \
  --cloudflare-action block \
  --cloudflare-description "Block hosting providers - Updated 2026-01-15" \
  -o block_hosting.json
```

## Expression Limitations

### Maximum ASNs

Cloudflare expressions have size limits:
- Maximum expression length: 4096 characters
- Recommended: Keep ASN lists under 500-1000 ASNs per rule

### Large ASN Lists

For very large ASN lists, consider:

1. **Split into multiple rules**:
   ```bash
   # Split IP list into chunks
   split -l 500 large_list.txt chunk_
   
   # Generate rules for each chunk
   python main.py chunk_aa -f cloudflare -o rules_aa.json
   python main.py chunk_ab -f cloudflare -o rules_ab.json
   ```

2. **Filter before generating rules**:
   ```bash
   # Filter to specific ASNs first
   python main.py ips.txt --fields IP ASN | grep "AS12345" > filtered.txt
   python main.py filtered.txt -f cloudflare -o filtered_rules.json
   ```

## Testing Rules

Before applying rules to production:

1. **Test in Development**:
   - Apply rules to a test zone first
   - Verify behavior matches expectations

2. **Monitor Logs**:
   - Check Cloudflare firewall event logs
   - Verify rules are triggering correctly

3. **Gradual Rollout**:
   - Start with less aggressive rules
   - Monitor impact
   - Adjust as needed

## Best Practices

1. **Document Rules**: Use descriptive `description` fields
2. **Test First**: Test rules in development/staging
3. **Monitor Impact**: Check logs after applying rules
4. **Regular Updates**: Update ASN lists regularly
5. **Combine with Other Rules**: Use ASN rules with other firewall rules
6. **Review Periodically**: Review and update rules periodically

## Troubleshooting

### Rule Not Working

**Issue**: Rule doesn't block/allow traffic

**Solutions**:
1. Verify expression syntax is correct
2. Check ASN numbers are valid (numbers only, no "AS" prefix)
3. Verify rule is active in Cloudflare dashboard
4. Check rule priority (higher priority rules execute first)
5. Review Cloudflare firewall event logs

### Expression Too Long

**Issue**: Error about expression length

**Solutions**:
1. Split ASN list into multiple rules
2. Filter ASN list to most important ASNs
3. Use multiple smaller rules instead of one large rule

### Invalid ASN Format

**Issue**: Rule doesn't match ASNs

**Solutions**:
1. Verify ASN format in expression (numbers only)
2. Check ASN numbers are correct
3. Verify ASN exists and is valid

## Examples

### Complete Workflow

```bash
# 1. Collect IPs from logs
cat access.log | awk '{print $1}' | sort -u > ip_list.txt

# 2. Detect VPN ASNs
python main.py ip_list.txt --detect-vpn --full -o analysis.csv

# 3. Separate VPN from Normal
python main.py ip_list.txt --detect-vpn --separate-by Type

# 4. Generate Cloudflare rules for VPN ASNs
python main.py exports/results_VPN.csv -f cloudflare \
  --cloudflare-action block \
  --cloudflare-description "Block VPN ASNs from access logs" \
  -o block_vpn_rules.json

# 5. Apply to Cloudflare (via API or dashboard)
```

### Block Known Bad ASNs

```bash
# Generate rules to block specific ASNs
python main.py known_bad_ips.txt -f cloudflare \
  --cloudflare-action block \
  --cloudflare-description "Block known malicious ASNs" \
  -o block_malicious.json
```

### Allow Trusted Partners

```bash
# Generate rules to allow partner ASNs
python main.py partner_ips.txt -f cloudflare \
  --cloudflare-action allow \
  --cloudflare-description "Allow partner ASNs" \
  -o allow_partners.json
```

## Next Steps

- See [User Guide](USER_GUIDE.md) for general usage
- Check [VPN Detection](VPN_DETECTION.md) for VPN-specific features
- Review [Examples](EXAMPLES.md) for more scenarios
