# Language Switcher Feature Demo

## Overview
The bot now supports 7 languages with a user-friendly language switcher.

## Supported Languages
1. 🇨🇳 **简体中文** (zh-CN) - Chinese Simplified [DEFAULT]
2. 🇺🇸 **English (US)** (en-US) - English
3. 🇷🇺 **Русский** (ru) - Russian
4. 🇲🇲 **မြန်မာ** (my) - Myanmar (Burmese)
5. 🇧🇩 **বাংলা** (bn) - Bengali
6. 🇸🇦 **العربية** (ar) - Arabic
7. 🇻🇳 **Tiếng Việt** (vi) - Vietnamese

## Feature Highlights

### Main Menu Localization
When a user selects a language, all main menu buttons update to that language:

#### Chinese (Default)
```
🚀 账号检测
🔄 格式转换
🔐 修改2FA
🛡️ 防止找回
🔗 API转换
📦 账号分类
📝 文件重命名
🧩 账户合并
💳 开通/兑换会员
ℹ️ 帮助
⚙️ 状态
🌐 切换语言
```

#### English
```
🚀 Account Check
🔄 Format Convert
🔐 Change 2FA
🛡️ Anti-recovery
🔗 API Convert
📦 Account Split
📝 Rename Files
🧩 Merge Accounts
💳 Membership/Code
ℹ️ Help
⚙️ Status
🌐 Switch Language
```

#### Russian
```
🚀 Проверка аккаунтов
🔄 Преобразование формата
🔐 Изменить 2FA
🛡️ Защита от восстановления
🔗 API-конвертация
📦 Разделение аккаунтов
📝 Переименовать файлы
🧩 Объединить аккаунты
💳 Подписка/Код
ℹ️ Помощь
⚙️ Статус
🌐 Сменить язык
```

### Language Selection Panel
```
🌐 选择语言 / Language Selection

当前语言 / Current: 🇨🇳 简体中文

请选择您喜欢的语言：
Please select your preferred language:

✅ 🇨🇳 简体中文          [Current selection]
🇺🇸 English (US)
🇷🇺 Русский
🇲🇲 မြန်မာ
🇧🇩 বাংলা
🇸🇦 العربية
🇻🇳 Tiếng Việt

🔙 返回 / Back
```

## User Flow

1. **User opens bot** → Sees main menu in default language (Chinese)
2. **User clicks "🌐 切换语言"** → Language selection panel appears
3. **User selects a language** (e.g., English) → Toast notification confirms change
4. **Main menu refreshes** → All buttons now show in English
5. **Language persists** → Next time user opens bot, sees English menu

## Technical Implementation

### Files Modified
- `TGapibot.py` - Added language handlers and updated main menu
- `i18n.py` (NEW) - Internationalization module with translations

### Database Changes
- Added `lang` column to `users` table
- User language preference persists across sessions

### Key Functions
- `get_user_lang(user_id)` - Retrieves user's language
- `set_user_lang(user_id, lang_code)` - Saves language preference
- `get_menu_labels(lang_code)` - Returns localized menu labels
- `handle_language_menu()` - Shows language picker
- `handle_set_language()` - Handles language selection

## Migration & Safety
- ✅ Non-breaking database migration
- ✅ Existing users default to Chinese
- ✅ No data loss or conflicts
- ✅ Safe to deploy immediately

## Future Enhancements
Phase 1 focuses on main menu localization. Future phases can add:
- Localized help text
- Localized error messages
- Localized status pages
- Localized broadcast messages

To add new text to localization:
1. Add key to all 7 languages in `i18n.LANGS`
2. Use `get_text(user_lang, key)` in bot code
3. Test with all languages

## Example Code Usage

```python
# Get user's language
user_lang = self.db.get_user_lang(user_id)

# Get localized menu labels
menu_labels = get_menu_labels(user_lang)

# Create button with localized text
InlineKeyboardButton(menu_labels["check"], callback_data="start_check")

# Change user's language
self.db.set_user_lang(user_id, "en-US")
```

## Testing
All functionality tested and verified:
- ✅ i18n module imports correctly
- ✅ Database methods work as expected
- ✅ Language selection persists
- ✅ Menu updates in real-time
- ✅ All 7 languages render correctly
- ✅ No security vulnerabilities (CodeQL scan passed)
