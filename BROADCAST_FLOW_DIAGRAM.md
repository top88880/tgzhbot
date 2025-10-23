# Broadcast Wizard - Visual Flow Diagram

## User Interaction Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    管理员面板 (Admin Panel)                    │
│                                                               │
│  [👑 管理员面板] → [📢 群发通知] → broadcast_menu            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   群发通知管理 (Broadcast Menu)                │
│                                                               │
│  Options:                                                     │
│  • [📝 创建群发] → broadcast_create                           │
│  • [📜 历史记录] → broadcast_history                          │
│  • [🔙 返回] → admin_panel                                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    broadcast_create clicked
                              ↓
┌─────────────────────────────────────────────────────────────┐
│          📝 创建群发通知 (Two-Column Editor UI)               │
│                                                               │
│  📊 当前状态:                                                  │
│  ⚪/✅ 媒体: 未设置/已设置                                      │
│  ⚪/✅ 文本: 未设置/已设置 (必填)                              │
│  ⚪/✅ 按钮: 0-4 个                                            │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Row 1: 媒体操作                                        │  │
│  │  [📸 媒体]  [👁️ 查看]  [🗑️ 清除]                       │  │
│  │    ↓           ↓          ↓                             │  │
│  │ broadcast_ broadcast_  broadcast_                       │  │
│  │   media    media_view media_clear                       │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Row 2: 文本操作                                        │  │
│  │  [📝 文本]  [👁️ 查看]                                  │  │
│  │    ↓           ↓                                        │  │
│  │ broadcast_ broadcast_                                   │  │
│  │   text     text_view                                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Row 3: 按钮操作                                        │  │
│  │  [🔘 按钮]  [👁️ 查看]  [🗑️ 清除]                       │  │
│  │    ↓           ↓          ↓                             │  │
│  │ broadcast_ broadcast_  broadcast_                       │  │
│  │ buttons   buttons_view buttons_clear                    │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Row 4: 预览                                            │  │
│  │  [🔍 完整预览]                                          │  │
│  │       ↓                                                 │  │
│  │  broadcast_preview                                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Row 5: 导航                                            │  │
│  │  [🔙 返回]    [➡️ 下一步]                               │  │
│  │     ↓             ↓                                     │  │
│  │ broadcast_   broadcast_next                             │  │
│  │  cancel     (→ target selection)                        │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Callback Routing Architecture

```
┌──────────────────────────────────────────────────────────────┐
│              Telegram Update (callback_query)                 │
│                   data = "broadcast_*"                        │
└──────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────┐
│         CallbackQueryHandler Registration Order               │
│                                                                │
│  1. back_to_main handler (pattern: ^back_to_main$)           │
│  2. broadcast handler (pattern: ^broadcast_) ← NEW!           │
│  3. generic handler (catches all remaining)                   │
└──────────────────────────────────────────────────────────────┘
                              ↓
             Caught by broadcast handler (priority)
                              ↓
┌──────────────────────────────────────────────────────────────┐
│       handle_broadcast_callbacks_router()                     │
│                                                                │
│  Step 1: query.answer() with try/except ← SAFETY             │
│  Step 2: Admin permission check                               │
│  Step 3: Dispatch table lookup                                │
│                                                                │
│  dispatch_table = {                                           │
│    "broadcast_menu": λ show_broadcast_menu(),                 │
│    "broadcast_create": λ start_broadcast_wizard(),            │
│    "broadcast_media": λ handle_broadcast_media(),             │
│    "broadcast_text": λ handle_broadcast_text(),               │
│    "broadcast_buttons": λ handle_broadcast_buttons(),         │
│    "broadcast_preview": λ handle_broadcast_preview(),         │
│    "broadcast_next": λ handle_broadcast_next(),               │
│    ... (15 total entries)                                     │
│  }                                                             │
│                                                                │
│  Step 4: Execute corresponding method                         │
│  Step 5: Error handling with try/except                       │
└──────────────────────────────────────────────────────────────┘
                              ↓
                  Method executed successfully
                              ↓
                    UI updated or status changed
```

## Media Upload Flow

