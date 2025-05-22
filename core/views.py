from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Merchant, PlatformUser
from core.utils.wallet import generate_wallet_for_user
import os

@api_view(['POST'])
def import_user(request):
    api_key = request.data.get("merchant_api_key")
    user_id = request.data.get("user_id")
    username = request.data.get("username")
    email = request.data.get("email")

    if not all([api_key, user_id, username, email]):
        return Response({"error": "Missing required fields"}, status=400)

    try:
        merchant = Merchant.objects.get(api_key=api_key)
    except Merchant.DoesNotExist:
        return Response({"error": "Invalid API Key"}, status=403)

    user, created = PlatformUser.objects.get_or_create(
        merchant=merchant,
        user_id=user_id,
        defaults={"username": username, "email": email}
    )

    # 读取加密密钥（从 .env 中读取）
    secret_key = os.getenv("WALLET_SECRET_KEY", "")
    if not secret_key or len(secret_key) != 32:
        return Response({"error": "Invalid WALLET_SECRET_KEY config"}, status=500)

    count = generate_wallet_for_user(user, secret_key)

    return Response({
        "status": "success",
        "user_created": created,
        "wallets_created": count
    }, status=200)


from django.shortcuts import render
from .models import TelegramWatchAddress

def watchlist_view(request):
    chain_type = request.GET.get("chain", "").upper()
    addresses = TelegramWatchAddress.objects.all()

    if chain_type in ["ERC20", "TRC20", "BTC"]:
        addresses = addresses.filter(chain_type=chain_type)

    addresses = addresses.order_by('-added_at')[:100]
    return render(request, "core/watchlist.html", {
        "addresses": addresses,
        "selected_chain": chain_type,
    })