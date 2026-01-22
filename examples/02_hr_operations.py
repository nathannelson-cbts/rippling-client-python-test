#!/usr/bin/env python3
"""
HR Operations Examples for Rippling API Client

This script demonstrates HR-related API operations:
- Managing employees/workers
- Departments and teams
- Compensation data
- Leave management
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

from rippling_client import SyncRipplingClient, RipplingSettings, RipplingAPIError


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
        # Example 1: Get Full Employee Directory
        # =====================================================================
        print("\n--- Example 1: Employee Directory (limited to 25) ---")
        try:
            workers = list(client.workers.list(max_results=25))
            print(f"Fetched {len(workers)} workers (limited for demo)")
            
            # Show sample worker data
            if workers:
                worker = workers[0]
                print(f"\nSample worker fields available:")
                for field in dir(worker):
                    if not field.startswith('_'):
                        value = getattr(worker, field, None)
                        if not callable(value):
                            print(f"  {field}: {value}")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 2: Department Structure
        # =====================================================================
        print("\n--- Example 2: Department Structure (limited to 25) ---")
        try:
            departments = list(client.departments.list(max_results=25))
            print(f"Fetched {len(departments)} departments")
            
            for dept in departments[:10]:  # Show first 10
                parent_info = f" (Parent: {dept.parent_id})" if hasattr(dept, 'parent_id') and dept.parent_id else ""
                print(f"  - {dept.name}{parent_info}")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 3: Teams
        # =====================================================================
        print("\n--- Example 3: Teams (limited to 25) ---")
        try:
            teams = list(client.teams.list(max_results=25))
            print(f"Fetched {len(teams)} teams")
            
            for team in teams[:10]:  # First 10
                print(f"  - {team.name} (ID: {team.id})")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 4: Levels (Career Tracks)
        # =====================================================================
        print("\n--- Example 4: Levels ---")
        try:
            levels = list(client.levels.list())
            print(f"Total levels: {len(levels)}")
            
            for level in levels:
                print(f"  - {level.name}")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 5: Legal Entities
        # =====================================================================
        print("\n--- Example 5: Legal Entities ---")
        try:
            entities = list(client.legal_entities.list())
            print(f"Total legal entities: {len(entities)}")
            
            for entity in entities:
                name = entity.legal_name or "(no legal name)"
                print(f"  - {name} (ID: {entity.id})")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 6: Compensation Data
        # =====================================================================
        print("\n--- Example 6: Compensation Data (limited to 25) ---")
        try:
            compensations = list(client.compensations.list(max_results=25))
            print(f"Fetched {len(compensations)} compensation records")
            
            # Show sample compensation data (be careful with sensitive data!)
            if compensations:
                comp = compensations[0]
                print(f"\nSample compensation record fields:")
                for field in dir(comp):
                    if not field.startswith('_'):
                        value = getattr(comp, field, None)
                        if not callable(value):
                            # Mask sensitive values
                            print(f"  {field}: [AVAILABLE]")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 7: Leave Types
        # =====================================================================
        print("\n--- Example 7: Leave Types ---")
        try:
            leave_types = list(client.leave_types.list())
            print(f"Total leave types: {len(leave_types)}")
            
            for lt in leave_types:
                print(f"  - {lt.name} (ID: {lt.id})")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 8: Leave Balances
        # =====================================================================
        print("\n--- Example 8: Leave Balances (limited to 25) ---")
        try:
            balances = list(client.leave_balances.list(max_results=25))
            print(f"Fetched {len(balances)} leave balance records")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 9: Leave Requests
        # =====================================================================
        print("\n--- Example 9: Leave Requests (limited to 25) ---")
        try:
            requests = list(client.leave_requests.list(max_results=25))
            print(f"Fetched {len(requests)} leave requests")
            
            if requests:
                req = requests[0]
                print(f"\nSample leave request fields:")
                for field in dir(req):
                    if not field.startswith('_'):
                        value = getattr(req, field, None)
                        if not callable(value):
                            print(f"  {field}: {value}")
        except RipplingAPIError as e:
            print(f"Error: {e}")

    print("\n" + "=" * 60)
    print("HR Operations examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
