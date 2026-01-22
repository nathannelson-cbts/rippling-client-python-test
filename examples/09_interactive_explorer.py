#!/usr/bin/env python3
"""
Interactive Testing Script for Rippling API Client

Run this to interactively explore your Rippling data.
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

from rippling_client import (
    SyncRipplingClient,
    RipplingSettings,
    RipplingAPIError,
)


def get_settings() -> RipplingSettings:
    """Load settings from environment variables."""
    bearer_token = os.getenv('RIPPLING_BEARER_TOKEN')
    if not bearer_token:
        print("ERROR: RIPPLING_BEARER_TOKEN environment variable is required")
        print("Set it in your .env file or export it in your shell")
        sys.exit(1)
    
    return RipplingSettings(
        bearer_token=bearer_token,
        base_url=os.getenv('RIPPLING_BASE_URL', 'https://rest.ripplingapis.com'),
    )


def print_menu():
    """Print the interactive menu."""
    print("\n" + "=" * 60)
    print("Rippling API Explorer (limited to 25 items per query)")
    print("=" * 60)
    print("1.  List Companies")
    print("2.  List Workers")
    print("3.  List Users")
    print("4.  List Departments")
    print("5.  List Teams")
    print("6.  List Work Locations")
    print("7.  List Legal Entities")
    print("8.  List Levels")
    print("9.  List Tracks")
    print("10. List Compensations")
    print("11. List Leave Types")
    print("12. List Leave Requests")
    print("13. List Leave Balances")
    print("14. List Leave Accruals")
    print("15. List Time Cards")
    print("16. List Time Entries")
    print("17. List Candidates")
    print("18. List Candidate Applications")
    print("19. List Custom Fields")
    print("20. List Custom Objects")
    print("0.  Exit")
    print("-" * 60)


def explore_resource(name, items, max_display=10):
    """Display items from a resource."""
    print(f"\n--- {name} ({len(items)} total) ---")
    
    if not items:
        print("  No items found.")
        return
    
    # Show first few items
    for i, item in enumerate(items[:max_display]):
        # Try common display patterns
        display = getattr(item, 'name', None)
        if not display:
            display = getattr(item, 'display_name', None)
        if not display:
            display = getattr(item, 'email', None)
        if not display:
            display = item.id
        
        print(f"  {i+1}. {display} (ID: {item.id})")
    
    if len(items) > max_display:
        print(f"  ... and {len(items) - max_display} more")
    
    # Offer to show details of first item
    if items:
        print(f"\nFirst item details:")
        first = items[0]
        for field in sorted(dir(first)):
            if not field.startswith('_'):
                value = getattr(first, field, None)
                if not callable(value):
                    # Truncate long values
                    str_value = str(value)
                    if len(str_value) > 100:
                        str_value = str_value[:100] + "..."
                    print(f"    {field}: {str_value}")


def main():
    print("Initializing Rippling Client...")
    settings = get_settings()
    print(f"Using API: {settings.base_url}")
    
    with SyncRipplingClient(settings=settings) as client:
        print("Connected successfully!")
        
        while True:
            print_menu()
            
            try:
                choice = input("Enter your choice (0-20): ").strip()
                
                if choice == "0":
                    print("Goodbye!")
                    break
                
                elif choice == "1":
                    items = list(client.companies.list(page_size=10, max_results=25))
                    explore_resource("Companies", items)
                
                elif choice == "2":
                    items = list(client.workers.list(page_size=10, max_results=25))
                    explore_resource("Workers", items)
                
                elif choice == "3":
                    items = list(client.users.list(page_size=10, max_results=25))
                    explore_resource("Users", items)
                
                elif choice == "4":
                    items = list(client.departments.list(page_size=10, max_results=25))
                    explore_resource("Departments", items)
                
                elif choice == "5":
                    items = list(client.teams.list(page_size=10, max_results=25))
                    explore_resource("Teams", items)
                
                elif choice == "6":
                    items = list(client.work_locations.list(page_size=10, max_results=25))
                    explore_resource("Work Locations", items)
                
                elif choice == "7":
                    items = list(client.legal_entities.list(page_size=10, max_results=25))
                    explore_resource("Legal Entities", items)
                
                elif choice == "8":
                    items = list(client.levels.list(page_size=10, max_results=25))
                    explore_resource("Levels", items)
                
                elif choice == "9":
                    items = list(client.tracks.list(page_size=10, max_results=25))
                    explore_resource("Tracks", items)
                
                elif choice == "10":
                    items = list(client.compensations.list(page_size=10, max_results=25))
                    explore_resource("Compensations", items)
                
                elif choice == "11":
                    items = list(client.leave_types.list(page_size=10, max_results=25))
                    explore_resource("Leave Types", items)
                
                elif choice == "12":
                    items = list(client.leave_requests.list(page_size=10, max_results=25))
                    explore_resource("Leave Requests", items)
                
                elif choice == "13":
                    items = list(client.leave_balances.list(page_size=10, max_results=25))
                    explore_resource("Leave Balances", items)
                
                elif choice == "14":
                    items = list(client.leave_accruals.list(page_size=10, max_results=25))
                    explore_resource("Leave Accruals", items)
                
                elif choice == "15":
                    items = list(client.time_cards.list(page_size=10, max_results=25))
                    explore_resource("Time Cards", items)
                
                elif choice == "16":
                    items = list(client.time_entries.list(page_size=10, max_results=25))
                    explore_resource("Time Entries", items)
                
                elif choice == "17":
                    items = list(client.candidates.list(page_size=10, max_results=25))
                    explore_resource("Candidates", items)
                
                elif choice == "18":
                    items = list(client.candidate_applications.list(page_size=10, max_results=25))
                    explore_resource("Candidate Applications", items)
                
                elif choice == "19":
                    items = list(client.custom_fields.list(page_size=10, max_results=25))
                    explore_resource("Custom Fields", items)
                
                elif choice == "20":
                    items = list(client.custom_objects.list(page_size=10, max_results=25))
                    explore_resource("Custom Objects", items)
                
                else:
                    print("Invalid choice. Please enter 0-20.")
                    
            except RipplingAPIError as e:
                print(f"\nAPI Error: {e}")
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"\nError: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
