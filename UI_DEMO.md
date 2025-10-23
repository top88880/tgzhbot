# UI Demo: File Rename & Account Merge Features

## Visual Walkthrough

### Main Menu (Updated)

```
┌─────────────────────────────────────┐
│  🔍 Telegram账号机器人 V8.0         │
│                                     │
│  👤 用户信息                         │
│  • 昵称: John                       │
│  • ID: 123456789                    │
│  • 会员: 💎 会员                    │
│  • 到期: 2024-12-31 23:59:59       │
│                                     │
│  📡 代理状态                         │
│  • 代理模式: 🟢启用                 │
│  • 代理数量: 5个                    │
│  • 当前时间: 2024-10-23 12:00:00   │
└─────────────────────────────────────┘

┌────────────────┬────────────────┐
│  🚀 账号检测    │  🔄 格式转换    │
├────────────────┼────────────────┤
│  🔐 修改2FA     │  🛡️ 防止找回    │
├────────────────┼────────────────┤
│  🔗 API转换     │  📦 账号拆分    │
├────────────────┼────────────────┤
│ 📝 文件重命名   │ 🧩 账户合并     │  ← NEW!
├────────────────┴────────────────┤
│     💳 开通/兑换会员              │
├──────────────────────────────────┤
│          ℹ️ 帮助                  │
├──────────────────────────────────┤
│          ⚙️ 状态                  │
└──────────────────────────────────┘
```

---

## Feature 1: File Rename Demo

### Step 1: Start Rename
**User Action:** Click "📝 文件重命名"

```
┌─────────────────────────────────────┐
│  📝 文件重命名                       │
│                                     │
│  💡 功能说明                         │
│  • 支持任意格式文件                  │
│  • 保留原始文件扩展名                │
│  • 自动清理非法字符                  │
│  • 无需电脑即可重命名                │
│                                     │
│  📤 请上传需要重命名的文件            │
│                                     │
│  ⏰ 5分钟内未上传将自动取消           │
└─────────────────────────────────────┘

┌──────────────────────────────────┐
│         ❌ 取消                   │
└──────────────────────────────────┘
```

### Step 2: Upload File
**User Action:** Upload "vacation_2024.jpg"

```
┌─────────────────────────────────────┐
│  ✅ 文件已接收                       │
│                                     │
│  📁 原文件名: vacation_2024.jpg     │
│  📏 文件大小: 2.34 MB               │
│                                     │
│  ✏️ 请输入新的文件名                 │
│                                     │
│  • 只需输入文件名（不含扩展名）       │
│  • 扩展名 .jpg 将自动保留            │
│  • 非法字符将自动清理                │
│                                     │
│  ⏰ 5分钟内未输入将自动取消           │
└─────────────────────────────────────┘
```

### Step 3: Enter New Name
**User Action:** Type "summer_trip_italy"

```
[User sends message: summer_trip_italy]
```

### Step 4: Success & File Sent
```
┌─────────────────────────────────────┐
│  ✅ 文件重命名成功                   │
│                                     │
│  原文件名: vacation_2024.jpg        │
│  新文件名: summer_trip_italy.jpg    │
└─────────────────────────────────────┘

[Document sent: summer_trip_italy.jpg - 2.34 MB]

┌─────────────────────────────────────┐
│  ✅ 文件已发送！                     │
└─────────────────────────────────────┘
```

---

## Feature 2: Account Merge Demo

### Step 1: Start Merge
**User Action:** Click "🧩 账户合并"

```
┌─────────────────────────────────────┐
│  🧩 账户文件合并                     │
│                                     │
│  💡 功能说明                         │
│  • 自动识别 TData ZIP 文件           │
│  • 自动配对 Session + JSON 文件      │
│  • 智能分类归档                      │
│                                     │
│  📤 请上传文件                       │
│                                     │
│  支持的文件类型：                    │
│  • .zip (TData格式)                 │
│  • .session (Session文件)           │
│  • .json (配置文件)                 │
│                                     │
│  上传完成后点击"✅ 完成合并"          │
└─────────────────────────────────────┘

┌────────────────┬────────────────┐
│ ✅ 完成合并     │   ❌ 取消      │
└────────────────┴────────────────┘
```

### Step 2-4: Upload Files
**User Action:** Upload "tdata1.zip"

```
┌─────────────────────────────────────┐
│  ✅ 已接收文件 1                     │
│                                     │
│  文件名: tdata1.zip                 │
│                                     │
│  继续上传或点击 "✅ 完成合并"         │
└─────────────────────────────────────┘
```

**User Action:** Upload "user123.session"

```
┌─────────────────────────────────────┐
│  ✅ 已接收文件 2                     │
│                                     │
│  文件名: user123.session            │
│                                     │
│  继续上传或点击 "✅ 完成合并"         │
└─────────────────────────────────────┘
```

