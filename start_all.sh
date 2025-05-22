#!/bin/bash

# 进入项目目录（根据你的实际路径调整）
cd /root/wallet_v1 || exit

# 激活虚拟环境
source venv/bin/activate

# 启动 Telegram Bot
tmux new-session -d -s tg_bot "source venv/bin/activate && python manage.py tg_bot"

# 启动 TRC20 监听
tmux new-session -d -s monitor_trx "source venv/bin/activate && python manage.py monitor_trx"

# 启动 ERC20 监听
tmux new-session -d -s monitor_erc "source venv/bin/activate && python manage.py monitor_erc"

# 启动 BTC 监听
tmux new-session -d -s monitor_erc "source venv/bin/activate && python manage.py monitor_btc"


echo "✅ 所有服务已通过 tmux 启动。使用 tmux ls 查看会话，tmux attach -t [会话名] 进入。"