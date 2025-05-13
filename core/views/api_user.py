from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import PlatformUser, WalletAddress, Merchant
from core.utils import encrypt_private_key
from eth_account import Account
import os

@api_view(['POST'])
def import_user(request):
    """
    商户导入平台用户并自动生成绑定钱包地址（ERC20）
    """
    merchant_key = request.data.get("merchant_key")
    user_id = request.data.get("user_id")
    email = request.data.get("email")
    chain_type = request.data.get("chain", "erc20")
    token_type = request.data.get("token", "usdt").lower()

    if not all([merchant_key, user_id, email]):
        return Response({"detail": "缺少必要字段"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        merchant = Merchant.objects.get(api_key=merchant_key)
    except Merchant.DoesNotExist:
        return Response({"detail": "无效商户 Key"}, status=status.HTTP_403_FORBIDDEN)

    # 创建平台用户
    user, _ = PlatformUser.objects.get_or_create(user_id=user_id, merchant=merchant, defaults={"email": email})

    # 检查是否已有该链+币的钱包
    if WalletAddress.objects.filter(user=user, chain_type=chain_type, token_type=token_type).exists():
        wallet = WalletAddress.objects.get(user=user, chain_type=chain_type, token_type=token_type)
        return Response({
            "address": wallet.address,
            "token": wallet.token_type,
            "chain": wallet.chain_type
        })

    # 创建新钱包（ERC20）
    acct = Account.create()
    address = acct.address
    private_key = acct.key.hex()

    # 加密私钥
    secret_key = os.getenv("WALLET_SECRET_KEY", "")
    encrypted_pk = encrypt_private_key(private_key, secret_key)

    # 保存钱包
    wallet = WalletAddress.objects.create(
        user=user,
        address=address,
        encrypted_private_key=encrypted_pk,
        chain_type=chain_type,
        token_type=token_type
    )

    return Response({
        "address": wallet.address,
        "chain": wallet.chain_type,
        "token": wallet.token_type
    })