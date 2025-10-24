# -*- coding: utf-8 -*-
# 完整的多语言字典与工具

LANGS = {
    "zh-CN": {
        "label": "🇨🇳 简体中文",
        "menu": {
            "check": "🚀 账号检测",
            "convert": "🔄 格式转换",
            "change2fa": "🔐 修改2FA",
            "antirecover": "🛡️ 防止找回",
            "api": "🔗 API转换",
            "classify": "📦 账号分类",
            "rename": "📝 文件重命名",
            "merge": "🧩 账户合并",
            "vip": "💳 开通/兑换会员",
            "help": "ℹ️ 帮助",
            "status": "⚙️ 状态",
            "admin_panel": "👑 管理员面板",
            "proxy_panel": "📡 代理管理",
            "switch_lang": "🌐 切换语言",
            "back_main": "🔙 返回主菜单"
        },
        "welcome_title": "🔍 Telegram账号机器人 V8.0",
        "help": {
            "title": "📖 详细说明",
            "enhanced_features": "🚀 增强功能",
            "proxy_mode_detect": "• 代理连接模式自动检测",
            "status_display": "• 状态|数量分离实时显示",
            "auto_send_files": "• 检测完成后自动发送分类文件",
            "proxy_advantages": "📡 代理优势",
            "improve_success": "• 提高检测成功率",
            "avoid_ip_limit": "• 避免IP限制",
            "auto_failover": "• 自动故障转移"
        },
        "status": {
            "title": "⚙️ 系统状态",
            "bot_info": "🤖 机器人信息",
            "version": "• 版本: 8.0 (完整版)",
            "status_running": "• 状态: ✅正常运行",
            "current_time": "• 当前时间: {time}"
        },
        "proxy": {
            "title": "📡 代理管理面板",
            "current_status": "📊 当前状态",
            "system_config": "• 系统配置: {config}",
            "proxy_switch": "• 代理开关: {status}",
            "proxy_file": "• 代理文件: {file}",
            "available_proxies": "• 可用代理: {count}个",
            "residential_proxies": "• 住宅代理: {count}个",
            "normal_timeout": "• 普通超时: {timeout}秒",
            "residential_timeout": "• 住宅超时: {timeout}秒",
            "actual_mode": "• 实际模式: {mode}",
            "format_support": "📝 代理格式支持",
            "http_format": "• HTTP: ip:port",
            "http_auth_format": "• HTTP认证: ip:port:username:password",
            "socks5_format": "• SOCKS5: socks5:ip:port:username:password",
            "socks4_format": "• SOCKS4: socks4:ip:port",
            "abc_format": "• ABCProxy住宅代理: host.abcproxy.vip:port:username:password",
            "operation_guide": "🛠️ 操作说明",
            "enable_disable": "• 启用/禁用：控制代理开关状态",
            "reload": "• 重新加载：从文件重新读取代理列表",
            "test": "• 测试代理：检测代理连接性能",
            "view_status": "• 查看状态：显示详细代理信息",
            "statistics": "• 代理统计：查看使用数据统计",
            "btn_disable": "🔴 禁用代理",
            "btn_enable": "🟢 启用代理",
            "btn_reload": "🔄 重新加载代理",
            "btn_status": "📊 代理状态",
            "btn_test": "🧪 测试代理",
            "btn_clean": "🧹 清理失效代理",
            "enabled": "🟢已启用",
            "disabled": "🔴已禁用",
            "proxy_mode": "🟢代理模式",
            "local_mode": "🔴本地模式",
            "use_proxy_true": "🟢USE_PROXY=true",
            "use_proxy_false": "🔴USE_PROXY=false",
            "admin_only": "❌ 仅管理员可以访问代理管理面板"
        },
        "common": {
            "success": "✅ 成功",
            "failed": "❌ 失败",
            "processing": "🔄 处理中...",
            "cancel": "❌ 取消",
            "confirm": "✅ 确认",
            "back": "🔙 返回",
            "next": "➡️ 下一步",
            "complete": "✅ 完成",
            "error": "❌ 错误",
            "admin_only": "❌ 仅管理员可访问"
        }
    },
    "ru": {
        "label": "🇷🇺 Русский",
        "menu": {
            "check": "🚀 Проверка аккаунтов",
            "convert": "🔄 Преобразование формата",
            "change2fa": "🔐 Изменить 2FA",
            "antirecover": "🛡️ Защита от восстановления",
            "api": "🔗 API-конвертация",
            "classify": "📦 Разделение аккаунтов",
            "rename": "📝 Переименовать файлы",
            "merge": "🧩 Объединить аккаунты",
            "vip": "💳 Подписка/Код",
            "help": "ℹ️ Помощь",
            "status": "⚙️ Статус",
            "admin_panel": "👑 Панель админа",
            "proxy_panel": "📡 Менеджер прокси",
            "switch_lang": "🌐 Сменить язык",
            "back_main": "🔙 Назад в меню"
        },
        "welcome_title": "🔍 Бот проверки Telegram аккаунтов V8.0",
        "help": {
            "title": "📖 Подробное описание",
            "enhanced_features": "🚀 Расширенные функции",
            "proxy_mode_detect": "• Автоопределение режима прокси-соединения",
            "status_display": "• Отдельное отображение статуса и количества в реальном времени",
            "auto_send_files": "• Автоматическая отправка классифицированных файлов после проверки",
            "proxy_advantages": "📡 Преимущества прокси",
            "improve_success": "• Повышение успешности проверки",
            "avoid_ip_limit": "• Избежание ограничений IP",
            "auto_failover": "• Автоматическое переключение при сбое"
        },
        "status": {
            "title": "⚙️ Состояние системы",
            "bot_info": "🤖 Информация о боте",
            "version": "• Версия: 8.0 (полная)",
            "status_running": "• Статус: ✅работает нормально",
            "current_time": "• Текущее время: {time}"
        },
        "proxy": {
            "title": "📡 Панель управления прокси",
            "current_status": "📊 Текущий статус",
            "system_config": "• Конфигурация системы: {config}",
            "proxy_switch": "• Переключатель прокси: {status}",
            "proxy_file": "• Файл прокси: {file}",
            "available_proxies": "• Доступные прокси: {count}",
            "residential_proxies": "• Резидентные прокси: {count}",
            "normal_timeout": "• Обычный таймаут: {timeout} сек",
            "residential_timeout": "• Резидентный таймаут: {timeout} сек",
            "actual_mode": "• Фактический режим: {mode}",
            "format_support": "📝 Поддерживаемые форматы прокси",
            "http_format": "• HTTP: ip:port",
            "http_auth_format": "• HTTP с аутентификацией: ip:port:username:password",
            "socks5_format": "• SOCKS5: socks5:ip:port:username:password",
            "socks4_format": "• SOCKS4: socks4:ip:port",
            "abc_format": "• ABCProxy резидентные прокси: host.abcproxy.vip:port:username:password",
            "operation_guide": "🛠️ Руководство по эксплуатации",
            "enable_disable": "• Включить/Выключить: Управление состоянием переключателя прокси",
            "reload": "• Перезагрузить: Повторное чтение списка прокси из файла",
            "test": "• Тест прокси: Проверка производительности прокси-соединения",
            "view_status": "• Просмотр статуса: Отображение подробной информации о прокси",
            "statistics": "• Статистика прокси: Просмотр статистики использования данных",
            "btn_disable": "🔴 Отключить прокси",
            "btn_enable": "🟢 Включить прокси",
            "btn_reload": "🔄 Перезагрузить прокси",
            "btn_status": "📊 Статус прокси",
            "btn_test": "🧪 Тестировать прокси",
            "btn_clean": "🧹 Очистить неработающие прокси",
            "enabled": "🟢включено",
            "disabled": "🔴отключено",
            "proxy_mode": "🟢режим прокси",
            "local_mode": "🔴локальный режим",
            "use_proxy_true": "🟢USE_PROXY=true",
            "use_proxy_false": "🔴USE_PROXY=false",
            "admin_only": "❌ Доступ только для администраторов"
        },
        "common": {
            "success": "✅ Успех",
            "failed": "❌ Ошибка",
            "processing": "🔄 Обработка...",
            "cancel": "❌ Отмена",
            "confirm": "✅ Подтвердить",
            "back": "🔙 Назад",
            "next": "➡️ Далее",
            "complete": "✅ Завершено",
            "error": "❌ Ошибка",
            "admin_only": "❌ Только для администраторов"
        }
    },
    "en-US": {
        "label": "🇺🇸 English (US)",
        "menu": {
            "check": "🚀 Account Check",
            "convert": "🔄 Format Convert",
            "change2fa": "🔐 Change 2FA",
            "antirecover": "🛡️ Anti-recovery",
            "api": "🔗 API Convert",
            "classify": "📦 Account Split",
            "rename": "📝 Rename Files",
            "merge": "🧩 Merge Accounts",
            "vip": "💳 Membership/Code",
            "help": "ℹ️ Help",
            "status": "⚙️ Status",
            "admin_panel": "👑 Admin Panel",
            "proxy_panel": "📡 Proxy Manager",
            "switch_lang": "🌐 Switch Language",
            "back_main": "🔙 Back to Main"
        },
        "welcome_title": "🔍 Telegram Account Bot V8.0",
        "help": {
            "title": "📖 Detailed Description",
            "enhanced_features": "🚀 Enhanced Features",
            "proxy_mode_detect": "• Automatic proxy connection mode detection",
            "status_display": "• Real-time display of status and quantity separately",
            "auto_send_files": "• Auto-send classified files after detection",
            "proxy_advantages": "📡 Proxy Advantages",
            "improve_success": "• Improve detection success rate",
            "avoid_ip_limit": "• Avoid IP restrictions",
            "auto_failover": "• Automatic failover"
        },
        "status": {
            "title": "⚙️ System Status",
            "bot_info": "🤖 Bot Information",
            "version": "• Version: 8.0 (Full)",
            "status_running": "• Status: ✅Running normally",
            "current_time": "• Current time: {time}"
        },
        "proxy": {
            "title": "📡 Proxy Management Panel",
            "current_status": "📊 Current Status",
            "system_config": "• System Config: {config}",
            "proxy_switch": "• Proxy Switch: {status}",
            "proxy_file": "• Proxy File: {file}",
            "available_proxies": "• Available Proxies: {count}",
            "residential_proxies": "• Residential Proxies: {count}",
            "normal_timeout": "• Normal Timeout: {timeout}s",
            "residential_timeout": "• Residential Timeout: {timeout}s",
            "actual_mode": "• Actual Mode: {mode}",
            "format_support": "📝 Proxy Format Support",
            "http_format": "• HTTP: ip:port",
            "http_auth_format": "• HTTP Auth: ip:port:username:password",
            "socks5_format": "• SOCKS5: socks5:ip:port:username:password",
            "socks4_format": "• SOCKS4: socks4:ip:port",
            "abc_format": "• ABCProxy Residential: host.abcproxy.vip:port:username:password",
            "operation_guide": "🛠️ Operation Guide",
            "enable_disable": "• Enable/Disable: Control proxy switch status",
            "reload": "• Reload: Re-read proxy list from file",
            "test": "• Test Proxy: Check proxy connection performance",
            "view_status": "• View Status: Display detailed proxy information",
            "statistics": "• Proxy Statistics: View usage data statistics",
            "btn_disable": "🔴 Disable Proxy",
            "btn_enable": "🟢 Enable Proxy",
            "btn_reload": "🔄 Reload Proxy",
            "btn_status": "📊 Proxy Status",
            "btn_test": "🧪 Test Proxy",
            "btn_clean": "🧹 Clean Invalid Proxies",
            "enabled": "🟢Enabled",
            "disabled": "🔴Disabled",
            "proxy_mode": "🟢Proxy Mode",
            "local_mode": "🔴Local Mode",
            "use_proxy_true": "🟢USE_PROXY=true",
            "use_proxy_false": "🔴USE_PROXY=false",
            "admin_only": "❌ Admin access only"
        },
        "common": {
            "success": "✅ Success",
            "failed": "❌ Failed",
            "processing": "🔄 Processing...",
            "cancel": "❌ Cancel",
            "confirm": "✅ Confirm",
            "back": "🔙 Back",
            "next": "➡️ Next",
            "complete": "✅ Complete",
            "error": "❌ Error",
            "admin_only": "❌ Admin only"
        }
    }
}

