from django.db import models

# 商户信息表
class Merchant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=128, unique=True)
    callback_url = models.URLField()
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 商户归集地址配置（区分链和币种）
class MerchantCollectionAddress(models.Model):
    CHAIN_CHOICES = (('ERC20', 'Ethereum'), ('TRC20', 'Tron'))
    TOKEN_CHOICES = (('ETH', 'ETH'), ('USDT', 'USDT'), ('USDC', 'USDC'), ('TRX', 'TRX'))

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    chain_type = models.CharField(max_length=10, choices=CHAIN_CHOICES)
    token_type = models.CharField(max_length=10, choices=TOKEN_CHOICES)
    collection_address = models.CharField(max_length=128)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('merchant', 'chain_type', 'token_type')

# 平台传入的用户
class PlatformUser(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('merchant', 'user_id')

# 钱包地址记录
class WalletAddress(models.Model):
    CHAIN_CHOICES = (('ERC20', 'Ethereum'), ('TRC20', 'Tron'))
    TOKEN_CHOICES = (('ETH', 'ETH'), ('USDT', 'USDT'), ('USDC', 'USDC'), ('TRX', 'TRX'))

    user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, unique=True)
    private_key_encrypted = models.TextField()
    chain_type = models.CharField(max_length=10, choices=CHAIN_CHOICES)
    token_type = models.CharField(max_length=10, choices=TOKEN_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'chain_type', 'token_type')

class RechargeLog(models.Model):
    wallet = models.ForeignKey(WalletAddress, on_delete=models.CASCADE, null=True, blank=True)  # 修改这里
    tx_hash = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    confirmed = models.BooleanField(default=True)
    chain_type = models.CharField(max_length=10)
    token_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

class CollectionLog(models.Model):
    wallet = models.ForeignKey(WalletAddress, on_delete=models.CASCADE)
    to_address = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    tx_hash = models.CharField(max_length=100, unique=True)
    success = models.BooleanField(default=True)
    chain_type = models.CharField(max_length=10)
    token_type = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)



from django.db import models

class TelegramWatchAddress(models.Model):
    chat_id = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    chain_type = models.CharField(max_length=16)
    token_type = models.CharField(max_length=16)
    added_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('chat_id', 'address', 'chain_type')

    def __str__(self):
        return f"{self.chain_type} | {self.address} by {self.chat_id}"