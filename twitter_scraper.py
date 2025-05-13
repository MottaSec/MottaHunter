#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MottaHunter Twitter Scraper Module
Developed by MottaSec Ghost for the MottaHunter toolkit

This module handles Twitter API interactions to find email addresses.
As MottaSec Ghost says: "People reveal more than they think in their tweets."

Author: MottaSec Ghost
Website: https://mottasec.com
Contact: ghost@mottasec.com
"""

import os
import re
import time
import tweepy
from dotenv import load_dotenv

# ANSI color codes for terminal - MottaSec style!
GREEN = "\033[92m"  # Success - MottaSec Fox approved
RED = "\033[91m"    # Failure - MottaSec Ghost says no
BLUE = "\033[94m"   # Info - MottaSec Aces intel
RESET = "\033[0m"   # Reset to default color

def motta_setup_twitter_api():
    """
    Setup Twitter API using credentials from environment variables.
    
    MottaSec Aces always keep their API keys secure in environment variables!
    
    Returns:
        Authenticated Tweepy API instance
    
    Raises:
        ValueError: If Twitter API credentials are missing
    """
    load_dotenv()
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise ValueError("🚨 MottaSec Alert: Twitter API credentials not found in environment variables")
    
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)

def motta_twitter_hunt(domain, debug=0):
    """
    Hunt through Twitter for potential email addresses associated with the domain.
    
    MottaSec Ghost's specialty is finding information people didn't know they shared.
    This function uses Twitter's API to search for mentions of the domain and
    extracts email addresses from the tweets.
    
    Args:
        domain (str): The domain to search for
        debug (int): Debug level (0=minimal, 1=moderate, 2=verbose)
    
    Returns:
        list: List of unique email addresses found
    """
    emails = set()
    
    try:
        # MottaSec Ghost prepares for the hunt
        api = motta_setup_twitter_api()
        if debug >= 1:
            print(f"{BLUE}👻 MottaSec Ghost has successfully infiltrated Twitter API{RESET}")
        
        # Craft search queries - MottaSec Ghost's secret sauce
        queries = [
            f"email {domain}",
            f"contact {domain}",
            f"reach {domain}",
            f"{domain} email",
            f"{domain} contact"
        ]
        
        # MottaSec Ghost hunts through each query
        for query in queries:
            if debug >= 1:
                print(f"{BLUE}🔍 MottaSec Ghost is searching Twitter for: {query}{RESET}")
                
            # Use cursor to handle pagination - MottaSec Ghost can search far and wide
            tweet_count = 0
            for tweet in tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode="extended").items(50):
                tweet_count += 1
                if debug >= 2:
                    print(f"{BLUE}📝 Processing tweet {tweet_count}: {tweet.full_text[:50]}...{RESET}")
                    
                # Extract emails from tweet text - MottaSec Ghost's pattern recognition
                email_regex = r"[a-zA-Z0-9._%+-]+@" + re.escape(domain)
                found_emails = re.findall(email_regex, tweet.full_text)
                
                if found_emails and debug >= 1:
                    print(f"{GREEN}🎯 MottaSec Ghost found emails in tweet: {found_emails}{RESET}")
                    
                emails.update(found_emails)
                
                # Rate limiting - MottaSec Ghost moves cautiously
                time.sleep(2)  # Be nice to Twitter's API
            
            # MottaSec Ghost needs to rest between queries
            if debug >= 1:
                print(f"{BLUE}⏱️ MottaSec Ghost is resting for 5 seconds between queries...{RESET}")
            time.sleep(5)
        
        # MottaSec Ghost reports findings
        if debug >= 1:
            print(f"{BLUE}📊 MottaSec Ghost's hunt summary: Found {len(emails)} unique email(s) on Twitter{RESET}")
            
        return list(emails)
        
    except Exception as e:
        if debug >= 1:
            print(f"{RED}🚨 MottaSec Ghost encountered an error during Twitter hunting: {e}{RESET}")
        return []

# Aliases for backward compatibility
setup_twitter_api = motta_setup_twitter_api
scrape_twitter = motta_twitter_hunt