# Add missing language definitions for my (Myanmar), bn (Bangladesh), ar (Arabic), vi (Vietnamese)
LANGS["my"] = {
    "label": "🇲🇲 မြန်မာဘာသာ",
    "menu": {
        "check": "🚀 အကောင့်စစ်ဆေးခြင်း",
        "convert": "🔄 ဖော်မတ်ပြောင်းခြင်း",
        "change2fa": "🔐 2FA ပြောင်းခြင်း",
        "antirecover": "🛡️ ပြန်လည်ရယူခြင်းကာကွယ်",
        "api": "🔗 API ပြောင်းခြင်း",
        "classify": "📦 အကောင့်ခွဲခြားခြင်း",
        "rename": "📝 ဖိုင်အမည်ပြောင်းခြင်း",
        "merge": "🧩 အကောင့်ပေါင်းခြင်း",
        "vip": "💳 အဖွဲ့ဝင်/ကုဒ်",
        "help": "ℹ️ အကူအညီ",
        "status": "⚙️ အခြေအနေ",
        "admin_panel": "👑 စီမံခန့်ခွဲမှုပြားပြား",
        "proxy_panel": "📡 Proxy စီမံခန့်ခွဲမှု",
        "switch_lang": "🌐 ဘာသာစကားပြောင်းရန်",
        "back_main": "🔙 ပင်မမီနူးသို့ပြန်သွားရန်"
    },
    "welcome_title": "🔍 Telegram အကောင့် Bot V8.0",
    "help": LANGS["zh-CN"]["help"].copy(),
    "status": LANGS["zh-CN"]["status"].copy(),
    "proxy": LANGS["zh-CN"]["proxy"].copy(),
    "common": LANGS["zh-CN"]["common"].copy()
}

