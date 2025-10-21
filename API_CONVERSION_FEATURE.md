# API Conversion Feature Documentation

## Overview
This feature allows users to batch convert TData or Session files to Web Login API links for getting verification codes.

## Implementation Summary

### 1. User Interface Changes

#### Main Menu Button
- Added "🌐 api转换" button in the main menu
- Position: Second row, alongside "🔐 修改2FA"
- Callback data: `api_convert`

### 2. User Flow

```
User clicks "🌐 api转换" 
    ↓
Bot shows instructions and waits for ZIP upload
    ↓
User uploads ZIP file (containing TData or Session files)
    ↓
Bot processes files:
  - If TData: Converts to Session format first
  - If Session: Uses directly
    ↓
Bot registers each session with LoginApiService
    ↓
Bot generates TXT file with format:
  phone1 url1
  phone2 url2
  ...
    ↓
Bot sends summary + TXT file to user
```

### 3. Code Components

#### A. Callback Handler (`handle_api_convert`)
- **Location**: `TGapibot.py`, after `handle_change_2fa` method
- **Function**: 
  - Checks user permissions (requires membership)
  - Verifies LoginApiService is available
  - Shows detailed instructions
  - Sets user status to `waiting_api_convert_file`

#### B. File Upload Handler (`handle_file`)
- **Changes**: Added branch for `waiting_api_convert_file` status
- **Action**: Spawns thread to run `process_api_conversion` asynchronously

#### C. Main Processing Method (`process_api_conversion`)
- **Location**: `TGapibot.py`, after `complete_2fa_change_with_passwords` method
- **Steps**:
  1. Downloads and scans uploaded ZIP file
  2. Detects file type (TData or Session) using `FileProcessor.scan_zip_file`
  3. **For TData files**:
     - Calls `FormatConverter.batch_convert_with_progress`
     - Converts to Session format
     - Shows real-time progress
     - Collects successful conversions
  4. **For Session files**:
     - Extracts phone numbers from filenames
     - Uses sessions directly
  5. **API Registration**:
     - For each valid session file, calls:
       ```python
       url = self.login_api_service.register_session(
           session_path=session_path,
           phone=phone,
           api_id=config.API_ID,
           api_hash=config.API_HASH
       )
       ```
  6. **Result Generation**:
     - Creates TXT file: `批量转换API_获取成功_{N}.txt`
     - Format: One line per account: `{phone} {url}`
     - Saves to `config.RESULTS_DIR`
  7. **Send Results**:
     - Shows summary statistics
     - Sends TXT file as document
  8. **Cleanup**:
     - Removes temporary directories
     - Deletes result file after sending

### 4. Integration Points

#### Required Services
- `LoginApiService` (from PR #1): Must be available and running
- `FormatConverter`: For TData to Session conversion
- `FileProcessor`: For ZIP file scanning

#### Configuration
Uses existing config values:
- `config.API_ID` and `config.API_HASH`: For Telegram API
- `config.RESULTS_DIR`: For storing result files
- `config.UPLOADS_DIR`: For temporary file extraction

### 5. Output Format

#### TXT File
```
94750902488 https://otp.example.com/login/abc123...
94750911855 https://otp.example.com/login/def456...
```

#### Summary Message
```
批量转换API｜统计数据

🟢 获取成功: 2

⏱️ 处理时间: 15 秒
📊 文件类型: TDATA

📦 正在发送结果文件...
```

### 6. Error Handling

The implementation includes comprehensive error handling:
- Checks if user has membership
- Verifies LoginApiService is available
- Handles file processing failures
- Manages conversion errors
- Cleans up resources in finally blocks

### 7. Real-time Progress

During TData conversion:
```
🔄 转换 API 进行中...

📊 当前进度
• 已处理: 5/10
• 速度: 2.3 个/秒
• 用时: 2 秒

✅ 转换成功: 4
❌ 转换错误: 1

⏱️ 预计剩余: 2 秒
```

## Testing Checklist

- [ ] Main menu displays "🌐 api转换" button
- [ ] Clicking button shows instructions and waits for file
- [ ] Uploading TData ZIP:
  - [ ] Detects as TData format
  - [ ] Converts to Session
  - [ ] Shows real-time progress
  - [ ] Registers sessions to API
  - [ ] Generates TXT file
  - [ ] Sends file to user
- [ ] Uploading Session ZIP:
  - [ ] Detects as Session format
  - [ ] Skips conversion
  - [ ] Registers sessions to API
  - [ ] Generates TXT file
  - [ ] Sends file to user
- [ ] TXT file format is correct:
  - [ ] One line per account
  - [ ] Format: `phone url`
  - [ ] UTF-8 encoding
- [ ] Links open to Login API web page
- [ ] Cleanup removes temporary files
- [ ] Error messages are clear and helpful

## Dependencies

No new dependencies added. Uses existing:
- `python-telegram-bot==13.15`
- `telethon`
- `opentele` (for TData conversion)
- `aiohttp` (for LoginApiService, already required by PR #1)

## Notes

- Feature is non-breaking: existing functionality remains unchanged
- Reuses existing code components where possible
- Follows established patterns in the codebase
- Chinese UI text matches existing style
- Progress updates use same throttling mechanism as other features
