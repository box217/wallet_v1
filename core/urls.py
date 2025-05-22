from django.urls import path
from .views import import_user

urlpatterns = [
    path('import-user/', import_user),
]

from Crypto.Cipher import AES
import base64
import os

def decrypt_private_key(encrypted: str, key: str) -> str:
    raw = base64.b64decode(encrypted)
    iv = raw[:16]
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv=iv)
    decrypted = cipher.decrypt(raw[16:])
    return decrypted.decode('utf-8')

from django.urls import path
from .views import watchlist_view

urlpatterns = [
    path("watchlist/", watchlist_view, name="watchlist"),
]