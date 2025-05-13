#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MottaHunter Email Validation Module
Developed by MottaSec Ghost for the MottaHunter toolkit

This module handles email permutation generation and SMTP-based validation.
As MottaSec Fox says: "Trust, but verify!"

Author: MottaSec Ghost
Website: https://mottasec.com
Contact: ghost@mottasec.com
"""

import random
import time
from dns.resolver import resolve
import smtplib
from typing import List, Tuple

# ANSI color codes for terminal - MottaSec style!
GREEN = "\033[92m"  # Success - MottaSec Fox approved
RED = "\033[91m"    # Failure - MottaSec Ghost says no
BLUE = "\033[94m"   # Info - MottaSec Aces intel
RESET = "\033[0m"   # Reset to default color

def motta_generate_permutations(first_name: str, last_name: str, domain: str, level: int) -> List[str]:
    """
    Generate email permutations based on the selected level.
    Returns a list of complete email addresses (user@domain).
    
    MottaSec Fox has carefully crafted these permutation patterns
    based on extensive research of common email formats.
    
    Args:
        first_name: First name to use in permutations
        last_name: Last name to use in permutations
        domain: Domain to append to usernames
        level: Permutation level (1=light, 2=medium, 3=heavy)
        
    Returns:
        List of email address permutations
    """
    # Ensure domain is lowercase for consistency
    domain = domain.lower()
    
    # Basic permutations (level 1) - MottaSec Ghost's essentials
    permutations = [
        f"{first_name.lower()}{last_name.lower()}@{domain}",
        f"{first_name.lower()}.{last_name.lower()}@{domain}",
        f"{first_name[0].lower()}{last_name.lower()}@{domain}",
        f"{first_name[0].lower()}.{last_name.lower()}@{domain}",
        f"{first_name[0].lower()}_{last_name.lower()}@{domain}",
        f"{first_name.lower()}-{last_name.lower()}@{domain}",
    ]
    
    # Add medium level permutations - MottaSec Fox's favorites
    if level >= 2:
        permutations.extend([
            f"{first_name.lower()}@{domain}",
            f"{last_name.lower()}@{domain}",
            f"{first_name.lower()}_{last_name.lower()}@{domain}",
            f"{last_name.lower()}.{first_name.lower()}@{domain}",
            f"{last_name.lower()}_{first_name.lower()}@{domain}",
            f"{last_name.lower()}{first_name.lower()}@{domain}",
        ])
    
    # Add heavy level permutations - MottaSec Aces' advanced patterns
    if level >= 3:
        permutations.extend([
            f"{first_name[0].lower()}{last_name[:3].lower()}@{domain}",
            f"{first_name[0].lower()}.{last_name[:3].lower()}@{domain}",
            f"{first_name[:3].lower()}{last_name[0].lower()}@{domain}",
            f"{last_name[:3].lower()}{first_name[0].lower()}@{domain}",
            f"{first_name.lower()}{last_name[0].lower()}@{domain}",
            f"{last_name.lower()}{first_name[0].lower()}@{domain}",
        ])
    
    return list(dict.fromkeys(permutations))  # Remove duplicates while preserving order

def motta_validate_email_smtp(email: str, sender_email: str, mx_server: str, debug: int) -> bool:
    """
    Validate an email address via SMTP.
    
    MottaSec Jedis know that SMTP validation is the most reliable way
    to check if an email address exists without actually sending mail.
    
    Args:
        email: Email address to validate
        sender_email: Email to use as MAIL FROM
        mx_server: MX server to connect to
        debug: Debug level (0=minimal, 1=moderate, 2=verbose)
        
    Returns:
        True if email exists, False otherwise
    """
    try:
        if debug >= 1:
            print(f"{BLUE}🔌 Connecting to MX server: {mx_server}...{RESET}")
        
        with smtplib.SMTP(mx_server, 25, timeout=10) as smtp:
            if debug == 2:
                smtp.set_debuglevel(1)

            smtp.helo("mottasec.com")  # MottaSec Fox's calling card
            smtp.mail(sender_email)
            response = smtp.rcpt(email)

            if debug >= 1:
                print(f"{BLUE}📨 RCPT TO response for {email}: {response}{RESET}")

            return response[0] == 250
    except Exception as e:
        if debug >= 1:
            print(f"{RED}⚠️ SMTP Error for {email}: {e}{RESET}")
        return False

def motta_validate_info_address(domain: str, sender_email: str, mx_server: str, debug: int, 
                         no_check: bool = False, check_email: str = None) -> Tuple[bool, bool]:
    """
    Validate the existence of info@domain and check catch-all.
    
    MottaSec Ghost's trick: Always check a standard email and a random one
    to determine if the domain has catch-all enabled.
    
    Args:
        domain: Target domain
        sender_email: Email to use as MAIL FROM
        mx_server: MX server to connect to
        debug: Debug level (0=minimal, 1=moderate, 2=verbose)
        no_check: If True, skip checking default email
        check_email: Custom email to check instead of info@domain
        
    Returns:
        Tuple of (is_valid, is_catch_all)
    """
    try:
        # Skip check if requested - MottaSec Fox respects user preferences
        if no_check:
            if debug >= 1:
                print(f"\n{BLUE}🦊 MottaSec Fox: Skipping default email check as requested{RESET}")
            return True, False

        # Use custom email if provided, otherwise use info@domain
        test_email = check_email if check_email else f"info@{domain}"
        result = motta_validate_email_smtp(test_email, sender_email, mx_server, debug)

        print("\n")  # Empty line before
        if result:
            print(f"{GREEN}✅ MottaSec Fox confirms: {test_email} is valid.{RESET}")
        else:
            print(f"{RED}❌ MottaSec Ghost reports: {test_email} is invalid.{RESET}")
        print("\n")  # Empty line after

        # Check for catch-all - MottaSec Aces' special technique
        random_string = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
        test_email = f"mottasec-{random_string}@{domain}"
        is_catch_all = motta_validate_email_smtp(test_email, sender_email, mx_server, debug)
        if is_catch_all:
            print(f"{RED}⚠️ MottaSec Fox Alert: Domain {domain} is a catch-all domain!{RESET}")
        return result, is_catch_all

    except Exception as e:
        print(f"{RED}🚨 MottaSec Error validating {test_email}: {e}{RESET}")
        return False, False

def motta_validate_email_permutations(permutations: List[str], domain: str, sender_email: str, 
                              delay: List[int], debug: int, no_check: bool = False, 
                              check_email: str = None) -> None:
    """
    Validate a list of email permutations via SMTP.
    
    MottaSec Jedis always validate their findings thoroughly!
    
    Args:
        permutations: List of complete email addresses to validate
        domain: Domain for MX lookup
        sender_email: Email to use as MAIL FROM
        delay: List of [min, max] delay in seconds
        debug: Debug level (0=minimal, 1=moderate, 2=verbose)
        no_check: If True, skip checking default email
        check_email: Custom email to check instead of info@domain
    """
    try:
        mx_records = resolve(domain, 'MX')
        if not mx_records:
            print(f"{RED}🚨 MottaSec Fox Alert: No MX records found for {domain}{RESET}")
            return
            
        mx_server = mx_records[0].exchange.to_text()
        if debug >= 1:
            print(f"{BLUE}🔍 MottaSec Fox found MX server: {mx_server}{RESET}")

        # Validate info@domain and check catch-all
        info_valid, is_catch_all = motta_validate_info_address(
            domain, sender_email, mx_server, debug, no_check, check_email
        )
        if not info_valid or is_catch_all:
            return

        # Validate each permutation - MottaSec Fox's hunting ground
        valid_count = 0
        for email in permutations:
            is_valid = motta_validate_email_smtp(email, sender_email, mx_server, debug)

            # Add empty lines for readability
            print("\n")
            if is_valid:
                valid_count += 1
                print(f"{GREEN}✅ MottaSec Fox found: {email} is valid.{RESET}")
            else:
                print(f"{RED}❌ MottaSec Ghost reports: {email} is invalid.{RESET}")
            print("\n")

            # Add delay with timestamp - MottaSec Ninja stealth technique
            delay_duration = random.uniform(*delay)
            print(f"{BLUE}⏱️ MottaSec Fox is waiting for {delay_duration:.2f} seconds at {time.strftime('%Y-%m-%d %H:%M:%S')}...{RESET}")
            time.sleep(delay_duration)
            
        # Summary - MottaSec Aces like good reports
        print(f"\n{BLUE}📊 MottaSec Summary: Found {valid_count} valid email(s) out of {len(permutations)} tested.{RESET}")

    except Exception as e:
        print(f"{RED}🚨 MottaSec Error: Failed to retrieve MX server for {domain}: {e}{RESET}")

def motta_validate_scraped_emails(emails: List[str], domain: str, sender_email: str, 
                          delay: List[int], debug: int, no_check: bool = False, 
                          check_email: str = None) -> None:
    """
    Validate a list of scraped emails via SMTP.
    
    MottaSec Ghost always verifies what it finds!
    
    Args:
        emails: List of email addresses to validate
        domain: Domain for MX lookup
        sender_email: Email to use as MAIL FROM
        delay: List of [min, max] delay in seconds
        debug: Debug level (0=minimal, 1=moderate, 2=verbose)
        no_check: If True, skip checking default email
        check_email: Custom email to check instead of info@domain
    """
    try:
        mx_records = resolve(domain, 'MX')
        if not mx_records:
            print(f"{RED}🚨 MottaSec Fox Alert: No MX records found for {domain}{RESET}")
            return
            
        mx_server = mx_records[0].exchange.to_text()
        if debug >= 1:
            print(f"{BLUE}🔍 MottaSec Fox found MX server: {mx_server}{RESET}")

        # Validate info@domain and check catch-all
        info_valid, is_catch_all = motta_validate_info_address(
            domain, sender_email, mx_server, debug, no_check, check_email
        )
        if not info_valid or is_catch_all:
            return

        # Validate each email - MottaSec Ghost's verification process
        valid_count = 0
        for email in emails:
            is_valid = motta_validate_email_smtp(email, sender_email, mx_server, debug)

            # Add empty lines for readability
            print("\n")
            if is_valid:
                valid_count += 1
                print(f"{GREEN}✅ MottaSec Ghost confirms: {email} is valid.{RESET}")
            else:
                print(f"{RED}❌ MottaSec Ghost reports: {email} is invalid.{RESET}")
            print("\n")

            # Add delay with timestamp - MottaSec Ninja stealth technique
            delay_duration = random.uniform(*delay)
            print(f"{BLUE}⏱️ MottaSec Ghost is waiting for {delay_duration:.2f} seconds at {time.strftime('%Y-%m-%d %H:%M:%S')}...{RESET}")
            time.sleep(delay_duration)
            
        # Summary - MottaSec Aces like good reports
        print(f"\n{BLUE}📊 MottaSec Summary: Found {valid_count} valid email(s) out of {len(emails)} tested.{RESET}")

    except Exception as e:
        print(f"{RED}🚨 MottaSec Error: Failed to retrieve MX server for {domain}: {e}{RESET}")

# Aliases for backward compatibility
generate_permutations = motta_generate_permutations
validate_email_smtp = motta_validate_email_smtp
validate_info_address = motta_validate_info_address
validate_email_permutations = motta_validate_email_permutations
validate_scraped_emails = motta_validate_scraped_emails