LANGS["bn"] = {
    "label": "🇧🇩 বাংলা",
    "menu": {
        "check": "🚀 অ্যাকাউন্ট পরীক্ষা",
        "convert": "🔄 ফরম্যাট রূপান্তর",
        "change2fa": "🔐 2FA পরিবর্তন",
        "antirecover": "🛡️ পুনরুদ্ধার প্রতিরোধ",
        "api": "🔗 API রূপান্তর",
        "classify": "📦 অ্যাকাউন্ট বিভাজন",
        "rename": "📝 ফাইল পুনঃনামকরণ",
        "merge": "🧩 অ্যাকাউন্ট একত্রিত",
        "vip": "💳 সদস্যপদ/কোড",
        "help": "ℹ️ সাহায্য",
        "status": "⚙️ অবস্থা",
        "admin_panel": "👑 প্রশাসক প্যানেল",
        "proxy_panel": "📡 প্রক্সি ম্যানেজার",
        "switch_lang": "🌐 ভাষা পরিবর্তন",
        "back_main": "🔙 মূল মেনুতে ফিরে যান"
    },
    "welcome_title": "🔍 Telegram অ্যাকাউন্ট Bot V8.0",
    "help": LANGS["zh-CN"]["help"].copy(),
    "status": LANGS["zh-CN"]["status"].copy(),
    "proxy": LANGS["zh-CN"]["proxy"].copy(),
    "common": LANGS["zh-CN"]["common"].copy()
}

