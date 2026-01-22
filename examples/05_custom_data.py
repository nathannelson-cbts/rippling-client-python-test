#!/usr/bin/env python3
"""
Custom Fields and Objects Examples for Rippling API Client

This script demonstrates working with custom data:
- Custom fields (company-defined employee attributes)
- Custom objects (company-defined data structures)
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
        # Example 1: List Custom Fields
        # =====================================================================
        print("\n--- Example 1: Custom Fields ---")
        try:
            custom_fields = list(client.custom_fields.list())
            print(f"Total custom fields: {len(custom_fields)}")

            for cf in custom_fields:
                field_type = getattr(cf, "type", "unknown")
                print(f"  - {cf.name} (Type: {field_type}, ID: {cf.id})")
        except RipplingAPIError as e:
            print(f"Error: {e}")

        # =====================================================================
        # Example 2: List Custom Objects
        # =====================================================================
        print("\n--- Example 2: Custom Objects ---")
        try:
            custom_objects = list(client.custom_objects.list())
            print(f"Total custom objects: {len(custom_objects)}")

            for co in custom_objects:
                print(f"  - {co.name} (ID: {co.id})")

                # Show fields if available
                if hasattr(co, "fields") and co.fields:
                    for field in co.fields:
                        field_name = getattr(field, "name", "unnamed")
                        field_type = getattr(field, "type", "unknown")
                        print(f"      Field: {field_name} ({field_type})")
        except RipplingAPIError as e:
            print(f"Error: {e}")

    print("\n" + "=" * 60)
    print("Custom Fields/Objects examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
