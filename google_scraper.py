#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MottaHunter Google Scraper Module
Developed by MottaSec Fox for the MottaHunter toolkit

This module handles Google search scraping to find email addresses.
As MottaSec Ghost says: "Google knows all, we just need to ask nicely."

Author: MottaSec Fox
Website: https://mottasec.com
Contact: ghost@mottasec.com
"""

import re
import requests
import time
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

# ANSI color codes for terminal - MottaSec style!
GREEN = "\033[92m"  # Success - MottaSec Fox approved
RED = "\033[91m"    # Failure - MottaSec Ghost says no
BLUE = "\033[94m"   # Info - MottaSec Aces intel
RESET = "\033[0m"   # Reset to default color

def motta_google_hunt(domain, debug=0, pages=1):
    """
    Hunt through Google search results for potential emails related to the domain.
    
    MottaSec Fox's favorite hunting ground is Google - so much information
    just waiting to be discovered with the right search queries!
    
    Features:
    - Supports pagination across multiple result pages
    - Uses random delays to avoid detection
    - Randomizes User-Agent headers for stealth
    - Focuses on domain-specific email patterns
    
    Args:
        domain: The domain to search for emails
        debug: Debug level (0=minimal, 1=moderate, 2=verbose)
        pages: Number of Google search pages to process
        
    Returns:
        List of unique email addresses found
    """
    emails = set()
    ua = UserAgent()  # Initialize the UserAgent for randomization - MottaSec Fox's disguise

    try:
        for page in range(pages):
            start = page * 10  # Each Google page has 10 results
            
            # MottaSec Fox's favorite search queries
            queries = [
                f"site:{domain} email OR contact OR mailto",
                f"site:{domain} email",
                f"site:{domain} contact us"
            ]
            
            # Use a different query for each page for better results
            query = queries[page % len(queries)]
            url = f"https://www.google.com/search?q={query}&start={start}"

            # Randomize User-Agent - MottaSec Ninja stealth technique
            headers = {
                "User-Agent": ua.random
            }

            if debug >= 1:
                print(f"{BLUE}🔍 MottaSec Fox is searching: {url}{RESET}")
                print(f"{BLUE}🥸 Using disguise: {headers['User-Agent']}{RESET}")

            # Add a random delay between 2 and 5 seconds - MottaSec Ghost's patience
            delay = random.uniform(2, 5)
            if debug >= 2:
                print(f"{BLUE}⏱️ MottaSec Fox is waiting for {delay:.2f} seconds before pouncing...{RESET}")
            time.sleep(delay)

            # Make the request - MottaSec Fox's hunt begins
            response = requests.get(url, headers=headers)
            if debug >= 1:
                print(f"{BLUE}📡 Google hunt response: {response.status_code}{RESET}")

            # Check for successful response
            if response.status_code != 200:
                print(f"{RED}⚠️ MottaSec Fox was blocked: HTTP {response.status_code}{RESET}")
                continue

            # Parse the HTML using BeautifulSoup - MottaSec Aces' analysis
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract text and filter valid emails using regex - MottaSec Ghost's specialty
            email_regex = r"[a-zA-Z0-9._%+-]+@" + re.escape(domain)  # Match only emails ending with the domain
            for text in soup.stripped_strings:
                matches = re.findall(email_regex, text)
                if matches and debug >= 2:
                    print(f"{GREEN}🎯 MottaSec Fox found: {matches}{RESET}")
                emails.update(matches)

        if debug >= 1:
            print(f"{BLUE}📊 MottaSec Fox's hunt summary: Found {len(emails)} unique email(s) on Google{RESET}")
        return list(emails)

    except Exception as e:
        print(f"{RED}🚨 MottaSec Fox encountered an error during Google hunting: {e}{RESET}")
        return []

# Alias for backward compatibility
scrape_google = motta_google_hunt