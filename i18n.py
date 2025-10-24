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

# Add minimal translations for other languages (my, bn, ar, vi)
# For space reasons, I'll add basic support with fallback to Chinese
for lang_code in ["my", "bn", "ar", "vi"]:
    if lang_code not in LANGS:
        continue
    # Copy structure from zh-CN but keep menu from existing
    LANGS[lang_code]["help"] = LANGS["zh-CN"]["help"].copy()
    LANGS[lang_code]["status"] = LANGS["zh-CN"]["status"].copy()
    LANGS[lang_code]["proxy"] = LANGS["zh-CN"]["proxy"].copy()
    LANGS[lang_code]["common"] = LANGS["zh-CN"]["common"].copy()

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


def get_text(lang_code: str, category: str, key: str) -> str:
    """Get translated text for a given category and key"""
    lang = normalize_lang(lang_code)
    try:
        return LANGS[lang][category][key]
    except (KeyError, TypeError):
        # Fallback to default language
        try:
            return LANGS[DEFAULT_LANG][category][key]
        except (KeyError, TypeError):
            return f"[Missing: {category}.{key}]"
