# 🦊 MottaHunter: Email Reconnaissance Tool

<p align="center">
  <img src="images/logo2.png" alt="MottaHunter Logo" width="300">
</p>

**MottaHunter** is a powerful email reconnaissance and validation tool developed by the MottaSec team for internal use. We're sharing it with the community because we believe in making security tools accessible to everyone.

> "Finding the right email is like hunting for treasure. MottaHunter is your map." - *MottaSec Ghost*

## 🚀 Features

- **Multi-source Email Scraping**: Extract email addresses from Google, Twitter, and LinkedIn
- **Smart Email Permutation**: Generate likely email addresses based on name patterns
- **SMTP Validation**: Verify if email addresses actually exist
- **Catch-all Detection**: Identify domains that accept all emails
- **Rate Limiting**: Avoid detection with configurable delays
- **Permutation Splitting**: Split validation tasks to avoid rate limits
- **Custom Default Checks**: Configure how validation checks are performed

## 📋 Requirements

- Python 3.6+
- Required Python packages (see `requirements.txt`)
- API credentials for Twitter (optional)
- LinkedIn account for scraping (optional)

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/MottaSec/mottahunter.git
cd mottahunter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

## 🎮 Usage

MottaHunter has two main commands: `scrape` and `validate`.

### Scraping Emails

```bash
# Scrape emails from Google (saves results to files)
python harvester.py scrape --domain example.com --google

# Scrape from multiple sources
python harvester.py scrape --domain example.com --google --twitter --linkedin

# Scrape and validate in one go
python harvester.py scrape --domain example.com --google --validate --sender-email your@email.com
```

### Validating Email Permutations

```bash
# Validate all permutations
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com

# Validate with custom check email
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com --check-email contact@example.com

# Skip default email check
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com --no-check

# Split permutations (e.g., part 2 of 4)
python harvester.py validate --domain example.com --first-name John --last-name Doe --sender-email your@email.com --part 2 --total-parts 4
```

### Advanced Options

- `--level`: Permutation level (1=light, 2=medium, 3=heavy)
- `--delay`: Random delay range in seconds (min max)
- `--debug`: Debug level (0=minimal, 1=moderate, 2=verbose)
- `--pages`: Number of Google search pages to scrape
- `--no-check`: Skip checking default email (info@domain)
- `--check-email`: Custom email to check instead of info@domain

## 🦊 MottaSec Fox Tips

- Use a dedicated email for validation to avoid being flagged
- Start with small delays and increase if needed
- Use the `--debug 2` option to see detailed SMTP responses
- Split permutations for domains with strict rate limits
- Always check if a domain is catch-all before validating permutations

## 🔒 Security & Ethics

This tool is for educational and authorized security assessment purposes only. Always:

1. Obtain proper authorization before scanning any domain
2. Respect rate limits and robots.txt
3. Follow each platform's terms of service
4. Use responsibly and ethically

## 🧪 Testing

Run the test suite to verify everything is working correctly:

```bash
python -m unittest tests.py
```

## 📜 License

This project is licensed under the MottaSec Custom License - see the [LICENSE](LICENSE) file for details.

## 👥 About MottaSec

MottaSec is a team of security professionals with a passion for building effective security tools. Our team (Ghost, Fox, Aces, and the rest of the Jedis) believes security tools should be powerful yet accessible.

## 📞 Contact

For questions, feedback, or collaboration, reach out to us at ghost@mottasec.com

---

*"May the Fox be with you!"* - MottaSec Team 