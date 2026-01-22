#!/usr/bin/env python3
"""
Async Client Examples for Rippling API Client

This script demonstrates using the async client for better performance
when making multiple concurrent API calls.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()

from rippling_client import AsyncRipplingClient, RipplingSettings, RipplingAPIError


async def collect_list(async_iter, max_results: int | None = None):
    """Helper to collect async iterator into a list with optional limit."""
    results = []
    async for item in async_iter:
        results.append(item)
        if max_results is not None and len(results) >= max_results:
            break
    return results


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


async def main():
    settings = get_settings()
    
    async with AsyncRipplingClient(settings=settings) as client:
        # =====================================================================
        # Example 1: Fetch Multiple Resources Concurrently
        # =====================================================================
        print("\n--- Example 1: Concurrent API Calls (limited to 25 each) ---")
        
        try:
            # Launch all requests concurrently for better performance
            results = await asyncio.gather(
                collect_list(client.companies.list(max_results=25), max_results=25),
                collect_list(client.departments.list(max_results=25), max_results=25),
                collect_list(client.teams.list(max_results=25), max_results=25),
                collect_list(client.work_locations.list(max_results=25), max_results=25),
                return_exceptions=True  # Don't fail all if one fails
            )
            
            companies, departments, teams, locations = results
            
            # Handle potential errors
            if isinstance(companies, Exception):
                print(f"Companies error: {companies}")
            else:
                print(f"Companies: {len(companies)}")
            
            if isinstance(departments, Exception):
                print(f"Departments error: {departments}")
            else:
                print(f"Departments: {len(departments)}")
            
            if isinstance(teams, Exception):
                print(f"Teams error: {teams}")
            else:
                print(f"Teams: {len(teams)}")
            
            if isinstance(locations, Exception):
                print(f"Locations error: {locations}")
            else:
                print(f"Work Locations: {len(locations)}")
                
        except Exception as e:
            print(f"Error in concurrent fetch: {e}")

        # =====================================================================
        # Example 2: Fetch Worker Details in Parallel
        # =====================================================================
        print("\n--- Example 2: Parallel Worker Lookups (limited to 25) ---")
        
        try:
            # First get list of workers (limited for demo)
            workers = await collect_list(client.workers.list(max_results=25), max_results=25)
            print(f"Fetched {len(workers)} workers")
            
            # If there's a get method, we could fetch details for multiple workers
            # concurrently. For now, just demonstrate the pattern:
            if workers and len(workers) > 1:
                # Get first 5 worker IDs
                worker_ids = [w.id for w in workers[:5]]
                print(f"Sample worker IDs: {worker_ids}")
                
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 3: Dashboard Data Aggregation
        # =====================================================================
        print("\n--- Example 3: Dashboard Data Aggregation (limited to 25 each) ---")
        
        try:
            # Simulate building a dashboard by fetching multiple data sources
            results = await asyncio.gather(
                collect_list(client.workers.list(max_results=25), max_results=25),
                collect_list(client.departments.list(max_results=25), max_results=25),
                collect_list(client.leave_requests.list(max_results=25), max_results=25),
                collect_list(client.leave_types.list(max_results=25), max_results=25),
                return_exceptions=True
            )
            
            workers, departments, leave_requests, leave_types = results
            
            dashboard_data = {}
            
            if not isinstance(workers, Exception):
                dashboard_data['total_employees'] = len(workers)
            
            if not isinstance(departments, Exception):
                dashboard_data['total_departments'] = len(departments)
            
            if not isinstance(leave_requests, Exception):
                dashboard_data['pending_leave_requests'] = len([
                    r for r in leave_requests 
                    if hasattr(r, 'status') and str(r.status).lower() == 'pending'
                ])
                dashboard_data['total_leave_requests'] = len(leave_requests)
            
            if not isinstance(leave_types, Exception):
                dashboard_data['leave_types'] = len(leave_types)
            
            print("Dashboard Summary:")
            for key, value in dashboard_data.items():
                print(f"  {key}: {value}")
                
        except Exception as e:
            print(f"Error building dashboard: {e}")

    print("\n" + "=" * 60)
    print("Async examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
