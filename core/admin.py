from django.contrib import admin
from .models import (
    Merchant,
    MerchantCollectionAddress,
    PlatformUser,
    WalletAddress,
    TelegramWatchAddress  # ✅ 添加这个
)

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active', 'created_at')

@admin.register(MerchantCollectionAddress)
class MerchantCollectionAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'chain_type', 'token_type', 'collection_address', 'enabled')

@admin.register(PlatformUser)
class PlatformUserAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'user_id', 'username', 'email', 'created_at')

@admin.register(WalletAddress)
class WalletAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'chain_type', 'token_type', 'address', 'created_at')

@admin.register(TelegramWatchAddress)  # ✅ 注册 Telegram 地址表
class TelegramWatchAddressAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'address', 'chain_type', 'added_at')
    search_fields = ('chat_id', 'address')
    list_filter = ('chain_type',)