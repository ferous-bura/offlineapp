import requests
from django.shortcuts import get_object_or_404
from bingo.models import BingoUser, User

BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

def update_balance(request, user_id):
    """Fetches balance from remote API and updates local user balance."""
    headers = {"User-Agent": BROWSER_USER_AGENT}
    response = requests.get(f"https://remote-server.com/api/balance/{user_id}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        user = get_object_or_404(User, id=user_id)
        BingoUser.objects.filter(owner=user).update(balance=data.get("balance", 0))
        return {"success": True, "message": "Balance updated successfully."}
    
    return {"success": False, "message": "Failed to fetch balance."}