**User Action:** Upload "user123.json"

```
┌─────────────────────────────────────┐
│  ✅ 已接收文件 3                     │
│                                     │
│  文件名: user123.json               │
│                                     │
│  继续上传或点击 "✅ 完成合并"         │
└─────────────────────────────────────┘
```

**User Action:** Upload "user456.session"

```
┌─────────────────────────────────────┐
│  ✅ 已接收文件 4                     │
│                                     │
│  文件名: user456.session            │
│                                     │
│  继续上传或点击 "✅ 完成合并"         │
└─────────────────────────────────────┘
```

### Step 5: Complete Merge
**User Action:** Click "✅ 完成合并"

```
┌─────────────────────────────────────┐
│  🔄 正在处理文件...                  │
└─────────────────────────────────────┘
```

### Step 6: Results

```
┌─────────────────────────────────────┐
│  ✅ 账户文件合并完成！               │
│                                     │
│  📊 处理结果                         │
│  • TData ZIP: 1 个                  │
│  • Session+JSON 配对: 1 对          │
│  • 未配对 Session: 1 个             │
│  • 未配对 JSON: 0 个                │
│  • 其他文件: 0 个                   │
│                                     │
│  📦 生成文件                         │
└─────────────────────────────────────┘

[Document 1 sent]
┌─────────────────────────────────────┐
│  📦 TData 文件 (1 项)               │
└─────────────────────────────────────┘
File: tdata_only_1698067890.zip - 5.67 MB

[Document 2 sent]
┌─────────────────────────────────────┐
│  📦 Session+JSON 配对 (1 项)        │
└─────────────────────────────────────┘
File: session_json_pairs_1698067890.zip - 234 KB

[Document 3 sent]
┌─────────────────────────────────────┐
│  📦 未配对/其他 (1 项)              │
└─────────────────────────────────────┘
File: incomplete_1698067890.zip - 123 KB
```

---

## Error Scenarios

### Rename: Invalid Characters

**User uploads:** "report.pdf"
**User types:** "my<file>name|test"

```
┌─────────────────────────────────────┐
│  ✅ 文件重命名成功                   │
│                                     │
│  原文件名: report.pdf               │
│  新文件名: my_file_name_test.pdf    │
└─────────────────────────────────────┘

[Note: Special characters auto-sanitized]
```

### Merge: Unsupported File Type

**User uploads:** "notes.txt"

```
┌─────────────────────────────────────┐
│  ❌ 不支持的文件类型，请上传         │
│     .zip、.session 或 .json 文件    │
└─────────────────────────────────────┘
```

### Merge: No Files

**User clicks:** "✅ 完成合并" without uploading

```
┌─────────────────────────────────────┐
│  ❌ 没有上传任何文件                 │
└─────────────────────────────────────┘
```

---

## Comparison: Before vs After

### Before
- Users needed to:
  1. Download file to computer
  2. Rename locally
  3. Re-upload to Telegram
  
- Account file organization:
  1. Manual sorting
  2. Manual pairing
  3. Error-prone process

### After
- File rename: Direct in-chat, 3 steps
- Account merge: Automated classification, smart pairing
- No computer needed
- Fast and efficient

---

## Technical Flow Diagram

### File Rename Flow
```
User → Click Button → Upload File → Enter Name → Receive File
  ↓        ↓            ↓             ↓            ↓
Status: - → waiting   → waiting    → processing → done
           _rename     _rename       file         ↓
           _file       _newname                  cleanup
```

### Account Merge Flow
```
User → Click → Upload → Upload → Upload → Click → Processing
  ↓      ↓       ↓        ↓        ↓       ↓        ↓
Files:  []  →  [f1] →  [f1,f2] → [f1,f2,f3] →  Analyze
                                                    ↓
                                         ┌──────────┴──────────┐
                                         ↓                     ↓
                                    TData ZIPs          Session+JSON
                                         ↓                     ↓
                                    Package              Package
                                         ↓                     ↓
                                    Send ZIP            Send ZIP
                                         ↓                     ↓
                                         └──────────┬──────────┘
                                                    ↓
                                                 Cleanup
```

---

## User Benefits

✅ **Convenience**
- No computer needed
- Direct in Telegram
- Quick and easy

✅ **Automation**
- Auto file classification
- Auto pairing
- Smart detection

✅ **Safety**
- Temp file cleanup
- No data retention
- Secure processing

✅ **Efficiency**
- Fast processing
- Batch operations
- Clear feedback

---

## Summary

Both features seamlessly integrate into the existing bot interface with:
- Clear visual feedback
- Step-by-step guidance
- Error handling
- Auto cleanup
- Professional UI

Ready for production deployment! 🚀
