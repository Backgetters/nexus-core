#!/usr/bin/env python3
"""
BambooHR API Integration for NEXUS
Lightweight wrapper using requests
"""

import os
import requests
from typing import Dict, List, Optional

class BambooHRClient:
    """BambooHR API client"""
    
    BASE_URL = "https://api.bamboohr.com/api/gateway.php"
    
    def __init__(self, company_domain: str, api_key: str):
        self.company_domain = company_domain
        self.api_key = api_key
        self.base_url = f"{self.BASE_URL}/{company_domain}/v1"
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make authenticated request"""
        url = f"{self.base_url}/{endpoint}"
        auth = (self.api_key, 'x')  # BambooHR uses API key as username
        
        response = requests.request(
            method=method,
            url=url,
            auth=auth,
            json=data,
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return response.json() if response.content else {}
    
    def get_employees(self) -> List[Dict]:
        """Get all employees"""
        return self._request("GET", "employees/directory")
    
    def get_employee(self, employee_id: str) -> Dict:
        """Get employee details"""
        return self._request("GET", f"employees/{employee_id}")
    
    def get_time_off(self, employee_id: str) -> List[Dict]:
        """Get time off requests"""
        return self._request("GET", f"employees/{employee_id}/time_off")
    
    def request_time_off(self, employee_id: str, start: str, end: str, 
                         time_off_type: str, notes: str = "") -> Dict:
        """Submit time off request"""
        data = {
            "start": start,
            "end": end,
            "timeOffType": time_off_type,
            "notes": notes
        }
        return self._request("POST", f"employees/{employee_id}/time_off", data)

if __name__ == "__main__":
    # Example usage
    client = BambooHRClient(
        company_domain=os.getenv("BAMBOOHR_DOMAIN"),
        api_key=os.getenv("BAMBOOHR_API_KEY")
    )
    
    employees = client.get_employees()
    print(f"Found {len(employees)} employees")
