#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MottaHunter Test Suite
Developed by the MottaSec Jedis for quality assurance

As MottaSec Fox says: "Test thoroughly, hunt confidently!"

Author: MottaSec Team
Website: https://mottasec.com
Contact: ghost@mottasec.com
"""

import unittest
from unittest.mock import patch, MagicMock
from email_validation import motta_generate_permutations
from harvester import MottaHunter

# ANSI color codes for terminal - MottaSec style!
GREEN = "\033[92m"  # Success - MottaSec Fox approved
RED = "\033[91m"    # Failure - MottaSec Ghost says no
BLUE = "\033[94m"   # Info - MottaSec Aces intel
RESET = "\033[0m"   # Reset to default color

class TestMottaPermutations(unittest.TestCase):
    """Test the email permutation generator - MottaSec style!"""
    
    def test_basic_permutations(self):
        """Test basic (level 1) permutations"""
        print(f"{BLUE}🦊 MottaSec Fox is testing basic permutations...{RESET}")
        perms = motta_generate_permutations("John", "Doe", "example.com", 1)
        expected = [
            "johndoe@example.com",
            "john.doe@example.com",
            "jdoe@example.com",
            "j.doe@example.com",
            "j_doe@example.com",
            "john-doe@example.com",
        ]
        self.assertEqual(set(perms), set(expected))
        print(f"{GREEN}✅ MottaSec Fox approves: Basic permutations test passed!{RESET}")
        
    def test_medium_permutations(self):
        """Test medium (level 2) permutations"""
        print(f"{BLUE}🦊 MottaSec Fox is testing medium permutations...{RESET}")
        perms = motta_generate_permutations("John", "Doe", "example.com", 2)
        # Level 2 should include all level 1 permutations plus more
        self.assertIn("john@example.com", perms)
        self.assertIn("doe@example.com", perms)
        self.assertTrue(len(perms) > 6)  # More than basic permutations
        print(f"{GREEN}✅ MottaSec Fox approves: Medium permutations test passed!{RESET}")
        
    def test_heavy_permutations(self):
        """Test heavy (level 3) permutations - for the MottaSec Ninjas!"""
        print(f"{BLUE}🦊 MottaSec Fox is testing advanced permutations...{RESET}")
        perms = motta_generate_permutations("John", "Doe", "example.com", 3)
        # Level 3 should include all level 2 permutations plus more
        self.assertIn("jdoe@example.com", perms)
        self.assertTrue(len(perms) > 12)  # More than medium permutations
        print(f"{GREEN}✅ MottaSec Fox approves: Advanced permutations test passed!{RESET}")
        
    def test_lowercase_conversion(self):
        """Test that all emails are converted to lowercase - MottaSec standard!"""
        print(f"{BLUE}🦊 MottaSec Fox is testing case normalization...{RESET}")
        perms = motta_generate_permutations("John", "DOE", "Example.COM", 1)
        for email in perms:
            self.assertEqual(email, email.lower())
        print(f"{GREEN}✅ MottaSec Fox approves: Case normalization test passed!{RESET}")


class TestMottaHunter(unittest.TestCase):
    """Test the main MottaHunter class - MottaSec command center!"""
    
    def test_motta_split(self):
        """Test splitting permutations into parts - MottaSec Fox's divide and conquer strategy"""
        print(f"{BLUE}🦊 MottaSec Fox is testing permutation splitting...{RESET}")
        # Create mock args
        args = MagicMock()
        hunter = MottaHunter(args)
        
        # Test with 10 items, 4 parts
        perms = ["email1@test.com", "email2@test.com", "email3@test.com", 
                "email4@test.com", "email5@test.com", "email6@test.com",
                "email7@test.com", "email8@test.com", "email9@test.com", 
                "email10@test.com"]
        
        # Part 1 should have 3 items (items 0, 1, 2)
        part1 = hunter._motta_split(perms, 4, 1)
        self.assertEqual(len(part1), 3)
        self.assertEqual(part1[0], "email1@test.com")
        
        # Part 2 should have 3 items (items 3, 4, 5)
        part2 = hunter._motta_split(perms, 4, 2)
        self.assertEqual(len(part2), 3)
        self.assertEqual(part2[0], "email4@test.com")
        
        # Part 3 should have 2 items (items 6, 7)
        part3 = hunter._motta_split(perms, 4, 3)
        self.assertEqual(len(part3), 2)
        self.assertEqual(part3[0], "email7@test.com")
        
        # Part 4 should have 2 items (items 8, 9)
        part4 = hunter._motta_split(perms, 4, 4)
        self.assertEqual(len(part4), 2)
        self.assertEqual(part4[0], "email9@test.com")
        print(f"{GREEN}✅ MottaSec Fox approves: Permutation splitting test passed!{RESET}")
        
    def test_motta_split_invalid_part(self):
        """Test error handling for invalid part number - MottaSec quality control"""
        print(f"{BLUE}🦊 MottaSec Fox is testing error handling...{RESET}")
        # Create mock args
        args = MagicMock()
        hunter = MottaHunter(args)
        
        perms = ["email1@test.com", "email2@test.com"]
        
        with self.assertRaises(ValueError):
            hunter._motta_split(perms, 3, 4)  # Part 4 of 3 is invalid
        print(f"{GREEN}✅ MottaSec Fox approves: Error handling test passed!{RESET}")


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════╗
    ║  🦊 MottaHunter - Test Suite                  ║
    ║      Quality Assurance by MottaSec Jedis      ║
    ╚═══════════════════════════════════════════════╝
    """)
    unittest.main() 