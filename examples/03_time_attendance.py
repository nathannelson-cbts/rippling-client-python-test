#!/usr/bin/env python3
"""
Time & Attendance Examples for Rippling API Client

This script demonstrates time tracking and attendance operations:
- Time cards
- Time entries
- Tracks (work schedules)
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

from rippling_client import RipplingAPIError, RipplingSettings, SyncRipplingClient


def get_settings() -> RipplingSettings:
    """Load settings from environment variables."""
    bearer_token = os.getenv("RIPPLING_BEARER_TOKEN")
    if not bearer_token:
        print("ERROR: RIPPLING_BEARER_TOKEN environment variable is required")
        sys.exit(1)

    return RipplingSettings(
        bearer_token=bearer_token,  # type: ignore[arg-type]
        base_url=os.getenv("RIPPLING_BASE_URL", "https://rest.ripplingapis.com"),
    )


def main():
    settings = get_settings()

    with SyncRipplingClient(settings=settings) as client:
        # =====================================================================
        # Example 1: List Time Cards
        # =====================================================================
        print("\n--- Example 1: Time Cards (limited to 25) ---")
        try:
            time_cards = list(client.time_cards.list(page_size=10, max_results=25))
            print(f"Fetched {len(time_cards)} time cards")

            if time_cards:
                tc = time_cards[0]
                print("\nSample time card fields:")
                for field in dir(tc):
                    if not field.startswith("_"):
                        value = getattr(tc, field, None)
                        if not callable(value):
                            print(f"  {field}: {value}")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 2: List Time Entries
        # =====================================================================
        print("\n--- Example 2: Time Entries (limited to 25) ---")
        try:
            time_entries = list(client.time_entries.list(page_size=10, max_results=25))
            print(f"Fetched {len(time_entries)} time entries")

            if time_entries:
                entry = time_entries[0]
                print("\nSample time entry fields:")
                for field in dir(entry):
                    if not field.startswith("_"):
                        value = getattr(entry, field, None)
                        if not callable(value):
                            print(f"  {field}: {value}")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 3: List Tracks (Work Schedules)
        # =====================================================================
        print("\n--- Example 3: Tracks (Work Schedules) ---")
        try:
            tracks = list(client.tracks.list())
            print(f"Total tracks: {len(tracks)}")

            for track in tracks:
                print(f"  - {track.name} (ID: {track.id})")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 4: Leave Accruals
        # =====================================================================
        print("\n--- Example 4: Leave Accruals (limited to 25) ---")
        try:
            accruals = list(client.leave_accruals.list(page_size=10, max_results=25))
            print(f"Fetched {len(accruals)} leave accrual records")

            if accruals:
                accrual = accruals[0]
                print("\nSample leave accrual fields:")
                for field in dir(accrual):
                    if not field.startswith("_"):
                        value = getattr(accrual, field, None)
                        if not callable(value):
                            print(f"  {field}: {value}")
        except RipplingAPIError as e:
            print(f"Error: {e}")

    print("\n" + "=" * 60)
    print("Time & Attendance examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
