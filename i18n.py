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
            "admin_only": "❌ 仅管理员可访问",
            "admin": "👑 管理员",
            "no_membership": "❌ 无会员",
            "enabled": "🟢启用",
            "local_connection": "🔴本地连接"
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
            "admin_only": "❌ Только для администраторов",
            "admin": "👑 Администратор",
            "no_membership": "❌ Нет подписки",
            "enabled": "🟢включено",
            "local_connection": "🔴Локальное соединение"
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
            "admin_only": "❌ Admin only",
            "admin": "👑 Administrator",
            "no_membership": "❌ No Membership",
            "enabled": "🟢Enabled",
            "local_connection": "🔴Local Connection"
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
    "help": LANGS["zh-CN"]["help"],
    "status": LANGS["zh-CN"]["status"],
    "proxy": LANGS["zh-CN"]["proxy"],
    "common": {
        "success": "✅ အောင်မြင်",
        "failed": "❌ မအောင်မြင်",
        "processing": "🔄 လုပ်ဆောင်နေသည်...",
        "cancel": "❌ ပယ်ဖျက်",
        "confirm": "✅ အတည်ပြု",
        "back": "🔙 ပြန်သွားရန်",
        "next": "➡️ နောက်တစ်ဆင့်",
        "complete": "✅ ပြီးစီး",
        "error": "❌ အမှားအယွင်း",
        "admin_only": "❌ စီမံခန့်ခွဲသူများသာ",
        "admin": "👑 စီမံခန့်ခွဲသူ",
        "no_membership": "❌ အဖွဲ့ဝင်မဟုတ်ပါ",
        "enabled": "🟢ဖွင့်ထားသည်",
        "local_connection": "🔴ဒေသခံချိတ်ဆက်မှု"
    }
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
    "help": LANGS["zh-CN"]["help"],
    "status": LANGS["zh-CN"]["status"],
    "proxy": LANGS["zh-CN"]["proxy"],
    "common": {
        "success": "✅ সফল",
        "failed": "❌ ব্যর্থ",
        "processing": "🔄 প্রক্রিয়াকরণ...",
        "cancel": "❌ বাতিল",
        "confirm": "✅ নিশ্চিত করুন",
        "back": "🔙 ফিরে যান",
        "next": "➡️ পরবর্তী",
        "complete": "✅ সম্পন্ন",
        "error": "❌ ত্রুটি",
        "admin_only": "❌ শুধুমাত্র প্রশাসক",
        "admin": "👑 প্রশাসক",
        "no_membership": "❌ কোন সদস্যপদ নেই",
        "enabled": "🟢সক্রিয়",
        "local_connection": "🔴স্থানীয় সংযোগ"
    }
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
    "help": LANGS["zh-CN"]["help"],
    "status": LANGS["zh-CN"]["status"],
    "proxy": LANGS["zh-CN"]["proxy"],
    "common": {
        "success": "✅ نجح",
        "failed": "❌ فشل",
        "processing": "🔄 المعالجة...",
        "cancel": "❌ إلغاء",
        "confirm": "✅ تأكيد",
        "back": "🔙 رجوع",
        "next": "➡️ التالي",
        "complete": "✅ مكتمل",
        "error": "❌ خطأ",
        "admin_only": "❌ للمسؤولين فقط",
        "admin": "👑 المسؤول",
        "no_membership": "❌ لا عضوية",
        "enabled": "🟢مفعل",
        "local_connection": "🔴اتصال محلي"
    }
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
    "help": LANGS["zh-CN"]["help"],
    "status": LANGS["zh-CN"]["status"],
    "proxy": LANGS["zh-CN"]["proxy"],
    "common": {
        "success": "✅ Thành công",
        "failed": "❌ Thất bại",
        "processing": "🔄 Đang xử lý...",
        "cancel": "❌ Hủy",
        "confirm": "✅ Xác nhận",
        "back": "🔙 Quay lại",
        "next": "➡️ Tiếp theo",
        "complete": "✅ Hoàn tất",
        "error": "❌ Lỗi",
        "admin_only": "❌ Chỉ quản trị viên",
        "admin": "👑 Quản trị viên",
        "no_membership": "❌ Không có thành viên",
        "enabled": "🟢Đã bật",
        "local_connection": "🔴Kết nối cục bộ"
    }
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
    "welcome_message": {
        "zh-CN": "欢迎使用机器人",
        "en-US": "Welcome to the bot",
        "ru": "Добро пожаловать в бот",
        "my": "Bot သို့ကြိုဆိုပါသည်",
        "bn": "বটে স্বাগতম",
        "ar": "مرحبا بك في البوت",
        "vi": "Chào mừng đến với bot"
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
    # Help command specific strings
    "help_main_features": {
        "zh-CN": "主要功能",
        "en-US": "Main Features",
        "ru": "Основные функции",
        "my": "အဓိကအင်္ဂါရပ်များ",
        "bn": "প্রধান বৈশিষ্ট্য",
        "ar": "الميزات الرئيسية",
        "vi": "Tính năng chính"
    },
    "help_feature_1": {
        "zh-CN": "代理连接模式自动检测账号状态",
        "en-US": "Proxy connection mode auto-detects account status",
        "ru": "Режим прокси-соединения автоматически определяет статус аккаунта",
        "my": "Proxy ချိတ်ဆက်မှုမုဒ်သည် အကောင့်အခြေအနေကို အလိုအလျောက် စစ်ဆေးသည်",
        "bn": "প্রক্সি সংযোগ মোড স্বয়ংক্রিয়ভাবে অ্যাকাউন্ট স্থিতি সনাক্ত করে",
        "ar": "وضع اتصال البروكسي يكتشف حالة الحساب تلقائيًا",
        "vi": "Chế độ kết nối proxy tự động phát hiện trạng thái tài khoản"
    },
    "help_feature_2": {
        "zh-CN": "实时进度显示和自动文件发送",
        "en-US": "Real-time progress display and automatic file sending",
        "ru": "Отображение прогресса в реальном времени и автоматическая отправка файлов",
        "my": "အချိန်နှင့်တပြေးညီ တိုးတက်မှုပြသခြင်းနှင့် အလိုအလျောက် ဖိုင်ပေးပို့ခြင်း",
        "bn": "রিয়েল-টাইম অগ্রগতি প্রদর্শন এবং স্বয়ংক্রিয় ফাইল পাঠানো",
        "ar": "عرض التقدم في الوقت الفعلي وإرسال الملفات تلقائيًا",
        "vi": "Hiển thị tiến trình theo thời gian thực và gửi tệp tự động"
    },
    "help_feature_3": {
        "zh-CN": "支持Session和TData格式",
        "en-US": "Supports Session and TData formats",
        "ru": "Поддержка форматов Session и TData",
        "my": "Session နှင့် TData ဖော်မတ်များကို ပံ့ပိုးသည်",
        "bn": "Session এবং TData ফরম্যাট সমর্থন করে",
        "ar": "يدعم تنسيقات Session و TData",
        "vi": "Hỗ trợ định dạng Session và TData"
    },
    "help_supported_formats": {
        "zh-CN": "支持格式",
        "en-US": "Supported Formats",
        "ru": "Поддерживаемые форматы",
        "my": "ပံ့ပိုးထားသော ဖော်မတ်များ",
        "bn": "সমর্থিত ফরম্যাট",
        "ar": "التنسيقات المدعومة",
        "vi": "Định dạng được hỗ trợ"
    },
    "help_files": {
        "zh-CN": "文件",
        "en-US": "files",
        "ru": "файлы",
        "my": "ဖိုင်များ",
        "bn": "ফাইল",
        "ar": "ملفات",
        "vi": "tệp"
    },
    "help_folders": {
        "zh-CN": "文件夹",
        "en-US": "folders",
        "ru": "папки",
        "my": "ဖိုင်တွဲများ",
        "bn": "ফোল্ডার",
        "ar": "مجلدات",
        "vi": "thư mục"
    },
    "help_archives": {
        "zh-CN": "压缩包",
        "en-US": "archives",
        "ru": "архивы",
        "my": "ဖိုင်များ",
        "bn": "সংরক্ষণাগার",
        "ar": "أرشيف",
        "vi": "tệp nén"
    },
    "help_format_conversion": {
        "zh-CN": "格式转换",
        "en-US": "Format Conversion",
        "ru": "Преобразование формата",
        "my": "ဖော်မတ်ပြောင်းခြင်း",
        "bn": "ফরম্যাট রূপান্তর",
        "ar": "تحويل التنسيق",
        "vi": "Chuyển đổi định dạng"
    },
    "help_batch_processing": {
        "zh-CN": "批量并发处理",
        "en-US": "Batch concurrent processing",
        "ru": "Пакетная параллельная обработка",
        "my": "အစုလိုက် တစ်ပြိုင်နက် စီမံဆောင်ရွက်ခြင်း",
        "bn": "ব্যাচ সমান্তরাল প্রক্রিয়াকরণ",
        "ar": "معالجة دفعة متزامنة",
        "vi": "Xử lý đồng thời hàng loạt"
    },
    "help_proxy_features": {
        "zh-CN": "代理功能",
        "en-US": "Proxy Features",
        "ru": "Функции прокси",
        "my": "Proxy လုပ်ဆောင်ချက်များ",
        "bn": "প্রক্সি বৈশিষ্ট্য",
        "ar": "ميزات البروكسي",
        "vi": "Tính năng Proxy"
    },
    "help_proxy_auto_read": {
        "zh-CN": "自动读取proxy.txt文件",
        "en-US": "Auto-read proxy.txt file",
        "ru": "Автоматическое чтение файла proxy.txt",
        "my": "proxy.txt ဖိုင်ကို အလိုအလျောက် ဖတ်ခြင်း",
        "bn": "স্বয়ংক্রিয়ভাবে proxy.txt ফাইল পড়ুন",
        "ar": "قراءة ملف proxy.txt تلقائيًا",
        "vi": "Tự động đọc tệp proxy.txt"
    },
    "help_proxy_support": {
        "zh-CN": "支持HTTP/SOCKS4/SOCKS5代理",
        "en-US": "Supports HTTP/SOCKS4/SOCKS5 proxies",
        "ru": "Поддержка прокси HTTP/SOCKS4/SOCKS5",
        "my": "HTTP/SOCKS4/SOCKS5 proxy များကို ပံ့ပိုးသည်",
        "bn": "HTTP/SOCKS4/SOCKS5 প্রক্সি সমর্থন করে",
        "ar": "يدعم بروكسيات HTTP/SOCKS4/SOCKS5",
        "vi": "Hỗ trợ proxy HTTP/SOCKS4/SOCKS5"
    },
    "help_admin_commands": {
        "zh-CN": "管理员命令",
        "en-US": "Admin Commands",
        "ru": "Команды администратора",
        "my": "စီမံခန့်ခွဲသူ အမိန့်များ",
        "bn": "প্রশাসক কমান্ড",
        "ar": "أوامر المسؤول",
        "vi": "Lệnh quản trị"
    },
    "help_speed_optimization": {
        "zh-CN": "速度优化功能",
        "en-US": "Speed Optimization",
        "ru": "Оптимизация скорости",
        "my": "အမြန်နှုန်းမြှင့်တင်ခြင်း",
        "bn": "গতি অপ্টিমাইজেশন",
        "ar": "تحسين السرعة",
        "vi": "Tối ưu hóa tốc độ"
    },
    "help_username": {
        "zh-CN": "用户名",
        "en-US": "username",
        "ru": "имя пользователя",
        "my": "အသုံးပြုသူအမည်",
        "bn": "ব্যবহারকারীর নাম",
        "ar": "اسم المستخدم",
        "vi": "tên người dùng"
    },
    "help_add_admin": {
        "zh-CN": "添加管理员",
        "en-US": "Add admin",
        "ru": "Добавить администратора",
        "my": "စီမံခန့်ခွဲသူထည့်ရန်",
        "bn": "প্রশাসক যোগ করুন",
        "ar": "إضافة مسؤول",
        "vi": "Thêm quản trị viên"
    },
    "help_remove_admin": {
        "zh-CN": "移除管理员",
        "en-US": "Remove admin",
        "ru": "Удалить администратора",
        "my": "စီမံခန့်ခွဲသူဖယ်ရှားရန်",
        "bn": "প্রশাসক সরান",
        "ar": "إزالة المسؤول",
        "vi": "Xóa quản trị viên"
    },
    "help_list_admins": {
        "zh-CN": "查看管理员列表",
        "en-US": "List admins",
        "ru": "Список администраторов",
        "my": "စီမံခန့်ခွဲသူများစာရင်း",
        "bn": "প্রশাসক তালিকা",
        "ar": "قائمة المسؤولين",
        "vi": "Danh sách quản trị viên"
    },
    "help_proxy_status": {
        "zh-CN": "代理状态管理",
        "en-US": "Proxy status",
        "ru": "Статус прокси",
        "my": "Proxy အခြေအနေ",
        "bn": "প্রক্সি স্থিতি",
        "ar": "حالة البروكسي",
        "vi": "Trạng thái proxy"
    },
    "help_test_proxy": {
        "zh-CN": "测试代理",
        "en-US": "Test proxies",
        "ru": "Тест прокси",
        "my": "Proxy စမ်းသပ်ရန်",
        "bn": "প্রক্সি পরীক্ষা",
        "ar": "اختبار البروكسي",
        "vi": "Kiểm tra proxy"
    },
    "help_clean_proxy": {
        "zh-CN": "清理失效代理",
        "en-US": "Clean invalid proxies",
        "ru": "Очистить неработающие прокси",
        "my": "မမှန်ကန်သော proxy များကို ရှင်းလင်းရန်",
        "bn": "অবৈধ প্রক্সি পরিষ্কার করুন",
        "ar": "تنظيف البروكسيات غير الصالحة",
        "vi": "Dọn proxy không hợp lệ"
    },
    "help_fast_mode": {
        "zh-CN": "快速模式",
        "en-US": "Fast mode",
        "ru": "Быстрый режим",
        "my": "အမြန်မုဒ်",
        "bn": "দ্রুত মোড",
        "ar": "الوضع السريع",
        "vi": "Chế độ nhanh"
    },
    "help_concurrent_checks": {
        "zh-CN": "并发检测",
        "en-US": "Concurrent checks",
        "ru": "Параллельные проверки",
        "my": "တစ်ပြိုင်နက် စစ်ဆေးမှုများ",
        "bn": "সমান্তরাল পরীক্ষা",
        "ar": "الفحوصات المتزامنة",
        "vi": "Kiểm tra đồng thời"
    },
    "help_smart_retry": {
        "zh-CN": "智能重试",
        "en-US": "Smart retry",
        "ru": "Умная повторная попытка",
        "my": "အသိဉာဏ်ရှိသော ပြန်လုပ်ခြင်း",
        "bn": "স্মার্ট পুনঃচেষ্টা",
        "ar": "إعادة محاولة ذكية",
        "vi": "Thử lại thông minh"
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
        "zh-CN": "📖 详细说明",
        "en-US": "📖 Detailed Description",
        "ru": "📖 Подробное описание",
        "my": "📖 အသေးစိတ်ဖော်ပြချက်",
        "bn": "📖 বিস্তারিত বিবরণ",
        "ar": "📖 وصف تفصيلي",
        "vi": "📖 Mô tả chi tiết"
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
    # Admin panel messages
    "admin_panel_title": {
        "zh-CN": "👑 <b>管理员面板</b>",
        "en-US": "👑 <b>Admin Panel</b>",
        "ru": "👑 <b>Панель администратора</b>",
        "my": "👑 <b>စီမံခန့်ခွဲမှု ပြားပြား</b>",
        "bn": "👑 <b>প্রশাসক প্যানেল</b>",
        "ar": "👑 <b>لوحة الإدارة</b>",
        "vi": "👑 <b>Bảng quản trị</b>"
    },
    "admin_only_access": {
        "zh-CN": "❌ 仅管理员可访问",
        "en-US": "❌ Admin access only",
        "ru": "❌ Доступ только для администраторов",
        "my": "❌ စီမံခန့်ခွဲသူများသာ ဝင်ရောက်နိုင်သည်",
        "bn": "❌ শুধুমাত্র প্রশাসক অ্যাক্সেস",
        "ar": "❌ الوصول للمسؤولين فقط",
        "vi": "❌ Chỉ quản trị viên mới truy cập được"
    },
    # VIP messages
    "vip_menu_title": {
        "zh-CN": "💳 <b>会员中心</b>",
        "en-US": "💳 <b>Membership Center</b>",
        "ru": "💳 <b>Центр подписки</b>",
        "my": "💳 <b>အဖွဲ့ဝင်အချက်အလက် စင်တာ</b>",
        "bn": "💳 <b>সদস্যপদ কেন্দ্র</b>",
        "ar": "💳 <b>مركز العضوية</b>",
        "vi": "💳 <b>Trung tâm thành viên</b>"
    },
    # API conversion messages
    "api_conversion_title": {
        "zh-CN": "🔗 <b>API格式转换</b>",
        "en-US": "🔗 <b>API Format Conversion</b>",
        "ru": "🔗 <b>API-конвертация</b>",
        "my": "🔗 <b>API ဖော်မတ်ပြောင်းခြင်း</b>",
        "bn": "🔗 <b>API ফরম্যাট রূপান্তর</b>",
        "ar": "🔗 <b>تحويل تنسيق API</b>",
        "vi": "🔗 <b>Chuyển đổi định dạng API</b>"
    },
    # Broadcast messages
    "broadcast_title": {
        "zh-CN": "📢 <b>群发消息</b>",
        "en-US": "📢 <b>Broadcast Message</b>",
        "ru": "📢 <b>Массовая рассылка</b>",
        "my": "📢 <b>အစုလိုက် မက်ဆေ့ချ်</b>",
        "bn": "📢 <b>ব্রডকাস্ট বার্তা</b>",
        "ar": "📢 <b>رسالة جماعية</b>",
        "vi": "📢 <b>Tin nhắn quảng bá</b>"
    },
    # Classify messages
    "classify_title": {
        "zh-CN": "📦 <b>账号分类</b>",
        "en-US": "📦 <b>Account Classification</b>",
        "ru": "📦 <b>Классификация аккаунтов</b>",
        "my": "📦 <b>အကောင့်ခွဲခြားခြင်း</b>",
        "bn": "📦 <b>অ্যাকাউন্ট শ্রেণীবিভাগ</b>",
        "ar": "📦 <b>تصنيف الحسابات</b>",
        "vi": "📦 <b>Phân loại tài khoản</b>"
    },
    # Rename messages
    "rename_title": {
        "zh-CN": "📝 <b>文件重命名</b>",
        "en-US": "📝 <b>File Rename</b>",
        "ru": "📝 <b>Переименование файлов</b>",
        "my": "📝 <b>ဖိုင်အမည်ပြောင်းခြင်း</b>",
        "bn": "📝 <b>ফাইল পুনঃনামকরণ</b>",
        "ar": "📝 <b>إعادة تسمية الملف</b>",
        "vi": "📝 <b>Đổi tên tệp</b>"
    },
    # Merge messages
    "merge_title": {
        "zh-CN": "🧩 <b>账户合并</b>",
        "en-US": "🧩 <b>Account Merge</b>",
        "ru": "🧩 <b>Объединение аккаунтов</b>",
        "my": "🧩 <b>အကောင့်ပေါင်းခြင်း</b>",
        "bn": "🧩 <b>অ্যাকাউন্ট একত্রিত করুন</b>",
        "ar": "🧩 <b>دمج الحسابات</b>",
        "vi": "🧩 <b>Hợp nhất tài khoản</b>"
    },
    # 2FA messages
    "twofa_title": {
        "zh-CN": "🔐 <b>修改2FA</b>",
        "en-US": "🔐 <b>Change 2FA</b>",
        "ru": "🔐 <b>Изменить 2FA</b>",
        "my": "🔐 <b>2FA ပြောင်းခြင်း</b>",
        "bn": "🔐 <b>2FA পরিবর্তন করুন</b>",
        "ar": "🔐 <b>تغيير 2FA</b>",
        "vi": "🔐 <b>Thay đổi 2FA</b>"
    },
    # Anti-recovery messages
    "antirecover_title": {
        "zh-CN": "🛡️ <b>防止找回</b>",
        "en-US": "🛡️ <b>Anti-recovery</b>",
        "ru": "🛡️ <b>Защита от восстановления</b>",
        "my": "🛡️ <b>ပြန်လည်ရယူခြင်းကာကွယ်</b>",
        "bn": "🛡️ <b>পুনরুদ্ধার প্রতিরোধ</b>",
        "ar": "🛡️ <b>منع الاسترداد</b>",
        "vi": "🛡️ <b>Chống khôi phục</b>"
    },
    # File upload prompts
    "upload_file_prompt": {
        "zh-CN": "📤 请上传文件...",
        "en-US": "📤 Please upload file...",
        "ru": "📤 Пожалуйста, загрузите файл...",
        "my": "📤 ဖိုင်ကို တင်ပါ...",
        "bn": "📤 ফাইল আপলোড করুন...",
        "ar": "📤 يرجى تحميل الملف...",
        "vi": "📤 Vui lòng tải lên tệp..."
    },
    # Processing messages
    "processing_wait": {
        "zh-CN": "🔄 处理中，请稍候...",
        "en-US": "🔄 Processing, please wait...",
        "ru": "🔄 Обработка, пожалуйста, подождите...",
        "my": "🔄 လုပ်ဆောင်နေသည်၊ ခဏစောင့်ပါ...",
        "bn": "🔄 প্রক্রিয়াকরণ, অনুগ্রহ করে অপেক্ষা করুন...",
        "ar": "🔄 المعالجة، يرجى الانتظار...",
        "vi": "🔄 Đang xử lý, vui lòng đợi..."
    },
    # File operations
    "file_received": {
        "zh-CN": "✅ 文件已接收",
        "en-US": "✅ File received",
        "ru": "✅ Файл получен",
        "my": "✅ ဖိုင်ရရှိပြီးပါပြီ",
        "bn": "✅ ফাইল গৃহীত হয়েছে",
        "ar": "✅ تم استلام الملف",
        "vi": "✅ Đã nhận tệp"
    },
    "file_processing": {
        "zh-CN": "🔄 正在处理文件...",
        "en-US": "🔄 Processing file...",
        "ru": "🔄 Обработка файла...",
        "my": "🔄 ဖိုင်ကို လုပ်ဆောင်နေသည်...",
        "bn": "🔄 ফাইল প্রক্রিয়াকরণ করা হচ্ছে...",
        "ar": "🔄 معالجة الملف...",
        "vi": "🔄 Đang xử lý tệp..."
    },
    # API conversion messages (expanded)
    "api_feature_unavailable": {
        "zh-CN": "❌ API转换功能不可用\n\n原因: Flask库未安装\n💡 请安装: pip install flask jinja2",
        "en-US": "❌ API conversion feature unavailable\n\nReason: Flask library not installed\n💡 Please install: pip install flask jinja2",
        "ru": "❌ Функция API-конвертации недоступна\n\nПричина: Библиотека Flask не установлена\n💡 Пожалуйста, установите: pip install flask jinja2",
        "my": "❌ API ပြောင်းလဲမှု လုပ်ဆောင်ချက် မရရှိနိုင်ပါ\n\nအကြောင်းအရင်း: Flask library မတင်ထားပါ\n💡 ကျေးဇူးပြု၍ တင်ပါ: pip install flask jinja2",
        "bn": "❌ API রূপান্তর বৈশিষ্ট্য উপলব্ধ নয়\n\nকারণ: Flask লাইব্রেরি ইনস্টল করা নেই\n💡 অনুগ্রহ করে ইনস্টল করুন: pip install flask jinja2",
        "ar": "❌ ميزة تحويل API غير متاحة\n\nالسبب: مكتبة Flask غير مثبتة\n💡 يرجى التثبيت: pip install flask jinja2",
        "vi": "❌ Tính năng chuyển đổi API không khả dụng\n\nLý do: Thư viện Flask chưa được cài đặt\n💡 Vui lòng cài đặt: pip install flask jinja2"
    },
    "api_function_description": {
        "zh-CN": "🔗 <b>API格式转换功能</b>\n\n<b>📱 功能说明</b>\n• 将TData/Session转换为API格式\n• 生成专属验证码接收链接\n• 自动提取手机号和2FA密码\n• 实时转发短信验证码",
        "en-US": "🔗 <b>API Format Conversion</b>\n\n<b>📱 Feature Description</b>\n• Convert TData/Session to API format\n• Generate dedicated verification code link\n• Auto-extract phone number and 2FA password\n• Real-time SMS verification forwarding",
        "ru": "🔗 <b>API-конвертация</b>\n\n<b>📱 Описание функции</b>\n• Преобразование TData/Session в формат API\n• Генерация специальной ссылки для получения кода\n• Автоматическое извлечение номера телефона и 2FA пароля\n• Пересылка SMS кодов в реальном времени",
        "my": "🔗 <b>API ဖော်မတ်ပြောင်းခြင်း</b>\n\n<b>📱 လုပ်ဆောင်ချက် ဖော်ပြချက်</b>\n• TData/Session ကို API ဖော်မတ်သို့ ပြောင်းခြင်း\n• အထူး အတည်ပြုကုဒ် လင့်ခ် ဖန်တီးခြင်း\n• ဖုန်းနံပါတ်နှင့် 2FA စကားဝှက်ကို အလိုအလျောက် ထုတ်ယူခြင်း\n• SMS အတည်ပြုကုဒ်များကို အချိန်နှင့်တပြေးညီ ပေးပို့ခြင်း",
        "bn": "🔗 <b>API ফরম্যাট রূপান্তর</b>\n\n<b>📱 বৈশিষ্ট্যের বিবরণ</b>\n• TData/Session কে API ফরম্যাটে রূপান্তর করুন\n• ডেডিকেটেড ভেরিফিকেশন কোড লিংক তৈরি করুন\n• ফোন নম্বর এবং 2FA পাসওয়ার্ড স্বয়ংক্রিয়ভাবে এক্সট্র্যাক্ট করুন\n• রিয়েল-টাইম SMS ভেরিফিকেশন ফরওয়ার্ডিং",
        "ar": "🔗 <b>تحويل تنسيق API</b>\n\n<b>📱 وصف الميزة</b>\n• تحويل TData/Session إلى تنسيق API\n• إنشاء رابط رمز التحقق المخصص\n• استخراج رقم الهاتف وكلمة مرور 2FA تلقائيًا\n• إعادة توجيه رمز التحقق عبر الرسائل القصيرة في الوقت الفعلي",
        "vi": "🔗 <b>Chuyển đổi định dạng API</b>\n\n<b>📱 Mô tả tính năng</b>\n• Chuyển đổi TData/Session sang định dạng API\n• Tạo liên kết mã xác minh chuyên dụng\n• Tự động trích xuất số điện thoại và mật khẩu 2FA\n• Chuyển tiếp mã xác minh SMS theo thời gian thực"
    },
    # Admin panel messages (expanded)
    "admin_stats_title": {
        "zh-CN": "📊 <b>统计数据</b>",
        "en-US": "📊 <b>Statistics</b>",
        "ru": "📊 <b>Статистика</b>",
        "my": "📊 <b>စာရင်းအင်းများ</b>",
        "bn": "📊 <b>পরিসংখ্যান</b>",
        "ar": "📊 <b>الإحصائيات</b>",
        "vi": "📊 <b>Thống kê</b>"
    },
    "admin_user_management": {
        "zh-CN": "👥 用户管理",
        "en-US": "👥 User Management",
        "ru": "👥 Управление пользователями",
        "my": "👥 အသုံးပြုသူ စီမံခန့်ခွဲမှု",
        "bn": "👥 ব্যবহারকারী ব্যবস্থাপনা",
        "ar": "👥 إدارة المستخدمين",
        "vi": "👥 Quản lý người dùng"
    },
    "admin_broadcast": {
        "zh-CN": "📢 群发消息",
        "en-US": "📢 Broadcast",
        "ru": "📢 Массовая рассылка",
        "my": "📢 အစုလိုက်မက်ဆေ့ချ်",
        "bn": "📢 ব্রডকাস্ট",
        "ar": "📢 البث",
        "vi": "📢 Quảng bá"
    },
    "admin_code_management": {
        "zh-CN": "🎫 兑换码管理",
        "en-US": "🎫 Redeem Code Management",
        "ru": "🎫 Управление кодами",
        "my": "🎫 Redeem ကုဒ် စီမံခန့်ခွဲမှု",
        "bn": "🎫 রিডিম কোড ব্যবস্থাপনা",
        "ar": "🎫 إدارة رموز الاسترداد",
        "vi": "🎫 Quản lý mã đổi thưởng"
    },
    "admin_add_success": {
        "zh-CN": "✅ 成功添加管理员: {username} (ID: {user_id})",
        "en-US": "✅ Successfully added admin: {username} (ID: {user_id})",
        "ru": "✅ Успешно добавлен администратор: {username} (ID: {user_id})",
        "my": "✅ စီမံခန့်ခွဲသူ အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ: {username} (ID: {user_id})",
        "bn": "✅ সফলভাবে প্রশাসক যোগ করা হয়েছে: {username} (ID: {user_id})",
        "ar": "✅ تمت إضافة المسؤول بنجاح: {username} (ID: {user_id})",
        "vi": "✅ Đã thêm quản trị viên thành công: {username} (ID: {user_id})"
    },
    "admin_remove_success": {
        "zh-CN": "✅ 已移除管理员: {user_id}",
        "en-US": "✅ Removed admin: {user_id}",
        "ru": "✅ Администратор удален: {user_id}",
        "my": "✅ စီမံခန့်ခွဲသူကို ဖယ်ရှားပြီးပါပြီ: {user_id}",
        "bn": "✅ প্রশাসক সরানো হয়েছে: {user_id}",
        "ar": "✅ تمت إزالة المسؤول: {user_id}",
        "vi": "✅ Đã xóa quản trị viên: {user_id}"
    },
    "admin_already_admin": {
        "zh-CN": "⚠️ 用户 {user_id} 已经是管理员",
        "en-US": "⚠️ User {user_id} is already an admin",
        "ru": "⚠️ Пользователь {user_id} уже является администратором",
        "my": "⚠️ အသုံးပြုသူ {user_id} သည် စီမံခန့်ခွဲသူ ဖြစ်နေပြီးဖြစ်သည်",
        "bn": "⚠️ ব্যবহারকারী {user_id} ইতিমধ্যে একজন প্রশাসক",
        "ar": "⚠️ المستخدم {user_id} مسؤول بالفعل",
        "vi": "⚠️ Người dùng {user_id} đã là quản trị viên"
    },
    "admin_not_admin": {
        "zh-CN": "⚠️ 用户 {user_id} 不是管理员",
        "en-US": "⚠️ User {user_id} is not an admin",
        "ru": "⚠️ Пользователь {user_id} не является администратором",
        "my": "⚠️ အသုံးပြုသူ {user_id} သည် စီမံခန့်ခွဲသူ မဟုတ်ပါ",
        "bn": "⚠️ ব্যবহারকারী {user_id} একজন প্রশাসক নয়",
        "ar": "⚠️ المستخدم {user_id} ليس مسؤولاً",
        "vi": "⚠️ Người dùng {user_id} không phải quản trị viên"
    },
    "admin_user_not_found": {
        "zh-CN": "❌ 找不到用户名 @{username}\n请确保用户已使用过机器人",
        "en-US": "❌ Username @{username} not found\nPlease ensure the user has used the bot",
        "ru": "❌ Имя пользователя @{username} не найдено\nПожалуйста, убедитесь, что пользователь использовал бота",
        "my": "❌ အသုံးပြုသူအမည် @{username} ကို ရှာမတွေ့ပါ\nအသုံးပြုသူသည် bot ကို အသုံးပြုခဲ့ကြောင်း သေချာပါစေ",
        "bn": "❌ ব্যবহারকারীর নাম @{username} পাওয়া যায়নি\nঅনুগ্রহ করে নিশ্চিত করুন যে ব্যবহারকারী বট ব্যবহার করেছেন",
        "ar": "❌ لم يتم العثور على اسم المستخدم @{username}\nيرجى التأكد من أن المستخدم قد استخدم البوت",
        "vi": "❌ Không tìm thấy tên người dùng @{username}\nVui lòng đảm bảo người dùng đã sử dụng bot"
    },
    "admin_cannot_remove_config": {
        "zh-CN": "❌ 无法移除配置文件中的管理员",
        "en-US": "❌ Cannot remove admin from config file",
        "ru": "❌ Невозможно удалить администратора из файла конфигурации",
        "my": "❌ config ဖိုင်ထဲမှ စီမံခန့်ခွဲသူကို ဖယ်ရှားလို့ မရပါ",
        "bn": "❌ কনফিগ ফাইল থেকে প্রশাসক সরানো যাবে না",
        "ar": "❌ لا يمكن إزالة المسؤول من ملف التكوين",
        "vi": "❌ Không thể xóa quản trị viên khỏi tệp cấu hình"
    },
    "admin_cannot_remove_self": {
        "zh-CN": "❌ 无法移除自己的管理员权限",
        "en-US": "❌ Cannot remove your own admin privileges",
        "ru": "❌ Невозможно удалить собственные права администратора",
        "my": "❌ သင့်ကိုယ်ပိုင် စီမံခန့်ခွဲမှု အခွင့်အရေးများကို ဖယ်ရှားလို့ မရပါ",
        "bn": "❌ আপনার নিজের প্রশাসক সুবিধা সরাতে পারবেন না",
        "ar": "❌ لا يمكنك إزالة امتيازات المسؤول الخاصة بك",
        "vi": "❌ Không thể xóa quyền quản trị viên của chính bạn"
    },
    "admin_list_empty": {
        "zh-CN": "📝 暂无管理员",
        "en-US": "📝 No admins yet",
        "ru": "📝 Администраторов пока нет",
        "my": "📝 စီမံခန့်ခွဲသူများ မရှိသေးပါ",
        "bn": "📝 এখনও কোন প্রশাসক নেই",
        "ar": "📝 لا يوجد مسؤولون بعد",
        "vi": "📝 Chưa có quản trị viên"
    },
    # Convert feature messages
    "convert_feature_unavailable": {
        "zh-CN": "❌ 格式转换功能不可用\n\n原因: opentele库未安装\n💡 请安装: pip install opentele",
        "en-US": "❌ Format conversion feature unavailable\n\nReason: opentele library not installed\n💡 Please install: pip install opentele",
        "ru": "❌ Функция преобразования формата недоступна\n\nПричина: Библиотека opentele не установлена\n💡 Пожалуйста, установите: pip install opentele",
        "my": "❌ ဖော်မတ်ပြောင်းလဲမှု လုပ်ဆောင်ချက် မရရှိနိုင်ပါ\n\nအကြောင်းအရင်း: opentele library မတင်ထားပါ\n💡 ကျေးဇူးပြု၍ တင်ပါ: pip install opentele",
        "bn": "❌ ফরম্যাট রূপান্তর বৈশিষ্ট্য উপলব্ধ নয়\n\nকারণ: opentele লাইব্রেরি ইনস্টল করা নেই\n💡 অনুগ্রহ করে ইনস্টল করুন: pip install opentele",
        "ar": "❌ ميزة تحويل التنسيق غير متاحة\n\nالسبب: مكتبة opentele غير مثبتة\n💡 يرجى التثبيت: pip install opentele",
        "vi": "❌ Tính năng chuyển đổi định dạng không khả dụng\n\nLý do: Thư viện opentele chưa được cài đặt\n💡 Vui lòng cài đặt: pip install opentele"
    },
    "convert_supported_conversions": {
        "zh-CN": "支持的转换",
        "en-US": "Supported Conversions",
        "ru": "Поддерживаемые преобразования",
        "my": "ပံ့ပိုးထားသော ပြောင်းလဲမှုများ",
        "bn": "সমর্থিত রূপান্তর",
        "ar": "التحويلات المدعومة",
        "vi": "Chuyển đổi được hỗ trợ"
    },
    "convert_tdata_to_session_desc": {
        "zh-CN": "将Telegram Desktop的tdata格式转换为Session格式",
        "en-US": "Convert Telegram Desktop tdata format to Session format",
        "ru": "Преобразование формата tdata Telegram Desktop в формат Session",
        "my": "Telegram Desktop ၏ tdata ဖော်မတ်ကို Session ဖော်မတ်သို့ ပြောင်းပါ",
        "bn": "Telegram Desktop এর tdata ফরম্যাটকে Session ফরম্যাটে রূপান্তর করুন",
        "ar": "تحويل تنسيق tdata من Telegram Desktop إلى تنسيق Session",
        "vi": "Chuyển đổi định dạng tdata của Telegram Desktop sang định dạng Session"
    },
    "convert_session_to_tdata_desc": {
        "zh-CN": "将Session格式转换为Telegram Desktop的tdata格式",
        "en-US": "Convert Session format to Telegram Desktop tdata format",
        "ru": "Преобразование формата Session в формат tdata Telegram Desktop",
        "my": "Session ဖော်မတ်ကို Telegram Desktop ၏ tdata ဖော်မတ်သို့ ပြောင်းပါ",
        "bn": "Session ফরম্যাটকে Telegram Desktop এর tdata ফরম্যাটে রূপান্তর করুন",
        "ar": "تحويل تنسيق Session إلى تنسيق tdata من Telegram Desktop",
        "vi": "Chuyển đổi định dạng Session sang định dạng tdata của Telegram Desktop"
    },
    "convert_features_title": {
        "zh-CN": "功能特点",
        "en-US": "Features",
        "ru": "Особенности",
        "my": "အင်္ဂါရပ်များ",
        "bn": "বৈশিষ্ট্য",
        "ar": "الميزات",
        "vi": "Tính năng"
    },
    "convert_batch_concurrent": {
        "zh-CN": "批量并发转换，提高效率",
        "en-US": "Batch concurrent conversion for efficiency",
        "ru": "Пакетное параллельное преобразование для эффективности",
        "my": "စွမ်းဆောင်ရည်မြှင့်တင်ရန် အစုစုပေါင်းပြောင်းလဲမှု",
        "bn": "দক্ষতার জন্য ব্যাচ সমান্তরাল রূপান্তর",
        "ar": "تحويل دفعة متزامن للكفاءة",
        "vi": "Chuyển đổi đồng thời hàng loạt để nâng cao hiệu quả"
    },
    "convert_realtime_progress": {
        "zh-CN": "实时进度显示",
        "en-US": "Real-time progress display",
        "ru": "Отображение прогресса в реальном времени",
        "my": "အချိန်နှင့်တပြေးညီ တိုးတက်မှု ပြသခြင်း",
        "bn": "রিয়েল-টাইম অগ্রগতি প্রদর্শন",
        "ar": "عرض التقدم في الوقت الفعلي",
        "vi": "Hiển thị tiến trình theo thời gian thực"
    },
    "convert_instructions": {
        "zh-CN": "操作说明",
        "en-US": "Instructions",
        "ru": "Инструкции",
        "my": "လမ်းညွှန်ချက်များ",
        "bn": "নির্দেশাবলী",
        "ar": "التعليمات",
        "vi": "Hướng dẫn"
    },
    # Error messages
    "error_generic": {
        "zh-CN": "❌ 发生错误: {error}",
        "en-US": "❌ Error occurred: {error}",
        "ru": "❌ Произошла ошибка: {error}",
        "my": "❌ အမှားအယွင်း ဖြစ်ပွားခဲ့သည်: {error}",
        "bn": "❌ ত্রুটি ঘটেছে: {error}",
        "ar": "❌ حدث خطأ: {error}",
        "vi": "❌ Đã xảy ra lỗi: {error}"
    },
    "error_operation_failed": {
        "zh-CN": "❌ 操作失败",
        "en-US": "❌ Operation failed",
        "ru": "❌ Операция не удалась",
        "my": "❌ လုပ်ဆောင်မှု မအောင်မြင်ပါ",
        "bn": "❌ অপারেশন ব্যর্থ হয়েছে",
        "ar": "❌ فشلت العملية",
        "vi": "❌ Thao tác thất bại"
    },
    "error_add_admin_failed": {
        "zh-CN": "❌ 添加管理员失败",
        "en-US": "❌ Failed to add admin",
        "ru": "❌ Не удалось добавить администратора",
        "my": "❌ စီမံခန့်ခွဲသူ ထည့်ရန် မအောင်မြင်ပါ",
        "bn": "❌ প্রশাসক যোগ করতে ব্যর্থ হয়েছে",
        "ar": "❌ فشل في إضافة المسؤول",
        "vi": "❌ Không thể thêm quản trị viên"
    },
    "error_remove_admin_failed": {
        "zh-CN": "❌ 移除管理员失败",
        "en-US": "❌ Failed to remove admin",
        "ru": "❌ Не удалось удалить администратора",
        "my": "❌ စီမံခန့်ခွဲသူကို ဖယ်ရှားရန် မအောင်မြင်ပါ",
        "bn": "❌ প্রশাসক সরাতে ব্যর্থ হয়েছে",
        "ar": "❌ فشل في إزالة المسؤول",
        "vi": "❌ Không thể xóa quản trị viên"
    },
    "error_invalid_user_id": {
        "zh-CN": "❌ 请提供有效的用户ID",
        "en-US": "❌ Please provide a valid user ID",
        "ru": "❌ Пожалуйста, укажите действительный ID пользователя",
        "my": "❌ ကျေးဇူးပြု၍ တရားဝင် အသုံးပြုသူ ID တစ်ခု ပေးပါ",
        "bn": "❌ অনুগ্রহ করে একটি বৈধ ব্যবহারকারী ID প্রদান করুন",
        "ar": "❌ يرجى تقديم معرف مستخدم صالح",
        "vi": "❌ Vui lòng cung cấp ID người dùng hợp lệ"
    },
    # Proxy reload message
    "proxy_reload_count": {
        "zh-CN": "✅ 已重新加载代理文件\n📡 新代理数量: {count}个",
        "en-US": "✅ Proxy file reloaded\n📡 New proxy count: {count}",
        "ru": "✅ Файл прокси перезагружен\n📡 Новое количество прокси: {count}",
        "my": "✅ Proxy ဖိုင်ကို ပြန်လည်တင်ပြီးပါပြီ\n📡 Proxy အသစ် အရေအတွက်: {count}",
        "bn": "✅ প্রক্সি ফাইল পুনরায় লোড হয়েছে\n📡 নতুন প্রক্সি সংখ্যা: {count}",
        "ar": "✅ تم إعادة تحميل ملف البروكسي\n📡 عدد البروكسي الجديد: {count}",
        "vi": "✅ Đã tải lại tệp proxy\n📡 Số lượng proxy mới: {count}"
    },
    "proxy_test_failed": {
        "zh-CN": "❌ 代理测试失败: {error}",
        "en-US": "❌ Proxy test failed: {error}",
        "ru": "❌ Тест прокси не удался: {error}",
        "my": "❌ Proxy စမ်းသပ်မှု မအောင်မြင်ပါ: {error}",
        "bn": "❌ প্রক্সি পরীক্ষা ব্যর্থ হয়েছে: {error}",
        "ar": "❌ فشل اختبار البروكسي: {error}",
        "vi": "❌ Kiểm tra proxy thất bại: {error}"
    },
    "proxy_cleanup_cancelled": {
        "zh-CN": "❌ 代理清理已取消",
        "en-US": "❌ Proxy cleanup cancelled",
        "ru": "❌ Очистка прокси отменена",
        "my": "❌ Proxy ရှင်းလင်းမှုကို ပယ်ဖျက်လိုက်ပါပြီ",
        "bn": "❌ প্রক্সি পরিষ্কার বাতিল করা হয়েছে",
        "ar": "❌ تم إلغاء تنظيف البروكسي",
        "vi": "❌ Đã hủy dọn dẹp proxy"
    },
    "proxy_cleanup_failed": {
        "zh-CN": "❌ 代理清理过程失败: {error}",
        "en-US": "❌ Proxy cleanup process failed: {error}",
        "ru": "❌ Процесс очистки прокси не удался: {error}",
        "my": "❌ Proxy ရှင်းလင်းမှု လုပ်ငန်းစဉ် မအောင်မြင်ပါ: {error}",
        "bn": "❌ প্রক্সি পরিষ্কার প্রক্রিয়া ব্যর্থ হয়েছে: {error}",
        "ar": "❌ فشلت عملية تنظيف البروكسي: {error}",
        "vi": "❌ Quá trình dọn dẹp proxy thất bại: {error}"
    },
    "get_test_proxy_failed": {
        "zh-CN": "❌ 获取测试代理失败",
        "en-US": "❌ Failed to get test proxy",
        "ru": "❌ Не удалось получить тестовый прокси",
        "my": "❌ စမ်းသပ်မည့် proxy ရရန် မအောင်မြင်ပါ",
        "bn": "❌ টেস্ট প্রক্সি পেতে ব্যর্থ হয়েছে",
        "ar": "❌ فشل في الحصول على بروكسي الاختبار",
        "vi": "❌ Không thể lấy proxy thử nghiệm"
    },
    # API function detailed description
    "api_function_details": {
        "zh-CN": """🔗 <b>API格式转换功能</b>

<b>📱 功能说明</b>
• 将TData/Session转换为API格式
• 生成专属验证码接收链接
• 自动提取手机号和2FA密码
• 实时转发短信验证码

<b>📋 输出格式</b>
• JSON格式（开发者友好）
• CSV格式（Excel可打开）
• TXT格式（便于查看）

<b>🌐 验证码接收</b>
• 每个账号生成独立网页链接
• 自动刷新显示最新验证码
• 5分钟自动过期保护

<b>📤 操作说明</b>
请上传包含TData或Session文件的ZIP压缩包...""",
        "en-US": """🔗 <b>API Format Conversion</b>

<b>📱 Feature Description</b>
• Convert TData/Session to API format
• Generate dedicated verification code link
• Auto-extract phone number and 2FA password
• Real-time SMS verification forwarding

<b>📋 Output Format</b>
• JSON format (developer-friendly)
• CSV format (Excel compatible)
• TXT format (easy to view)

<b>🌐 Verification Code Reception</b>
• Independent web link for each account
• Auto-refresh to show latest code
• 5-minute auto-expiration protection

<b>📤 Instructions</b>
Please upload ZIP file containing TData or Session files...""",
        "ru": """🔗 <b>API-конвертация</b>

<b>📱 Описание функции</b>
• Преобразование TData/Session в формат API
• Генерация специальной ссылки для получения кода
• Автоматическое извлечение номера телефона и 2FA пароля
• Пересылка SMS кодов в реальном времени

<b>📋 Формат вывода</b>
• Формат JSON (удобен для разработчиков)
• Формат CSV (совместим с Excel)
• Формат TXT (легко просматривать)

<b>🌐 Прием кода верификации</b>
• Независимая веб-ссылка для каждого аккаунта
• Автообновление для отображения последнего кода
• Защита с автоматическим истечением через 5 минут

<b>📤 Инструкции</b>
Пожалуйста, загрузите ZIP-файл, содержащий файлы TData или Session...""",
        "my": """🔗 <b>API ဖော်မတ်ပြောင်းခြင်း</b>

<b>📱 လုပ်ဆောင်ချက် ဖော်ပြချက်</b>
• TData/Session ကို API ဖော်မတ်သို့ ပြောင်းခြင်း
• အထူး အတည်ပြုကုဒ် လင့်ခ် ဖန်တီးခြင်း
• ဖုန်းနံပါတ်နှင့် 2FA စကားဝှက်ကို အလိုအလျောက် ထုတ်ယူခြင်း
• SMS အတည်ပြုကုဒ်များကို အချိန်နှင့်တပြေးညီ ပေးပို့ခြင်း

<b>📋 ထွက်ရှိမည့်ဖော်မတ်</b>
• JSON ဖော်မတ် (developer-friendly)
• CSV ဖော်မတ် (Excel compatible)
• TXT ဖော်မတ် (လွယ်ကူစွာကြည့်ရှုနိုင်)

<b>🌐 အတည်ပြုကုဒ် လက်ခံခြင်း</b>
• အကောင့်တစ်ခုစီအတွက် သီးခြား web link
• နောက်ဆုံးကုဒ်ကို ပြသရန် အလိုအလျောက် refresh
• 5 မိနစ် အလိုအလျောက် သက်တမ်းကုန်ဆုံးခြင်း ကာကွယ်မှု

<b>📤 ညွှန်ကြားချက်များ</b>
TData သို့မဟုတ် Session ဖိုင်များပါရှိသော ZIP ဖိုင်ကို တင်ပါ...""",
        "bn": """🔗 <b>API ফরম্যাট রূপান্তর</b>

<b>📱 বৈশিষ্ট্যের বিবরণ</b>
• TData/Session কে API ফরম্যাটে রূপান্তর করুন
• ডেডিকেটেড ভেরিফিকেশন কোড লিংক তৈরি করুন
• ফোন নম্বর এবং 2FA পাসওয়ার্ড স্বয়ংক্রিয়ভাবে এক্সট্র্যাক্ট করুন
• রিয়েল-টাইম SMS ভেরিফিকেশন ফরওয়ার্ডিং

<b>📋 আউটপুট ফরম্যাট</b>
• JSON ফরম্যাট (ডেভেলপার-বান্ধব)
• CSV ফরম্যাট (Excel সামঞ্জস্যপূর্ণ)
• TXT ফরম্যাট (দেখতে সহজ)

<b>🌐 ভেরিফিকেশন কোড রিসেপশন</b>
• প্রতিটি অ্যাকাউন্টের জন্য স্বতন্ত্র ওয়েব লিংক
• সর্বশেষ কোড দেখাতে অটো-রিফ্রেশ
• 5-মিনিট অটো-মেয়াদ শেষ সুরক্ষা

<b>📤 নির্দেশাবলী</b>
TData বা Session ফাইল সমন্বিত ZIP ফাইল আপলোড করুন...""",
        "ar": """🔗 <b>تحويل تنسيق API</b>

<b>📱 وصف الميزة</b>
• تحويل TData/Session إلى تنسيق API
• إنشاء رابط رمز التحقق المخصص
• استخراج رقم الهاتف وكلمة مرور 2FA تلقائيًا
• إعادة توجيه رمز التحقق عبر الرسائل القصيرة في الوقت الفعلي

<b>📋 تنسيق الإخراج</b>
• تنسيق JSON (سهل للمطورين)
• تنسيق CSV (متوافق مع Excel)
• تنسيق TXT (سهل العرض)

<b>🌐 استقبال رمز التحقق</b>
• رابط ويب مستقل لكل حساب
• التحديث التلقائي لإظهار أحدث رمز
• حماية انتهاء صلاحية تلقائية لمدة 5 دقائق

<b>📤 التعليمات</b>
يرجى تحميل ملف ZIP يحتوي على ملفات TData أو Session...""",
        "vi": """🔗 <b>Chuyển đổi định dạng API</b>

<b>📱 Mô tả tính năng</b>
• Chuyển đổi TData/Session sang định dạng API
• Tạo liên kết mã xác minh chuyên dụng
• Tự động trích xuất số điện thoại và mật khẩu 2FA
• Chuyển tiếp mã xác minh SMS theo thời gian thực

<b>📋 Định dạng đầu ra</b>
• Định dạng JSON (thân thiện với nhà phát triển)
• Định dạng CSV (tương thích Excel)
• Định dạng TXT (dễ xem)

<b>🌐 Nhận mã xác minh</b>
• Liên kết web độc lập cho mỗi tài khoản
• Tự động làm mới để hiển thị mã mới nhất
• Bảo vệ hết hạn tự động sau 5 phút

<b>📤 Hướng dẫn</b>
Vui lòng tải lên tệp ZIP chứa các tệp TData hoặc Session..."""
    },
    "back_to_main_menu": {
        "zh-CN": "🔙 返回主菜单",
        "en-US": "🔙 Back to Main Menu",
        "ru": "🔙 Назад в главное меню",
        "my": "🔙 ပင်မမီနူးသို့ ပြန်သွားရန်",
        "bn": "🔙 প্রধান মেনুতে ফিরে যান",
        "ar": "🔙 العودة إلى القائمة الرئيسية",
        "vi": "🔙 Quay lại menu chính"
    },
    # Admin command usage messages
    "addadmin_usage": {
        "zh-CN": "📝 使用方法:\n/addadmin [用户ID或@用户名]\n\n示例:\n/addadmin 123456789\n/addadmin @username",
        "en-US": "📝 Usage:\n/addadmin [UserID or @username]\n\nExample:\n/addadmin 123456789\n/addadmin @username",
        "ru": "📝 Использование:\n/addadmin [ID пользователя или @имя]\n\nПример:\n/addadmin 123456789\n/addadmin @username",
        "my": "📝 အသုံးပြုနည်း:\n/addadmin [UserID သို့မဟုတ် @အမည်]\n\nဥပမာ:\n/addadmin 123456789\n/addadmin @username",
        "bn": "📝 ব্যবহার:\n/addadmin [UserID বা @username]\n\nউদাহরণ:\n/addadmin 123456789\n/addadmin @username",
        "ar": "📝 الاستخدام:\n/addadmin [معرف المستخدم أو @اسم المستخدم]\n\nمثال:\n/addadmin 123456789\n/addadmin @username",
        "vi": "📝 Cách sử dụng:\n/addadmin [UserID hoặc @username]\n\nVí dụ:\n/addadmin 123456789\n/addadmin @username"
    },
    "removeadmin_usage": {
        "zh-CN": "📝 使用方法:\n/removeadmin [用户ID]\n\n示例:\n/removeadmin 123456789",
        "en-US": "📝 Usage:\n/removeadmin [UserID]\n\nExample:\n/removeadmin 123456789",
        "ru": "📝 Использование:\n/removeadmin [ID пользователя]\n\nПример:\n/removeadmin 123456789",
        "my": "📝 အသုံးပြုနည်း:\n/removeadmin [UserID]\n\nဥပမာ:\n/removeadmin 123456789",
        "bn": "📝 ব্যবহার:\n/removeadmin [UserID]\n\nউদাহরণ:\n/removeadmin 123456789",
        "ar": "📝 الاستخدام:\n/removeadmin [معرف المستخدم]\n\nمثال:\n/removeadmin 123456789",
        "vi": "📝 Cách sử dụng:\n/removeadmin [UserID]\n\nVí dụ:\n/removeadmin 123456789"
    },
    "admin_add_details": {
        "zh-CN": "✅ 成功添加管理员\n\n👤 用户ID: {user_id}\n📝 用户名: @{username}\n🏷️ 昵称: {first_name}\n⏰ 添加时间: {time}",
        "en-US": "✅ Successfully added admin\n\n👤 User ID: {user_id}\n📝 Username: @{username}\n🏷️ Nickname: {first_name}\n⏰ Added: {time}",
        "ru": "✅ Администратор успешно добавлен\n\n👤 ID пользователя: {user_id}\n📝 Имя: @{username}\n🏷️ Никнейм: {first_name}\n⏰ Добавлен: {time}",
        "my": "✅ စီမံခန့်ခွဲသူ အောင်မြင်စွာ ထည့်သွင်းပြီးပါပြီ\n\n👤 အသုံးပြုသူ ID: {user_id}\n📝 အမည်: @{username}\n🏷️ ဆိုင်းဘုတ်: {first_name}\n⏰ ထည့်သွင်းသည့်အချိန်: {time}",
        "bn": "✅ সফলভাবে প্রশাসক যোগ করা হয়েছে\n\n👤 ব্যবহারকারী ID: {user_id}\n📝 ব্যবহারকারীর নাম: @{username}\n🏷️ ডাকনাম: {first_name}\n⏰ যোগ করা হয়েছে: {time}",
        "ar": "✅ تمت إضافة المسؤول بنجاح\n\n👤 معرف المستخدم: {user_id}\n📝 اسم المستخدم: @{username}\n🏷️ اللقب: {first_name}\n⏰ تمت الإضافة: {time}",
        "vi": "✅ Đã thêm quản trị viên thành công\n\n👤 ID người dùng: {user_id}\n📝 Tên người dùng: @{username}\n🏷️ Biệt danh: {first_name}\n⏰ Đã thêm: {time}"
    },
    "admin_list_title": {
        "zh-CN": "<b>👑 管理员列表</b>\n\n",
        "en-US": "<b>👑 Admin List</b>\n\n",
        "ru": "<b>👑 Список администраторов</b>\n\n",
        "my": "<b>👑 စီမံခန့်ခွဲသူ စာရင်း</b>\n\n",
        "bn": "<b>👑 প্রশাসক তালিকা</b>\n\n",
        "ar": "<b>👑 قائمة المسؤولين</b>\n\n",
        "vi": "<b>👑 Danh sách quản trị viên</b>\n\n"
    },
    "admin_list_total": {
        "zh-CN": "<b>📊 总计: {count} 个管理员</b>",
        "en-US": "<b>📊 Total: {count} admins</b>",
        "ru": "<b>📊 Всего: {count} администраторов</b>",
        "my": "<b>📊 စုစုပေါင်း: {count} စီမံခန့်ခွဲသူ</b>",
        "bn": "<b>📊 মোট: {count} প্রশাসক</b>",
        "ar": "<b>📊 المجموع: {count} مسؤول</b>",
        "vi": "<b>📊 Tổng: {count} quản trị viên</b>"
    },
    # Proxy command messages  
    "proxy_panel_title": {
        "zh-CN": "<b>📡 代理管理面板</b>",
        "en-US": "<b>📡 Proxy Management Panel</b>",
        "ru": "<b>📡 Панель управления прокси</b>",
        "my": "<b>📡 Proxy စီမံခန့်ခွဲမှု ပြားပြား</b>",
        "bn": "<b>📡 প্রক্সি ম্যানেজমেন্ট প্যানেল</b>",
        "ar": "<b>📡 لوحة إدارة البروكسي</b>",
        "vi": "<b>📡 Bảng điều khiển quản lý Proxy</b>"
    },
    "proxy_current_status_section": {
        "zh-CN": "<b>📊 当前状态</b>",
        "en-US": "<b>📊 Current Status</b>",
        "ru": "<b>📊 Текущий статус</b>",
        "my": "<b>📊 လက်ရှိအခြေအနေ</b>",
        "bn": "<b>📊 বর্তমান অবস্থা</b>",
        "ar": "<b>📊 الحالة الحالية</b>",
        "vi": "<b>📊 Trạng thái hiện tại</b>"
    },
    "proxy_format_support_section": {
        "zh-CN": "<b>📝 代理格式支持</b>",
        "en-US": "<b>📝 Proxy Format Support</b>",
        "ru": "<b>📝 Поддерживаемые форматы прокси</b>",
        "my": "<b>📝 Proxy ဖော်မတ် ပံ့ပိုးမှု</b>",
        "bn": "<b>📝 প্রক্সি ফরম্যাট সাপোর্ট</b>",
        "ar": "<b>📝 دعم تنسيق البروكسي</b>",
        "vi": "<b>📝 Hỗ trợ định dạng Proxy</b>"
    },
    "proxy_no_available": {
        "zh-CN": "❌ 没有可用的代理",
        "en-US": "❌ No proxies available",
        "ru": "❌ Нет доступных прокси",
        "my": "❌ အသုံးပြုနိုင်သော proxy များ မရှိပါ",
        "bn": "❌ কোন প্রক্সি উপলব্ধ নেই",
        "ar": "❌ لا توجد بروكسيات متاحة",
        "vi": "❌ Không có proxy nào khả dụng"
    },
    "proxy_no_test": {
        "zh-CN": "❌ 没有可用的代理进行测试",
        "en-US": "❌ No proxies available for testing",
        "ru": "❌ Нет доступных прокси для тестирования",
        "my": "❌ စမ်းသပ်ရန်အတွက် အသုံးပြုနိုင်သော proxy များ မရှိပါ",
        "bn": "❌ পরীক্ষার জন্য কোন প্রক্সি উপলব্ধ নেই",
        "ar": "❌ لا توجد بروكسيات متاحة للاختبار",
        "vi": "❌ Không có proxy nào để kiểm tra"
    },
    "proxy_no_cleanup": {
        "zh-CN": "❌ 没有可用的代理进行清理",
        "en-US": "❌ No proxies available for cleanup",
        "ru": "❌ Нет доступных прокси для очистки",
        "my": "❌ ရှင်းလင်းရန်အတွက် အသုံးပြုနိုင်သော proxy များ မရှိပါ",
        "bn": "❌ পরিষ্কারের জন্য কোন প্রক্সি উপলব্ধ নেই",
        "ar": "❌ لا توجد بروكسيات متاحة للتنظيف",
        "vi": "❌ Không có proxy nào để dọn dẹp"
    },
    "proxy_testing_progress": {
        "zh-CN": "🧪 <b>代理测试中...</b>\n\n📊 正在初始化测试环境...",
        "en-US": "🧪 <b>Testing Proxies...</b>\n\n📊 Initializing test environment...",
        "ru": "🧪 <b>Тестирование прокси...</b>\n\n📊 Инициализация тестовой среды...",
        "my": "🧪 <b>Proxy များကို စမ်းသပ်နေသည်...</b>\n\n📊 စမ်းသပ်မှု ပတ်ဝန်းကျင်ကို စတင်နေသည်...",
        "bn": "🧪 <b>প্রক্সি পরীক্ষা করা হচ্ছে...</b>\n\n📊 টেস্ট পরিবেশ শুরু করা হচ্ছে...",
        "ar": "🧪 <b>اختبار البروكسيات...</b>\n\n📊 تهيئة بيئة الاختبار...",
        "vi": "🧪 <b>Đang kiểm tra Proxy...</b>\n\n📊 Đang khởi tạo môi trường kiểm tra..."
    },
    "proxy_testing_in_progress": {
        "zh-CN": "🧪 <b>代理测试进行中...</b>\n\n📊 已测试: {tested}/{total}\n✅ 可用: {working}\n❌ 失败: {failed}",
        "en-US": "🧪 <b>Proxy Test In Progress...</b>\n\n📊 Tested: {tested}/{total}\n✅ Working: {working}\n❌ Failed: {failed}",
        "ru": "🧪 <b>Тест прокси в процессе...</b>\n\n📊 Протестировано: {tested}/{total}\n✅ Работает: {working}\n❌ Не работает: {failed}",
        "my": "🧪 <b>Proxy စမ်းသပ်မှု လုပ်ဆောင်နေသည်...</b>\n\n📊 စမ်းသပ်ပြီး: {tested}/{total}\n✅ အလုပ်လုပ်သည်: {working}\n❌ မအောင်မြင်ပါ: {failed}",
        "bn": "🧪 <b>প্রক্সি পরীক্ষা চলছে...</b>\n\n📊 পরীক্ষিত: {tested}/{total}\n✅ কাজ করছে: {working}\n❌ ব্যর্থ: {failed}",
        "ar": "🧪 <b>اختبار البروكسي قيد التقدم...</b>\n\n📊 تم الاختبار: {tested}/{total}\n✅ يعمل: {working}\n❌ فشل: {failed}",
        "vi": "🧪 <b>Đang kiểm tra Proxy...</b>\n\n📊 Đã kiểm tra: {tested}/{total}\n✅ Hoạt động: {working}\n❌ Thất bại: {failed}"
    },
    "proxy_testing_complete": {
        "zh-CN": "✅ <b>代理测试完成！</b>\n\n📊 总数: {total}\n✅ 可用: {working}\n❌ 失败: {failed}\n⏱️ 耗时: {duration}秒",
        "en-US": "✅ <b>Proxy Test Complete!</b>\n\n📊 Total: {total}\n✅ Working: {working}\n❌ Failed: {failed}\n⏱️ Duration: {duration}s",
        "ru": "✅ <b>Тест прокси завершен!</b>\n\n📊 Всего: {total}\n✅ Работает: {working}\n❌ Не работает: {failed}\n⏱️ Время: {duration}с",
        "my": "✅ <b>Proxy စမ်းသပ်မှု ပြီးစီးပါပြီ!</b>\n\n📊 စုစုပေါင်း: {total}\n✅ အလုပ်လုပ်သည်: {working}\n❌ မအောင်မြင်ပါ: {failed}\n⏱️ ကြာချိန်: {duration}စက္ကန့်",
        "bn": "✅ <b>প্রক্সি পরীক্ষা সম্পন্ন!</b>\n\n📊 মোট: {total}\n✅ কাজ করছে: {working}\n❌ ব্যর্থ: {failed}\n⏱️ সময়: {duration}সে",
        "ar": "✅ <b>اكتمل اختبار البروكسي!</b>\n\n📊 المجموع: {total}\n✅ يعمل: {working}\n❌ فشل: {failed}\n⏱️ المدة: {duration}ث",
        "vi": "✅ <b>Kiểm tra Proxy hoàn tất!</b>\n\n📊 Tổng: {total}\n✅ Hoạt động: {working}\n❌ Thất bại: {failed}\n⏱️ Thời gian: {duration}s"
    },
    "proxy_cleanup_confirm_title": {
        "zh-CN": "⚠️ <b>代理清理确认</b>",
        "en-US": "⚠️ <b>Proxy Cleanup Confirmation</b>",
        "ru": "⚠️ <b>Подтверждение очистки прокси</b>",
        "my": "⚠️ <b>Proxy ရှင်းလင်းမှု အတည်ပြုချက်</b>",
        "bn": "⚠️ <b>প্রক্সি পরিষ্কারের নিশ্চিতকরণ</b>",
        "ar": "⚠️ <b>تأكيد تنظيف البروكسي</b>",
        "vi": "⚠️ <b>Xác nhận dọn dẹp Proxy</b>"
    },
    "proxy_detailed_status_title": {
        "zh-CN": "<b>📡 代理详细状态</b>\n\n",
        "en-US": "<b>📡 Detailed Proxy Status</b>\n\n",
        "ru": "<b>📡 Подробный статус прокси</b>\n\n",
        "my": "<b>📡 Proxy အသေးစိတ်အခြေအနေ</b>\n\n",
        "bn": "<b>📡 বিস্তারিত প্রক্সি স্ট্যাটাস</b>\n\n",
        "ar": "<b>📡 حالة البروكسي التفصيلية</b>\n\n",
        "vi": "<b>📡 Trạng thái Proxy chi tiết</b>\n\n"
    },
    "proxy_more_proxies": {
        "zh-CN": "\n... 还有 {count} 个代理",
        "en-US": "\n... and {count} more proxies",
        "ru": "\n... и еще {count} прокси",
        "my": "\n... နောက်ထပ် {count} ခု ရှိသေးသည်",
        "bn": "\n... এবং আরও {count} প্রক্সি",
        "ar": "\n... و {count} بروكسي آخر",
        "vi": "\n... và {count} proxy khác"
    },
    "proxy_switch_status_section": {
        "zh-CN": "\n\n<b>📊 代理开关状态</b>\n",
        "en-US": "\n\n<b>📊 Proxy Switch Status</b>\n",
        "ru": "\n\n<b>📊 Статус переключателя прокси</b>\n",
        "my": "\n\n<b>📊 Proxy ခလုတ်အခြေအနေ</b>\n",
        "bn": "\n\n<b>📊 প্রক্সি সুইচ স্ট্যাটাস</b>\n",
        "ar": "\n\n<b>📊 حالة مفتاح البروكسي</b>\n",
        "vi": "\n\n<b>📊 Trạng thái chuyển đổi Proxy</b>\n"
    },
    "proxy_status_current": {
        "zh-CN": "• 当前状态: {status}\n",
        "en-US": "• Current Status: {status}\n",
        "ru": "• Текущий статус: {status}\n",
        "my": "• လက်ရှိအခြေအနေ: {status}\n",
        "bn": "• বর্তমান অবস্থা: {status}\n",
        "ar": "• الحالة الحالية: {status}\n",
        "vi": "• Trạng thái hiện tại: {status}\n"
    },
    "proxy_status_update_time": {
        "zh-CN": "• 更新时间: {time}\n",
        "en-US": "• Updated: {time}\n",
        "ru": "• Обновлено: {time}\n",
        "my": "• ပြင်ဆင်သည့်အချိန်: {time}\n",
        "bn": "• আপডেট করা হয়েছে: {time}\n",
        "ar": "• تم التحديث: {time}\n",
        "vi": "• Đã cập nhật: {time}\n"
    },
    "proxy_status_operator": {
        "zh-CN": "• 操作人员: {user}\n",
        "en-US": "• Operator: {user}\n",
        "ru": "• Оператор: {user}\n",
        "my": "• စစ်ဆေးသူ: {user}\n",
        "bn": "• অপারেটর: {user}\n",
        "ar": "• المشغل: {user}\n",
        "vi": "• Người vận hành: {user}\n"
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
        "zh": "zh-CN", "cn": "zh-CN", "ru-RU": "ru", "my-MM": "my", "mm": "my",
        "bn-BD": "bn", "ar-SA": "ar", "vi-VN": "vi", "en": "en-US", "us": "en-US", "en-us": "en-US"
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


def get_text(lang_code: str, *keys, default: str = "", **kwargs) -> str:
    """
    Get translated text with hierarchical key support and fallback.
    
    Supports multiple calling patterns:
    1. get_text(lang_code, "key_name")  - Direct TEXTS lookup
    2. get_text(lang_code, "status", "title")  - Hierarchical LANGS lookup
    3. get_text(lang_code, "status.title")  - Dot-notation path
    
    Args:
        lang_code: Language code (e.g., "zh-CN", "en-US", "ru")
        *keys: One or more keys to navigate the translation dictionaries
        default: Default text if translation not found
        **kwargs: Format parameters for string formatting
    
    Returns:
        Translated and formatted string
    
    Examples:
        get_text("en-US", "welcome_message")
        get_text("ru", "status", "title")
        get_text("zh-CN", "proxy", "enabled", count=5)
    """
    lang_code = normalize_lang(lang_code)
    
    if not keys:
        return default
    
    # Handle single dot-notation key
    if len(keys) == 1 and "." in str(keys[0]):
        keys = tuple(str(keys[0]).split("."))
    
    # Try TEXTS dictionary first (flat structure)
    if len(keys) == 1:
        key = keys[0]
        if key in TEXTS:
            text_dict = TEXTS[key]
            if isinstance(text_dict, dict):
                text = text_dict.get(lang_code) or text_dict.get(DEFAULT_LANG) or default
            else:
                text = str(text_dict) if text_dict else default
        else:
            # Try LANGS as fallback
            text = _get_from_langs(lang_code, keys, default)
    else:
        # Multiple keys - navigate LANGS hierarchy
        text = _get_from_langs(lang_code, keys, default)
    
    # Apply formatting if kwargs provided
    if kwargs and text:
        try:
            return text.format(**kwargs)
        except (KeyError, ValueError):
            # If formatting fails, return unformatted text
            return text
    return text or default


def _get_from_langs(lang_code: str, keys: tuple, default: str = "") -> str:
    """Helper function to navigate LANGS hierarchy"""
    try:
        # Try user's language first
        data = LANGS[lang_code]
        for key in keys:
            if isinstance(data, dict):
                data = data[key]
            else:
                raise KeyError
        return str(data) if data else default
    except (KeyError, TypeError):
        # Fallback to default language
        try:
            data = LANGS[DEFAULT_LANG]
            for key in keys:
                if isinstance(data, dict):
                    data = data[key]
                else:
                    raise KeyError
            return str(data) if data else default
        except (KeyError, TypeError):
            # Return default if all else fails
            return default


# Alias for convenience
tr = get_text


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
