# MottaHunter Usage Guide

This document provides examples of how to use MottaHunter for email reconnaissance.

## Basic Commands

### Hunting for Emails

```bash
# Hunt for emails on Google
python harvester.py hunt --domain example.com --google

# Hunt for emails on multiple sources
python harvester.py hunt --domain example.com --google --twitter --linkedin

# Hunt with multiple Google pages (10 pages)
python harvester.py hunt --domain example.com --google --pages 10

# Hunt and validate in one go
python harvester.py hunt --domain example.com --google --validate --sender-email your@email.com
```

### Validating Email Permutations

```bash
# Validate all permutations
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com

# Validate with higher permutation level
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com --level 3

# Validate with custom check email
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com --check-email contact@example.com

# Skip default email check
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com --no-check

# Split permutations (e.g., part 2 of 4)
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com --part 2 --total-parts 4
```

### Advanced Options

```bash
# Customize delay range (min max in seconds)
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com --delay 5 10

# Increase debug level for more verbose output
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com --debug 2
```

## Output Files

When hunting for emails, MottaHunter saves the results in the `motta_findings` directory:

- **TXT format**: `domain_timestamp.txt`
- **CSV format**: `domain_timestamp.csv`

## Running Tests

```bash
# Run the test suite
python -m unittest tests.py
```

## Tips from MottaSec Fox

1. Start with Google hunting as it's often the most fruitful source
2. Use the `--no-check` option when targeting domains that don't have standard info@ addresses
3. For domains with strict rate limits, use the permutation splitting feature
4. Always use a dedicated sender email for validation to avoid being flagged
5. Increase the delay between validation attempts if you encounter blocks

Remember: MottaHunter is for educational and authorized security assessment purposes only. Always obtain proper authorization before scanning any domain. 