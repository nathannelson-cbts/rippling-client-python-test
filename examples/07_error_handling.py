#!/usr/bin/env python3
"""
Error Handling Examples for Rippling API Client

This script demonstrates proper error handling patterns
for production-grade code.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

from rippling_client import (
    SyncRipplingClient,
    RipplingSettings,
    RipplingError,           # Base exception
    RipplingAPIError,        # General API errors
    RipplingAuthError,       # Authentication failures
    RipplingRateLimitError,  # Rate limiting
    RipplingTimeoutError,    # Timeouts
    RipplingServerError,     # 5xx errors
)


def get_settings() -> RipplingSettings:
    """Load settings from environment variables."""
    bearer_token = os.getenv('RIPPLING_BEARER_TOKEN')
    if not bearer_token:
        print("ERROR: RIPPLING_BEARER_TOKEN environment variable is required")
        sys.exit(1)
    
    return RipplingSettings(
        bearer_token=bearer_token,
        base_url=os.getenv('RIPPLING_BASE_URL', 'https://rest.ripplingapis.com'),
    )


def main():
    settings = get_settings()
    
    with SyncRipplingClient(settings=settings) as client:
        # =====================================================================
        # Example 1: Basic Error Handling
        # =====================================================================
        print("\n--- Example 1: Basic Error Handling (limited to 25) ---")
        
        try:
            workers = list(client.workers.list(max_results=25))
            print(f"Successfully fetched {len(workers)} workers")
        except RipplingAPIError as e:
            print(f"API Error: {e}")
            # You might log this or retry
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}")

        # =====================================================================
        # Example 2: Comprehensive Error Handling
        # =====================================================================
        print("\n--- Example 2: Comprehensive Error Handling (limited to 25) ---")
        
        try:
            departments = list(client.departments.list(max_results=25))
            print(f"Successfully fetched {len(departments)} departments")
            
        except RipplingAuthError as e:
            # Handle authentication issues
            print(f"Authentication failed: {e}")
            print("Action: Check your RIPPLING_BEARER_TOKEN")
            
        except RipplingRateLimitError as e:
            # Handle rate limiting
            print(f"Rate limited: {e}")
            print("Action: Implement exponential backoff or reduce request frequency")
            
        except RipplingTimeoutError as e:
            # Handle timeouts
            print(f"Request timed out: {e}")
            print("Action: Retry or increase timeout settings")
            
        except RipplingServerError as e:
            # Handle server-side errors (5xx)
            print(f"Server error: {e}")
            print("Action: Retry with backoff, Rippling may be experiencing issues")
            
        except RipplingAPIError as e:
            # Handle other API errors (4xx, etc.)
            print(f"API error: {e}")
            
        except RipplingError as e:
            # Catch-all for any Rippling-related errors
            print(f"Rippling error: {e}")
            
        except Exception as e:
            # Handle unexpected errors
            print(f"Unexpected error: {type(e).__name__}: {e}")

        # =====================================================================
        # Example 3: Retry Pattern
        # =====================================================================
        print("\n--- Example 3: Manual Retry Pattern (limited to 25) ---")
        
        import time
        
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                teams = list(client.teams.list(max_results=25))
                print(f"Attempt {attempt + 1}: Successfully fetched {len(teams)} teams")
                break  # Success, exit retry loop
                
            except RipplingRateLimitError:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                    print(f"Rate limited, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print("Max retries exceeded for rate limiting")
                    
            except RipplingServerError:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    print(f"Server error, waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    print("Max retries exceeded for server errors")
                    
            except RipplingAPIError as e:
                # Don't retry client errors (4xx)
                print(f"Client error (not retrying): {e}")
                break

        # =====================================================================
        # Example 4: Graceful Degradation
        # =====================================================================
        print("\n--- Example 4: Graceful Degradation (limited to 25 each) ---")
        
        def get_data_with_fallback():
            """Fetch data with fallback to cached/default values."""
            data = {
                'departments': [],
                'teams': [],
                'workers': [],
                'source': 'api'
            }
            
            try:
                data['departments'] = list(client.departments.list(max_results=25))
            except RipplingAPIError:
                data['departments'] = []  # Could load from cache
                data['source'] = 'partial'
                print("Warning: Using fallback for departments")
            
            try:
                data['teams'] = list(client.teams.list(max_results=25))
            except RipplingAPIError:
                data['teams'] = []
                data['source'] = 'partial'
                print("Warning: Using fallback for teams")
            
            try:
                data['workers'] = list(client.workers.list(max_results=25))
            except RipplingAPIError:
                data['workers'] = []
                data['source'] = 'partial'
                print("Warning: Using fallback for workers")
            
            return data
        
        result = get_data_with_fallback()
        print(f"Data source: {result['source']}")
        print(f"Departments: {len(result['departments'])}, Teams: {len(result['teams'])}, Workers: {len(result['workers'])}")

    print("\n" + "=" * 60)
    print("Error handling examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
