#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MottaHunter LinkedIn Scraper Module
Developed by MottaSec Aces for the MottaHunter toolkit

This module handles LinkedIn scraping to find email addresses.
As MottaSec Aces say: "The professional network holds professional secrets."

Author: MottaSec Aces
Website: https://mottasec.com
Contact: ghost@mottasec.com
"""

import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

# ANSI color codes for terminal - MottaSec style!
GREEN = "\033[92m"  # Success - MottaSec Fox approved
RED = "\033[91m"    # Failure - MottaSec Ghost says no
BLUE = "\033[94m"   # Info - MottaSec Aces intel
RESET = "\033[0m"   # Reset to default color

def motta_setup_driver():
    """
    Setup Chrome WebDriver with appropriate options.
    
    MottaSec Aces know that proper browser configuration is essential
    for successful reconnaissance operations.
    
    Returns:
        Configured Chrome WebDriver instance
    """
    print(f"{BLUE}🛠️ MottaSec Aces are preparing the reconnaissance vehicle...{RESET}")
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    # MottaSec Aces use a custom user agent to blend in
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(f"{GREEN}✅ MottaSec Aces' reconnaissance vehicle is ready!{RESET}")
        return driver
    except Exception as e:
        print(f"{RED}🚨 MottaSec Aces encountered an error setting up the driver: {e}{RESET}")
        raise

def motta_linkedin_login(driver, debug=0):
    """
    Login to LinkedIn using credentials from environment variables.
    
    MottaSec Aces always authenticate properly before beginning operations.
    
    Args:
        driver: Chrome WebDriver instance
        debug: Debug level (0=minimal, 1=moderate, 2=verbose)
        
    Raises:
        ValueError: If LinkedIn credentials are missing
        Exception: If login fails
    """
    load_dotenv()
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    
    if not email or not password:
        raise ValueError(f"{RED}🚨 MottaSec Alert: LinkedIn credentials not found in environment variables{RESET}")
    
    try:
        if debug >= 1:
            print(f"{BLUE}🔑 MottaSec Aces are authenticating with LinkedIn...{RESET}")
            
        driver.get('https://www.linkedin.com/login')
        
        # Wait for and fill in email - MottaSec Aces are patient
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_field.send_keys(email)
        
        # Fill in password and submit - MottaSec Aces are thorough
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        
        # Wait for login to complete - MottaSec Aces verify success
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".feed-identity-module"))
        )
        
        if debug >= 1:
            print(f"{GREEN}✅ MottaSec Aces have successfully infiltrated LinkedIn{RESET}")
            
    except Exception as e:
        if debug >= 1:
            print(f"{RED}🚨 MottaSec Aces failed to login to LinkedIn: {e}{RESET}")
        raise

def motta_linkedin_hunt(domain, debug=0):
    """
    Hunt through LinkedIn for potential email addresses associated with the domain.
    
    MottaSec Aces excel at finding professional contact information through
    company pages, employee profiles, and about sections.
    
    Args:
        domain: The domain to search for
        debug: Debug level (0=minimal, 1=moderate, 2=verbose)
    
    Returns:
        list: List of unique email addresses found
    """
    emails = set()
    driver = None
    
    try:
        # MottaSec Aces prepare for the hunt
        driver = motta_setup_driver()
        if debug >= 1:
            print(f"{BLUE}🚀 MottaSec Aces' reconnaissance mission has begun{RESET}")
        
        # Login to LinkedIn - MottaSec Aces always authenticate
        try:
            motta_linkedin_login(driver, debug)
        except Exception as e:
            print(f"{RED}🚨 Authentication failed, continuing with limited reconnaissance: {e}{RESET}")
            # Continue without login, but with limited capabilities
        
        # Extract company name from domain - MottaSec Aces' intelligence gathering
        company_name = domain.split('.')[0]  # Simple extraction
        
        # Try to find better company name if possible
        if '.' in domain and len(domain.split('.')) > 2:
            parts = domain.split('.')
            if len(parts) >= 3 and len(parts[-3]) > 3:  # Likely the company name
                company_name = parts[-3]
        
        if debug >= 1:
            print(f"{BLUE}🔍 MottaSec Aces are searching for company: {company_name}{RESET}")
        
        # MottaSec Aces' hunt begins - search for the company
        search_url = f"https://www.linkedin.com/search/results/companies/?keywords={company_name}"
        driver.get(search_url)
        time.sleep(3)  # Wait for results to load
        
        # Hunt through company search results
        company_urls = []
        try:
            # Find company links - MottaSec Aces cast a wide net
            company_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.app-aware-link"))
            )
            
            # Extract company URLs - MottaSec Aces are thorough
            for link in company_links[:3]:  # Check top 3 results
                url = link.get_attribute('href')
                if '/company/' in url:
                    company_urls.append(url)
                    if debug >= 2:
                        print(f"{BLUE}🏢 MottaSec Aces found company page: {url}{RESET}")
            
            if not company_urls:
                if debug >= 1:
                    print(f"{RED}⚠️ MottaSec Aces couldn't find company pages for {company_name}{RESET}")
        except TimeoutException:
            if debug >= 1:
                print(f"{RED}⚠️ MottaSec Aces: No company results found{RESET}")
        
        # Visit each company page - MottaSec Aces investigate thoroughly
        for company_url in company_urls:
            if debug >= 1:
                print(f"{BLUE}🔎 MottaSec Aces are investigating: {company_url}{RESET}")
                
            driver.get(company_url)
            time.sleep(3)
            
            # Check "About" section - MottaSec Aces know where to look
            try:
                about_button = driver.find_element(By.XPATH, "//a[contains(@href, '/about/')]")
                about_url = about_button.get_attribute('href')
                driver.get(about_url)
                time.sleep(2)
            except NoSuchElementException:
                if debug >= 2:
                    print(f"{BLUE}ℹ️ MottaSec Aces: No About section found, checking main page{RESET}")
            
            # Extract text content - MottaSec Aces gather intelligence
            page_content = driver.page_source
            
            # Find email addresses - MottaSec Aces' pattern recognition
            email_regex = r"[a-zA-Z0-9._%+-]+@" + re.escape(domain)
            found_emails = re.findall(email_regex, page_content)
            
            if found_emails:
                if debug >= 1:
                    print(f"{GREEN}🎯 MottaSec Aces found emails: {found_emails}{RESET}")
                emails.update(found_emails)
        
        # If no emails found, try people search - MottaSec Aces' backup plan
        if not emails and debug >= 1:
            print(f"{BLUE}🔄 MottaSec Aces are trying alternative approach: people search{RESET}")
            
            people_url = f"https://www.linkedin.com/search/results/people/?keywords={company_name}"
            driver.get(people_url)
            time.sleep(3)
            
            # Extract text content from people search
            page_content = driver.page_source
            
            # Find email addresses
            email_regex = r"[a-zA-Z0-9._%+-]+@" + re.escape(domain)
            found_emails = re.findall(email_regex, page_content)
            
            if found_emails:
                if debug >= 1:
                    print(f"{GREEN}🎯 MottaSec Aces found emails from people search: {found_emails}{RESET}")
                emails.update(found_emails)
        
        # MottaSec Aces report findings
        if debug >= 1:
            print(f"{BLUE}📊 MottaSec Aces' hunt summary: Found {len(emails)} unique email(s) on LinkedIn{RESET}")
            
        return list(emails)
        
    except Exception as e:
        if debug >= 1:
            print(f"{RED}🚨 MottaSec Aces encountered an error during LinkedIn hunting: {e}{RESET}")
        return []
        
    finally:
        # MottaSec Aces always clean up after operations
        if driver:
            if debug >= 1:
                print(f"{BLUE}🧹 MottaSec Aces are covering their tracks...{RESET}")
            driver.quit()

# Aliases for backward compatibility
setup_driver = motta_setup_driver
login_to_linkedin = motta_linkedin_login
scrape_linkedin = motta_linkedin_hunt