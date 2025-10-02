import requests
from typing import List, Dict, Any
import os
import json
from pathlib import Path

class APIClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("BACKEND_URL", "http://localhost:8000")
        self.token_file = Path.home() / ".expense_tracker_token.json"
        self.access_token = None
        self.refresh_token = None
        self.load_tokens()

    def get_users(self) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.base_url}/users/", headers=self._auth_header())
        response.raise_for_status()
        return response.json()

    def create_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.post(f"{self.base_url}/users/", json=user)
        response.raise_for_status()
        return response.json()

    def get_categories(self, user_id: int) -> List[Dict[str, Any]]:
        response = requests.get(f"{self.base_url}/categories/", params={"user_id": user_id}, headers=self._auth_header())
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
        response = requests.get(f"{self.base_url}/expenses/", params=params, headers=self._auth_header())
        response.raise_for_status()
        return response.json()

    def create_expense(self, expense: Dict[str, Any], user_id: int) -> Dict[str, Any]:
        expense["user_id"] = user_id
        response = requests.post(f"{self.base_url}/expenses/", json=expense, headers=self._auth_header())
        response.raise_for_status()
        return response.json()

    def update_expense(self, expense_id: int, expense: Dict[str, Any]) -> Dict[str, Any]:
        response = requests.put(f"{self.base_url}/expenses/{expense_id}", json=expense)
        response.raise_for_status()
        return response.json()

    def delete_expense(self, expense_id: int):
        response = requests.delete(f"{self.base_url}/expenses/{expense_id}", headers=self._auth_header())
        response.raise_for_status()

    def _auth_header(self):
        if self.access_token:
            return {"Authorization": f"Bearer {self.access_token}"}
        return {}

    def save_tokens(self):
        data = {"access_token": self.access_token, "refresh_token": self.refresh_token}
        try:
            with open(self.token_file, "w") as f:
                json.dump(data, f)
        except Exception:
            pass

    def load_tokens(self):
        try:
            if self.token_file.exists():
                with open(self.token_file) as f:
                    data = json.load(f)
                    self.access_token = data.get("access_token")
                    self.refresh_token = data.get("refresh_token")
        except Exception:
            pass

    def set_tokens(self, access_token: str, refresh_token: str | None = None):
        self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token
        self.save_tokens()

    def refresh_access_token(self):
        if not self.refresh_token:
            return False
        resp = requests.post(f"{self.base_url}/refresh", data={"token": self.refresh_token})
        if resp.status_code == 200:
            self.access_token = resp.json().get("access_token")
            self.save_tokens()
            return True
        return False