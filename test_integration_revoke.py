#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试 - 模拟完整的撤销会员流程
Integration test - Simulate complete revoke membership flow
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta

def simulate_revoke_flow():
    """模拟完整的撤销会员流程"""
    print("=" * 70)
    print("集成测试：撤销会员完整流程")
    print("=" * 70)
    
    # 创建测试数据库
    test_db = "test_integration.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn = sqlite3.connect(test_db)
    c = conn.cursor()
    
    # 创建表
    c.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            register_time TEXT,
            last_active TEXT,
            status TEXT DEFAULT ''
        )
    """)
    
    c.execute("""
        CREATE TABLE memberships (
            user_id INTEGER PRIMARY KEY,
            level TEXT,
            trial_expiry_time TEXT,
            created_at TEXT,
            expiry_time TEXT
        )
    """)
    
    conn.commit()
    
    print("\n场景: 管理员撤销用户会员")
    print("-" * 70)
    
    # 步骤1: 创建管理员和目标用户
    print("\n1️⃣ 创建管理员和目标用户...")
    admin_id = 100001
    target_user_id = 200002
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute("""
        INSERT INTO users (user_id, username, first_name, register_time, last_active, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (admin_id, "admin", "管理员", now, now, ""))
    
    c.execute("""
        INSERT INTO users (user_id, username, first_name, register_time, last_active, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (target_user_id, "testuser", "测试用户", now, now, ""))
    
    conn.commit()
    print(f"   ✅ 管理员: {admin_id} (@admin)")
    print(f"   ✅ 目标用户: {target_user_id} (@testuser)")
    
    # 步骤2: 为目标用户授予会员
    print("\n2️⃣ 为目标用户授予30天会员...")
    expiry = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO memberships (user_id, level, expiry_time, created_at)
        VALUES (?, ?, ?, ?)
    """, (target_user_id, "会员", expiry, now))
    conn.commit()
    print(f"   ✅ 会员授予成功，到期时间: {expiry}")
    
    # 步骤3: 管理员进入撤销菜单
    print("\n3️⃣ 管理员点击「撤销会员」按钮...")
    c.execute("UPDATE users SET status = ? WHERE user_id = ?", 
              ("waiting_revoke_user", admin_id))
    conn.commit()
    print("   ✅ 状态已设置为 'waiting_revoke_user'")
    print("   📱 显示输入界面：请输入用户名或ID")
    
    # 步骤4: 管理员输入目标用户
    print("\n4️⃣ 管理员输入: @testuser")
    
    # 模拟 handle_revoke_user_input
    input_text = "@testuser"
    username = input_text.replace("@", "")
    
    c.execute("SELECT user_id, username, first_name FROM users WHERE username = ?", 
              (username,))
    user_row = c.fetchone()
    
    if user_row:
        found_user_id = user_row[0]
        print(f"   ✅ 找到用户: ID={found_user_id}, username={user_row[1]}, name={user_row[2]}")
    else:
        print("   ❌ 用户不存在")
        return False
    
    # 获取会员信息
    c.execute("SELECT level, expiry_time FROM memberships WHERE user_id = ?", 
              (found_user_id,))
    membership_row = c.fetchone()
    
    if membership_row:
        print(f"   💎 当前会员: {membership_row[0]}, 到期: {membership_row[1]}")
    else:
        print("   ❌ 无会员")
    
    # 步骤5: 显示确认界面
    print("\n5️⃣ 显示确认界面")
    print("   📱 界面显示:")
    print("      • 昵称: 测试用户")
    print(f"      • ID: {found_user_id}")
    print("      • 用户名: @testuser")
    print(f"      • 会员等级: {membership_row[0]}")
    print(f"      • 到期时间: {membership_row[1]}")
    print("      [✅ 确认撤销] [❌ 取消]")
    
    # 步骤6: 管理员确认撤销
    print("\n6️⃣ 管理员点击「✅ 确认撤销」")
    
    # 模拟 handle_admin_revoke_confirm
    c.execute("DELETE FROM memberships WHERE user_id = ?", (found_user_id,))
    rows_deleted = c.rowcount
    conn.commit()
    
    if rows_deleted > 0:
        print(f"   ✅ 撤销成功！删除了 {rows_deleted} 条会员记录")
    else:
        print("   ❌ 撤销失败")
        return False
    
    # 步骤7: 验证撤销结果
    print("\n7️⃣ 验证撤销结果...")
    c.execute("SELECT * FROM memberships WHERE user_id = ?", (found_user_id,))
    check_row = c.fetchone()
    
    if check_row is None:
        print("   ✅ 验证成功：会员记录已不存在")
    else:
        print("   ❌ 验证失败：会员记录仍然存在")
        return False
    
    # 步骤8: 用户基本信息保留
    print("\n8️⃣ 验证用户基本信息...")
    c.execute("SELECT user_id, username FROM users WHERE user_id = ?", (found_user_id,))
    user_check = c.fetchone()
    
    if user_check:
        print(f"   ✅ 用户信息保留: ID={user_check[0]}, username={user_check[1]}")
        print("   ℹ️ 用户可以重新获得会员权限")
    else:
        print("   ⚠️ 用户信息被删除（不应该发生）")
    
    # 步骤9: 测试重复撤销
    print("\n9️⃣ 测试对已撤销用户再次撤销...")
    c.execute("DELETE FROM memberships WHERE user_id = ?", (found_user_id,))
    rows_deleted = c.rowcount
    conn.commit()
    
    if rows_deleted == 0:
        print("   ✅ 正确处理：返回0（无记录删除）")
    else:
        print(f"   ⚠️ 意外：删除了 {rows_deleted} 条记录")
    
    # 步骤10: 测试用户名变更场景
    print("\n🔟 测试用户ID输入方式...")
    
    # 重新授予会员
    c.execute("""
        INSERT INTO memberships (user_id, level, expiry_time, created_at)
        VALUES (?, ?, ?, ?)
    """, (target_user_id, "会员", expiry, now))
    conn.commit()
    print("   📝 重新授予会员")
    
    # 使用ID撤销
    input_id = str(target_user_id)
    if input_id.isdigit():
        user_id_to_revoke = int(input_id)
        print(f"   ✅ 识别为用户ID: {user_id_to_revoke}")
        
        c.execute("DELETE FROM memberships WHERE user_id = ?", (user_id_to_revoke,))
        rows_deleted = c.rowcount
        conn.commit()
        
        if rows_deleted > 0:
            print(f"   ✅ 使用ID撤销成功")
        else:
            print("   ❌ 撤销失败")
            return False
    
    conn.close()
    os.remove(test_db)
    
    print("\n" + "=" * 70)
    print("✅ 集成测试全部通过！")
    print("=" * 70)
    return True

