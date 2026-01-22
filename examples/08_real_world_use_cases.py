#!/usr/bin/env python3
"""
Real-World Use Case Examples for Rippling API Client

This script demonstrates practical integration scenarios.
"""

import os
import sys
import json
from datetime import datetime, timedelta
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


def export_employee_directory(client):
    """
    Use Case: Export employee directory to JSON for integration with other systems.
    Common for syncing with Slack, internal wikis, or ID badge systems.
    """
    print("\n--- Use Case: Export Employee Directory (limited to 25 each) ---")
    
    try:
        workers = list(client.workers.list(max_results=25))
        users = list(client.users.list(max_results=25))
        departments = list(client.departments.list(max_results=25))
        
        # Create a lookup for departments
        dept_map = {d.id: d.name for d in departments}
        
        # Build export data (simplified)
        directory = []
        for worker in workers:
            entry = {
                'id': worker.id,
            }
            
            # Add available fields
            for field in ['name', 'email', 'title', 'department_id', 'manager_id', 'start_date']:
                if hasattr(worker, field):
                    value = getattr(worker, field)
                    if value is not None:
                        entry[field] = str(value) if not isinstance(value, (str, int, float, bool)) else value
            
            # Resolve department name if available
            if 'department_id' in entry and entry['department_id'] in dept_map:
                entry['department_name'] = dept_map[entry['department_id']]
            
            directory.append(entry)
        
        print(f"Exported {len(directory)} employees")
        print(f"Sample entry: {json.dumps(directory[0] if directory else {}, indent=2, default=str)}")
        
        return directory
        
    except RipplingAPIError as e:
        print(f"Error exporting directory: {e}")
        return []


def generate_org_chart_data(client):
    """
    Use Case: Generate org chart data structure.
    Common for visualization tools and reporting.
    """
    print("\n--- Use Case: Generate Org Chart Data (limited to 25) ---")
    
    try:
        workers = list(client.workers.list(max_results=25))
        
        # Build hierarchy
        org_structure = {}
        top_level = []
        
        for worker in workers:
            worker_id = worker.id
            manager_id = getattr(worker, 'manager_id', None)
            
            org_structure[worker_id] = {
                'id': worker_id,
                'name': getattr(worker, 'name', worker_id),
                'title': getattr(worker, 'title', 'Unknown'),
                'manager_id': manager_id,
                'reports': []
            }
        
        # Build relationships
        for worker_id, data in org_structure.items():
            manager_id = data.get('manager_id')
            if manager_id and manager_id in org_structure:
                org_structure[manager_id]['reports'].append(worker_id)
            elif not manager_id:
                top_level.append(worker_id)
        
        print(f"Total employees: {len(org_structure)}")
        print(f"Top-level (no manager): {len(top_level)}")
        
        # Find who has the most direct reports
        most_reports = max(org_structure.values(), key=lambda x: len(x['reports']), default=None)
        if most_reports and most_reports['reports']:
            print(f"Most direct reports: {most_reports['name']} ({len(most_reports['reports'])} reports)")
        
        return org_structure
        
    except RipplingAPIError as e:
        print(f"Error generating org chart: {e}")
        return {}


def department_headcount_report(client):
    """
    Use Case: Generate department headcount report.
    Common for HR analytics and budget planning.
    """
    print("\n--- Use Case: Department Headcount Report (limited to 25 each) ---")
    
    try:
        workers = list(client.workers.list(max_results=25))
        departments = list(client.departments.list(max_results=25))
        
        # Create department lookup
        dept_map = {d.id: d.name for d in departments}
        
        # Count by department
        headcount = {}
        no_dept_count = 0
        
        for worker in workers:
            dept_id = getattr(worker, 'department_id', None)
            if dept_id:
                dept_name = dept_map.get(dept_id, f"Unknown ({dept_id})")
                headcount[dept_name] = headcount.get(dept_name, 0) + 1
            else:
                no_dept_count += 1
        
        # Sort by headcount descending
        sorted_headcount = sorted(headcount.items(), key=lambda x: x[1], reverse=True)
        
        print(f"\nHeadcount by Department:")
        print("-" * 40)
        for dept, count in sorted_headcount:
            bar = "█" * min(count, 50)
            print(f"{dept:30} {count:4} {bar}")
        
        if no_dept_count:
            print(f"{'(No Department)':30} {no_dept_count:4}")
        
        print("-" * 40)
        print(f"{'TOTAL':30} {len(workers):4}")
        
        return dict(sorted_headcount)
        
    except RipplingAPIError as e:
        print(f"Error generating report: {e}")
        return {}


