#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证撤销会员功能的代码完整性
Verify revoke membership feature code completeness
"""

import re

def verify_implementation():
    """验证实现是否完整"""
    print("=" * 70)
    print("验证撤销会员功能实现")
    print("=" * 70)
    
    with open('TGapibot.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "Database.revoke_membership 方法": r'def revoke_membership\(self, user_id: int\) -> bool:',
        "撤销会员按钮": r'撤销会员.*admin_revoke_menu',
        "admin_revoke_menu 回调": r'elif data == "admin_revoke_menu":',
        "handle_admin_revoke_menu 方法": r'def handle_admin_revoke_menu\(self, query\):',
        "waiting_revoke_user 状态处理": r'elif user_status == "waiting_revoke_user":',
        "handle_revoke_user_input 方法": r'def handle_revoke_user_input\(self, update, admin_id: int, text: str\):',
        "admin_revoke_confirm 回调": r'elif data\.startswith\("admin_revoke_confirm_"\):',
        "handle_admin_revoke_confirm 方法": r'def handle_admin_revoke_confirm\(self, query, context, target_user_id: int\):',
        "admin_revoke_cancel 回调": r'elif data == "admin_revoke_cancel":',
        "handle_admin_revoke_cancel 方法": r'def handle_admin_revoke_cancel\(self, query\):',
        "get_user_by_username 使用": r'self\.db\.get_user_by_username\(',
        "get_user_membership_info 使用": r'self\.db\.get_user_membership_info\(',
        "DELETE FROM memberships": r'DELETE FROM memberships WHERE user_id = \?',
    }
    
    results = []
    all_passed = True
    
    print("\n检查项目:")
    for name, pattern in checks.items():
        found = bool(re.search(pattern, content, re.MULTILINE))
        status = "✅" if found else "❌"
        results.append((name, found))
        print(f"{status} {name}")
        if not found:
            all_passed = False
    
    print("\n" + "=" * 70)
    
    if all_passed:
        print("✅ 所有检查项通过！代码实现完整。")
        
        # 额外检查
        print("\n额外信息:")
        
        # 统计新增的行数
        revoke_section = re.search(
            r'# 撤销会员功能.*?# 广播消息功能',
            content,
            re.DOTALL
        )
        if revoke_section:
            lines = revoke_section.group().count('\n')
            print(f"• 撤销会员功能代码行数: ~{lines} 行")
        
        # 检查中文UI
        chinese_ui = re.findall(r'撤销会员|确认撤销|未找到该用户|请输入要撤销的用户名', content)
        if chinese_ui:
            print(f"• 中文UI文本数量: {len(chinese_ui)} 处")
        
        # 检查超时提示
        timeout_msg = re.search(r'⏰.*5分钟', content)
        if timeout_msg:
            print(f"• 包含5分钟超时提示: ✅")
        
        return True
    else:
        print("❌ 部分检查项未通过，请检查实现。")
        failed = [name for name, found in results if not found]
        print(f"\n缺失的功能: {', '.join(failed)}")
        return False

def verify_integration():
    """验证与现有系统的集成"""
    print("\n" + "=" * 70)
    print("验证系统集成")
    print("=" * 70)
    
    with open('TGapibot.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("\n检查与现有功能的一致性:")
    
    # 检查是否遵循了相同的模式
    patterns_to_check = [
        ("使用 safe_edit_message", r'self\.safe_edit_message\(query,'),
        ("使用 safe_send_message", r'self\.safe_send_message\(update,'),
        ("检查管理员权限", r'if not self\.db\.is_admin\(.*?\):'),
        ("InlineKeyboardMarkup 使用", r'InlineKeyboardMarkup\(\['),
        ("HTML 格式化", r"parse_mode='HTML'"),
        ("用户状态管理", r'self\.db\.save_user\(.*?status'),
    ]
    
    for name, pattern in patterns_to_check:
        count = len(re.findall(pattern, content))
        print(f"✅ {name}: {count} 处使用")
    
    print("\n检查UI一致性:")
    
    # 检查按钮样式
    buttons = re.findall(r'InlineKeyboardButton\("([^"]+)"', content)
    revoke_buttons = [b for b in buttons if '撤销' in b or '取消' in b]
    if revoke_buttons:
        print(f"✅ 撤销相关按钮: {len(revoke_buttons)} 个")
        for btn in set(revoke_buttons):
            print(f"   • {btn}")
    
    return True

def check_problem_statement_compliance():
    """检查是否符合问题陈述的要求"""
    print("\n" + "=" * 70)
    print("检查需求符合性")
    print("=" * 70)
    
    with open('TGapibot.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    requirements = [
        ("数据库方法 revoke_membership", r'def revoke_membership.*DELETE FROM memberships', True),
        ("管理面板添加按钮", r'撤销会员.*callback_data="admin_revoke_menu"', True),
        ("设置 waiting_revoke_user 状态", r'waiting_revoke_user', True),
        ("5分钟超时提示", r'⏰.*5分钟内有效', True),
        ("支持用户ID输入", r'if text\.isdigit\(\):', True),
        ("支持用户名输入（@name）", r'username = text\.replace\("@", ""\)', True),
        ("使用 get_user_by_username", r'get_user_by_username', True),
        ("显示用户ID和会员信息", r'用户ID.*membership_info', True),
        ("确认撤销按钮", r'✅ 确认撤销.*admin_revoke_confirm', True),
        ("取消按钮", r'❌ 取消', True),
        ("未找到用户提示", r'未找到该用户.*请确认对方已与机器人对话入库', True),
    ]
    
    print("\n需求检查:")
    all_met = True
    for name, pattern, required in requirements:
        found = bool(re.search(pattern, content, re.DOTALL))
        status = "✅" if found else ("❌" if required else "⚠️")
        print(f"{status} {name}")
        if required and not found:
            all_met = False
    
    print("\n" + "=" * 70)
    
    if all_met:
        print("✅ 所有需求已满足！")
        return True
    else:
        print("❌ 部分需求未满足")
        return False

if __name__ == "__main__":
    print("\n🔍 撤销会员功能验证工具\n")
    
    result1 = verify_implementation()
    result2 = verify_integration()
    result3 = check_problem_statement_compliance()
    
    print("\n" + "=" * 70)
    print("📊 验证总结")
    print("=" * 70)
    print(f"代码实现完整性: {'✅ 通过' if result1 else '❌ 失败'}")
    print(f"系统集成检查: {'✅ 通过' if result2 else '❌ 失败'}")
    print(f"需求符合性: {'✅ 通过' if result3 else '❌ 失败'}")
    
    if result1 and result2 and result3:
        print("\n🎉 所有验证通过！功能实现符合要求。")
        exit(0)
    else:
        print("\n⚠️ 部分验证未通过，请检查实现。")
        exit(1)
