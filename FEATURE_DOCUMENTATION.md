# Feature Documentation: File Rename & Account Merge

## Overview

Two new features have been added to the Telegram bot, accessible directly from the main menu without requiring commands.

## 1. File Rename (📝 文件重命名)

### Purpose
Allow users to rename any file directly in Telegram without needing a computer.

### User Flow

```
Main Menu
    ↓ (User clicks "📝 文件重命名")
Upload Screen
    ↓ (User uploads file)
Confirmation + Request New Name
    ↓ (User sends new filename)
Rename & Send Back
    ↓
Complete!
```

### UI Messages

#### Step 1: Initial Screen
```
📝 文件重命名

💡 功能说明
• 支持任意格式文件
• 保留原始文件扩展名
• 自动清理非法字符
• 无需电脑即可重命名

📤 请上传需要重命名的文件

⏰ 5分钟内未上传将自动取消

[❌ 取消]
```

#### Step 2: File Received
```
✅ 文件已接收

📁 原文件名: document.pdf
📏 文件大小: 123.45 KB

✏️ 请输入新的文件名

• 只需输入文件名（不含扩展名）
• 扩展名 .pdf 将自动保留
• 非法字符将自动清理

⏰ 5分钟内未输入将自动取消
```

#### Step 3: Success
```
✅ 文件重命名成功

原文件名: document.pdf
新文件名: my_renamed_document.pdf

[Renamed file sent as document]
```

### Technical Details

**Status Tracking:**
- `waiting_rename_file` - Waiting for file upload
- `waiting_rename_newname` - Waiting for new filename input

**Data Storage:**
```python
self.pending_rename[user_id] = {
    'temp_dir': '/tmp/temp_rename_xxx',
    'file_path': '/tmp/temp_rename_xxx/original.pdf',
    'orig_name': 'original.pdf',
    'ext': '.pdf'
}
```

**File Naming Rules:**
- Invalid characters `<>:"/\|?*` replaced with `_`
- Control characters removed
- Max length: 200 characters
- Leading/trailing spaces and dots removed
- Empty names default to `unnamed_file`

**Cleanup:**
- Temp directory removed after completion
- User status reset
- Task removed from pending_rename dict

---

## 2. Account Files Merge (🧩 账户合并)

### Purpose
Let users upload multiple mixed account files and have the bot automatically classify and package them into organized categories.

### Categories

1. **TData-only ZIPs** - ZIP files containing `D877F783D5D3EF8C` directory
2. **Session+JSON Pairs** - Same basename `.session` and `.json` files
3. **Incomplete/Unknown** - Unpaired files or non-TData ZIPs

### User Flow

```
Main Menu
    ↓ (User clicks "🧩 账户合并")
Upload Screen
    ↓ (User uploads file 1)
File Accepted
    ↓ (User uploads file 2)
File Accepted
    ↓ (User uploads file 3)
File Accepted
    ↓ (User clicks "✅ 完成合并")
Processing...
    ↓
Results Sent (Multiple ZIP files)
```

### UI Messages

#### Step 1: Initial Screen
```
🧩 账户文件合并

💡 功能说明
• 自动识别 TData ZIP 文件
• 自动配对 Session + JSON 文件
• 智能分类归档

📤 请上传文件

支持的文件类型：
• .zip (TData格式)
• .session (Session文件)
• .json (配置文件)

上传完成后点击"✅ 完成合并"

[✅ 完成合并] [❌ 取消]
```

#### Step 2: File Received (After each upload)
```
✅ 已接收文件 3

文件名: user2.session

继续上传或点击 "✅ 完成合并"
```

#### Step 3: Processing
```
🔄 正在处理文件...
```

#### Step 4: Results Summary
```
✅ 账户文件合并完成！

📊 处理结果
• TData ZIP: 2 个
• Session+JSON 配对: 3 对
• 未配对 Session: 1 个
• 未配对 JSON: 1 个
• 其他文件: 1 个

📦 生成文件
```