def leave_summary_report(client):
    """
    Use Case: Summarize leave requests for management review.
    Common for HR dashboards and manager tools.
    """
    print("\n--- Use Case: Leave Summary Report (limited to 25 each) ---")
    
    try:
        leave_requests = list(client.leave_requests.list(max_results=25))
        leave_types = list(client.leave_types.list(max_results=25))
        
        # Create leave type lookup
        type_map = {lt.id: lt.name for lt in leave_types}
        
        # Summarize by status
        by_status = {}
        by_type = {}
        
        for req in leave_requests:
            status = str(getattr(req, 'status', 'unknown'))
            by_status[status] = by_status.get(status, 0) + 1
            
            leave_type_id = getattr(req, 'leave_type_id', None)
            leave_type_name = type_map.get(leave_type_id, 'Unknown')
            by_type[leave_type_name] = by_type.get(leave_type_name, 0) + 1
        
        print(f"\nTotal Leave Requests: {len(leave_requests)}")
        
        print("\nBy Status:")
        for status, count in sorted(by_status.items()):
            print(f"  {status}: {count}")
        
        print("\nBy Leave Type:")
        for leave_type, count in sorted(by_type.items(), key=lambda x: x[1], reverse=True):
            print(f"  {leave_type}: {count}")
        
        return {'by_status': by_status, 'by_type': by_type}
        
    except RipplingAPIError as e:
        print(f"Error generating leave summary: {e}")
        return {}


def sync_check(client):
    """
    Use Case: Compare data between Rippling and another system.
    Common for data integrity validation.
    """
    print("\n--- Use Case: Data Sync Validation (limited to 25 each) ---")
    
    try:
        # Fetch all core data
        workers = list(client.workers.list(max_results=25))
        departments = list(client.departments.list(max_results=25))
        locations = list(client.work_locations.list(max_results=25))
        
        # Simulate checking against another system
        # In real use, you'd compare with your internal database
        
        validation_results = {
            'workers_count': len(workers),
            'departments_count': len(departments),
            'locations_count': len(locations),
            'workers_with_dept': sum(1 for w in workers if getattr(w, 'department_id', None)),
            'workers_with_location': sum(1 for w in workers if getattr(w, 'work_location_id', None)),
        }
        
        print("\nSync Validation Results:")
        for key, value in validation_results.items():
            print(f"  {key}: {value}")
        
        # Calculate completeness
        if workers:
            dept_completeness = (validation_results['workers_with_dept'] / len(workers)) * 100
            loc_completeness = (validation_results['workers_with_location'] / len(workers)) * 100
            print(f"\nData Completeness:")
            print(f"  Department assigned: {dept_completeness:.1f}%")
            print(f"  Location assigned: {loc_completeness:.1f}%")
        
        return validation_results
        
    except RipplingAPIError as e:
        print(f"Error in sync check: {e}")
        return {}


def main():
    settings = get_settings()
    
    with SyncRipplingClient(settings=settings) as client:
        # Run all use cases
        export_employee_directory(client)
        generate_org_chart_data(client)
        department_headcount_report(client)
        leave_summary_report(client)
        sync_check(client)

    print("\n" + "=" * 60)
    print("Real-world use case examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