LANGS["ar"] = {
    "label": "🇸🇦 العربية",
    "menu": {
        "check": "🚀 فحص الحساب",
        "convert": "🔄 تحويل التنسيق",
        "change2fa": "🔐 تغيير 2FA",
        "antirecover": "🛡️ منع الاسترداد",
        "api": "🔗 تحويل API",
        "classify": "📦 تصنيف الحساب",
        "rename": "📝 إعادة تسمية الملفات",
        "merge": "🧩 دمج الحسابات",
        "vip": "💳 العضوية/الرمز",
        "help": "ℹ️ مساعدة",
        "status": "⚙️ الحالة",
        "admin_panel": "👑 لوحة الإدارة",
        "proxy_panel": "📡 مدير البروكسي",
        "switch_lang": "🌐 تغيير اللغة",
        "back_main": "🔙 العودة إلى القائمة"
    },
    "welcome_title": "🔍 بوت حساب Telegram V8.0",
    "help": LANGS["zh-CN"]["help"].copy(),
    "status": LANGS["zh-CN"]["status"].copy(),
    "proxy": LANGS["zh-CN"]["proxy"].copy(),
    "common": LANGS["zh-CN"]["common"].copy()
}

LANGS["vi"] = {
    "label": "🇻🇳 Tiếng Việt",
    "menu": {
        "check": "🚀 Kiểm tra tài khoản",
        "convert": "🔄 Chuyển đổi định dạng",
        "change2fa": "🔐 Thay đổi 2FA",
        "antirecover": "🛡️ Chống khôi phục",
        "api": "🔗 Chuyển đổi API",
        "classify": "📦 Phân loại tài khoản",
        "rename": "📝 Đổi tên tệp",
        "merge": "🧩 Hợp nhất tài khoản",
        "vip": "💳 Thành viên/Mã",
        "help": "ℹ️ Trợ giúp",
        "status": "⚙️ Trạng thái",
        "admin_panel": "👑 Bảng quản trị",
        "proxy_panel": "📡 Quản lý Proxy",
        "switch_lang": "🌐 Đổi ngôn ngữ",
        "back_main": "🔙 Quay lại menu chính"
    },
    "welcome_title": "🔍 Bot tài khoản Telegram V8.0",
    "help": LANGS["zh-CN"]["help"].copy(),
    "status": LANGS["zh-CN"]["status"].copy(),
    "proxy": LANGS["zh-CN"]["proxy"].copy(),
    "common": LANGS["zh-CN"]["common"].copy()
}

