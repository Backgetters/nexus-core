#!/usr/bin/env python3
"""
Gusto API Integration for NEXUS
Lightweight wrapper for payroll/benefits
"""

import os
import requests
from typing import Dict, List

class GustoClient:
    """Gusto API client"""
    
    BASE_URL = "https://api.gusto.com/v1"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make authenticated request"""
        url = f"{self.BASE_URL}/{endpoint}"
        
        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json() if response.content else {}
    
    def get_company(self, company_id: str) -> Dict:
        """Get company details"""
        return self._request("GET", f"companies/{company_id}")
    
    def get_employees(self, company_id: str) -> List[Dict]:
        """Get all employees"""
        return self._request("GET", f"companies/{company_id}/employees")
    
    def get_payrolls(self, company_id: str) -> List[Dict]:
        """Get payroll history"""
        return self._request("GET", f"companies/{company_id}/payrolls")
    
    def run_payroll(self, company_id: str, payroll_data: dict) -> Dict:
        """Process payroll"""
        return self._request("POST", f"companies/{company_id}/payrolls", payroll_data)
    
    def get_benefits(self, company_id: str) -> List[Dict]:
        """Get company benefits"""
        return self._request("GET", f"companies/{company_id}/company_benefits")

if __name__ == "__main__":
    client = GustoClient(access_token=os.getenv("GUSTO_ACCESS_TOKEN"))
    # Example usage
    print("Gusto client ready")
