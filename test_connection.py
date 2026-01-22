#!/usr/bin/env python3
"""
Quick Connection Test for Rippling API Client

Run this first to verify your API token and connection work.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    print("=" * 60)
    print("Rippling API Client - Connection Test")
    print("=" * 60)
    
    # Check for token
    bearer_token = os.getenv('RIPPLING_BEARER_TOKEN')
    if not bearer_token:
        print("\n❌ ERROR: RIPPLING_BEARER_TOKEN not found in environment")
        print("\nTo fix this:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your API token to the .env file")
        print("  3. Run this script again")
        sys.exit(1)
    
    print(f"\n✓ Token found (length: {len(bearer_token)} chars)")
    
    # Test imports
    print("\nTesting imports...")
    try:
        from rippling_client import (
            SyncRipplingClient,
            AsyncRipplingClient,
            RipplingSettings,
            RipplingAPIError,
        )
        print("✓ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)
    
    # Test client initialization
    print("\nTesting client initialization...")
    try:
        base_url = os.getenv('RIPPLING_BASE_URL', 'https://rest.ripplingapis.com')
        settings = RipplingSettings(
            bearer_token=bearer_token,
            base_url=base_url,
        )
        print(f"✓ Settings loaded")
        print(f"  Base URL: {settings.base_url}")
        print(f"  Timeout (connect): {settings.timeout_connect}s")
        print(f"  Timeout (read): {settings.timeout_read}s")
        print(f"  Max retries: {settings.max_retries}")
    except Exception as e:
        print(f"❌ Settings error: {e}")
        sys.exit(1)
    
    # Test API connection
    print("\nTesting API connection...")
    try:
        with SyncRipplingClient(settings=settings) as client:
            # Try to fetch companies (usually the simplest call)
            companies = client.companies.list()
            print(f"✓ API connection successful!")
            print(f"  Companies found: {len(companies)}")
            
            if companies:
                print(f"  First company: {companies[0].name}")
            
            # Try workers too
            workers = client.workers.list()
            print(f"  Workers found: {len(workers)}")
            
    except RipplingAPIError as e:
        print(f"❌ API Error: {e}")
        print("\nThis could mean:")
        print("  - Invalid API token")
        print("  - Insufficient permissions")
        print("  - API endpoint issues")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Connection error: {type(e).__name__}: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ All tests passed! Your Rippling client is ready to use.")
    print("=" * 60)
    print("\nNext steps:")
    print("  - Run: python examples/01_basic_usage.py")
    print("  - Or:  python examples/09_interactive_explorer.py")


if __name__ == "__main__":
    main()