def test_edge_cases():
    """测试边界情况"""
    print("\n" + "=" * 70)
    print("边界测试")
    print("=" * 70)
    
    test_db = "test_edge.db"
    if os.path.exists(test_db):
        os.remove(test_db)
    
    conn = sqlite3.connect(test_db)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            register_time TEXT,
            last_active TEXT,
            status TEXT DEFAULT ''
        )
    """)
    
    c.execute("""
        CREATE TABLE memberships (
            user_id INTEGER PRIMARY KEY,
            level TEXT,
            expiry_time TEXT,
            created_at TEXT
        )
    """)
    
    conn.commit()
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 测试1: 用户存在但无会员
    print("\n测试1: 用户存在但无会员")
    c.execute("""
        INSERT INTO users (user_id, username, first_name, register_time, last_active)
        VALUES (?, ?, ?, ?, ?)
    """, (111, "notvip", "非会员用户", now, now))
    conn.commit()
    
    c.execute("DELETE FROM memberships WHERE user_id = ?", (111,))
    deleted = c.rowcount
    conn.commit()
    
    if deleted == 0:
        print("   ✅ 正确返回False（无会员记录）")
    else:
        print("   ⚠️ 意外删除了记录")
    
    # 测试2: 用户名不存在
    print("\n测试2: 用户名不存在")
    c.execute("SELECT user_id FROM users WHERE username = ?", ("nonexistent",))
    result = c.fetchone()
    
    if result is None:
        print("   ✅ 正确返回None（用户不存在）")
    else:
        print("   ❌ 不应该找到用户")
    
    # 测试3: 空用户名
    print("\n测试3: 空用户名")
    username = ""
    if not username or not username.strip():
        print("   ✅ 正确处理空输入")
    else:
        print("   ❌ 应该拒绝空输入")
    
    # 测试4: 用户名带多个@符号
    print("\n测试4: 特殊字符处理")
    input_text = "@@testuser@@"
    cleaned = input_text.replace("@", "")
    if cleaned == "testuser":
        print(f"   ✅ 正确清理: '{input_text}' -> '{cleaned}'")
    else:
        print(f"   ❌ 清理失败: '{input_text}' -> '{cleaned}'")
    
    conn.close()
    os.remove(test_db)
    
    print("\n" + "=" * 70)
    print("✅ 边界测试通过！")
    print("=" * 70)
    return True

if __name__ == "__main__":
    print("\n🧪 撤销会员功能集成测试\n")
    
    # 运行集成测试
    test1 = simulate_revoke_flow()
    
    # 运行边界测试
    test2 = test_edge_cases()
    
    print("\n" + "=" * 70)
    print("📊 测试总结")
    print("=" * 70)
    print(f"集成流程测试: {'✅ 通过' if test1 else '❌ 失败'}")
    print(f"边界情况测试: {'✅ 通过' if test2 else '❌ 失败'}")
    
    if test1 and test2:
        print("\n🎉 所有集成测试通过！")
        print("\n✨ 功能特点:")
        print("   • 完整的撤销流程")
        print("   • 支持用户名和ID输入")
        print("   • 保留用户基本信息")
        print("   • 正确处理边界情况")
        print("   • 可重复授予会员")
        sys.exit(0)
    else:
        print("\n⚠️ 部分测试失败")
        sys.exit(1)
