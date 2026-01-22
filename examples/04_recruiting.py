#!/usr/bin/env python3
"""
Recruiting/ATS Examples for Rippling API Client

This script demonstrates Applicant Tracking System operations:
- Candidates
- Applications
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

from rippling_client import (
    RipplingAPIError,
    RipplingAuthError,
    RipplingSettings,
    SyncRipplingClient,
)


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
        # Example 1: List Candidates
        # =====================================================================
        print("\n--- Example 1: Candidates ---")
        try:
            candidates = list(client.candidates.list())
            print(f"Total candidates: {len(candidates)}")

            if candidates:
                candidate = candidates[0]
                print("\nSample candidate fields:")
                for field in dir(candidate):
                    if not field.startswith("_"):
                        value = getattr(candidate, field, None)
                        if not callable(value):
                            # Mask PII
                            if field in ("email", "phone", "name"):
                                print(f"  {field}: [MASKED]")
                            else:
                                print(f"  {field}: {value}")
        except RipplingAuthError as e:
            print(f"Auth Error (403): {e}")
            print("  (This endpoint requires additional API permissions)")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 2: List Candidate Applications
        # =====================================================================
        print("\n--- Example 2: Candidate Applications ---")
        try:
            applications = list(client.candidate_applications.list())
            print(f"Total applications: {len(applications)}")

            if applications:
                app = applications[0]
                print("\nSample application fields:")
                for field in dir(app):
                    if not field.startswith("_"):
                        value = getattr(app, field, None)
                        if not callable(value):
                            print(f"  {field}: {value}")
        except RipplingAuthError as e:
            print(f"Auth Error (403): {e}")
            print("  (This endpoint requires additional API permissions)")
        except RipplingAPIError as e:
            print(f"Error: {e}")

    print("\n" + "=" * 60)
    print("Recruiting/ATS examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