# Comprehensive text keys for all UI surfaces
# Usage: bot.t(user_id, TEXTS["key_name"])
TEXTS = {
    # Main menu and welcome
    "user_info_title": {
        "zh-CN": "👤 <b>用户信息</b>",
        "en-US": "👤 <b>User Information</b>",
        "ru": "👤 <b>Информация о пользователе</b>",
        "my": "👤 <b>အသုံးပြုသူအချက်အလက်</b>",
        "bn": "👤 <b>ব্যবহারকারীর তথ্য</b>",
        "ar": "👤 <b>معلومات المستخدم</b>",
        "vi": "👤 <b>Thông tin người dùng</b>"
    },
    "nickname": {
        "zh-CN": "• 昵称: {name}",
        "en-US": "• Nickname: {name}",
        "ru": "• Никнейм: {name}",
        "my": "• အမည်: {name}",
        "bn": "• ডাকনাম: {name}",
        "ar": "• اللقب: {name}",
        "vi": "• Biệt danh: {name}"
    },
    "user_id": {
        "zh-CN": "• ID: <code>{user_id}</code>",
        "en-US": "• ID: <code>{user_id}</code>",
        "ru": "• ID: <code>{user_id}</code>",
        "my": "• ID: <code>{user_id}</code>",
        "bn": "• ID: <code>{user_id}</code>",
        "ar": "• ID: <code>{user_id}</code>",
        "vi": "• ID: <code>{user_id}</code>"
    },
    "membership": {
        "zh-CN": "• 会员: {status}",
        "en-US": "• Membership: {status}",
        "ru": "• Подписка: {status}",
        "my": "• အဖွဲ့ဝင်: {status}",
        "bn": "• সদস্যপদ: {status}",
        "ar": "• العضوية: {status}",
        "vi": "• Thành viên: {status}"
    },
    "expiry": {
        "zh-CN": "• 到期: {expiry}",
        "en-US": "• Expiry: {expiry}",
        "ru": "• Истекает: {expiry}",
        "my": "• သက်တမ်းကုန်ဆုံးရက်: {expiry}",
        "bn": "• মেয়াদ শেষ: {expiry}",
        "ar": "• الانتهاء: {expiry}",
        "vi": "• Hết hạn: {expiry}"
    },
    "proxy_status_title": {
        "zh-CN": "📡 <b>代理状态</b>",
        "en-US": "📡 <b>Proxy Status</b>",
        "ru": "📡 <b>Статус прокси</b>",
        "my": "📡 <b>Proxy အခြေအနေ</b>",
        "bn": "📡 <b>প্রক্সি স্ট্যাটাস</b>",
        "ar": "📡 <b>حالة البروكسي</b>",
        "vi": "📡 <b>Trạng thái Proxy</b>"
    },
    "proxy_mode": {
        "zh-CN": "• 代理模式: {mode}",
        "en-US": "• Proxy Mode: {mode}",
        "ru": "• Режим прокси: {mode}",
        "my": "• Proxy မုဒ်: {mode}",
        "bn": "• প্রক্সি মোড: {mode}",
        "ar": "• وضع البروكسي: {mode}",
        "vi": "• Chế độ Proxy: {mode}"
    },
    "proxy_count": {
        "zh-CN": "• 代理数量: {count}个",
        "en-US": "• Proxy Count: {count}",
        "ru": "• Количество прокси: {count}",
        "my": "• Proxy အရေအတွက်: {count}",
        "bn": "• প্রক্সি সংখ্যা: {count}",
        "ar": "• عدد البروكسي: {count}",
        "vi": "• Số lượng Proxy: {count}"
    },
    "current_time": {
        "zh-CN": "• 当前时间: {time}",
        "en-US": "• Current time: {time}",
        "ru": "• Текущее время: {time}",
        "my": "• လက်ရှိအချိန်: {time}",
        "bn": "• বর্তমান সময়: {time}",
        "ar": "• الوقت الحالي: {time}",
        "vi": "• Thời gian hiện tại: {time}"
    },
    "enabled": {
        "zh-CN": "🟢启用",
        "en-US": "🟢Enabled",
        "ru": "🟢Включено",
        "my": "🟢ဖွင့်ထားသည်",
        "bn": "🟢সক্রিয়",
        "ar": "🟢مفعل",
        "vi": "🟢Đã bật"
    },
    "local_connection": {
        "zh-CN": "🔴本地连接",
        "en-US": "🔴Local Connection",
        "ru": "🔴Локальное соединение",
        "my": "🔴ဒေသခံချိတ်ဆက်မှု",
        "bn": "🔴স্থানীয় সংযোগ",
        "ar": "🔴اتصال محلي",
        "vi": "🔴Kết nối cục bộ"
    },
    "admin_status": {
        "zh-CN": "👑 管理员",
        "en-US": "👑 Administrator",
        "ru": "👑 Администратор",
        "my": "👑 စီမံခန့်ခွဲသူ",
        "bn": "👑 প্রশাসক",
        "ar": "👑 المسؤول",
        "vi": "👑 Quản trị viên"
    },
    "no_membership": {
        "zh-CN": "❌ 无会员",
        "en-US": "❌ No Membership",
        "ru": "❌ Нет подписки",
        "my": "❌ အဖွဲ့ဝင်မဟုတ်ပါ",
        "bn": "❌ কোন সদস্যপদ নেই",
        "ar": "❌ لا عضوية",
        "vi": "❌ Không có thành viên"
    },
    # Membership and access messages
    "need_membership": {
        "zh-CN": "❌ 需要会员权限才能使用此功能",
        "en-US": "❌ Membership required to use this feature",
        "ru": "❌ Требуется подписка для использования этой функции",
        "my": "❌ ဤအင်္ဂါရပ်ကို အသုံးပြုရန် အဖွဲ့ဝင်ခွင့်လိုအပ်သည်",
        "bn": "❌ এই বৈশিষ্ট্য ব্যবহার করতে সদস্যপদ প্রয়োজন",
        "ar": "❌ العضوية مطلوبة لاستخدام هذه الميزة",
        "vi": "❌ Cần thành viên để sử dụng tính năng này"
    },
    # Language selection
    "language_selection_title": {
        "zh-CN": "<b>🌐 选择语言 / Language Selection</b>",
        "en-US": "<b>🌐 Language Selection / 选择语言</b>",
        "ru": "<b>🌐 Выбор языка / Language Selection</b>",
        "my": "<b>🌐 ဘာသာစကားရွေးချယ်ရန် / Language Selection</b>",
        "bn": "<b>🌐 ভাষা নির্বাচন / Language Selection</b>",
        "ar": "<b>🌐 اختيار اللغة / Language Selection</b>",
        "vi": "<b>🌐 Chọn ngôn ngữ / Language Selection</b>"
    },
    "current_language": {
        "zh-CN": "当前语言 / Current: {lang}",
        "en-US": "Current Language / 当前语言: {lang}",
        "ru": "Текущий язык / Current: {lang}",
        "my": "လက်ရှိဘာသာစကား / Current: {lang}",
        "bn": "বর্তমান ভাষা / Current: {lang}",
        "ar": "اللغة الحالية / Current: {lang}",
        "vi": "Ngôn ngữ hiện tại / Current: {lang}"
    },
    "select_language_prompt": {
        "zh-CN": "请选择您喜欢的语言：\nPlease select your preferred language:",
        "en-US": "Please select your preferred language:\n请选择您喜欢的语言：",
        "ru": "Пожалуйста, выберите предпочитаемый язык:\nPlease select your preferred language:",
        "my": "သင်နှစ်သက်သောဘာသာစကားကို ရွေးချယ်ပါ:\nPlease select your preferred language:",
        "bn": "আপনার পছন্দের ভাষা নির্বাচন করুন:\nPlease select your preferred language:",
        "ar": "يرجى اختيار اللغة المفضلة لديك:\nPlease select your preferred language:",
        "vi": "Vui lòng chọn ngôn ngữ ưa thích của bạn:\nPlease select your preferred language:"
    },
    "language_changed": {
        "zh-CN": "✅ 语言已切换到 {lang}",
        "en-US": "✅ Language changed to {lang}",
        "ru": "✅ Язык изменен на {lang}",
        "my": "✅ ဘာသာစကားကို {lang} သို့ ပြောင်းလဲပြီးပါပြီ",
        "bn": "✅ ভাষা {lang} এ পরিবর্তিত হয়েছে",
        "ar": "✅ تم تغيير اللغة إلى {lang}",
        "vi": "✅ Đã chuyển ngôn ngữ sang {lang}"
    },
    "language_change_failed": {
        "zh-CN": "❌ 设置语言失败",
        "en-US": "❌ Failed to set language",
        "ru": "❌ Не удалось установить язык",
        "my": "❌ ဘာသာစကား သတ်မှတ်ရန် မအောင်မြင်ပါ",
        "bn": "❌ ভাষা সেট করতে ব্যর্থ",
        "ar": "❌ فشل في تعيين اللغة",
        "vi": "❌ Không thể đặt ngôn ngữ"
    },
    "back_button": {
        "zh-CN": "🔙 返回 / Back",
        "en-US": "🔙 Back / 返回",
        "ru": "🔙 Назад / Back",
        "my": "🔙 ပြန်သွားရန် / Back",
        "bn": "🔙 ফিরে যান / Back",
        "ar": "🔙 رجوع / Back",
        "vi": "🔙 Quay lại / Back"
    },
}

