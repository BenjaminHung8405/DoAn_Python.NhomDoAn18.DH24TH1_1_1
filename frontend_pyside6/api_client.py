import requests
from typing import List, Dict, Any

class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def get_users(self) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.base_url}/users/")
        response.raise_for_status()
        return response.json()

    def create_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/users/", json=user)
        response.raise_for_status()
        return response.json()

    def get_categories(self, user_id: int) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.base_url}/categories/", params={"user_id": user_id})
        response.raise_for_status()
        return response.json()

    def create_category(self, category: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        category["user_id"] = user_id
        response = requests.post(f"{self.base_url}/categories/", json=category)
        response.raise_for_status()
        return response.json()

    def update_category(self, category_id: int, category: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.put(f"{self.base_url}/categories/{category_id}", json=category)
        response.raise_for_status()
        return response.json()

    def delete_category(self, category_id: int):
        response = requests.delete(f"{self.base_url}/categories/{category_id}")
        response.raise_for_status()

    def get_expenses(self, user_id: int, **filters) -> List[Dict[str, Any]]:
        params = {"user_id": user_id, **filters}
        response = requests.get(f"{self.base_url}/expenses/", params=params)
        response.raise_for_status()
        return response.json()

    def create_expense(self, expense: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        expense["user_id"] = user_id
        response = requests.post(f"{self.base_url}/expenses/", json=expense)
        response.raise_for_status()
        return response.json()

    def update_expense(self, expense_id: int, expense: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.put(f"{self.base_url}/expenses/{expense_id}", json=expense)
        response.raise_for_status()
        return response.json()

    def delete_expense(self, expense_id: int):
        response = requests.delete(f"{self.base_url}/expenses/{expense_id}")
        response.raise_for_status()