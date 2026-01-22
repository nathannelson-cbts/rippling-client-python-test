#!/usr/bin/env python3
"""
Basic Usage Examples for Rippling API Client

This script demonstrates the fundamental patterns for using the Rippling API client.
Before running, ensure you have a .env file with RIPPLING_BEARER_TOKEN set.
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from rippling_client import RipplingAPIError, RipplingSettings, SyncRipplingClient


def get_settings() -> RipplingSettings:
    """Load settings from environment variables."""
    bearer_token = os.getenv("RIPPLING_BEARER_TOKEN")
    if not bearer_token:
        print("ERROR: RIPPLING_BEARER_TOKEN environment variable is required")
        print("Set it in your .env file or export it in your shell")
        sys.exit(1)

    # Optional: Override base URL for sandbox/testing
    base_url = os.getenv("RIPPLING_BASE_URL", "https://rest.ripplingapis.com")

    return RipplingSettings(
        bearer_token=bearer_token,  # type: ignore[arg-type]
        base_url=base_url,
    )


def main():
    # =========================================================================
    # Initialize client with explicit settings
    # =========================================================================
    print("=" * 60)
    print("Initializing Rippling Client")
    print("=" * 60)

    settings = get_settings()
    print(f"Using API base URL: {settings.base_url}")

    # Create the client with settings
    with SyncRipplingClient(settings=settings) as client:
        # =====================================================================
        # Example 1: List Companies
        # =====================================================================
        print("\n--- Example 1: List Companies ---")
        try:
            companies = list(client.companies.list())
            print(f"Found {len(companies)} company/companies")
            for company in companies:
                print(f"  - {company.name} (ID: {company.id})")
        except RipplingAPIError as e:
            print(f"Error fetching companies: {e}")

        # =====================================================================
        # Example 2: List Employees/Workers
        # =====================================================================
        print("\n--- Example 2: List Workers (limited to 25 for demo) ---")
        try:
            # Use max_results to limit pagination - fetches ~2-3 pages
            workers = list(client.workers.list(page_size=10, max_results=25))
            print(f"Fetched {len(workers)} workers")
            for worker in workers[:5]:  # Show first 5
                print(f"  - {worker.id}")
        except RipplingAPIError as e:
            print(f"Error fetching workers: {e}")

        # =====================================================================
        # Example 3: List Users
        # =====================================================================
        print("\n--- Example 3: List Users (limited to 25 for demo) ---")
        try:
            # Use max_results to limit pagination
            users = list(client.users.list(page_size=10, max_results=25))
            print(f"Fetched {len(users)} users")
            for user in users[:5]:  # Show first 5
                display_name = getattr(user, "display_name", None) or getattr(
                    user, "email", user.id
                )
                print(f"  - {display_name}")
        except RipplingAPIError as e:
            print(f"Error fetching users: {e}")

        # =====================================================================
        # Example 4: List Departments
        # =====================================================================
        print("\n--- Example 4: List Departments ---")
        try:
            departments = list(client.departments.list())
            print(f"Found {len(departments)} departments")
            for dept in departments[:10]:  # Show first 10
                print(f"  - {dept.name} (ID: {dept.id})")
        except RipplingAPIError as e:
            print(f"Error fetching departments: {e}")

        # =====================================================================
        # Example 5: List Work Locations
        # =====================================================================
        print("\n--- Example 5: List Work Locations ---")
        try:
            locations = list(client.work_locations.list())
            print(f"Found {len(locations)} work locations")
            for loc in locations[:10]:  # Show first 10
                print(f"  - {loc.name} (ID: {loc.id})")
        except RipplingAPIError as e:
            print(f"Error fetching work locations: {e}")

    print("\n" + "=" * 60)
    print("Basic examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