```
User clicks [📸 媒体]
        ↓
broadcast_media callback
        ↓
handle_broadcast_media()
        ↓
Set user status: "waiting_broadcast_media"
        ↓
Show upload prompt
        ↓
User uploads photo
        ↓
MessageHandler(Filters.photo) catches it
        ↓
handle_photo() method
        ↓
Check status == "waiting_broadcast_media"
        ↓
Save photo.file_id to task['media_file_id']
        ↓
Clear user status
        ↓
Show confirmation + return to editor
        ↓
User sees updated editor with ✅ 媒体: 已设置
```

## Text Input Flow

```
User clicks [📝 文本]
        ↓
broadcast_text callback
        ↓
handle_broadcast_text()
        ↓
Set user status: "waiting_broadcast_content"
        ↓
Show HTML format instructions
        ↓
User sends text message
        ↓
MessageHandler(Filters.text) catches it
        ↓
handle_text() → check status → handle_broadcast_content_input()
        ↓
Validate content (non-empty)
        ↓
Save to task['content']
        ↓
Clear user status
        ↓
Show confirmation + return to editor
        ↓
User sees updated editor with ✅ 文本: 已设置
```

## Complete Preview Flow

```
User clicks [🔍 完整预览]
        ↓
broadcast_preview callback
        ↓
handle_broadcast_preview()
        ↓
Check task['content'] exists (required)
        ↓
Build keyboard from task['buttons']
        ↓
Send preview message:
  - If media exists: send_photo with caption
  - Otherwise: send_message with text
        ↓
User sees actual broadcast appearance
        ↓
query.answer("✅ 已发送预览")
```

## Next Step (Target Selection) Flow

```
User clicks [➡️ 下一步]
        ↓
broadcast_next callback
        ↓
handle_broadcast_next()
        ↓
Validate task['content'] exists
        ↓
Call show_target_selection()
        ↓
Query user counts:
  - all_users = len(db.get_target_users('all'))
  - members = len(db.get_target_users('members'))
  - active_7d = len(db.get_target_users('active_7d'))
  - new_7d = len(db.get_target_users('new_7d'))
        ↓
Show target selection UI:
  [👥 全部用户 (N)]     → broadcast_target_all
  [💎 仅会员 (N)]       → broadcast_target_members
  [🔥 活跃用户(7天) (N)] → broadcast_target_active_7d
  [🆕 新用户(7天) (N)]   → broadcast_target_new_7d
  [❌ 取消]             → broadcast_cancel
        ↓
User selects target
        ↓
broadcast_target_* callback
        ↓
handle_broadcast_target_selection()
        ↓
Show preview with confirmation
        ↓
[✅ 开始发送] → broadcast_confirm_send
[✏️ 返回修改] → broadcast_edit
[❌ 取消] → broadcast_cancel
```

## Error Handling Flow

```
Any broadcast_* callback triggered
        ↓
handle_broadcast_callbacks_router()
        ↓
Try: query.answer()
Except: log warning, continue
        ↓
Check: is_admin(user_id)
If False: query.answer("❌ 仅管理员...", show_alert=True)
          return
        ↓
Try: dispatch_table[data]()
Except: 
  - Log error with traceback
  - safe_edit_message(query, "❌ 操作失败: ...")
  - Return gracefully
        ↓
User sees error message, system remains stable
```

## Key Improvements Summary

### Before Fix ❌
```
User clicks button → No callback handler → No response → Stuck
```

### After Fix ✅
```
User clicks button 
  → Dedicated handler (pattern: ^broadcast_)
  → query.answer() safety
  → Dispatch table lookup
  → Execute method
  → Update UI
  → Success!
```

## Technical Highlights

1. **Handler Priority**: Broadcast handler registered BEFORE generic
2. **Safety First**: All callbacks wrapped with query.answer()
3. **Clean Dispatch**: 15 actions → 15 lambdas → 13 methods
4. **State Management**: User status + pending_broadcasts dict
5. **Media Support**: Photo handler + file_id storage
6. **Error Recovery**: Try/except everywhere + graceful fallback
7. **Admin Guard**: Permission check at router level
8. **Backward Compatible**: Old methods preserved

## Testing Coverage

✅ Handler registration order
✅ Dispatch table completeness
✅ query.answer() safety
✅ All methods exist
✅ Photo handler present
✅ Two-column UI buttons
✅ Syntax validation
