# Broadcast Wizard - Quick Reference Guide

## 🚀 Quick Start

### For Administrators

1. **Access Broadcast Menu**
   ```
   /start → [👑 管理员面板] → [📢 群发通知]
   ```

2. **Create New Broadcast**
   ```
   [📝 创建群发] → Opens two-column editor
   ```

3. **Set Content** (Required)
   - Click `📝 文本`
   - Enter HTML-formatted content
   - Supports: `<b>`, `<i>`, `<code>`, `<a href="">`
   - Returns to editor automatically

4. **Add Media** (Optional)
   - Click `📸 媒体`
   - Upload photo (JPG/PNG/GIF)
   - Returns to editor with ✅ status

5. **Add Buttons** (Optional)
   - Click `🔘 按钮`
   - Format: `Text|https://url` or `Text|callback:message`
   - Max 4 buttons
   - Or type "skip" to skip

6. **Preview & Send**
   - Click `🔍 完整预览` to test
   - Click `➡️ 下一步` to choose targets
   - Select target group (all/members/active/new)
   - Click `✅ 开始发送`

## 🎯 Button Functions

### Main Editor Buttons

| Button | Action | Callback |
|--------|--------|----------|
| 📸 媒体 | Upload photo | `broadcast_media` |
| 👁️ 查看 (Media) | View current photo | `broadcast_media_view` |
| 🗑️ 清除 (Media) | Remove photo | `broadcast_media_clear` |
| 📝 文本 | Enter HTML text | `broadcast_text` |
| 👁️ 查看 (Text) | Preview text | `broadcast_text_view` |
| 🔘 按钮 | Add custom buttons | `broadcast_buttons` |
| 👁️ 查看 (Buttons) | View button list | `broadcast_buttons_view` |
| 🗑️ 清除 (Buttons) | Remove buttons | `broadcast_buttons_clear` |
| 🔍 完整预览 | Full preview | `broadcast_preview` |
| 🔙 返回 | Cancel | `broadcast_cancel` |
| ➡️ 下一步 | Select targets | `broadcast_next` |

## 📝 Text Formatting

### Supported HTML Tags

```html
<b>粗体文本</b>                    → Bold
<i>斜体文本</i>                    → Italic
<code>代码文本</code>              → Monospace
<a href="https://url">链接</a>    → Hyperlink
<pre>预格式化文本</pre>             → Preformatted
```

### Example Message

```html
<b>🎉 特别优惠通知</b>

尊敬的用户：

我们为您准备了以下优惠：
• 会员 <b>5折</b> 优惠
• 新用户 <i>首次免费</i>
• 活动时间：限时3天

优惠码：<code>PROMO2024</code>

<a href="https://example.com">立即查看详情</a>
```

## 🔘 Button Configuration

### URL Button
```
按钮文本|https://example.com
```

Example:
```
官方网站|https://telegram.org
立即购买|https://shop.example.com
```

### Callback Button
```
按钮文本|callback:提示信息
```

Example:
```
点击试试|callback:感谢您的关注！
客服咨询|callback:请联系 @support
```

### Multiple Buttons (Max 4)

```
官方网站|https://telegram.org
使用教程|https://docs.example.com
立即体验|https://app.example.com
客服帮助|callback:24小时在线客服
```

## 🎯 Target Groups

### Available Options

| Target | Description | Filter |
|--------|-------------|--------|
| 👥 全部用户 | All registered users | None |
| 💎 仅会员 | Active members only | Valid membership |
| 🔥 活跃用户(7天) | Recently active | Last active < 7 days |
| 🆕 新用户(7天) | New registrations | Registered < 7 days |

### Selection Tips

- **System Maintenance**: Use "全部用户"
- **Member Offers**: Use "仅会员"
- **New Features**: Use "活跃用户(7天)"
- **Welcome Messages**: Use "新用户(7天)"

## ⚙️ Status Indicators

### Editor Status

```
⚪ 未设置 (Not configured)
✅ 已设置 (Configured)
```

### Requirements

- ⚪ 媒体 - Optional
- ✅ 文本 - **Required**
- ⚪ 按钮 - Optional

## 🔍 Troubleshooting

### Problem: Button Not Responding
**Solution**: This is now fixed! All buttons respond properly.

### Problem: Text Required Warning
**Solution**: Click `📝 文本` and enter content before proceeding.

### Problem: Upload Failed
**Solution**: 
- Check photo size (< 10MB recommended)
- Use JPG/PNG/GIF format
- Try again or skip media

### Problem: Preview Not Showing
**Solution**: 
- Ensure text content is set
- Check HTML formatting
- Try preview again

### Problem: Send Failed
**Solution**: 
- Check target group has users
- Verify admin permissions
- Review error message

## ⏱️ Timeouts

- **Input Timeout**: 5 minutes per step
- **Session Cleanup**: Automatic after timeout
- **Restart**: Use `/start` to begin new broadcast

## 📊 Monitoring

### During Send

Real-time display:
- Progress: N/Total (XX%)
- Success: N users
- Failed: N users
- Speed: N users/sec
- ETA: N seconds

### After Send

Summary shows:
- Total users targeted
- Success count and rate
- Failed count
- Total duration
- Broadcast ID

### History

Access via `[📜 历史记录]`:
- Last 10 broadcasts
- Status, target, counts
- Click for detailed view

## 🛡️ Safety Features

### Automatic
- ✅ query.answer() for all callbacks
- ✅ Admin permission checks
- ✅ Input validation
- ✅ Timeout protection
- ✅ Error recovery

### Best Practices
- Test with small groups first
- Use preview before sending
- Avoid frequent broadcasts (max 2-3/week)
- Keep messages concise
- Verify HTML formatting

## 🔄 Workflow Examples

### Simple Text Broadcast

```
1. Create → 2. Set Text → 3. Next → 4. Select All → 5. Send
```

### Image + Text Broadcast

```
1. Create → 2. Upload Media → 3. Set Text → 4. Preview
→ 5. Next → 6. Select Target → 7. Send
```

### Full-Featured Broadcast

```
1. Create → 2. Upload Media → 3. Set Text → 4. Add Buttons
→ 5. Preview → 6. Next → 7. Select Target → 8. Confirm → 9. Send
```

## 📞 Support

### Getting Help

- Check this guide first
- Review BROADCAST_FEATURE.md for details
- Review BROADCAST_FIX_SUMMARY.md for technical info
- Contact development team for issues

### Reporting Issues

Include:
- What you were trying to do
- Which button you clicked
- Error message (if any)
- Screenshot (if possible)

## 🔮 Future Features

Coming soon:
- Multiple image support
- Video/GIF support
- Scheduled broadcasts
- Broadcast templates
- A/B testing
- Analytics dashboard

---

**Version**: 2.0 (with responsive buttons)  
**Last Updated**: 2025-10-23  
**Status**: Production Ready ✅