DEFAULT_LANG = "zh-CN"

def normalize_lang(code: str) -> str:
    if not code:
        return DEFAULT_LANG
    code = code.strip()
    if code in LANGS:
        return code
    aliases = {
        "zh": "zh-CN", "cn": "zh-CN", "ru-RU": "ru", "my-MM": "my",
        "bn-BD": "bn", "ar-SA": "ar", "vi-VN": "vi", "en": "en-US", "us": "en-US"
    }
    return aliases.get(code, DEFAULT_LANG)


def get_menu_labels(lang_code: str) -> dict:
    lang = normalize_lang(lang_code)
    return LANGS.get(lang, LANGS[DEFAULT_LANG])["menu"]


def get_lang_label(lang_code: str) -> str:
    lang = normalize_lang(lang_code)
    return LANGS.get(lang, LANGS[DEFAULT_LANG])["label"]


def list_languages() -> list:
    order = ["zh-CN", "en-US", "ru", "my", "bn", "ar", "vi"]
    result = []
    for c in order:
        result.append((c, LANGS[c]["label"]))
    return result


def get_welcome_title(lang_code: str) -> str:
    lang = normalize_lang(lang_code)
    return LANGS.get(lang, LANGS[DEFAULT_LANG])["welcome_title"]


def get_text(tr: dict, default: str = "", **kwargs) -> str:
    """
    Get translated text with fallback support and formatting.
    
    Args:
        tr: Dictionary with translations for each language (keys are language codes)
        default: Default text if translation not found
        **kwargs: Format parameters for string formatting
    
    Returns:
        Translated and formatted string
    
    Usage:
        # In bot code, use bot.t(user_id, {...translations...})
        text = get_text({"zh-CN": "你好 {name}", "en-US": "Hello {name}"}, name="World")
    """
    # This function is designed to work with the bot.t() helper
    # It receives pre-selected language text
    if isinstance(tr, str):
        text = tr
    elif isinstance(tr, dict):
        # If dict, return the default language or first available
        text = tr.get(DEFAULT_LANG) or next(iter(tr.values()), default)
    else:
        text = default
    
    # Apply formatting if kwargs provided
    if kwargs and text:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            return text
    return text or default


def get_text_by_key(lang_code: str, category: str, key: str, **kwargs) -> str:
    """Get translated text for a given category and key (legacy support)"""
    lang = normalize_lang(lang_code)
    try:
        text = LANGS[lang][category][key]
        if kwargs:
            return text.format(**kwargs)
        return text
    except (KeyError, TypeError):
        # Fallback to default language
        try:
            text = LANGS[DEFAULT_LANG][category][key]
            if kwargs:
                return text.format(**kwargs)
            return text
        except (KeyError, TypeError):
            return f"[Missing: {category}.{key}]"
