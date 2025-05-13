import hashlib
import random
import string
from .models import WalletAddress

def generate_wallet(chain_type):
    # 模拟生成私钥
    seed = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    private_key = hashlib.sha256(seed.encode()).hexdigest()
    if chain_type == 'ERC20':
        address = '0x' + private_key[-40:]
    elif chain_type == 'TRC20':
        address = 'T' + private_key[-33:].upper()
    else:
        return None, None
    encrypted = hashlib.sha256(("enc:" + private_key).encode()).hexdigest()
    return address, encrypted

def generate_wallet_for_user(user):
    created = 0
    chains = [('ERC20', 'ETH'), ('ERC20', 'USDT'), ('ERC20', 'USDC'), ('TRC20', 'TRX'), ('TRC20', 'USDT')]
    for chain_type, token in chains:
        if not WalletAddress.objects.filter(user=user, chain_type=chain_type, token_type=token).exists():
            addr, enc_key = generate_wallet(chain_type)
            WalletAddress.objects.create(
                user=user,
                address=addr,
                private_key_encrypted=enc_key,
                chain_type=chain_type,
                token_type=token
            )
            created += 1
    return created

from Crypto.Cipher import AES
import base64
import os

def decrypt_private_key(encrypted: str, key: str) -> str:
    raw = base64.b64decode(encrypted)
    iv = raw[:16]
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv=iv)
    decrypted = cipher.decrypt(raw[16:])
    return decrypted.decode('utf-8')