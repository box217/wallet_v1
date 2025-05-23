# Generated by Django 5.2 on 2025-05-07 11:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('api_key', models.CharField(max_length=128, unique=True)),
                ('callback_url', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlatformUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.merchant')),
            ],
            options={
                'unique_together': {('merchant', 'user_id')},
            },
        ),
        migrations.CreateModel(
            name='WalletAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, unique=True)),
                ('private_key_encrypted', models.TextField()),
                ('chain_type', models.CharField(choices=[('ERC20', 'Ethereum'), ('TRC20', 'Tron')], max_length=10)),
                ('token_type', models.CharField(choices=[('ETH', 'ETH'), ('USDT', 'USDT'), ('USDC', 'USDC'), ('TRX', 'TRX')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.platformuser')),
            ],
            options={
                'unique_together': {('user', 'chain_type', 'token_type')},
            },
        ),
        migrations.CreateModel(
            name='RechargeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tx_hash', models.CharField(max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=20)),
                ('confirmed', models.BooleanField(default=True)),
                ('chain_type', models.CharField(max_length=10)),
                ('token_type', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.walletaddress')),
            ],
        ),
        migrations.CreateModel(
            name='MerchantCollectionAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chain_type', models.CharField(choices=[('ERC20', 'Ethereum'), ('TRC20', 'Tron')], max_length=10)),
                ('token_type', models.CharField(choices=[('ETH', 'ETH'), ('USDT', 'USDT'), ('USDC', 'USDC'), ('TRX', 'TRX')], max_length=10)),
                ('collection_address', models.CharField(max_length=128)),
                ('enabled', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.merchant')),
            ],
            options={
                'unique_together': {('merchant', 'chain_type', 'token_type')},
            },
        ),
    ]
