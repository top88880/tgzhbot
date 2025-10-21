# Web Login API Documentation

## Overview

The Web Login API service provides a built-in web interface for viewing Telegram login verification codes. Each account gets a unique URL where users can see their phone number, 2FA status, and the latest verification code from the 777000 bot.

## Features

- **Public web pages** per account showing:
  - Phone number with copy-to-clipboard functionality
  - 2FA status (enabled/disabled/unknown)
  - Latest 777000 verification code (5-6 digits)
  - Automatic refresh every 5 seconds
  - Bilingual UI (Chinese and English)
  
- **JSON API endpoints**:
  - `GET /api/v1/info/{token}` - Account information
  - `GET /api/v1/code/{token}?wait=30` - Code polling with long-poll support
  - `GET /healthz` - Health check
  
- **Visual styling** matching the PVBOT design:
  - Red gradient left panel with logo and envelope icon
  - Clean white content area with status cards
  - Responsive design for mobile and desktop

## Configuration

Add these variables to your `.env` file:

```env
API_SERVER_HOST=0.0.0.0
API_SERVER_PORT=8080
PUBLIC_BASE_URL=https://your-domain.com
```

- `API_SERVER_HOST`: Host to bind the server (default: 0.0.0.0)
- `API_SERVER_PORT`: Port to listen on (default: 8080)
- `PUBLIC_BASE_URL`: Optional public URL for generated links (defaults to http://host:port)

## Usage

### 1. Automatic Registration (Tdata → Session Conversion)

When you convert Tdata files to Session format, the bot automatically registers all successfully converted sessions and provides web links:

```
✅ 转换任务完成！

📊 转换统计
• 总计: 5个
• ✅ 成功: 5个 (100.0%)
• ❌ 失败: 0个 (0.0%)

🌐 Web Login API 链接
📱 +1234567890
🔗 http://localhost:8080/login/AbC123...

✅ 已注册 5 个账号到 Web Login API
```

### 2. Manual Registration (/api command)

Use the `/api` command to scan your `sessions/` directory and publish links for existing session files:

```
/api
```

Response:
```
🌐 Web Login API 链接

📊 找到 3 个 session 文件

📱 +1234567890
🔗 http://localhost:8080/login/AbC123XyZ456

📱 +9876543210
🔗 http://localhost:8080/login/DeF789GhI012

📱 +5551234567
🔗 http://localhost:8080/login/JkL345MnO678

💡 使用说明:
• 点击链接访问登录页面
• 页面会实时显示收到的验证码
• 支持 API 接口查询验证码
```

## API Endpoints

### GET /login/{token}

Returns the HTML login page for the account.

**Example:**
```
http://localhost:8080/login/AbC123XyZ456
```

### GET /api/v1/info/{token}

Returns JSON with account information:

```json
{
  "phone": "+1234567890",
  "has_2fa": true,
  "last_code": "123456",
  "last_code_at": "2025-10-21T10:49:13.123456"
}
```

### GET /api/v1/code/{token}?wait=30

Returns JSON with the latest verification code. Supports long-polling:

**Query Parameters:**
- `wait` (optional): Seconds to wait for a new code (0-30)

**Response:**
```json
{
  "last_code": "123456",
  "last_code_at": "2025-10-21T10:49:13.123456"
}
```

### GET /healthz

Health check endpoint:

**Response:**
```
OK
```

## How It Works

1. **Session Registration**: When a session is registered, a unique token is generated and the account is added to the service.

2. **Lazy Connection**: The Telethon client connects to Telegram only when the page is first accessed.

3. **Event Subscription**: Once connected, the service subscribes to new messages from bot 777000 (Telegram's verification code bot).

4. **Code Extraction**: When a message arrives, the service extracts 5-6 digit codes using regex.

5. **Real-time Updates**: The web page polls the API every 5 seconds for new codes, and displays them automatically.

## Security Notes

- Each account has a unique, unguessable token (128-bit random)
- Tokens are never stored persistently (generated on registration)
- The service runs on localhost by default
- For production use, consider:
  - Setting up HTTPS with a reverse proxy (nginx, Caddy)
  - Restricting access with firewall rules
  - Using authentication middleware if needed

## Dependencies

The Web Login API requires `aiohttp>=3.9`:

```bash
pip install aiohttp
```

This is automatically included in `requirements.txt`.

## Architecture

```
┌─────────────────┐
│   TGapibot.py   │
│  (Main Bot)     │
└────────┬────────┘
         │
         │ initializes
         ▼
┌─────────────────┐
│  login_api.py   │
│ LoginApiService │
└────────┬────────┘
         │
         ├─ Background Thread
         │  └─ aiohttp Server
         │
         ├─ AccountContext Storage
         │  └─ {token: account_info}
         │
         └─ Telethon Clients
            └─ Event handlers for 777000
```

## Troubleshooting

### Service not starting

**Error**: `Web Login API 服务不可用`

**Solution**: Install aiohttp:
```bash
pip install aiohttp
```

### No sessions found

**Error**: `sessions 目录中没有找到 .session 文件`

**Solution**: 
- Place your `.session` files in the `sessions/` directory
- Or convert Tdata files to Session format first

### Code not appearing

**Possible causes**:
1. Session not authorized - log in to the account first
2. No recent messages from 777000 (codes expire after 30 minutes)
3. Client not connected - check Session Status on the page

**Solution**: Trigger a new login from a Telegram client to receive a fresh code.

## Customization

The page branding can be customized by editing `login_api.py`:

```python
# In _generate_login_page_html method:
brand_name = "PVBOT"  # Change to your brand
brand_handle = "@PvBot"  # Change to your handle
```

The HTML template uses inline CSS for easy customization without external dependencies.
