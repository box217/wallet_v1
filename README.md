# 📦 Erc20/Trc20 多链多币种钱包监控系统  
### 💬 Telegram 通知机器人 + 自动余额监控 + 回调系统

---

## ✅ 功能概述

该系统是一个集成式多链钱包监控解决方案，支持以下功能：

- 📡 **监控地址余额变动**（支持 TRC20 与 ERC20 链）
- 🤖 **通过 Telegram 机器人实时通知**
- 📥 **支持添加/删除监听地址**
- 📈 **每日余额变化统计（收入 / 支出 / 利润）**
- 🔄 **回调到商户服务器通知变动事件**

---

## 📋 支持命令一览（通过 Telegram 使用）

| 命令 | 描述 |
|------|------|
| `/start` | 启动机器人 |
| `/help` | 获取帮助命令列表 |
| `/watch <链> <地址>` | 添加监听地址（支持 erc20 / trc20） |
| `/unwatch <地址>` | 删除监听地址 |
| `/list` | 查看当前监听的地址列表 |
| `/check <地址>` | 查询单个地址的余额 |
| `/balance` | 查询当前所有监听地址余额及今日统计 |

---

## 🔌 使用接口说明

### 📍 Tron（TRC20）

- 使用 `tronpy` 库进行链上操作和余额查询
- 使用 `https://api.trongrid.io` 接口拉取交易记录
- 需设置 `TRONGRID_API_KEY` 环境变量（免费有速率限制）

### 📍 Ethereum（ERC20）

- 使用 `web3.py` 连接 `Infura`
- ERC20 USDT 合约地址：`0xdAC17F958D2ee523a2206206994597C13D831ec7`
- 查询余额使用标准 `balanceOf` ABI 调用
- 需设置 `INFURA_URL` 环境变量（建议添加多个 Project Key）

---

## 📦 主要依赖版本

```text
python==3.11.x
Django==5.2
djangorestframework==3.16.0
python-telegram-bot==20.6
web3==6.15.1
tronpy==0.3.0
eth-account==0.9.0
eth-abi==4.2.1
pymysql==1.1.0
gunicorn==23.0.0
python-dotenv==1.0.1
pycryptodome==3.22.0
nest_asyncio==1.6.0
```

---

## 🏗️ 系统结构与模块说明

- `core.models`：商户、用户、钱包、充值记录、回调记录、Telegram监听表
- `core.utils.wallet`：链上余额查询、钱包生成、交易记录分析等
- `core.management.commands.tg_bot`：Telegram Bot 控制逻辑
- `monitor_trx`：可扩展的链上扫描进程，用于定时获取链上交易并写入 `RechargeLog`

---

## 🌐 回调机制说明

监听地址发生充值行为时，会将数据写入 `RechargeLog`，并：

- 检测 `RechargeLog` 中新增记录
- 定位钱包归属商户
- 将以下结构回调至商户配置的 `callback_url`

```json
{
  "address": "钱包地址",
  "amount": "充值金额",
  "tx_hash": "交易哈希",
  "token": "USDT",
  "chain": "TRC20 / ERC20",
  "timestamp": "时间戳"
}
```

---

## ⚙️ 部署要求 & 配置环境变量

### 系统环境：

- Python 3.11+
- MySQL 数据库（或可自定义 ORM 支持的其他 DB）
- Redis（用于 Celery / 消息队列，如扩展异步任务）
- Linux / macOS / Ubuntu 推荐

### 关键环境变量 `.env` 示例：

```env
TG_BOT_TOKEN=123456:ABC-Telegram-Bot-Token
INFURA_URL=https://mainnet.infura.io/v3/your_key
TRONGRID_API_KEY=your_trongrid_api_key
DJANGO_SECRET_KEY=your_secret
DATABASE_URL=mysql://user:pass@127.0.0.1/db
```

### 启动方式：

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py tg_bot
```

> 建议使用 `supervisord` 或 `pm2` 持久运行 Telegram 机器人。

---

## 🚀 TODO 可扩展方向

- ✅ 支持更多币种（如 BSC、MATIC）
- ✅ 添加回调重试机制
- ✅ 使用 Celery 异步处理链上交易分析
- ✅ 记录回调失败日志
- ✅ 引入数据库缓存机制降低调用频率




🗓️ 更新日期：2025-05-22

📌 项目：钱包监听机器人（wallet_v1）

🧾 版本：v1.1.0

⸻

🔧 新增功能
	•	BTC链监听功能
	•	自动识别 BTC 地址（bech32 格式）
	•	使用 Blockstream API 查询余额及收支
	•	/watch 指令或按钮支持 BTC 地址监听
	•	钱包余额查询优化
	•	新增 /check <地址> 指令支持单地址查询（TRC20/ERC20/BTC）
	•	点击“📋 查看我的监听地址”按钮跳转 Web 页面
	•	Web 前端服务
	•	集成 FastAPI 提供监听地址可视化页面 /watchlist/{chat_id}
	•	自动根据 .env 或 settings.py 加载域名配置 (WEB_DOMAIN)
	•	manage.py tg_bot 启动时会自动启动 Web 服务
	•	支持菜单快捷按钮
	•	查询钱包余额 与 添加监控钱包 一键引导
	•	用户发送地址后自动识别链类型并监听

⸻

🧠 智能判断链类型
	•	地址自动识别为：ERC20、TRC20、BTC
	•	/watch 命令参数支持自动推断链类型

⸻

🔒 配置增强
	•	将 .env 中的配置参数迁移至 settings.py（如 WEB_HOST, WEB_PORT, WEB_DOMAIN）
	•	自动 fallback 到默认域名 https://yourdomain.com，避免错误链接

⸻

🐞 修复优化
	•	修复监听按钮立即返回“无法识别地址”问题
	•	修复导入错误、地址识别异常、重复导入等问题
	•	修复 unique_together 设置未识别字段引起的 model 报错

⸻

📁 文件结构优化
	•	新增模块：
	•	core/utils/address_utils.py: 地址识别、链类型推断、余额消息生成
	•	core/webserver.py: FastAPI Web 服务入口
	•	core/bot_handlers.py: Bot 命令注册模块化

	