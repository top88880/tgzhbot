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
    # Proxy panel messages
    "proxy_panel_admin_only": {
        "zh-CN": "❌ 仅管理员可以访问代理管理面板",
        "en-US": "❌ Admin access only for proxy management panel",
        "ru": "❌ Доступ только для администраторов",
        "my": "❌ စီမံခန့်ခွဲသူများသာ ဝင်ရောက်ခွင့်ရှိသည်",
        "bn": "❌ শুধুমাত্র প্রশাসকদের জন্য অ্যাক্সেস",
        "ar": "❌ الوصول للمسؤولين فقط",
        "vi": "❌ Chỉ quản trị viên mới truy cập được"
    },
    "proxy_enabled_success": {
        "zh-CN": "✅ 代理已启用",
        "en-US": "✅ Proxy enabled",
        "ru": "✅ Прокси включено",
        "my": "✅ Proxy ဖွင့်ထားပြီး",
        "bn": "✅ প্রক্সি সক্রিয় করা হয়েছে",
        "ar": "✅ تم تفعيل البروكسي",
        "vi": "✅ Proxy đã được bật"
    },
    "proxy_disabled_success": {
        "zh-CN": "✅ 代理已禁用",
        "en-US": "✅ Proxy disabled",
        "ru": "✅ Прокси отключено",
        "my": "✅ Proxy ပိတ်ထားပြီး",
        "bn": "✅ প্রক্সি নিষ্ক্রিয় করা হয়েছে",
        "ar": "✅ تم تعطيل البروكسي",
        "vi": "✅ Proxy đã được tắt"
    },
    "proxy_reload_success": {
        "zh-CN": "✅ 已重新加载代理列表\n📡 加载了 {count} 个代理",
        "en-US": "✅ Proxy list reloaded\n📡 Loaded {count} proxies",
        "ru": "✅ Список прокси перезагружен\n📡 Загружено {count} прокси",
        "my": "✅ Proxy စာရင်းကို ပြန်လည်တင်ပြီးပါပြီ\n📡 {count} ခု တင်ထားသည်",
        "bn": "✅ প্রক্সি তালিকা পুনরায় লোড হয়েছে\n📡 {count} প্রক্সি লোড করা হয়েছে",
        "ar": "✅ تم إعادة تحميل قائمة البروكسي\n📡 تم تحميل {count} بروكسي",
        "vi": "✅ Đã tải lại danh sách proxy\n📡 Đã tải {count} proxy"
    },
    "proxy_testing_start": {
        "zh-CN": "🧪 开始测试代理...\n这可能需要几分钟时间",
        "en-US": "🧪 Starting proxy test...\nThis may take a few minutes",
        "ru": "🧪 Начинается тест прокси...\nЭто может занять несколько минут",
        "my": "🧪 Proxy စမ်းသပ်မှု စတင်နေပါသည်...\nမိနစ်အနည်းငယ် ကြာနိုင်ပါသည်",
        "bn": "🧪 প্রক্সি পরীক্ষা শুরু হচ্ছে...\nএটি কয়েক মিনিট সময় নিতে পারে",
        "ar": "🧪 بدء اختبار البروكسي...\nقد يستغرق هذا بضع دقائق",
        "vi": "🧪 Bắt đầu kiểm tra proxy...\nĐiều này có thể mất vài phút"
    },
    "proxy_test_results": {
        "zh-CN": "📊 代理测试结果\n\n✅ 可用: {working}个\n❌ 失败: {failed}个\n⏱️ 耗时: {duration}秒",
        "en-US": "📊 Proxy Test Results\n\n✅ Working: {working}\n❌ Failed: {failed}\n⏱️ Duration: {duration}s",
        "ru": "📊 Результаты теста прокси\n\n✅ Работает: {working}\n❌ Не работает: {failed}\n⏱️ Время: {duration}с",
        "my": "📊 Proxy စမ်းသပ်မှု ရလဒ်များ\n\n✅ အလုပ်လုပ်သည်: {working}\n❌ မအောင်မြင်ပါ: {failed}\n⏱️ ကြာချိန်: {duration}စက္ကန့်",
        "bn": "📊 প্রক্সি পরীক্ষার ফলাফল\n\n✅ কাজ করছে: {working}\n❌ ব্যর্থ: {failed}\n⏱️ সময়: {duration}সে",
        "ar": "📊 نتائج اختبار البروكسي\n\n✅ يعمل: {working}\n❌ فشل: {failed}\n⏱️ المدة: {duration}ث",
        "vi": "📊 Kết quả kiểm tra Proxy\n\n✅ Hoạt động: {working}\n❌ Thất bại: {failed}\n⏱️ Thời gian: {duration}s"
    },
    "proxy_cleanup_confirm": {
        "zh-CN": "🧹 <b>清理失效代理</b>\n\n确认要清理测试失败的代理吗？\n这将从proxy.txt中移除失效代理。",
        "en-US": "🧹 <b>Clean Invalid Proxies</b>\n\nConfirm cleaning failed proxies?\nThis will remove invalid proxies from proxy.txt.",
        "ru": "🧹 <b>Очистка неработающих прокси</b>\n\nПодтвердить очистку неудачных прокси?\nЭто удалит неработающие прокси из proxy.txt.",
        "my": "🧹 <b>မမှန်ကန်သော Proxy များကို ရှင်းလင်းရန်</b>\n\nမအောင်မြင်သော proxy များကို ရှင်းလင်းမှာ သေချာပါသလား?\nဒါက proxy.txt ထဲက မမှန်ကန်သော proxy များကို ဖယ်ရှားပါမည်။",
        "bn": "🧹 <b>অবৈধ প্রক্সি পরিষ্কার করুন</b>\n\nব্যর্থ প্রক্সি পরিষ্কার করার নিশ্চিত করুন?\nএটি proxy.txt থেকে অবৈধ প্রক্সি সরিয়ে দেবে।",
        "ar": "🧹 <b>تنظيف البروكسيات غير الصالحة</b>\n\nتأكيد تنظيف البروكسيات الفاشلة؟\nسيؤدي هذا إلى إزالة البروكسيات غير الصالحة من proxy.txt.",
        "vi": "🧹 <b>Dọn dẹp Proxy không hợp lệ</b>\n\nXác nhận dọn dẹp proxy thất bại?\nĐiều này sẽ xóa proxy không hợp lệ khỏi proxy.txt."
    },
    "proxy_cleanup_success": {
        "zh-CN": "✅ 清理完成\n🗑️ 移除了 {count} 个失效代理",
        "en-US": "✅ Cleanup completed\n🗑️ Removed {count} invalid proxies",
        "ru": "✅ Очистка завершена\n🗑️ Удалено {count} неработающих прокси",
        "my": "✅ ရှင်းလင်းမှု ပြီးစီးပါပြီ\n🗑️ မမှန်ကန်သော proxy {count} ခု ဖယ်ရှားပြီးပါပြီ",
        "bn": "✅ পরিষ্কার সম্পন্ন হয়েছে\n🗑️ {count} অবৈধ প্রক্সি সরানো হয়েছে",
        "ar": "✅ اكتمل التنظيف\n🗑️ تمت إزالة {count} بروكسي غير صالح",
        "vi": "✅ Dọn dẹp hoàn tất\n🗑️ Đã xóa {count} proxy không hợp lệ"
    },
    "proxy_no_test_results": {
        "zh-CN": "❌ 没有测试结果\n请先运行代理测试",
        "en-US": "❌ No test results\nPlease run proxy test first",
        "ru": "❌ Нет результатов теста\nПожалуйста, сначала запустите тест прокси",
        "my": "❌ စမ်းသပ်မှု ရလဒ်များ မရှိပါ\nကျေးဇူးပြု၍ ပထမဦးစွာ proxy စမ်းသပ်မှု လုပ်ပါ",
        "bn": "❌ কোন পরীক্ষার ফলাফল নেই\nপ্রথমে প্রক্সি পরীক্ষা চালান",
        "ar": "❌ لا توجد نتائج اختبار\nيرجى تشغيل اختبار البروكسي أولاً",
        "vi": "❌ Không có kết quả kiểm tra\nVui lòng chạy kiểm tra proxy trước"
    },
    # Help and status messages
    "help_text": {
        "zh-CN": get_text_by_key("zh-CN", "help", "title"),
        "en-US": get_text_by_key("en-US", "help", "title"),
        "ru": get_text_by_key("ru", "help", "title"),
        "my": get_text_by_key("my", "help", "title"),
        "bn": get_text_by_key("bn", "help", "title"),
        "ar": get_text_by_key("ar", "help", "title"),
        "vi": get_text_by_key("vi", "help", "title")
    },
    # Convert messages
    "convert_menu_title": {
        "zh-CN": "🔄 <b>格式转换</b>",
        "en-US": "🔄 <b>Format Conversion</b>",
        "ru": "🔄 <b>Преобразование формата</b>",
        "my": "🔄 <b>ဖော်မတ်ပြောင်းခြင်း</b>",
        "bn": "🔄 <b>ফরম্যাট রূপান্তর</b>",
        "ar": "🔄 <b>تحويل التنسيق</b>",
        "vi": "🔄 <b>Chuyển đổi định dạng</b>"
    },
    "convert_select_direction": {
        "zh-CN": "请选择转换方向：",
        "en-US": "Please select conversion direction:",
        "ru": "Пожалуйста, выберите направление преобразования:",
        "my": "ကျေးဇူးပြု၍ ပြောင်းလဲမှု ဦးတည်ချက်ကို ရွေးချယ်ပါ:",
        "bn": "রূপান্তর দিক নির্বাচন করুন:",
        "ar": "يرجى تحديد اتجاه التحويل:",
        "vi": "Vui lòng chọn hướng chuyển đổi:"
    },
    "convert_tdata_to_session": {
        "zh-CN": "📤 TData → Session",
        "en-US": "📤 TData → Session",
        "ru": "📤 TData → Session",
        "my": "📤 TData → Session",
        "bn": "📤 TData → Session",
        "ar": "📤 TData → Session",
        "vi": "📤 TData → Session"
    },
    "convert_session_to_tdata": {
        "zh-CN": "📥 Session → TData",
        "en-US": "📥 Session → TData",
        "ru": "📥 Session → TData",
        "my": "📥 Session → Session",
        "bn": "📥 Session → TData",
        "ar": "📥 Session → TData",
        "vi": "📥 Session → TData"
    },
    "convert_upload_prompt": {
        "zh-CN": "请上传包含{format}文件的ZIP压缩包...",
        "en-US": "Please upload ZIP file containing {format} files...",
        "ru": "Пожалуйста, загрузите ZIP-файл, содержащий файлы {format}...",
        "my": "{format} ဖိုင်များပါရှိသော ZIP ဖိုင်ကို တင်ပါ...",
        "bn": "{format} ফাইল সমন্বিত ZIP ফাইল আপলোড করুন...",
        "ar": "يرجى تحميل ملف ZIP يحتوي على ملفات {format}...",
        "vi": "Vui lòng tải lên tệp ZIP chứa các tệp {format}..."
    },
    "convert_processing": {
        "zh-CN": "🔄 正在转换...\n\n处理中: {current}/{total}\n已完成: {success}\n失败: {failed}",
        "en-US": "🔄 Converting...\n\nProcessing: {current}/{total}\nCompleted: {success}\nFailed: {failed}",
        "ru": "🔄 Преобразование...\n\nОбработка: {current}/{total}\nЗавершено: {success}\nНеудачно: {failed}",
        "my": "🔄 ပြောင်းလဲနေသည်...\n\nလုပ်ဆောင်နေသည်: {current}/{total}\nပြီးစီးပြီ: {success}\nမအောင်မြင်ပါ: {failed}",
        "bn": "🔄 রূপান্তর হচ্ছে...\n\nপ্রক্রিয়াকরণ: {current}/{total}\nসম্পন্ন: {success}\nব্যর্থ: {failed}",
        "ar": "🔄 جارٍ التحويل...\n\nمعالجة: {current}/{total}\nمكتمل: {success}\nفشل: {failed}",
        "vi": "🔄 Đang chuyển đổi...\n\nĐang xử lý: {current}/{total}\nĐã hoàn thành: {success}\nThất bại: {failed}"
    },
    "convert_success": {
        "zh-CN": "✅ 转换完成！\n\n✅ 成功: {success}\n❌ 失败: {failed}\n⏱️ 耗时: {duration}秒",
        "en-US": "✅ Conversion completed!\n\n✅ Success: {success}\n❌ Failed: {failed}\n⏱️ Duration: {duration}s",
        "ru": "✅ Преобразование завершено!\n\n✅ Успешно: {success}\n❌ Неудачно: {failed}\n⏱️ Время: {duration}с",
        "my": "✅ ပြောင်းလဲမှု ပြီးစီးပါပြီ!\n\n✅ အောင်မြင်: {success}\n❌ မအောင်မြင်: {failed}\n⏱️ ကြာချိန်: {duration}စက္ကန့်",
        "bn": "✅ রূপান্তর সম্পন্ন হয়েছে!\n\n✅ সফল: {success}\n❌ ব্যর্থ: {failed}\n⏱️ সময়: {duration}সে",
        "ar": "✅ اكتمل التحويل!\n\n✅ نجح: {success}\n❌ فشل: {failed}\n⏱️ المدة: {duration}ث",
        "vi": "✅ Chuyển đổi hoàn tất!\n\n✅ Thành công: {success}\n❌ Thất bại: {failed}\n⏱️ Thời gian: {duration}s"
    },
    # Check account messages
    "check_upload_prompt": {
        "zh-CN": "📤 <b>账号检测</b>\n\n请上传包含TData或Session文件的ZIP压缩包...\n\n支持格式:\n• TData文件夹\n• Session文件",
        "en-US": "📤 <b>Account Check</b>\n\nPlease upload ZIP file containing TData or Session files...\n\nSupported formats:\n• TData folders\n• Session files",
        "ru": "📤 <b>Проверка аккаунтов</b>\n\nПожалуйста, загрузите ZIP-файл, содержащий файлы TData или Session...\n\nПоддерживаемые форматы:\n• Папки TData\n• Файлы Session",
        "my": "📤 <b>အကောင့်စစ်ဆေးခြင်း</b>\n\nTData သို့မဟုတ် Session ဖိုင်များပါရှိသော ZIP ဖိုင်ကို တင်ပါ...\n\nပံ့ပိုးထားသော ဖော်မတ်များ:\n• TData ဖိုင်တွဲများ\n• Session ဖိုင်များ",
        "bn": "📤 <b>অ্যাকাউন্ট পরীক্ষা</b>\n\nTData বা Session ফাইল সমন্বিত ZIP ফাইল আপলোড করুন...\n\nসমর্থিত ফরম্যাট:\n• TData ফোল্ডার\n• Session ফাইল",
        "ar": "📤 <b>فحص الحساب</b>\n\nيرجى تحميل ملف ZIP يحتوي على ملفات TData أو Session...\n\nالتنسيقات المدعومة:\n• مجلدات TData\n• ملفات Session",
        "vi": "📤 <b>Kiểm tra tài khoản</b>\n\nVui lòng tải lên tệp ZIP chứa các tệp TData hoặc Session...\n\nĐịnh dạng được hỗ trợ:\n• Thư mục TData\n• Tệp Session"
    },
    "check_processing": {
        "zh-CN": "🔍 正在检测...\n\n处理: {current}/{total}\n✅ 正常: {normal}\n❌ 异常: {abnormal}\n⏱️ 已用时: {elapsed}秒",
        "en-US": "🔍 Checking...\n\nProcessing: {current}/{total}\n✅ Normal: {normal}\n❌ Abnormal: {abnormal}\n⏱️ Elapsed: {elapsed}s",
        "ru": "🔍 Проверка...\n\nОбработка: {current}/{total}\n✅ Нормальные: {normal}\n❌ Аномальные: {abnormal}\n⏱️ Прошло: {elapsed}с",
        "my": "🔍 စစ်ဆေးနေသည်...\n\nလုပ်ဆောင်နေသည်: {current}/{total}\n✅ ပုံမှန်: {normal}\n❌ ပုံမှန်မဟုတ်သော: {abnormal}\n⏱️ ကုန်ဆုံးသွားပြီ: {elapsed}စက္ကန့်",
        "bn": "🔍 পরীক্ষা করা হচ্ছে...\n\nপ্রক্রিয়াকরণ: {current}/{total}\n✅ স্বাভাবিক: {normal}\n❌ অস্বাভাবিক: {abnormal}\n⏱️ অতিবাহিত: {elapsed}সে",
        "ar": "🔍 جارٍ الفحص...\n\nمعالجة: {current}/{total}\n✅ طبيعي: {normal}\n❌ غير طبيعي: {abnormal}\n⏱️ منقضي: {elapsed}ث",
        "vi": "🔍 Đang kiểm tra...\n\nĐang xử lý: {current}/{total}\n✅ Bình thường: {normal}\n❌ Bất thường: {abnormal}\n⏱️ Đã trôi qua: {elapsed}s"
    },
    "check_complete": {
        "zh-CN": "✅ <b>检测完成</b>\n\n📊 总数: {total}\n✅ 正常: {normal}\n❌ 异常: {abnormal}\n⏱️ 总耗时: {duration}秒",
        "en-US": "✅ <b>Check Complete</b>\n\n📊 Total: {total}\n✅ Normal: {normal}\n❌ Abnormal: {abnormal}\n⏱️ Total time: {duration}s",
        "ru": "✅ <b>Проверка завершена</b>\n\n📊 Всего: {total}\n✅ Нормальные: {normal}\n❌ Аномальные: {abnormal}\n⏱️ Общее время: {duration}с",
        "my": "✅ <b>စစ်ဆေးမှု ပြီးစီးပါပြီ</b>\n\n📊 စုစုပေါင်း: {total}\n✅ ပုံမှန်: {normal}\n❌ ပုံမှန်မဟုတ်သော: {abnormal}\n⏱️ စုစုပေါင်းအချိန်: {duration}စက္ကန့်",
        "bn": "✅ <b>পরীক্ষা সম্পন্ন</b>\n\n📊 মোট: {total}\n✅ স্বাভাবিক: {normal}\n❌ অস্বাভাবিক: {abnormal}\n⏱️ মোট সময়: {duration}সে",
        "ar": "✅ <b>اكتمل الفحص</b>\n\n📊 المجموع: {total}\n✅ طبيعي: {normal}\n❌ غير طبيعي: {abnormal}\n⏱️ الوقت الإجمالي: {duration}ث",
        "vi": "✅ <b>Kiểm tra hoàn tất</b>\n\n📊 Tổng: {total}\n✅ Bình thường: {normal}\n❌ Bất thường: {abnormal}\n⏱️ Tổng thời gian: {duration}s"
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