#### Step 5: Result Files
```
[Document 1: tdata_only_1234567890.zip]
Caption: 📦 TData 文件 (2 项)

[Document 2: session_json_pairs_1234567890.zip]
Caption: 📦 Session+JSON 配对 (3 项)

[Document 3: incomplete_1234567890.zip]
Caption: 📦 未配对/其他 (3 项)
```

### Technical Details

**Status Tracking:**
- `waiting_merge_files` - Waiting for file uploads

**Data Storage:**
```python
self.pending_merge[user_id] = {
    'temp_dir': '/tmp/temp_merge_xxx',
    'files': ['file1.zip', 'user1.session', 'user1.json']
}
```

**Detection Logic:**

1. **TData ZIP Detection:**
   ```python
   # Check if ZIP contains D877F783D5D3EF8C directory
   with zipfile.ZipFile(zip_path, 'r') as zf:
       if 'D877F783D5D3EF8C' in any(zf.namelist()):
           return True
   ```

2. **Session+JSON Pairing:**
   ```python
   # Extract basenames and match
   session_basenames = {f.replace('.session', ''): f}
   json_basenames = {f.replace('.json', ''): f}
   
   # Find pairs
   for basename in session_basenames:
       if basename in json_basenames:
           paired.append((session_file, json_file))
   ```

**Output Files:**
- `tdata_only_{timestamp}.zip` - All TData ZIPs
- `session_json_pairs_{timestamp}.zip` - All paired accounts
- `incomplete_{timestamp}.zip` - Everything else

**Cleanup:**
- Temp directory removed after completion
- User status reset
- Task removed from pending_merge dict

---

## Main Menu Integration

The new buttons are added to the main menu in a dedicated row:

```
Main Menu Layout:

[🚀 账号检测]  [🔄 格式转换]
[🔐 修改2FA]   [🛡️ 防止找回]
[🔗 API转换]   [📦 账号拆分]
[📝 文件重命名] [🧩 账户合并]  ← NEW ROW
[💳 开通/兑换会员]
[ℹ️ 帮助]
[⚙️ 状态]
```

---

## Error Handling

### Common Errors

1. **File Too Large**
   - Currently inherits from main file handler (100MB limit)
   - For rename: Any reasonable file size works
   - For merge: Multiple files under limit

2. **Unsupported File Type** (Merge only)
   ```
   ❌ 不支持的文件类型，请上传 .zip、.session 或 .json 文件
   ```

3. **No Files Uploaded** (Merge only)
   ```
   ❌ 没有上传任何文件
   ```

4. **Invalid Filename** (Rename only)
   ```
   ❌ 文件名无效，请重新输入
   ```

5. **Timeout**
   - After 5 minutes of inactivity
   - Auto-cleanup triggered
   - User must restart operation

6. **System Errors**
   - Download failures
   - Disk space issues
   - Permission problems
   - All show appropriate error messages

---

## Performance Considerations

### File Rename
- Single file operation
- Minimal resource usage
- Fast completion (<1 second typically)

### Account Merge
- Multiple file operation
- Processes in background thread
- Async processing with asyncio
- Large batches may take longer
- Progress shown during processing

---

## Security Considerations

1. **Temporary Files**
   - Created in system temp directory
   - Unique names with user_id prefix
   - Cleaned up after completion or error

2. **File Validation**
   - Extension checking
   - Size limits enforced
   - No code execution from uploaded files

3. **User Isolation**
   - Each user has separate temp directory
   - No file conflicts between users
   - Proper cleanup prevents data leaks

4. **Status Management**
   - User status properly tracked
   - Prevents state confusion
   - Timeout protection

---

## Testing

See `TEST_SCENARIOS.md` for comprehensive test cases.

See `test_new_features.py` for automated unit tests.

---

## Future Enhancements

Possible future improvements:

1. **Batch Rename**
   - Upload multiple files
   - Rename all with pattern

2. **Merge Options**
   - Custom categories
   - Filtering rules
   - Preview before merging

3. **Advanced Rename**
   - Pattern matching
   - Regex support
   - Bulk operations

4. **Statistics**
   - Track usage
   - Show merge history
   - Export reports
