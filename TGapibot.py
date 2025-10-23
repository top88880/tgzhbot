#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram账号检测机器人 - V8.0
群发通知完整版
"""

# 放在所有 import 附近（顶层，只执行一次）
import os
try:
    from dotenv import load_dotenv, find_dotenv  # pip install python-dotenv
    _ENV_FILE = os.getenv("ENV_FILE") or find_dotenv(".env", usecwd=True)
    load_dotenv(_ENV_FILE, override=True)  # override=True 覆盖系统进程里已有的同名键
    print(f"✅ .env loaded: {_ENV_FILE or 'None'}")
except Exception as e:
    print(f"⚠️ dotenv not used: {e}")
import sys
import sqlite3
import logging
import asyncio
import tempfile
import shutil
import zipfile
import json
import random
import string
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from io import BytesIO
import threading
import struct
import base64
from pathlib import Path
print("🔍 Telegram账号检测机器人 V8.0")
print(f"📅 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ================================
# 环境变量加载
# ================================

def load_environment():
    """加载.env文件"""
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

load_environment()

# ================================
# 必要库导入
# ================================

try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, InputFile
    from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
    from telegram.error import RetryAfter, TimedOut, NetworkError, BadRequest
    print("✅ telegram库导入成功")
except ImportError as e:
    print(f"❌ telegram库导入失败: {e}")
    print("💡 请安装: pip install python-telegram-bot==13.15")
    sys.exit(1)

try:
    from telethon import TelegramClient, functions
    from telethon.errors import *
    from telethon.tl.functions.messages import SendMessageRequest, GetHistoryRequest
    TELETHON_AVAILABLE = True
    print("✅ telethon库导入成功")
except ImportError:
    print("❌ telethon未安装")
    print("💡 请安装: pip install telethon")
    TELETHON_AVAILABLE = False

try:
    import socks
    PROXY_SUPPORT = True
    print("✅ 代理支持库导入成功")
except ImportError:
    print("⚠️ 代理支持库未安装，将使用基础代理功能")
    PROXY_SUPPORT = False

try:
    from opentele.api import API, UseCurrentSession
    from opentele.td import TDesktop
    from opentele.tl import TelegramClient as OpenTeleClient
    OPENTELE_AVAILABLE = True
    print("✅ opentele库导入成功")
except ImportError:
    print("⚠️ opentele未安装，格式转换功能不可用")
    print("💡 请安装: pip install opentele")
    OPENTELE_AVAILABLE = False

try:
    from account_classifier import AccountClassifier
    CLASSIFY_AVAILABLE = True
    print("✅ 账号分类模块导入成功")
except Exception as e:
    CLASSIFY_AVAILABLE = False
    print(f"⚠️ 账号分类模块不可用: {e}")

try:
    import phonenumbers
    print("✅ phonenumbers 导入成功")
except Exception:
    print("⚠️ 未安装 phonenumbers（账号国家识别将不可用）")
# Flask相关导入（新增或确认存在）
try:
    from flask import Flask, jsonify, request, render_template_string
    FLASK_AVAILABLE = True
    print("✅ Flask库导入成功")
except ImportError:
    FLASK_AVAILABLE = False
    print("❌ Flask未安装（验证码网页功能不可用）")
# ================================
# 代理管理器
# ================================

class ProxyManager:
    """代理管理器"""
    
    def __init__(self, proxy_file: str = "proxy.txt"):
        self.proxy_file = proxy_file
        self.proxies = []
        self.current_index = 0
        self.load_proxies()
    
    def is_proxy_mode_active(self, db: 'Database') -> bool:
        """判断代理模式是否真正启用（USE_PROXY=true 且存在有效代理 且数据库开关启用）"""
        try:
            proxy_enabled = db.get_proxy_enabled()
            has_valid_proxies = len(self.proxies) > 0
            return config.USE_PROXY and proxy_enabled and has_valid_proxies
        except:
            return config.USE_PROXY and len(self.proxies) > 0
    
    def load_proxies(self):
        """加载代理列表"""
        if not os.path.exists(self.proxy_file):
            print(f"⚠️ 代理文件不存在: {self.proxy_file}")
            print(f"💡 创建示例代理文件...")
            self.create_example_proxy_file()
            return
        
        try:
            with open(self.proxy_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self.proxies = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    proxy_info = self.parse_proxy_line(line)
                    if proxy_info:
                        self.proxies.append(proxy_info)
            
            print(f"📡 加载了 {len(self.proxies)} 个代理")
            
        except Exception as e:
            print(f"❌ 加载代理文件失败: {e}")
    
    def create_example_proxy_file(self):
        """创建示例代理文件"""
        example_content = """# 代理文件示例 - proxy.txt
# 支持的格式：
# HTTP代理：ip:port
# HTTP认证：ip:port:username:password
# SOCKS5：socks5:ip:port:username:password
# SOCKS4：socks4:ip:port
# ABCProxy住宅代理：host:port:username:password

# 示例（请替换为真实代理）
# 127.0.0.1:8080
# 127.0.0.1:1080:user:pass
# socks5:127.0.0.1:1080:user:pass
# socks4:127.0.0.1:1080

# ABCProxy住宅代理示例：
# f01a4db3d3952561.abcproxy.vip:4950:FlBaKtPm7l-zone-abc:00937128

# 注意：
# - 以#开头的行为注释行，会被忽略
# - 住宅代理（如ABCProxy）会自动使用更长的超时时间（30秒）
# - 系统会自动检测住宅代理并优化连接参数
"""
        try:
            with open(self.proxy_file, 'w', encoding='utf-8') as f:
                f.write(example_content)
            print(f"✅ 已创建示例代理文件: {self.proxy_file}")
        except Exception as e:
            print(f"❌ 创建示例代理文件失败: {e}")
    
    def is_residential_proxy(self, host: str) -> bool:
        """检测是否为住宅代理"""
        host_lower = host.lower()
        for pattern in config.RESIDENTIAL_PROXY_PATTERNS:
            if pattern.strip().lower() in host_lower:
                return True
        return False
    
    def parse_proxy_line(self, line: str) -> Optional[Dict]:
        """解析代理行（支持ABCProxy等住宅代理格式）"""
        try:
            parts = line.split(':')
            if len(parts) == 2:
                # ip:port
                host = parts[0].strip()
                return {
                    'type': 'http',
                    'host': host,
                    'port': int(parts[1].strip()),
                    'username': None,
                    'password': None,
                    'is_residential': self.is_residential_proxy(host)
                }
            elif len(parts) == 4:
                # ip:port:username:password 或 ABCProxy格式
                # 例如: f01a4db3d3952561.abcproxy.vip:4950:FlBaKtPm7l-zone-abc:00937128
                host = parts[0].strip()
                return {
                    'type': 'http',
                    'host': host,
                    'port': int(parts[1].strip()),
                    'username': parts[2].strip(),
                    'password': parts[3].strip(),
                    'is_residential': self.is_residential_proxy(host)
                }
            elif len(parts) >= 3 and parts[0].lower() in ['socks5', 'socks4', 'http']:
                # socks5:ip:port or socks5:ip:port:username:password
                proxy_type = parts[0].lower()
                host = parts[1].strip()
                port = int(parts[2].strip())
                username = parts[3].strip() if len(parts) > 3 else None
                password = parts[4].strip() if len(parts) > 4 else None
                
                return {
                    'type': proxy_type,
                    'host': host,
                    'port': port,
                    'username': username,
                    'password': password,
                    'is_residential': self.is_residential_proxy(host)
                }
        except Exception as e:
            print(f"❌ 解析代理行失败: {line} - {e}")
        
        return None
    
    def get_next_proxy(self) -> Optional[Dict]:
        """获取下一个代理"""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
    
    def get_random_proxy(self) -> Optional[Dict]:
        """获取随机代理"""
        if not self.proxies:
            return None
        return random.choice(self.proxies)
    
    def remove_proxy(self, proxy_to_remove: Dict):
        """从内存中移除代理"""
        self.proxies = [p for p in self.proxies if not (
            p['host'] == proxy_to_remove['host'] and p['port'] == proxy_to_remove['port']
        )]
    
    def backup_proxy_file(self) -> bool:
        """备份原始代理文件"""
        try:
            if os.path.exists(self.proxy_file):
                backup_file = self.proxy_file.replace('.txt', '_backup.txt')
                shutil.copy2(self.proxy_file, backup_file)
                print(f"✅ 代理文件已备份到: {backup_file}")
                return True
        except Exception as e:
            print(f"❌ 备份代理文件失败: {e}")
        return False
    
    def save_working_proxies(self, working_proxies: List[Dict]):
        """保存可用代理到新文件"""
        try:
            working_file = self.proxy_file.replace('.txt', '_working.txt')
            with open(working_file, 'w', encoding='utf-8') as f:
                f.write("# 可用代理文件 - 自动生成\n")
                f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 总数: {len(working_proxies)}个\n\n")
                
                for proxy in working_proxies:
                    if proxy['username'] and proxy['password']:
                        if proxy['type'] == 'http':
                            line = f"{proxy['host']}:{proxy['port']}:{proxy['username']}:{proxy['password']}\n"
                        else:
                            line = f"{proxy['type']}:{proxy['host']}:{proxy['port']}:{proxy['username']}:{proxy['password']}\n"
                    else:
                        if proxy['type'] == 'http':
                            line = f"{proxy['host']}:{proxy['port']}\n"
                        else:
                            line = f"{proxy['type']}:{proxy['host']}:{proxy['port']}\n"
                    f.write(line)
            
            print(f"✅ 可用代理已保存到: {working_file}")
            return working_file
        except Exception as e:
            print(f"❌ 保存可用代理失败: {e}")
            return None
    
    def save_failed_proxies(self, failed_proxies: List[Dict]):
        """保存失效代理到备份文件"""
        try:
            failed_file = self.proxy_file.replace('.txt', '_failed.txt')
            with open(failed_file, 'w', encoding='utf-8') as f:
                f.write("# 失效代理文件 - 自动生成\n")
                f.write(f"# 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 总数: {len(failed_proxies)}个\n\n")
                
                for proxy in failed_proxies:
                    if proxy['username'] and proxy['password']:
                        if proxy['type'] == 'http':
                            line = f"{proxy['host']}:{proxy['port']}:{proxy['username']}:{proxy['password']}\n"
                        else:
                            line = f"{proxy['type']}:{proxy['host']}:{proxy['port']}:{proxy['username']}:{proxy['password']}\n"
                    else:
                        if proxy['type'] == 'http':
                            line = f"{proxy['host']}:{proxy['port']}\n"
                        else:
                            line = f"{proxy['type']}:{proxy['host']}:{proxy['port']}\n"
                    f.write(line)
            
            print(f"✅ 失效代理已保存到: {failed_file}")
            return failed_file
        except Exception as e:
            print(f"❌ 保存失效代理失败: {e}")
            return None

# ================================
# 代理测试器（新增）
# ================================

class ProxyTester:
    """代理测试器 - 快速验证和清理代理"""
    
    def __init__(self, proxy_manager: ProxyManager):
        self.proxy_manager = proxy_manager
        self.test_url = "http://httpbin.org/ip"
        self.test_timeout = config.PROXY_CHECK_TIMEOUT
        self.max_concurrent = config.PROXY_CHECK_CONCURRENT
        
    async def test_proxy_connection(self, proxy_info: Dict) -> Tuple[bool, str, float]:
        """测试单个代理连接（支持住宅代理更长超时）"""
        start_time = time.time()
        
        # 住宅代理使用更长的超时时间
        is_residential = proxy_info.get('is_residential', False)
        test_timeout = config.RESIDENTIAL_PROXY_TIMEOUT if is_residential else self.test_timeout
        
        try:
            import aiohttp
            import aiosocks
            
            connector = None
            
            # 根据代理类型创建连接器
            if proxy_info['type'] == 'socks5':
                connector = aiosocks.SocksConnector.from_url(
                    f"socks5://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:{proxy_info['port']}"
                    if proxy_info.get('username') and proxy_info.get('password')
                    else f"socks5://{proxy_info['host']}:{proxy_info['port']}"
                )
            elif proxy_info['type'] == 'socks4':
                connector = aiosocks.SocksConnector.from_url(
                    f"socks4://{proxy_info['host']}:{proxy_info['port']}"
                )
            else:  # HTTP代理
                proxy_url = f"http://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:{proxy_info['port']}" \
                    if proxy_info.get('username') and proxy_info.get('password') \
                    else f"http://{proxy_info['host']}:{proxy_info['port']}"
                
                connector = aiohttp.TCPConnector()
            
            timeout = aiohttp.ClientTimeout(total=test_timeout)
            
            async with aiohttp.ClientSession(
                connector=connector,
                timeout=timeout
            ) as session:
                if proxy_info['type'] in ['socks4', 'socks5']:
                    async with session.get(self.test_url) as response:
                        if response.status == 200:
                            elapsed = time.time() - start_time
                            proxy_type = "住宅代理" if is_residential else "代理"
                            return True, f"{proxy_type}连接成功 {elapsed:.2f}s", elapsed
                else:
                    # HTTP代理
                    proxy_url = f"http://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:{proxy_info['port']}" \
                        if proxy_info.get('username') and proxy_info.get('password') \
                        else f"http://{proxy_info['host']}:{proxy_info['port']}"
                    
                    async with session.get(self.test_url, proxy=proxy_url) as response:
                        if response.status == 200:
                            elapsed = time.time() - start_time
                            proxy_type = "住宅代理" if is_residential else "代理"
                            return True, f"{proxy_type}连接成功 {elapsed:.2f}s", elapsed
                            
        except ImportError:
            # 如果没有aiohttp和aiosocks，使用基础方法
            return await self.basic_test_proxy(proxy_info, start_time, is_residential)
        except Exception as e:
            elapsed = time.time() - start_time
            error_msg = str(e)
            if "timeout" in error_msg.lower():
                return False, f"连接超时 {elapsed:.2f}s", elapsed
            elif "connection" in error_msg.lower():
                return False, f"连接失败 {elapsed:.2f}s", elapsed
            else:
                return False, f"错误: {error_msg[:20]} {elapsed:.2f}s", elapsed
        
        elapsed = time.time() - start_time
        return False, f"未知错误 {elapsed:.2f}s", elapsed
    
    async def basic_test_proxy(self, proxy_info: Dict, start_time: float, is_residential: bool = False) -> Tuple[bool, str, float]:
        """基础代理测试（不依赖aiohttp）"""
        try:
            import socket
            
            # 住宅代理使用更长的超时时间
            test_timeout = config.RESIDENTIAL_PROXY_TIMEOUT if is_residential else self.test_timeout
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(test_timeout)
            
            result = sock.connect_ex((proxy_info['host'], proxy_info['port']))
            elapsed = time.time() - start_time
            sock.close()
            
            if result == 0:
                return True, f"端口开放 {elapsed:.2f}s", elapsed
            else:
                return False, f"端口关闭 {elapsed:.2f}s", elapsed
                
        except Exception as e:
            elapsed = time.time() - start_time
            return False, f"测试失败: {str(e)[:20]} {elapsed:.2f}s", elapsed
    
    async def test_all_proxies(self, progress_callback=None) -> Tuple[List[Dict], List[Dict], Dict]:
        """测试所有代理"""
        if not self.proxy_manager.proxies:
            return [], [], {}
        
        print(f"🧪 开始测试 {len(self.proxy_manager.proxies)} 个代理...")
        print(f"⚡ 并发数: {self.max_concurrent}, 超时: {self.test_timeout}秒")
        
        working_proxies = []
        failed_proxies = []
        statistics = {
            'total': len(self.proxy_manager.proxies),
            'tested': 0,
            'working': 0,
            'failed': 0,
            'avg_response_time': 0,
            'start_time': time.time()
        }
        
        # 创建信号量控制并发
        semaphore = asyncio.Semaphore(self.max_concurrent)
        response_times = []
        
        async def test_single_proxy(proxy_info):
            async with semaphore:
                success, message, response_time = await self.test_proxy_connection(proxy_info)
                
                statistics['tested'] += 1
                
                if success:
                    working_proxies.append(proxy_info)
                    statistics['working'] += 1
                    response_times.append(response_time)
                    print(f"✅ {proxy_info['host']}:{proxy_info['port']} - {message}")
                else:
                    failed_proxies.append(proxy_info)
                    statistics['failed'] += 1
                    print(f"❌ {proxy_info['host']}:{proxy_info['port']} - {message}")
                
                # 更新统计
                if response_times:
                    statistics['avg_response_time'] = sum(response_times) / len(response_times)
                
                # 调用进度回调
                if progress_callback:
                    await progress_callback(statistics['tested'], statistics['total'], statistics)
        
        # 分批处理代理
        batch_size = config.PROXY_BATCH_SIZE
        for i in range(0, len(self.proxy_manager.proxies), batch_size):
            batch = self.proxy_manager.proxies[i:i + batch_size]
            tasks = [test_single_proxy(proxy) for proxy in batch]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # 批次间短暂休息
            await asyncio.sleep(0.1)
        
        total_time = time.time() - statistics['start_time']
        test_speed = statistics['total'] / total_time if total_time > 0 else 0
        
        print(f"\n📊 代理测试完成:")
        print(f"   总计: {statistics['total']} 个")
        print(f"   可用: {statistics['working']} 个 ({statistics['working']/statistics['total']*100:.1f}%)")
        print(f"   失效: {statistics['failed']} 个 ({statistics['failed']/statistics['total']*100:.1f}%)")
        print(f"   平均响应: {statistics['avg_response_time']:.2f} 秒")
        print(f"   测试速度: {test_speed:.1f} 代理/秒")
        print(f"   总耗时: {total_time:.1f} 秒")
        
        return working_proxies, failed_proxies, statistics
    
    async def cleanup_and_update_proxies(self, auto_confirm: bool = False) -> Tuple[bool, str]:
        """清理并更新代理文件"""
        if not config.PROXY_AUTO_CLEANUP and not auto_confirm:
            return False, "自动清理已禁用"
        
        # 备份原始文件
        if not self.proxy_manager.backup_proxy_file():
            return False, "备份失败"
        
        # 测试所有代理
        working_proxies, failed_proxies, stats = await self.test_all_proxies()
        
        if not working_proxies:
            return False, "没有可用的代理"
        
        # 保存分类结果
        working_file = self.proxy_manager.save_working_proxies(working_proxies)
        failed_file = self.proxy_manager.save_failed_proxies(failed_proxies)
        
        # 更新原始代理文件为可用代理
        try:
            with open(self.proxy_manager.proxy_file, 'w', encoding='utf-8') as f:
                f.write("# 自动清理后的可用代理文件\n")
                f.write(f"# 清理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 原始数量: {stats['total']}, 可用数量: {stats['working']}\n\n")
                
                for proxy in working_proxies:
                    if proxy['username'] and proxy['password']:
                        if proxy['type'] == 'http':
                            line = f"{proxy['host']}:{proxy['port']}:{proxy['username']}:{proxy['password']}\n"
                        else:
                            line = f"{proxy['type']}:{proxy['host']}:{proxy['port']}:{proxy['username']}:{proxy['password']}\n"
                    else:
                        if proxy['type'] == 'http':
                            line = f"{proxy['host']}:{proxy['port']}\n"
                        else:
                            line = f"{proxy['type']}:{proxy['host']}:{proxy['port']}\n"
                    f.write(line)
            
            # 重新加载代理
            self.proxy_manager.load_proxies()
            
            result_msg = f"""✅ 代理清理完成!
            
📊 清理统计:
• 原始代理: {stats['total']} 个
• 可用代理: {stats['working']} 个 
• 失效代理: {stats['failed']} 个
• 成功率: {stats['working']/stats['total']*100:.1f}%

📁 文件保存:
• 主文件: {self.proxy_manager.proxy_file} (已更新为可用代理)
• 可用代理: {working_file}
• 失效代理: {failed_file}
• 备份文件: {self.proxy_manager.proxy_file.replace('.txt', '_backup.txt')}"""
            
            return True, result_msg
            
        except Exception as e:
            return False, f"更新代理文件失败: {e}"

# ================================
# 配置类（增强）
# ================================

class Config:
    def __init__(self):
        self.TOKEN = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
        self.API_ID = int(os.getenv("API_ID", "0"))
        self.API_HASH = os.getenv("API_HASH", "")
        
        admin_ids = os.getenv("ADMIN_IDS", "")
        self.ADMIN_IDS = []
        if admin_ids:
            try:
                self.ADMIN_IDS = [int(x.strip()) for x in admin_ids.split(",") if x.strip()]
            except:
                pass
        
        self.TRIAL_DURATION = int(os.getenv("TRIAL_DURATION", "30"))
        self.TRIAL_DURATION_UNIT = os.getenv("TRIAL_DURATION_UNIT", "minutes")
        
        if self.TRIAL_DURATION_UNIT == "minutes":
            self.TRIAL_DURATION_SECONDS = self.TRIAL_DURATION * 60
        else:
            self.TRIAL_DURATION_SECONDS = self.TRIAL_DURATION
        
        self.DB_NAME = "bot_data.db"
        self.MAX_CONCURRENT_CHECKS = int(os.getenv("MAX_CONCURRENT_CHECKS", "20"))
        self.CHECK_TIMEOUT = int(os.getenv("CHECK_TIMEOUT", "15"))
        self.SPAMBOT_WAIT_TIME = float(os.getenv("SPAMBOT_WAIT_TIME", "2.0"))
        
        # 代理配置
        self.USE_PROXY = os.getenv("USE_PROXY", "true").lower() == "true"
        self.PROXY_TIMEOUT = int(os.getenv("PROXY_TIMEOUT", "10"))
        self.PROXY_FILE = os.getenv("PROXY_FILE", "proxy.txt")
        
        # 住宅代理配置
        self.RESIDENTIAL_PROXY_TIMEOUT = int(os.getenv("RESIDENTIAL_PROXY_TIMEOUT", "30"))
        self.RESIDENTIAL_PROXY_PATTERNS = os.getenv(
            "RESIDENTIAL_PROXY_PATTERNS", 
            "abcproxy,residential,resi,mobile"
        ).split(",")
                # 新增：对外访问的基础地址，用于生成验证码网页链接
        # 例如: http://45.147.196.113:5000 或 https://your.domain
        self.BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")
        ...
        print(f"🌐 验证码网页 BASE_URL: {self.BASE_URL}")
        # 新增速度优化配置
        self.PROXY_CHECK_CONCURRENT = int(os.getenv("PROXY_CHECK_CONCURRENT", "50"))
        self.PROXY_CHECK_TIMEOUT = int(os.getenv("PROXY_CHECK_TIMEOUT", "3"))
        self.PROXY_AUTO_CLEANUP = os.getenv("PROXY_AUTO_CLEANUP", "true").lower() == "true"
        self.PROXY_FAST_MODE = os.getenv("PROXY_FAST_MODE", "true").lower() == "true"
        self.PROXY_RETRY_COUNT = int(os.getenv("PROXY_RETRY_COUNT", "2"))
        self.PROXY_BATCH_SIZE = int(os.getenv("PROXY_BATCH_SIZE", "20"))
        
        # 获取当前脚本目录
        self.SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        
        # 文件管理配置
        self.RESULTS_DIR = os.path.join(self.SCRIPT_DIR, "results")
        self.UPLOADS_DIR = os.path.join(self.SCRIPT_DIR, "uploads")
        
        # 创建目录
        os.makedirs(self.RESULTS_DIR, exist_ok=True)
        os.makedirs(self.UPLOADS_DIR, exist_ok=True)
        
        print(f"📁 上传目录: {self.UPLOADS_DIR}")
        print(f"📁 结果目录: {self.RESULTS_DIR}")
        print(f"📡 系统配置: USE_PROXY={'true' if self.USE_PROXY else 'false'}")
        print(f"💡 注意: 实际代理模式需要配置文件+数据库开关+有效代理文件同时满足")
    
    def validate(self):
        if not self.TOKEN or not self.API_ID or not self.API_HASH:
            self.create_env_file()
            return False
        return True
    
    def create_env_file(self):
        if not os.path.exists(".env"):
            env_content = """TOKEN=YOUR_BOT_TOKEN_HERE
API_ID=YOUR_API_ID_HERE
API_HASH=YOUR_API_HASH_HERE
ADMIN_IDS=123456789
TRIAL_DURATION=30
TRIAL_DURATION_UNIT=minutes
MAX_CONCURRENT_CHECKS=20
CHECK_TIMEOUT=15
SPAMBOT_WAIT_TIME=2.0
USE_PROXY=true
PROXY_TIMEOUT=10
PROXY_FILE=proxy.txt
RESIDENTIAL_PROXY_TIMEOUT=30
RESIDENTIAL_PROXY_PATTERNS=abcproxy,residential,resi,mobile
PROXY_CHECK_CONCURRENT=50
PROXY_CHECK_TIMEOUT=3
PROXY_AUTO_CLEANUP=true
PROXY_FAST_MODE=true
PROXY_RETRY_COUNT=2
PROXY_BATCH_SIZE=20
BASE_URL=http://127.0.0.1:5000
"""
            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)
            print("✅ 已创建.env配置文件，请填入正确的配置信息")

# ================================
# SpamBot检测器（增强代理支持）
# ================================

class SpamBotChecker:
    """SpamBot检测器（优化版）"""
    
    def __init__(self, proxy_manager: ProxyManager):
        # 根据快速模式调整并发数，提升到25
        concurrent_limit = config.PROXY_CHECK_CONCURRENT if config.PROXY_FAST_MODE else config.MAX_CONCURRENT_CHECKS
        # 至少使用25个并发
        concurrent_limit = max(concurrent_limit, 25)
        self.semaphore = asyncio.Semaphore(concurrent_limit)
        self.proxy_manager = proxy_manager
        
        # 优化超时设置
        self.fast_timeout = config.PROXY_CHECK_TIMEOUT if config.PROXY_FAST_MODE else config.CHECK_TIMEOUT
        self.connection_timeout = 6  # 连接超时6秒
        self.spambot_timeout = 3     # SpamBot超时3秒
        self.fast_wait = 0.1         # SpamBot等待0.1秒
        
        print(f"⚡ SpamBot检测器初始化: 并发={concurrent_limit}, 快速模式={'开启' if config.PROXY_FAST_MODE else '关闭'}")
        
        self.status_patterns = {
            "无限制": [
                "good news, no limits are currently applied",
                "you're free as a bird",
                "no limits",
                "free as a bird",
                "no restrictions"
            ],
            "垃圾邮件": [
                # 临时限制的关键指标（优先级最高）
                "account is now limited until",
                "limited until",
                "account is limited until",
                "moderators have confirmed the report",
                "users found your messages annoying",
                "will be automatically released",
                "limitations will last longer next time",
                "while the account is limited",
                # 原有的patterns
                "actions can trigger a harsh response from our anti-spam systems",
                "account was limited",
                "you will not be able to send messages",
                "anti-spam systems",
                "limited by mistake",
                "spam"
            ],
            "冻结": [
                # 永久限制的关键指标
                "permanently banned",
                "account has been frozen permanently",
                "permanently restricted",
                "account is permanently",
                "banned permanently",
                # 原有的patterns
                "account was blocked for violations",
                "telegram terms of service",
                "blocked for violations",
                "terms of service",
                "violations of the telegram",
                "banned",
                "suspended"
            ]
        }
    
    def translate_to_english(self, text: str) -> str:
        """翻译到英文"""
        translations = {
            'ограничения': 'limitations',
            'заблокирован': 'blocked',
            'спам': 'spam',
            'нарушение': 'violation',
            'жалобы': 'complaints',
            'модераторы': 'moderators',
            'хорошие новости': 'good news',
            'нет ограничений': 'no limits',
            'свободны как птица': 'free as a bird',
        }
        
        translated = text.lower()
        for ru, en in translations.items():
            translated = translated.replace(ru, en)
        
        return translated
    
    def create_proxy_dict(self, proxy_info: Dict) -> Optional[Dict]:
        """创建代理字典"""
        if not proxy_info:
            return None
        
        try:
            if PROXY_SUPPORT:
                if proxy_info['type'] == 'socks5':
                    proxy_type = socks.SOCKS5
                elif proxy_info['type'] == 'socks4':
                    proxy_type = socks.SOCKS4
                else:
                    proxy_type = socks.HTTP
                
                proxy_dict = {
                    'proxy_type': proxy_type,
                    'addr': proxy_info['host'],
                    'port': proxy_info['port']
                }
                
                if proxy_info.get('username') and proxy_info.get('password'):
                    proxy_dict['username'] = proxy_info['username']
                    proxy_dict['password'] = proxy_info['password']
            else:
                # 基础代理支持（仅限telethon内置）
                proxy_dict = (proxy_info['host'], proxy_info['port'])
            
            return proxy_dict
            
        except Exception as e:
            print(f"❌ 创建代理配置失败: {e}")
            return None
    
    async def check_account_status(self, session_path: str, account_name: str, db: 'Database') -> Tuple[str, str, str]:
        """检查账号状态（优化版 - 支持快速模式和智能重试）"""
        if not TELETHON_AVAILABLE:
            return "连接错误", "Telethon未安装", account_name
        
        async with self.semaphore:
            # 智能重试逻辑
            retry_count = config.PROXY_RETRY_COUNT if config.PROXY_FAST_MODE else 1
            
            for attempt in range(retry_count + 1):
                result = await self._single_check_attempt(session_path, account_name, db, attempt)
                
                # 如果成功或者是最后一次尝试，返回结果
                if result[0] != "连接错误" or attempt == retry_count:
                    return result
                
                # 短暂延迟后重试
                if attempt < retry_count:
                    await asyncio.sleep(0.5)
            
            return "连接错误", "多次尝试后仍然失败", account_name
    
    async def _single_check_attempt(self, session_path: str, account_name: str, db: 'Database', attempt: int) -> Tuple[str, str, str]:
        """单次检测尝试"""
        client = None
        proxy_used = "本地连接"
        proxy_info = None
        
        try:
            # 快速预检测模式
            if config.PROXY_FAST_MODE and attempt == 0:
                # 先进行快速连接测试
                quick_result = await self._quick_connection_test(session_path)
                if not quick_result:
                    return "连接错误", "快速连接测试失败", account_name
            
            # 尝试使用代理（检查数据库开关和配置）
            proxy_dict = None
            proxy_enabled = db.get_proxy_enabled() if db else True
            if config.USE_PROXY and proxy_enabled and self.proxy_manager.proxies:
                proxy_info = self.proxy_manager.get_next_proxy()
                if proxy_info:
                    proxy_dict = self.create_proxy_dict(proxy_info)
                    if proxy_dict:
                        proxy_type = "住宅代理" if proxy_info.get('is_residential', False) else "代理"
                        proxy_used = f"{proxy_type} {proxy_info['host']}:{proxy_info['port']}"
            
            # 根据代理类型调整超时时间
            if proxy_info and proxy_info.get('is_residential', False):
                # 住宅代理使用更长的超时时间
                client_timeout = config.RESIDENTIAL_PROXY_TIMEOUT
                connect_timeout = config.RESIDENTIAL_PROXY_TIMEOUT
            else:
                # 普通代理或本地连接使用标准超时
                client_timeout = self.fast_timeout
                connect_timeout = self.connection_timeout if proxy_dict else 5
            
            # 创建客户端（使用优化的超时设置）
            client = TelegramClient(
                session_path,
                config.API_ID,
                config.API_HASH,
                timeout=client_timeout,
                connection_retries=1,
                retry_delay=1,
                proxy=proxy_dict
            )
            
            # 连接（使用根据代理类型调整的超时）
            try:
                await asyncio.wait_for(client.connect(), timeout=connect_timeout)
            except Exception as e:
                # 如果代理失败且启用代理模式，尝试本地连接
                if proxy_dict and config.PROXY_FAST_MODE:
                    print(f"⚠️ 代理连接失败，快速切换本地: {account_name}")
                    if client:
                        await client.disconnect()
                    
                    client = TelegramClient(
                        session_path,
                        config.API_ID,
                        config.API_HASH,
                        timeout=self.fast_timeout,
                        connection_retries=1,
                        retry_delay=1
                    )
                    
                    await asyncio.wait_for(client.connect(), timeout=5)
                    proxy_used = "本地连接(代理失败)"
                else:
                    return "连接错误", f"网络连接失败", account_name
            
            # 快速授权检查
            try:
                is_authorized = await asyncio.wait_for(client.is_user_authorized(), timeout=3)
                if not is_authorized:
                    return "封禁", "账号未授权", account_name
            except Exception as e:
                return "封禁", f"授权检查失败", account_name
            
            # 获取用户信息（快速模式下可选）
            user_info = f"账号"
            if not config.PROXY_FAST_MODE or attempt > 0:
                try:
                    me = await asyncio.wait_for(client.get_me(), timeout=3)
                    user_info = f"ID:{me.id}"
                    if me.username:
                        user_info += f" @{me.username}"
                    if me.first_name:
                        user_info += f" {me.first_name}"
                except Exception as e:
                    # 快速模式下用户信息获取失败不算错误
                    if not config.PROXY_FAST_MODE:
                        return "封禁", f"获取用户信息失败", account_name
            
            # SpamBot测试（优化等待时间）
            try:
                await asyncio.wait_for(
                    client.send_message("SpamBot", "/start"), 
                    timeout=self.spambot_timeout
                )
                
                # 快速模式下减少等待时间
                wait_time = config.SPAMBOT_WAIT_TIME if not config.PROXY_FAST_MODE else 1.0
                await asyncio.sleep(wait_time)
                
                messages = await asyncio.wait_for(
                    client.get_messages("SpamBot", limit=1), 
                    timeout=3
                )
                
                if messages and messages[0].message:
                    spambot_reply = messages[0].message
                    english_reply = self.translate_to_english(spambot_reply)
                    status = self.analyze_spambot_response(english_reply.lower())
                    
                    # 快速模式下简化回复信息
                    if config.PROXY_FAST_MODE:
                        reply_preview = spambot_reply[:20] + "..." if len(spambot_reply) > 20 else spambot_reply
                    else:
                        reply_preview = spambot_reply[:30] + "..." if len(spambot_reply) > 30 else spambot_reply
                    
                    return status, f"{user_info} | {proxy_used} | {reply_preview}", account_name
                else:
                    return "封禁", f"{user_info} | {proxy_used} | SpamBot无回复", account_name
                    
            except Exception as e:
                error_str = str(e).lower()
                if any(word in error_str for word in ["restricted", "limited", "banned", "blocked", "flood"]):
                    return "封禁", f"{user_info} | {proxy_used} | 账号受限", account_name
                else:
                    return "连接错误", f"{user_info} | {proxy_used} | SpamBot通信失败", account_name
            
        except Exception as e:
            error_msg = str(e).lower()
            if any(word in error_msg for word in ["timeout", "network", "connection", "resolve"]):
                return "连接错误", f"{proxy_used} | 网络问题", account_name
            else:
                return "封禁", f"{proxy_used} | 检测失败", account_name
        finally:
            if client:
                try:
                    await client.disconnect()
                except:
                    pass
    
    async def _quick_connection_test(self, session_path: str) -> bool:
        """快速连接预测试"""
        try:
            # 检查session文件是否存在且有效
            if not os.path.exists(session_path):
                return False
            
            # 检查文件大小（太小的session文件通常无效）
            if os.path.getsize(session_path) < 100:
                return False
            
            return True
        except:
            return False
    
    def analyze_spambot_response(self, response: str) -> str:
        """分析SpamBot回复"""
        response_lower = response.lower()
        
        # 1. 首先检查冻结/封禁状态（最严重）
        for pattern in self.status_patterns["冻结"]:
            if pattern.lower() in response_lower:
                return "冻结"
        
        # 2. 然后检查垃圾邮件限制（中等限制）
        for pattern in self.status_patterns["垃圾邮件"]:
            if pattern.lower() in response_lower:
                return "垃圾邮件"
        
        # 3. 最后检查无限制（正常状态）
        for pattern in self.status_patterns["无限制"]:
            if pattern.lower() in response_lower:
                return "无限制"
        
        # 4. 默认返回无限制
        return "无限制"

# ================================
# 数据库管理（增强管理员功能）
# ================================

class Database:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                register_time TEXT,
                last_active TEXT,
                status TEXT DEFAULT ''
            )
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS memberships (
                user_id INTEGER PRIMARY KEY,
                level TEXT,
                trial_expiry_time TEXT,
                created_at TEXT
            )
        """)
        
        # 新增管理员表
        c.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                added_by INTEGER,
                added_time TEXT,
                is_super_admin INTEGER DEFAULT 0
            )
        """)
        
        # 新增代理设置表
        c.execute("""
            CREATE TABLE IF NOT EXISTS proxy_settings (
                id INTEGER PRIMARY KEY DEFAULT 1,
                proxy_enabled INTEGER DEFAULT 1,
                updated_time TEXT,
                updated_by INTEGER
            )
        """)
        
        # 广播消息表
        c.execute("""
            CREATE TABLE IF NOT EXISTS broadcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                buttons_json TEXT,
                target TEXT NOT NULL,
                created_by INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                total INTEGER DEFAULT 0,
                success INTEGER DEFAULT 0,
                failed INTEGER DEFAULT 0,
                duration_sec REAL DEFAULT 0
            )
        """)
        
        # 广播日志表
        c.execute("""
            CREATE TABLE IF NOT EXISTS broadcast_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                broadcast_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                error TEXT,
                sent_at TEXT NOT NULL,
                FOREIGN KEY (broadcast_id) REFERENCES broadcasts(id)
            )
        """)
        
        # 兑换码表
        c.execute("""
            CREATE TABLE IF NOT EXISTS redeem_codes (
                code TEXT PRIMARY KEY,
                level TEXT DEFAULT '会员',
                days INTEGER NOT NULL,
                status TEXT DEFAULT 'active',
                created_by INTEGER,
                created_at TEXT,
                redeemed_by INTEGER,
                redeemed_at TEXT
            )
        """)
        
        # 迁移：添加expiry_time列到memberships表
        try:
            c.execute("ALTER TABLE memberships ADD COLUMN expiry_time TEXT")
            print("✅ 已添加 memberships.expiry_time 列")
        except sqlite3.OperationalError:
            # 列已存在，忽略
            pass
        
        conn.commit()
        conn.close()
    
    def save_user(self, user_id: int, username: str, first_name: str, status: str = ""):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            c.execute("""
                INSERT OR REPLACE INTO users 
                (user_id, username, first_name, register_time, last_active, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, username, first_name, now, now, status))
            
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def save_membership(self, user_id: int, level: str):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            now = datetime.now()
            
            if level == "体验会员":
                expiry = now + timedelta(seconds=config.TRIAL_DURATION_SECONDS)
                c.execute("""
                    INSERT OR REPLACE INTO memberships 
                    (user_id, level, trial_expiry_time, created_at)
                    VALUES (?, ?, ?, ?)
                """, (user_id, level, expiry.strftime("%Y-%m-%d %H:%M:%S"), 
                      now.strftime("%Y-%m-%d %H:%M:%S")))
            
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def check_membership(self, user_id: int) -> Tuple[bool, str, str]:
        # 管理员优先
        if self.is_admin(user_id):
            return True, "管理员", "永久有效"
        
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT level, trial_expiry_time, expiry_time FROM memberships WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            conn.close()
            
            if not row:
                return False, "无会员", "未订阅"
            
            level, trial_expiry_time, expiry_time = row
            
            # 优先检查新的expiry_time字段
            if expiry_time:
                try:
                    expiry_dt = datetime.strptime(expiry_time, "%Y-%m-%d %H:%M:%S")
                    if expiry_dt > datetime.now():
                        return True, level, expiry_dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    pass
            
            # 兼容旧的trial_expiry_time字段
            if level == "体验会员" and trial_expiry_time:
                expiry_dt = datetime.strptime(trial_expiry_time, "%Y-%m-%d %H:%M:%S")
                if expiry_dt > datetime.now():
                    return True, level, expiry_dt.strftime("%Y-%m-%d %H:%M:%S")
            
            return False, "无会员", "已过期"
        except:
            return False, "无会员", "检查失败"
    
    def is_admin(self, user_id: int) -> bool:
        """检查用户是否为管理员"""
        # 检查配置文件中的管理员
        if user_id in config.ADMIN_IDS:
            return True
        
        # 检查数据库中的管理员
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT user_id FROM admins WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            conn.close()
            return row is not None
        except:
            return False
    
    def add_admin(self, user_id: int, username: str, first_name: str, added_by: int) -> bool:
        """添加管理员"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            c.execute("""
                INSERT OR REPLACE INTO admins 
                (user_id, username, first_name, added_by, added_time)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, username, first_name, added_by, now))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 添加管理员失败: {e}")
            return False
    
    def remove_admin(self, user_id: int) -> bool:
        """移除管理员"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("DELETE FROM admins WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 移除管理员失败: {e}")
            return False
    
    def get_all_admins(self) -> List[Tuple]:
        """获取所有管理员"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # 获取数据库中的管理员
            c.execute("""
                SELECT user_id, username, first_name, added_time 
                FROM admins 
                ORDER BY added_time DESC
            """)
            db_admins = c.fetchall()
            conn.close()
            
            # 合并配置文件中的管理员
            all_admins = []
            
            # 添加配置文件管理员
            for admin_id in config.ADMIN_IDS:
                all_admins.append((admin_id, "配置文件管理员", "", "系统内置"))
            
            # 添加数据库管理员
            all_admins.extend(db_admins)
            
            return all_admins
        except Exception as e:
            print(f"❌ 获取管理员列表失败: {e}")
            return []
    
    def get_user_by_username(self, username: str) -> Optional[Tuple]:
        """根据用户名获取用户信息"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            username = username.replace("@", "")  # 移除@符号
            c.execute("SELECT user_id, username, first_name FROM users WHERE username = ?", (username,))
            row = c.fetchone()
            conn.close()
            return row
        except:
            return None
    
    def get_proxy_enabled(self) -> bool:
        """获取代理开关状态"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT proxy_enabled FROM proxy_settings WHERE id = 1")
            row = c.fetchone()
            conn.close()
            
            if row:
                return bool(row[0])
            else:
                # 初始化默认设置
                self.set_proxy_enabled(True, None)
                return True
        except:
            return True  # 默认启用
    
    def set_proxy_enabled(self, enabled: bool, user_id: Optional[int]) -> bool:
        """设置代理开关状态"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            c.execute("""
                INSERT OR REPLACE INTO proxy_settings 
                (id, proxy_enabled, updated_time, updated_by)
                VALUES (1, ?, ?, ?)
            """, (int(enabled), now, user_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 设置代理开关失败: {e}")
            return False
    
    def grant_membership_days(self, user_id: int, days: int, level: str = "会员") -> bool:
        """授予用户会员（天数累加）"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            now = datetime.now()
            
            # 检查是否已有会员记录
            c.execute("SELECT expiry_time FROM memberships WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            
            if row and row[0]:
                # 已有到期时间，从到期时间继续累加
                try:
                    current_expiry = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                    # 如果到期时间在未来，从到期时间累加
                    if current_expiry > now:
                        new_expiry = current_expiry + timedelta(days=days)
                    else:
                        # 已过期，从当前时间累加
                        new_expiry = now + timedelta(days=days)
                except:
                    new_expiry = now + timedelta(days=days)
            else:
                # 没有记录或没有到期时间，从当前时间累加
                new_expiry = now + timedelta(days=days)
            
            c.execute("""
                INSERT OR REPLACE INTO memberships 
                (user_id, level, expiry_time, created_at)
                VALUES (?, ?, ?, ?)
            """, (user_id, level, new_expiry.strftime("%Y-%m-%d %H:%M:%S"), 
                  now.strftime("%Y-%m-%d %H:%M:%S")))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 授予会员失败: {e}")
            return False
    
    def redeem_code(self, user_id: int, code: str) -> Tuple[bool, str, int]:
        """兑换卡密"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # 查询卡密
            c.execute("""
                SELECT code, level, days, status 
                FROM redeem_codes 
                WHERE code = ?
            """, (code.upper(),))
            row = c.fetchone()
            
            if not row:
                conn.close()
                return False, "卡密不存在", 0
            
            code_val, level, days, status = row
            
            # 检查状态
            if status == 'used':
                conn.close()
                return False, "卡密已被使用", 0
            elif status == 'expired':
                conn.close()
                return False, "卡密已过期", 0
            elif status != 'active':
                conn.close()
                return False, "卡密状态无效", 0
            
            # 标记为已使用
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("""
                UPDATE redeem_codes 
                SET status = 'used', redeemed_by = ?, redeemed_at = ?
                WHERE code = ?
            """, (user_id, now, code.upper()))
            
            conn.commit()
            conn.close()
            
            # 授予会员
            if self.grant_membership_days(user_id, days, level):
                return True, f"成功兑换{days}天{level}", days
            else:
                return False, "兑换失败，请联系管理员", 0
                
        except Exception as e:
            print(f"❌ 兑换卡密失败: {e}")
            return False, f"兑换失败: {str(e)}", 0
    
    def create_redeem_code(self, level: str, days: int, code: Optional[str], created_by: int) -> Tuple[bool, str, str]:
        """生成兑换码"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # 如果没有提供code，自动生成
            if not code:
                # 生成8位大写字母数字组合
                while True:
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                    # 检查是否已存在
                    c.execute("SELECT code FROM redeem_codes WHERE code = ?", (code,))
                    if not c.fetchone():
                        break
            else:
                code = code.upper()[:10]  # 最多10位
                # 检查是否已存在
                c.execute("SELECT code FROM redeem_codes WHERE code = ?", (code,))
                if c.fetchone():
                    conn.close()
                    return False, code, "卡密已存在"
            
            # 插入卡密
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("""
                INSERT INTO redeem_codes 
                (code, level, days, status, created_by, created_at)
                VALUES (?, ?, ?, 'active', ?, ?)
            """, (code, level, days, created_by, now))
            
            conn.commit()
            conn.close()
            return True, code, "生成成功"
            
        except Exception as e:
            print(f"❌ 生成卡密失败: {e}")
            return False, "", f"生成失败: {str(e)}"
    
    def get_user_id_by_username(self, username: str) -> Optional[int]:
        """根据用户名获取用户ID"""
        user_info = self.get_user_by_username(username)
        if user_info:
            return user_info[0]  # user_id是第一个字段
        return None
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """获取用户统计信息"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # 总用户数
            c.execute("SELECT COUNT(*) FROM users")
            total_users = c.fetchone()[0]
            
            # 今日活跃用户
            today = datetime.now().strftime('%Y-%m-%d')
            c.execute("SELECT COUNT(*) FROM users WHERE last_active LIKE ?", (f"{today}%",))
            today_active = c.fetchone()[0]
            
            # 本周活跃用户
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            c.execute("SELECT COUNT(*) FROM users WHERE last_active >= ?", (week_ago,))
            week_active = c.fetchone()[0]
            
            # 会员统计
            c.execute("SELECT COUNT(*) FROM memberships WHERE level = '体验会员'")
            trial_members = c.fetchone()[0]
            
            # 有效会员（未过期）
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute("SELECT COUNT(*) FROM memberships WHERE trial_expiry_time > ?", (now,))
            active_members = c.fetchone()[0]
            
            # 最近注册用户（7天内）
            c.execute("SELECT COUNT(*) FROM users WHERE register_time >= ?", (week_ago,))
            recent_users = c.fetchone()[0]
            
            conn.close()
            
            return {
                'total_users': total_users,
                'today_active': today_active,
                'week_active': week_active,
                'trial_members': trial_members,
                'active_members': active_members,
                'recent_users': recent_users
            }
        except Exception as e:
            print(f"❌ 获取用户统计失败: {e}")
            return {}

    def get_recent_users(self, limit: int = 20) -> List[Tuple]:
        """获取最近注册的用户"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("""
                SELECT user_id, username, first_name, register_time, last_active, status
                FROM users 
                ORDER BY register_time DESC 
                LIMIT ?
            """, (limit,))
            result = c.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"❌ 获取最近用户失败: {e}")
            return []

    def get_active_users(self, days: int = 7, limit: int = 50) -> List[Tuple]:
        """获取活跃用户"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
            c.execute("""
                SELECT user_id, username, first_name, register_time, last_active, status
                FROM users 
                WHERE last_active >= ?
                ORDER BY last_active DESC 
                LIMIT ?
            """, (cutoff_date, limit))
            result = c.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"❌ 获取活跃用户失败: {e}")
            return []

    def search_user(self, query: str) -> List[Tuple]:
        """搜索用户（按ID、用户名、昵称）"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # 尝试按用户ID搜索
            if query.isdigit():
                c.execute("""
                    SELECT user_id, username, first_name, register_time, last_active, status
                    FROM users 
                    WHERE user_id = ?
                """, (int(query),))
                result = c.fetchall()
                if result:
                    conn.close()
                    return result
            
            # 按用户名和昵称模糊搜索
            like_query = f"%{query}%"
            c.execute("""
                SELECT user_id, username, first_name, register_time, last_active, status
                FROM users 
                WHERE username LIKE ? OR first_name LIKE ?
                ORDER BY last_active DESC
                LIMIT 20
            """, (like_query, like_query))
            result = c.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"❌ 搜索用户失败: {e}")
            return []

    def get_user_membership_info(self, user_id: int) -> Dict[str, Any]:
        """获取用户的详细会员信息"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # 获取用户基本信息
            c.execute("SELECT username, first_name, register_time, last_active, status FROM users WHERE user_id = ?", (user_id,))
            user_info = c.fetchone()
            
            if not user_info:
                conn.close()
                return {}
            
            # 获取会员信息
            c.execute("SELECT level, trial_expiry_time, created_at FROM memberships WHERE user_id = ?", (user_id,))
            membership_info = c.fetchone()
            
            conn.close()
            
            result = {
                'user_id': user_id,
                'username': user_info[0] or '',
                'first_name': user_info[1] or '',
                'register_time': user_info[2] or '',
                'last_active': user_info[3] or '',
                'status': user_info[4] or '',
                'is_admin': self.is_admin(user_id)
            }
            
            if membership_info:
                result.update({
                    'membership_level': membership_info[0],
                    'expiry_time': membership_info[1],
                    'membership_created': membership_info[2]
                })
            else:
                result.update({
                    'membership_level': '无会员',
                    'expiry_time': '',
                    'membership_created': ''
                })
            
            return result
        except Exception as e:
            print(f"❌ 获取用户会员信息失败: {e}")
            return {}    
    def get_proxy_setting_info(self) -> Tuple[bool, str, Optional[int]]:
        """获取代理设置详细信息"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT proxy_enabled, updated_time, updated_by FROM proxy_settings WHERE id = 1")
            row = c.fetchone()
            conn.close()
            
            if row:
                return bool(row[0]), row[1] or "未知", row[2]
            else:
                return True, "系统默认", None
        except:
            return True, "系统默认", None
    
    # ================================
    # 广播消息相关方法
    # ================================
    
    def get_target_users(self, target: str) -> List[int]:
        """获取目标用户列表"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            if target == "all":
                # 所有用户
                c.execute("SELECT user_id FROM users")
            elif target == "members":
                # 仅会员（有效会员）
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                c.execute("""
                    SELECT user_id FROM memberships 
                    WHERE trial_expiry_time > ?
                """, (now,))
            elif target == "active_7d":
                # 活跃用户（7天内）
                cutoff = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
                c.execute("""
                    SELECT user_id FROM users 
                    WHERE last_active >= ?
                """, (cutoff,))
            elif target == "new_7d":
                # 新用户（7天内）
                cutoff = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
                c.execute("""
                    SELECT user_id FROM users 
                    WHERE register_time >= ?
                """, (cutoff,))
            else:
                conn.close()
                return []
            
            result = [row[0] for row in c.fetchall()]
            conn.close()
            return result
        except Exception as e:
            print(f"❌ 获取目标用户失败: {e}")
            return []
    
    def insert_broadcast_record(self, title: str, content: str, buttons_json: str, 
                               target: str, created_by: int) -> Optional[int]:
        """插入广播记录并返回ID"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            c.execute("""
                INSERT INTO broadcasts 
                (title, content, buttons_json, target, created_by, created_at, status)
                VALUES (?, ?, ?, ?, ?, ?, 'pending')
            """, (title, content, buttons_json, target, created_by, now))
            
            broadcast_id = c.lastrowid
            conn.commit()
            conn.close()
            return broadcast_id
        except Exception as e:
            print(f"❌ 插入广播记录失败: {e}")
            return None
    
    def update_broadcast_progress(self, broadcast_id: int, success: int, 
                                 failed: int, status: str, duration: float):
        """更新广播进度"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            c.execute("""
                UPDATE broadcasts 
                SET success = ?, failed = ?, status = ?, duration_sec = ?, total = ?
                WHERE id = ?
            """, (success, failed, status, duration, success + failed, broadcast_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 更新广播进度失败: {e}")
            return False
    
    def add_broadcast_log(self, broadcast_id: int, user_id: int, 
                         status: str, error: Optional[str] = None):
        """添加广播日志"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            c.execute("""
                INSERT INTO broadcast_logs 
                (broadcast_id, user_id, status, error, sent_at)
                VALUES (?, ?, ?, ?, ?)
            """, (broadcast_id, user_id, status, error, now))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 添加广播日志失败: {e}")
            return False
    
    def get_broadcast_history(self, limit: int = 10) -> List[Tuple]:
        """获取广播历史记录"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            c.execute("""
                SELECT id, title, target, created_at, status, total, success, failed
                FROM broadcasts 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            
            result = c.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"❌ 获取广播历史失败: {e}")
            return []
    
    def get_broadcast_detail(self, broadcast_id: int) -> Optional[Dict[str, Any]]:
        """获取广播详情"""
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            c.execute("""
                SELECT id, title, content, buttons_json, target, created_by, 
                       created_at, status, total, success, failed, duration_sec
                FROM broadcasts 
                WHERE id = ?
            """, (broadcast_id,))
            
            row = c.fetchone()
            if not row:
                conn.close()
                return None
            
            result = {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'buttons_json': row[3],
                'target': row[4],
                'created_by': row[5],
                'created_at': row[6],
                'status': row[7],
                'total': row[8],
                'success': row[9],
                'failed': row[10],
                'duration_sec': row[11]
            }
            
            conn.close()
            return result
        except Exception as e:
            print(f"❌ 获取广播详情失败: {e}")
            return None

# ================================
# 文件处理器（保持原有功能）
# ================================

class FileProcessor:
    """文件处理器"""
    
    def __init__(self, checker: SpamBotChecker, db: Database):
        self.checker = checker
        self.db = db
    
    def extract_phone_from_tdata_directory(self, tdata_path: str) -> str:
        """
        从TData目录结构中提取手机号
        
        TData目录结构通常是：
        /path/to/phone_number/tdata/D877F783D5D3EF8C/
        或者
        /path/to/tdata/D877F783D5D3EF8C/ (tdata本身在根目录)
        """
        try:
            # 方法1: 从路径中提取 - 找到tdata目录的父目录
            path_parts = tdata_path.split(os.sep)
            
            # 找到"tdata"在路径中的位置
            tdata_index = -1
            for i, part in enumerate(path_parts):
                if part == "tdata":
                    tdata_index = i
                    break
            
            # 如果找到tdata，检查它的父目录
            if tdata_index > 0:
                phone_candidate = path_parts[tdata_index - 1]
                
                # 验证是否为手机号格式
                # 支持格式：+998xxxxxxxxx 或 998xxxxxxxxx 或其他数字
                if phone_candidate.startswith('+'):
                    phone_candidate = phone_candidate[1:]  # 移除+号
                
                if phone_candidate.isdigit() and len(phone_candidate) >= 10:
                    return phone_candidate
            
            # 方法2: 遍历路径中的所有部分，找到看起来像手机号的部分
            for part in reversed(path_parts):
                if part == "tdata" or part == "D877F783D5D3EF8C":
                    continue
                
                # 检查是否为手机号格式
                clean_part = part.lstrip('+')
                if clean_part.isdigit() and len(clean_part) >= 10:
                    return clean_part
            
            # 方法3: 如果都失败了，生成一个基于路径hash的标识符
            import hashlib
            path_hash = hashlib.md5(tdata_path.encode()).hexdigest()[:10]
            return f"tdata_{path_hash}"
            
        except Exception as e:
            print(f"⚠️ 提取手机号失败: {e}")
            # 返回一个基于时间戳的标识符
            return f"tdata_{int(time.time())}"
    
    def scan_zip_file(self, zip_path: str, user_id: int, task_id: str) -> Tuple[List[Tuple[str, str]], str, str]:
        """扫描ZIP文件"""
        session_files = []
        tdata_folders = []
        
        # 在uploads目录下为每个任务创建专属文件夹
        task_upload_dir = os.path.join(config.UPLOADS_DIR, f"task_{task_id}")
        os.makedirs(task_upload_dir, exist_ok=True)
        
        print(f"📁 任务上传目录: {task_upload_dir}")
        
        try:
            # 解压到任务专属目录
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(task_upload_dir)
            
            print(f"📦 文件解压完成: {task_upload_dir}")
            
            # 扫描解压后的文件
            for root, dirs, files in os.walk(task_upload_dir):
                for file in files:
                    if file.endswith('.session'):
                        file_full_path = os.path.join(root, file)
                        session_files.append((file_full_path, file))
                        print(f"📄 找到Session文件: {file}")
                
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    d877_check_path = os.path.join(dir_path, "D877F783D5D3EF8C")
                    if os.path.exists(d877_check_path):
                        # 使用新的提取方法获取手机号
                        display_name = self.extract_phone_from_tdata_directory(dir_path)
                        
                        tdata_folders.append((dir_path, display_name))
                        print(f"📂 找到TData目录: {display_name}")
        
        except Exception as e:
            print(f"❌ 文件扫描失败: {e}")
            shutil.rmtree(task_upload_dir, ignore_errors=True)
            return [], "", "error"
        
        # 优先级：TData > Session（修复检测优先级问题）
        if tdata_folders:
            print(f"🎯 检测到TData文件，优先使用TData检测")
            print(f"✅ 找到 {len(tdata_folders)} 个TData文件夹")
            if session_files:
                print(f"📱 同时发现 {len(session_files)} 个Session文件（已忽略，优先TData）")
            return tdata_folders, task_upload_dir, "tdata"
        elif session_files:
            print(f"📱 检测到Session文件，使用Session检测")
            print(f"✅ 找到 {len(session_files)} 个Session文件")
            return session_files, task_upload_dir, "session"
        else:
            print("❌ 未找到有效的账号文件")
            shutil.rmtree(task_upload_dir, ignore_errors=True)
            return [], "", "none"
    
    async def check_accounts_with_realtime_updates(self, files: List[Tuple[str, str]], file_type: str, update_callback) -> Dict[str, List[Tuple[str, str, str]]]:
        """实时更新检查"""
        results = {
            "无限制": [],
            "垃圾邮件": [],
            "冻结": [],
            "封禁": [],
            "连接错误": []
        }
        
        total = len(files)
        processed = 0
        start_time = time.time()
        last_update_time = 0
        
        async def process_single_account(file_path, file_name):
            nonlocal processed, last_update_time
            try:
                if file_type == "session":
                    status, info, account_name = await self.checker.check_account_status(file_path, file_name, self.db)
                else:  # tdata
                    # 使用新的真实SpamBot检测方法
                    status, info, account_name = await self.check_tdata_with_spambot(file_path, file_name)
                
                results[status].append((file_path, file_name, info))
                processed += 1
                
                print(f"✅ 检测完成 {processed}/{total}: {file_name} -> {status}")
                
                # 控制更新频率，每3秒或每10个账号更新一次
                current_time = time.time()
                if (current_time - last_update_time >= 3) or (processed % 10 == 0) or (processed == total):
                    if update_callback:
                        elapsed = time.time() - start_time
                        speed = processed / elapsed if elapsed > 0 else 0
                        await update_callback(processed, total, results, speed, elapsed)
                        last_update_time = current_time
                
            except Exception as e:
                results["连接错误"].append((file_path, file_name, f"异常: {str(e)[:20]}"))
                processed += 1
                print(f"❌ 检测失败 {processed}/{total}: {file_name} -> {str(e)}")
        
        # 分批并发执行
        batch_size = config.MAX_CONCURRENT_CHECKS
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            tasks = [process_single_account(file_path, file_name) for file_path, file_name in batch]
            await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    async def check_tdata_structure_async(self, tdata_path: str, tdata_name: str) -> Tuple[str, str, str]:
        """异步TData检查（已废弃，保留向后兼容）"""
        try:
            d877_path = os.path.join(tdata_path, "D877F783D5D3EF8C")
            maps_path = os.path.join(d877_path, "maps")
            
            if not os.path.exists(maps_path):
                return "连接错误", "TData结构无效", tdata_name
            
            maps_size = os.path.getsize(maps_path)
            if maps_size < 30:
                return "连接错误", "TData数据不完整", tdata_name
            
            return "无限制", f"TData有效 | {maps_size}字节", tdata_name
            
        except Exception as e:
            return "连接错误", f"TData检查失败", tdata_name
    
    def translate_spambot_reply(self, text: str) -> str:
        """智能翻译SpamBot回复"""
        # 常见俄语到英语的翻译
        translations = {
            'ограничения': 'limitations',
            'ограничено': 'limited', 
            'заблокирован': 'blocked',
            'спам': 'spam',
            'нарушение': 'violation',
            'жалобы': 'complaints',
            'хорошие новости': 'good news',
            'нет ограничений': 'no limitations',
            'свободны': 'free'
        }
        
        result = text.lower()
        for ru, en in translations.items():
            result = result.replace(ru, en)
        
        return result
    
    async def check_tdata_with_spambot(self, tdata_path: str, tdata_name: str) -> Tuple[str, str, str]:
        """基于opentele的真正TData SpamBot检测"""
        client = None
        session_name = None
        
        try:
            if not OPENTELE_AVAILABLE:
                return "连接错误", "opentele库未安装", tdata_name
            
            # 1. TData转Session（采用opentele方式）
            tdesk = TDesktop(tdata_path)
            
            if not tdesk.isLoaded():
                return "连接错误", "TData未授权或无效", tdata_name
            
            session_name = f"temp_{int(time.time()*1000)}"
            client = await tdesk.ToTelethon(session=session_name, flag=UseCurrentSession, api=API.TelegramDesktop)
            
            # 2. 快速连接测试
            await asyncio.wait_for(client.connect(), timeout=6)
            
            # 3. 检查授权状态
            if not await client.is_user_authorized():
                return "封禁", "账号未授权", tdata_name
            
            # 4. 获取手机号
            try:
                me = await client.get_me()
                phone = me.phone if me.phone else "未知号码"
            except Exception:
                phone = "未知号码"
            
            # 5. 冻结检测（采用FloodError检测）
            try:
                from telethon.tl.functions.account import GetPrivacyRequest
                from telethon.tl.types import InputPrivacyKeyPhoneNumber
                
                privacy_key = InputPrivacyKeyPhoneNumber()
                await asyncio.wait_for(client(GetPrivacyRequest(key=privacy_key)), timeout=3)
            except Exception as e:
                error_str = str(e).lower()
                if 'flood' in error_str:
                    return "冻结", f"手机号:{phone} | 账号冻结", tdata_name
            
            # 6. SpamBot检测
            try:
                await asyncio.wait_for(client.send_message('SpamBot', '/start'), timeout=3)
                await asyncio.sleep(0.1)  # 快速等待
                
                entity = await client.get_entity(178220800)  # SpamBot固定ID
                async for message in client.iter_messages(entity, limit=1):
                    text = message.raw_text.lower()
                    
                    # 智能翻译和状态判断
                    english_text = self.translate_spambot_reply(text)
                    
                    # 1. 首先检查临时限制（垃圾邮件）- 优先级最高
                    if any(keyword in english_text for keyword in [
                        'account is now limited until', 'limited until', 'account is limited until',
                        'moderators have confirmed the report', 'users found your messages annoying',
                        'will be automatically released', 'limitations will last longer next time',
                        'while the account is limited', 'account was limited',
                        'you will not be able to send messages', 'anti-spam systems', 'harsh response',
                        'spam'
                    ]):
                        return "垃圾邮件", f"手机号:{phone} | 垃圾邮件限制", tdata_name
                    
                    # 2. 然后检查永久冻结
                    elif any(keyword in english_text for keyword in [
                        'permanently banned', 'account has been frozen permanently',
                        'permanently restricted', 'account is permanently', 'banned permanently',
                        'blocked for violations', 'terms of service', 'violations of the telegram',
                        'account was blocked', 'banned', 'suspended'
                    ]):
                        return "冻结", f"手机号:{phone} | 账号被冻结/封禁", tdata_name
                    
                    # 3. 检查无限制状态
                    elif any(keyword in english_text for keyword in [
                        'no limits', 'free as a bird', 'no restrictions', 'good news'
                    ]):
                        return "无限制", f"手机号:{phone} | 正常无限制", tdata_name
                    
                    # 4. 默认返回无限制
                    else:
                        return "无限制", f"手机号:{phone} | 正常无限制", tdata_name
                
                # 如果没有消息回复
                return "封禁", f"手机号:{phone} | SpamBot无回复", tdata_name
        
            except Exception as e:
                error_str = str(e).lower()
                if any(word in error_str for word in ['restricted', 'banned', 'blocked']):
                    return "封禁", f"手机号:{phone} | 账号受限", tdata_name
                return "封禁", f"手机号:{phone} | SpamBot检测失败", tdata_name
                
        except Exception as e:
            error_str = str(e).lower()
            if 'database is locked' in error_str:
                return "连接错误", f"TData文件被占用", tdata_name
            elif 'timeout' in error_str or 'connection' in error_str:
                return "连接错误", f"连接超时", tdata_name
            else:
                return "封禁", f"连接失败: {str(e)[:30]}", tdata_name
        finally:
            # 清理资源
            if client:
                try:
                    await client.disconnect()
                except:
                    pass
            # 清理临时session文件
            if session_name:
                try:
                    session_file = f"{session_name}.session"
                    if os.path.exists(session_file):
                        os.remove(session_file)
                    session_journal = f"{session_file}-journal"
                    if os.path.exists(session_journal):
                        os.remove(session_journal)
                except:
                    pass
    
    def create_result_zips(self, results: Dict[str, List[Tuple[str, str, str]]], task_id: str, file_type: str) -> List[Tuple[str, str, int]]:
        """创建结果ZIP（修复版 - 解决目录重名问题并优化路径长度）"""
        result_files = []
        
        # 优化路径结构：使用短时间戳创建简洁的结果目录
        # 从 /www/sessionbot/results/task_5611529170/ 
        # 优化为 /www/sessionbot/results/conv_123456/
        timestamp_short = str(int(time.time()))[-6:]  # 只取后6位
        task_results_dir = os.path.join(config.RESULTS_DIR, f"conv_{timestamp_short}")
        os.makedirs(task_results_dir, exist_ok=True)
        
        print(f"📁 任务结果目录: {task_results_dir}")
        
        for status, files in results.items():
            if not files:
                continue
            
            print(f"📦 正在创建 {status} 结果文件，包含 {len(files)} 个账号")
            
            # 为每个状态创建唯一的临时目录（优化路径长度）
            # 使用短时间戳（只取后6位）+ status 以进一步缩短路径
            timestamp_short = str(int(time.time()))[-6:]
            status_temp_dir = os.path.join(task_results_dir, f"{status}_{timestamp_short}")
            os.makedirs(status_temp_dir, exist_ok=True)
            
            # 确保每个TData有唯一目录名
            used_names = set()
            
            try:
                for index, (file_path, file_name, info) in enumerate(files):
                    if file_type == "session":
                        # 复制session文件
                        dest_path = os.path.join(status_temp_dir, file_name)
                        shutil.copy2(file_path, dest_path)
                        print(f"📄 复制Session文件: {file_name}")
                        
                        # 查找对应的json文件
                        json_name = file_name.replace('.session', '.json')
                        json_path = os.path.join(os.path.dirname(file_path), json_name)
                        if os.path.exists(json_path):
                            json_dest = os.path.join(status_temp_dir, json_name)
                            shutil.copy2(json_path, json_dest)
                            print(f"📄 复制JSON文件: {json_name}")
                    
                    elif file_type == "tdata":
                        # 直接使用原始文件夹名称（通常是手机号）
                        original_name = file_name
                        
                        # 确保名称唯一性
                        unique_name = original_name
                        counter = 1
                        while unique_name in used_names:
                            unique_name = f"{original_name}_{counter}"
                            counter += 1
                        
                        used_names.add(unique_name)
                        
                        # 创建 +手机号/tdata/ 结构
                        phone_dir = os.path.join(status_temp_dir, unique_name)
                        target_dir = os.path.join(phone_dir, "tdata")
                        os.makedirs(target_dir, exist_ok=True)
                        
                        # 复制TData文件
                        if os.path.exists(file_path) and os.path.isdir(file_path):
                            for item in os.listdir(file_path):
                                item_path = os.path.join(file_path, item)
                                dest_path = os.path.join(target_dir, item)
                                if os.path.isdir(item_path):
                                    shutil.copytree(item_path, dest_path)
                                else:
                                    shutil.copy2(item_path, dest_path)
                            print(f"📂 复制TData: {unique_name}")
                
                # 创建ZIP文件
                zip_filename = f"{status}_{len(files)}个.zip"
                zip_path = os.path.join(task_results_dir, zip_filename)
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files_list in os.walk(status_temp_dir):
                        for file in files_list:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, status_temp_dir)
                            zipf.write(file_path, arcname)
                
                result_files.append((zip_path, status, len(files)))
                print(f"✅ 创建成功: {zip_filename}")
                
            except Exception as e:
                print(f"❌ 创建{status}结果文件失败: {e}")
            finally:
                # 清理临时状态目录
                if os.path.exists(status_temp_dir):
                    shutil.rmtree(status_temp_dir, ignore_errors=True)
        
        return result_files

# ================================
# 格式转换器
# ================================

class FormatConverter:
    """Tdata与Session格式互转器"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def generate_failure_files(self, tdata_path: str, tdata_name: str, error_message: str):
        """
        生成失败转换的session和JSON文件
        用于所有转换失败的情况
        """
        # 创建sessions目录用于存储所有转换的文件
        sessions_dir = os.path.join(os.getcwd(), "sessions")
        if not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir)
            print(f"📁 创建sessions目录: {sessions_dir}")
        
        phone = tdata_name
        
        # 生成失败的session文件
        failed_session_path = os.path.join(sessions_dir, f"{phone}.session")
        self.create_failed_session_file(failed_session_path, error_message)
        
        # 生成失败的JSON文件
        failed_json_data = self.generate_failed_json(phone, phone, error_message, tdata_name)
        failed_json_path = os.path.join(sessions_dir, f"{phone}.json")
        with open(failed_json_path, 'w', encoding='utf-8') as f:
            json.dump(failed_json_data, f, ensure_ascii=False, indent=2)
        
        print(f"❌ 转换失败，已生成失败标记文件: {tdata_name}")
        print(f"   📄 Session文件: sessions/{phone}.session")
        print(f"   📄 JSON文件: sessions/{phone}.json")
    
    def create_empty_session_file(self, session_path: str):
        """
        创建空的session文件占位符
        用于当临时session文件不存在时
        """
        try:
            # 创建一个空的SQLite数据库文件作为session文件
            # Telethon session文件是SQLite数据库格式
            import sqlite3
            conn = sqlite3.connect(session_path)
            cursor = conn.cursor()
            # 创建基本的Telethon session表结构
            cursor.execute('''
                CREATE TABLE sessions (
                    dc_id INTEGER PRIMARY KEY,
                    server_address TEXT,
                    port INTEGER,
                    auth_key BLOB
                )
            ''')
            cursor.execute('''
                CREATE TABLE entities (
                    id INTEGER PRIMARY KEY,
                    hash INTEGER NOT NULL,
                    username TEXT,
                    phone INTEGER,
                    name TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE sent_files (
                    md5_digest BLOB,
                    file_size INTEGER,
                    type INTEGER,
                    id INTEGER,
                    hash INTEGER,
                    PRIMARY KEY(md5_digest, file_size, type)
                )
            ''')
            cursor.execute('''
                CREATE TABLE update_state (
                    id INTEGER PRIMARY KEY,
                    pts INTEGER,
                    qts INTEGER,
                    date INTEGER,
                    seq INTEGER
                )
            ''')
            cursor.execute('''
                CREATE TABLE version (
                    version INTEGER PRIMARY KEY
                )
            ''')
            cursor.execute('INSERT INTO version VALUES (6)')
            conn.commit()
            conn.close()
            print(f"📄 创建空session文件: {os.path.basename(session_path)}")
        except Exception as e:
            print(f"⚠️ 创建空session文件失败: {e}")
    
    def create_failed_session_file(self, session_path: str, error_message: str):
        """
        创建失败标记的session文件
        用于转换失败的情况
        """
        self.create_empty_session_file(session_path)
        # 在同目录创建一个标记文件说明这是失败的session
        error_marker = session_path + ".error"
        try:
            with open(error_marker, 'w', encoding='utf-8') as f:
                f.write(f"转换失败: {error_message}\n")
                f.write(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        except:
            pass
    
    def generate_failed_json(self, phone: str, session_name: str, error_message: str, tdata_name: str) -> dict:
        """
        生成包含错误信息的JSON文件
        用于转换失败的情况
        """
        current_time = datetime.now()
        
        json_data = {
            "app_id": 2040,
            "app_hash": "b18441a1ff607e10a989891a5462e627",
            "sdk": "Windows 11",
            "device": "Desktop",
            "app_version": "6.1.4 x64",
            "lang_pack": "en",
            "system_lang_pack": "en-US",
            "twoFA": "",
            "role": None,
            "id": 0,
            "phone": phone,
            "username": None,
            "date_of_birth": None,
            "date_of_birth_integrity": None,
            "is_premium": False,
            "premium_expiry": None,
            "first_name": "",
            "last_name": None,
            "has_profile_pic": False,
            "spamblock": "unknown",
            "spamblock_end_date": None,
            "session_file": session_name,
            "stats_spam_count": 0,
            "stats_invites_count": 0,
            "last_connect_date": current_time.strftime('%Y-%m-%dT%H:%M:%S+0000'),
            "session_created_date": current_time.strftime('%Y-%m-%dT%H:%M:%S+0000'),
            "app_config_hash": None,
            "extra_params": "",
            "device_model": "Desktop",
            "user_id": 0,
            "ipv6": False,
            "register_time": None,
            "sex": None,
            "last_check_time": int(current_time.timestamp()),
            "device_token": "",
            "tz_offset": 0,
            "perf_cat": 2,
            "avatar": "img/default.png",
            "proxy": None,
            "block": False,
            "package_id": "",
            "installer": "",
            "email": "",
            "email_id": "",
            "secret": "",
            "category": "",
            "scam": False,
            "is_blocked": False,
            "voip_token": "",
            "last_reg_time": -62135596800,
            "has_password": False,
            "block_since_time": 0,
            "block_until_time": 0,
            "conversion_time": current_time.strftime('%Y-%m-%d %H:%M:%S'),
            "conversion_source": "TData",
            "conversion_status": "failed",
            "error_message": error_message,
            "original_tdata_name": tdata_name
        }
        
        return json_data
    
    async def generate_session_json(self, me, phone: str, session_name: str, output_dir: str) -> dict:
        """
        生成完整的Session JSON数据
        基于提供的JSON模板格式
        """
        current_time = datetime.now()
        
        # 从用户对象提取信息
        user_id = me.id if hasattr(me, 'id') else 0
        first_name = me.first_name if hasattr(me, 'first_name') and me.first_name else ""
        last_name = me.last_name if hasattr(me, 'last_name') and me.last_name else None
        username = me.username if hasattr(me, 'username') and me.username else None
        is_premium = me.premium if hasattr(me, 'premium') else False
        has_profile_pic = hasattr(me, 'photo') and me.photo is not None
        
        # 生成JSON数据(基于提供的模板)
        json_data = {
            "app_id": 2040,
            "app_hash": "b18441a1ff607e10a989891a5462e627",
            "sdk": "Windows 11",
            "device": "Desktop",
            "app_version": "6.1.4 x64",
            "lang_pack": "en",
            "system_lang_pack": "en-US",
            "twoFA": "",
            "role": None,
            "id": user_id,
            "phone": phone,
            "username": username,
            "date_of_birth": None,
            "date_of_birth_integrity": None,
            "is_premium": is_premium,
            "premium_expiry": None,
            "first_name": first_name,
            "last_name": last_name,
            "has_profile_pic": has_profile_pic,
            "spamblock": "free",
            "spamblock_end_date": None,
            "session_file": session_name,
            "stats_spam_count": 0,
            "stats_invites_count": 0,
            "last_connect_date": current_time.strftime('%Y-%m-%dT%H:%M:%S+0000'),
            "session_created_date": current_time.strftime('%Y-%m-%dT%H:%M:%S+0000'),
            "app_config_hash": None,
            "extra_params": "",
            "device_model": "Desktop",
            "user_id": user_id,
            "ipv6": False,
            "register_time": None,
            "sex": None,
            "last_check_time": int(current_time.timestamp()),
            "device_token": "",
            "tz_offset": 0,
            "perf_cat": 2,
            "avatar": "img/default.png",
            "proxy": None,
            "block": False,
            "package_id": "",
            "installer": "",
            "email": "",
            "email_id": "",
            "secret": "",
            "category": "",
            "scam": False,
            "is_blocked": False,
            "voip_token": "",
            "last_reg_time": -62135596800,
            "has_password": False,
            "block_since_time": 0,
            "block_until_time": 0,
            "conversion_time": current_time.strftime('%Y-%m-%d %H:%M:%S'),
            "conversion_source": "TData"
        }
        
        return json_data
    
    async def convert_tdata_to_session(self, tdata_path: str, tdata_name: str, api_id: int, api_hash: str) -> Tuple[str, str, str]:
        """
        将Tdata转换为Session
        返回: (状态, 信息, 账号名)
        """
        client = None
        session_file = None
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                if not OPENTELE_AVAILABLE:
                    error_msg = "opentele库未安装"
                    self.generate_failure_files(tdata_path, tdata_name, error_msg)
                    return "转换错误", error_msg, tdata_name
                
                print(f"🔄 尝试转换 {tdata_name} (尝试 {attempt + 1}/{max_retries})")
                
                # 加载TData
                tdesk = TDesktop(tdata_path)
                
                # 检查是否已授权
                if not tdesk.isLoaded():
                    print(f"❌ TData加载失败: {tdata_name}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        continue
                    error_msg = "TData未授权或无效"
                    self.generate_failure_files(tdata_path, tdata_name, error_msg)
                    return "转换错误", error_msg, tdata_name
                
                # 生成唯一的session名称以避免冲突
                unique_session_name = f"{tdata_name}_{int(time.time()*1000)}"
                session_file = f"{unique_session_name}.session"
                
                # 转换为Telethon Session (带超时)
                try:
                    client = await asyncio.wait_for(
                        tdesk.ToTelethon(
                            session=unique_session_name,
                            flag=UseCurrentSession,
                            api=API.TelegramDesktop
                        ),
                        timeout=30.0
                    )
                except asyncio.TimeoutError:
                    print(f"⏱️ TData转换超时: {tdata_name}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        continue
                    error_msg = "TData转换超时"
                    self.generate_failure_files(tdata_path, tdata_name, error_msg)
                    return "转换错误", error_msg, tdata_name
                
                # 连接并获取账号信息 (带超时)
                try:
                    await asyncio.wait_for(client.connect(), timeout=15.0)
                except asyncio.TimeoutError:
                    print(f"⏱️ 连接超时: {tdata_name}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        continue
                    error_msg = "连接超时"
                    self.generate_failure_files(tdata_path, tdata_name, error_msg)
                    return "转换错误", error_msg, tdata_name
                
                if not await client.is_user_authorized():
                    print(f"❌ 账号未授权: {tdata_name}")
                    error_msg = "账号未授权"
                    self.generate_failure_files(tdata_path, tdata_name, error_msg)
                    return "转换错误", error_msg, tdata_name
                
                # 获取完整用户信息
                me = await client.get_me()
                phone = me.phone if me.phone else "未知"
                username = me.username if me.username else "无用户名"
                
                # 重命名session文件为手机号
                final_session_name = phone if phone != "未知" else tdata_name
                final_session_file = f"{final_session_name}.session"
                
                # 确保连接关闭
                await client.disconnect()
                
                # 创建sessions目录用于存储所有转换的session文件
                sessions_dir = os.path.join(os.getcwd(), "sessions")
                if not os.path.exists(sessions_dir):
                    os.makedirs(sessions_dir)
                    print(f"📁 创建sessions目录: {sessions_dir}")
                
                # 重命名session文件
                # ToTelethon在当前工作目录创建session文件，而不是在tdata_path目录
                temp_session_path = os.path.join(os.getcwd(), session_file)
                final_session_path = os.path.join(sessions_dir, final_session_file)
                
                # 确保session文件总是被创建
                session_created = False
                if os.path.exists(temp_session_path):
                    # 如果目标文件已存在，先删除
                    if os.path.exists(final_session_path):
                        os.remove(final_session_path)
                    os.rename(temp_session_path, final_session_path)
                    session_created = True
                    
                    # 同时处理journal文件
                    temp_journal = temp_session_path + "-journal"
                    final_journal = final_session_path + "-journal"
                    if os.path.exists(temp_journal):
                        if os.path.exists(final_journal):
                            os.remove(final_journal)
                        os.rename(temp_journal, final_journal)
                else:
                    # 如果临时session文件不存在，创建一个空的session文件
                    print(f"⚠️ 临时session文件不存在，创建空session文件")
                    self.create_empty_session_file(final_session_path)
                    session_created = True
                
                # 生成完整的JSON文件
                json_data = await self.generate_session_json(me, phone, final_session_name, sessions_dir)
                json_path = os.path.join(sessions_dir, f"{final_session_name}.json")
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ 转换成功: {tdata_name} -> {phone}")
                print(f"   📄 Session文件: sessions/{final_session_file}")
                print(f"   📄 JSON文件: sessions/{final_session_name}.json")
                return "转换成功", f"手机号: {phone} | 用户名: @{username}", tdata_name
                
            except Exception as e:
                error_msg = str(e)
                print(f"❌ 转换错误 {tdata_name}: {error_msg}")
                
                # 清理临时文件
                if session_file:
                    try:
                        # ToTelethon在当前工作目录创建session文件
                        temp_session_path = os.path.join(os.getcwd(), session_file)
                        if os.path.exists(temp_session_path):
                            os.remove(temp_session_path)
                        temp_journal = temp_session_path + "-journal"
                        if os.path.exists(temp_journal):
                            os.remove(temp_journal)
                    except:
                        pass
                
                if attempt < max_retries - 1:
                    print(f"🔄 等待 {retry_delay} 秒后重试...")
                    await asyncio.sleep(retry_delay)
                    continue
                
                # 最后一次尝试失败，生成失败标记的文件
                # 确定错误类型和错误消息
                if "database is locked" in error_msg.lower():
                    final_error_msg = "TData文件被占用"
                elif "auth key" in error_msg.lower() or "authorization" in error_msg.lower():
                    final_error_msg = "授权密钥无效"
                elif "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                    final_error_msg = "连接超时"
                elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                    final_error_msg = "网络连接失败"
                else:
                    final_error_msg = f"转换失败: {error_msg[:50]}"
                
                self.generate_failure_files(tdata_path, tdata_name, final_error_msg)
                return "转换错误", final_error_msg, tdata_name
            finally:
                # 确保客户端连接关闭
                if client:
                    try:
                        await client.disconnect()
                    except:
                        pass
        
        # 如果到达这里说明所有重试都失败了
        error_msg = "多次重试后失败"
        self.generate_failure_files(tdata_path, tdata_name, error_msg)
        return "转换错误", error_msg, tdata_name
    
    async def convert_session_to_tdata(self, session_path: str, session_name: str, api_id: int, api_hash: str) -> Tuple[str, str, str]:
        """
        将Session转换为Tdata
        返回: (状态, 信息, 账号名)
        """
        try:
            if not OPENTELE_AVAILABLE:
                return "转换错误", "opentele库未安装", session_name
            
            # 创建Telethon客户端
            client = OpenTeleClient(session_path, api_id, api_hash)
            
            # 连接
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.disconnect()
                return "转换错误", "Session未授权", session_name
            
            # 获取账号信息
            me = await client.get_me()
            phone = me.phone if me.phone else "未知"
            username = me.username if me.username else "无用户名"
            
            # 转换为TData
            tdesk = await client.ToTDesktop(flag=UseCurrentSession)
            
            # 创建sessions目录用于存储所有转换的文件
            sessions_dir = os.path.join(os.getcwd(), "sessions")
            if not os.path.exists(sessions_dir):
                os.makedirs(sessions_dir)
                print(f"📁 创建sessions目录: {sessions_dir}")
            
            # 保存TData - 修改为: sessions/手机号/tdata/ 结构
            phone_dir = os.path.join(sessions_dir, phone)
            tdata_dir = os.path.join(phone_dir, "tdata")
            
            # 确保目录存在
            os.makedirs(phone_dir, exist_ok=True)
            
            tdesk.SaveTData(tdata_dir)
            
            await client.disconnect()
            
            return "转换成功", f"手机号: {phone} | 用户名: @{username}", session_name
            
        except Exception as e:
            error_msg = str(e)
            if "database is locked" in error_msg.lower():
                return "转换错误", "Session文件被占用", session_name
            elif "auth key" in error_msg.lower():
                return "转换错误", "授权密钥无效", session_name
            else:
                return "转换错误", f"转换失败: {error_msg[:50]}", session_name
    
    async def batch_convert_with_progress(self, files: List[Tuple[str, str]], conversion_type: str, 
                                         api_id: int, api_hash: str, update_callback) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        批量转换并提供实时进度更新
        conversion_type: "tdata_to_session" 或 "session_to_tdata"
        """
        results = {
            "转换成功": [],
            "转换错误": []
        }
        
        total = len(files)
        processed = 0
        start_time = time.time()
        last_update_time = 0
        
        # 线程安全的锁
        lock = asyncio.Lock()
        
        async def process_single_file(file_path, file_name):
            nonlocal processed, last_update_time
            
            # 为每个转换设置超时
            conversion_timeout = 60.0  # 每个文件最多60秒
            
            try:
                if conversion_type == "tdata_to_session":
                    status, info, name = await asyncio.wait_for(
                        self.convert_tdata_to_session(file_path, file_name, api_id, api_hash),
                        timeout=conversion_timeout
                    )
                else:  # session_to_tdata
                    status, info, name = await asyncio.wait_for(
                        self.convert_session_to_tdata(file_path, file_name, api_id, api_hash),
                        timeout=conversion_timeout
                    )
                
                async with lock:
                    results[status].append((file_path, file_name, info))
                    processed += 1
                    
                    print(f"✅ 转换完成 {processed}/{total}: {file_name} -> {status} | {info}")
                    
                    # 控制更新频率
                    current_time = time.time()
                    if current_time - last_update_time >= 2 or processed % 5 == 0 or processed == total:
                        elapsed = current_time - start_time
                        speed = processed / elapsed if elapsed > 0 else 0
                        
                        try:
                            await update_callback(processed, total, results, speed, elapsed)
                            last_update_time = current_time
                        except Exception as e:
                            print(f"⚠️ 更新回调失败: {e}")
                        
            except asyncio.TimeoutError:
                print(f"⏱️ 转换超时 {file_name}")
                async with lock:
                    results["转换错误"].append((file_path, file_name, "转换超时(60秒)"))
                    processed += 1
            except Exception as e:
                print(f"❌ 处理失败 {file_name}: {e}")
                async with lock:
                    results["转换错误"].append((file_path, file_name, f"异常: {str(e)[:50]}"))
                    processed += 1
        
        # 增加并发数以加快转换速度，从10提升到20
        batch_size = 20
        print(f"🚀 开始批量转换，并发数: {batch_size}")
        
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            tasks = [process_single_file(file_path, file_name) for file_path, file_name in batch]
            await asyncio.gather(*tasks, return_exceptions=True)
        
        return results
    
    def create_conversion_result_zips(self, results: Dict[str, List[Tuple[str, str, str]]], 
                                     task_id: str, conversion_type: str) -> List[Tuple[str, str, int]]:
        """创建转换结果ZIP文件（修正版）"""
        result_files = []
        
        # 根据转换类型确定文件名前缀
        if conversion_type == "tdata_to_session":
            success_prefix = "tdata转换session 成功"
            failure_prefix = "tdata转换session 失败"
        else:  # session_to_tdata
            success_prefix = "session转换tdata 成功"
            failure_prefix = "session转换tdata 失败"
        
        for status, files in results.items():
            if not files:
                continue
            
            # 优化路径长度：使用更短的时间戳和简化的目录结构
            timestamp_short = str(int(time.time()))[-6:]  # 只取后6位
            status_temp_dir = os.path.join(config.RESULTS_DIR, f"conv_{timestamp_short}_{status}")
            os.makedirs(status_temp_dir, exist_ok=True)
            
            try:
                for file_path, file_name, info in files:
                    if status == "转换成功":
                        if conversion_type == "tdata_to_session":
                            # Tdata转Session: 复制生成的session文件和JSON文件
                            sessions_dir = os.path.join(os.getcwd(), "sessions")
                            
                            # 从info中提取手机号
                            phone = "未知"
                            if "手机号:" in info:
                                phone_part = info.split("手机号:")[1].split("|")[0].strip()
                                phone = phone_part if phone_part else "未知"
                            
                            # Session文件应该保存在sessions目录下
                            session_file = f"{phone}.session"
                            session_path = os.path.join(sessions_dir, session_file)
                            
                            if os.path.exists(session_path):
                                dest_path = os.path.join(status_temp_dir, session_file)
                                shutil.copy2(session_path, dest_path)
                                print(f"📄 复制Session文件: {session_file}")
                            
                            # 复制对应的JSON文件
                            json_file = f"{phone}.json"
                            json_path = os.path.join(sessions_dir, json_file)
                            
                            if os.path.exists(json_path):
                                json_dest = os.path.join(status_temp_dir, json_file)
                                shutil.copy2(json_path, json_dest)
                                print(f"📄 复制JSON文件: {json_file}")
                        
                    
                        else:  # session_to_tdata - 修复路径问题
                            # 转换后的文件实际保存在sessions目录下，不是source_dir
                            sessions_dir = os.path.join(os.getcwd(), "sessions")
                            
                            # 从info中提取手机号
                            phone = "未知"
                            if "手机号:" in info:
                                phone_part = info.split("手机号:")[1].split("|")[0].strip()
                                phone = phone_part if phone_part else "未知"
                            
                            # 正确的路径：sessions/手机号/
                            phone_dir = os.path.join(sessions_dir, phone)
                            
                            if os.path.exists(phone_dir):
                                # 复制整个手机号目录结构
                                phone_dest = os.path.join(status_temp_dir, phone)
                                shutil.copytree(phone_dir, phone_dest)
                                print(f"📂 复制号码目录: {phone}/tdata/")
                                
                                # 将原始session和json文件复制到手机号目录下（与tdata同级）
                                if os.path.exists(file_path):
                                    session_dest = os.path.join(phone_dest, os.path.basename(file_path))
                                    shutil.copy2(file_path, session_dest)
                                    print(f"📄 复制原始Session: {os.path.basename(file_path)}")
                                
                                # 复制对应的json文件
                                json_name = file_name.replace('.session', '.json')
                                original_json = os.path.join(os.path.dirname(file_path), json_name)
                                if os.path.exists(original_json):
                                    json_dest = os.path.join(phone_dest, json_name)
                                    shutil.copy2(original_json, json_dest)
                                    print(f"📄 复制原始JSON: {json_name}")
                            else:
                                print(f"⚠️ 找不到转换后的目录: {phone_dir}")
                    
                    else:  # 转换错误 - 打包失败的文件
                        if conversion_type == "tdata_to_session":
                            if os.path.isdir(file_path):
                                dest_path = os.path.join(status_temp_dir, file_name)
                                shutil.copytree(file_path, dest_path)
                                print(f"📂 复制失败的TData: {file_name}")
                        else:
                            if os.path.exists(file_path):
                                dest_path = os.path.join(status_temp_dir, file_name)
                                shutil.copy2(file_path, dest_path)
                                print(f"📄 复制失败的Session: {file_name}")
                                
                                # 复制对应的json文件
                                json_name = file_name.replace('.session', '.json')
                                json_path = os.path.join(os.path.dirname(file_path), json_name)
                                if os.path.exists(json_path):
                                    json_dest = os.path.join(status_temp_dir, json_name)
                                    shutil.copy2(json_path, json_dest)
                                    print(f"📄 复制失败的JSON: {json_name}")
                        
                        # 创建详细的失败原因说明
                        error_file = os.path.join(status_temp_dir, f"{file_name}_错误原因.txt")
                        with open(error_file, 'w', encoding='utf-8') as f:
                            f.write(f"文件: {file_name}\n")
                            f.write(f"转换类型: {conversion_type}\n")
                            f.write(f"失败原因: {info}\n")
                            f.write(f"失败时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write(f"\n建议:\n")
                            if "授权" in info:
                                f.write("- 检查账号是否已登录\n")
                                f.write("- 验证TData文件是否有效\n")
                            elif "超时" in info:
                                f.write("- 检查网络连接\n")
                                f.write("- 尝试使用代理\n")
                            elif "占用" in info:
                                f.write("- 关闭其他使用该文件的程序\n")
                                f.write("- 重启后重试\n")
                
                # 创建 ZIP 文件 - 新格式
                if status == "转换成功":
                    zip_filename = f"{success_prefix}-{len(files)}.zip"
                else:
                    zip_filename = f"{failure_prefix}-{len(files)}.zip"
                
                zip_path = os.path.join(config.RESULTS_DIR, zip_filename)
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files_in_dir in os.walk(status_temp_dir):
                        for file in files_in_dir:
                            file_path_full = os.path.join(root, file)
                            arcname = os.path.relpath(file_path_full, status_temp_dir)
                            zipf.write(file_path_full, arcname)
                
                print(f"✅ 创建ZIP文件: {zip_filename}")
                
                # 创建 TXT 报告 - 新格式
                txt_filename = f"{success_prefix if status == '转换成功' else failure_prefix}-报告.txt"
                txt_path = os.path.join(config.RESULTS_DIR, txt_filename)
                
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(f"格式转换报告 - {status}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"转换类型: {conversion_type}\n")
                    f.write(f"总数: {len(files)}个\n\n")
                    
                    f.write("详细列表:\n")
                    f.write("-" * 50 + "\n\n")
                    
                    for idx, (file_path, file_name, info) in enumerate(files, 1):
                        f.write(f"{idx}. 文件: {file_name}\n")
                        f.write(f"   信息: {info}\n")
                        f.write(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                print(f"✅ 创建TXT报告: {txt_filename}")
                
                # ⚠️ 关键修复：返回 4 个值而不是 3 个
                result_files.append((zip_path, txt_path, status, len(files)))
                
            except Exception as e:
                print(f"❌ 创建{status}结果文件失败: {e}")
                import traceback
                traceback.print_exc()
            finally:
                if os.path.exists(status_temp_dir):
                    shutil.rmtree(status_temp_dir, ignore_errors=True)
        
        return result_files

# ================================
# 密码检测器（2FA）
# ================================

class PasswordDetector:
    """密码自动检测器 - 支持TData和Session格式"""
    
    def __init__(self):
        # TData格式的密码文件名（不区分大小写）
        self.tdata_password_files = ['2fa.txt', 'twofa.txt', 'password.txt']
        # Session JSON中的密码字段名
        self.session_password_fields = ['twoFA', '2fa', 'password', 'two_fa', 'twofa']
    
    def detect_tdata_password(self, tdata_path: str) -> Optional[str]:
        """
        检测TData格式中的密码
        
        Args:
            tdata_path: TData目录路径
            
        Returns:
            检测到的密码，如果未找到则返回None
        """
        try:
            # 检查D877F783D5D3EF8C目录
            d877_path = os.path.join(tdata_path, "D877F783D5D3EF8C")
            if not os.path.exists(d877_path):
                print(f"⚠️ TData目录结构无效: {tdata_path}")
                return None
            
            # 搜索密码文件
            for filename in self.tdata_password_files:
                # 尝试不同的大小写组合
                for root, dirs, files in os.walk(tdata_path):
                    for file in files:
                        if file.lower() == filename.lower():
                            password_file = os.path.join(root, file)
                            try:
                                with open(password_file, 'r', encoding='utf-8') as f:
                                    password = f.read().strip()
                                    if password:
                                        print(f"✅ 在TData中检测到密码文件: {file}")
                                        return password
                            except Exception as e:
                                print(f"⚠️ 读取密码文件失败 {file}: {e}")
                                continue
            
            print(f"ℹ️ 未在TData中找到密码文件")
            return None
            
        except Exception as e:
            print(f"❌ TData密码检测失败: {e}")
            return None
    
    def detect_session_password(self, json_path: str) -> Optional[str]:
        """
        检测Session JSON中的密码
        
        Args:
            json_path: JSON配置文件路径
            
        Returns:
            检测到的密码，如果未找到则返回None
        """
        try:
            if not os.path.exists(json_path):
                print(f"ℹ️ JSON文件不存在: {json_path}")
                return None
            
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 搜索密码字段
            for field_name in self.session_password_fields:
                if field_name in data:
                    password = data[field_name]
                    if password and isinstance(password, str) and password.strip():
                        # Security: Don't log actual password, only field name
                        print(f"✅ 在JSON中检测到密码字段: {field_name}")
                        return password.strip()
            
            print(f"ℹ️ 未在JSON中找到密码字段")
            return None
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return None
        except Exception as e:
            print(f"❌ Session密码检测失败: {e}")
            return None
    
    def detect_password(self, file_path: str, file_type: str) -> Optional[str]:
        """
        自动检测密码（根据文件类型）
        
        Args:
            file_path: 文件路径（TData目录或Session文件）
            file_type: 文件类型（'tdata' 或 'session'）
            
        Returns:
            检测到的密码，如果未找到则返回None
        """
        if file_type == 'tdata':
            return self.detect_tdata_password(file_path)
        elif file_type == 'session':
            # 对于session文件，尝试查找对应的JSON文件
            json_path = file_path.replace('.session', '.json')
            return self.detect_session_password(json_path)
        else:
            print(f"❌ 不支持的文件类型: {file_type}")
            return None

# ================================
# 二级密码管理器（2FA）
# ================================

class TwoFactorManager:
    """二级密码管理器 - 批量修改2FA密码"""
    
    def __init__(self, proxy_manager: ProxyManager, db: Database):
        self.proxy_manager = proxy_manager
        self.db = db
        self.password_detector = PasswordDetector()
        self.semaphore = asyncio.Semaphore(5)  # 限制并发数为5，避免过快
        # 用于存储待处理的2FA任务
        self.pending_2fa_tasks = {}  # {user_id: {'files': [...], 'file_type': '...', 'extract_dir': '...', 'task_id': '...'}}
    
    async def change_2fa_password(self, session_path: str, old_password: str, new_password: str, 
                                  account_name: str) -> Tuple[bool, str]:
        """
        修改单个账号的2FA密码
        
        Args:
            session_path: Session文件路径
            old_password: 旧密码
            new_password: 新密码
            account_name: 账号名称（用于日志）
            
        Returns:
            (是否成功, 详细信息)
        """
        if not TELETHON_AVAILABLE:
            return False, "Telethon未安装"
        
        async with self.semaphore:
            client = None
            proxy_dict = None
            proxy_used = "本地连接"
            
            try:
                # 尝试使用代理
                proxy_enabled = self.db.get_proxy_enabled() if self.db else True
                if config.USE_PROXY and proxy_enabled and self.proxy_manager.proxies:
                    proxy_info = self.proxy_manager.get_next_proxy()
                    if proxy_info:
                        proxy_dict = self.create_proxy_dict(proxy_info)
                        if proxy_dict:
                            proxy_used = f"代理 {proxy_info['host']}:{proxy_info['port']}"
                
                # 创建客户端
                client = TelegramClient(
                    session_path,
                    config.API_ID,
                    config.API_HASH,
                    timeout=30,
                    connection_retries=2,
                    retry_delay=1,
                    proxy=proxy_dict
                )
                
                # 连接
                await asyncio.wait_for(client.connect(), timeout=15)
                
                # 检查授权
                is_authorized = await asyncio.wait_for(client.is_user_authorized(), timeout=5)
                if not is_authorized:
                    return False, f"{proxy_used} | 账号未授权"
                
                # 获取用户信息
                try:
                    me = await asyncio.wait_for(client.get_me(), timeout=5)
                    user_info = f"ID:{me.id}"
                    if me.username:
                        user_info += f" @{me.username}"
                except Exception as e:
                    user_info = "账号"
                
                # 修改2FA密码 - 使用 Telethon 内置方法
                try:
                    # 使用 Telethon 的内置密码修改方法
                    result = await client.edit_2fa(
                        current_password=old_password if old_password else None,
                        new_password=new_password,
                        hint=f"Modified {datetime.now().strftime('%Y-%m-%d')}"
                    )
                    
                    # 修改成功后，更新文件中的密码
                    update_success = await self._update_password_files(
                        session_path, 
                        new_password, 
                        'session'
                    )
                    
                    if update_success:
                        return True, f"{user_info} | {proxy_used} | 密码修改成功，文件已更新"
                    else:
                        return True, f"{user_info} | {proxy_used} | 密码修改成功，但文件更新失败"
                    
                except AttributeError:
                    # 如果 edit_2fa 不存在，使用手动方法
                    return await self._change_2fa_manual(
                        client, session_path, old_password, new_password, 
                        user_info, proxy_used
                    )
                except Exception as e:
                    error_msg = str(e).lower()
                    if "password" in error_msg and "invalid" in error_msg:
                        return False, f"{user_info} | {proxy_used} | 旧密码错误"
                    elif "password" in error_msg and "incorrect" in error_msg:
                        return False, f"{user_info} | {proxy_used} | 旧密码不正确"
                    elif "flood" in error_msg:
                        return False, f"{user_info} | {proxy_used} | 操作过于频繁，请稍后重试"
                    else:
                        return False, f"{user_info} | {proxy_used} | 修改失败: {str(e)[:50]}"
                
            except Exception as e:
                error_msg = str(e).lower()
                if any(word in error_msg for word in ["timeout", "network", "connection"]):
                    return False, f"{proxy_used} | 网络连接失败"
                else:
                    return False, f"{proxy_used} | 错误: {str(e)[:50]}"
            finally:
                if client:
                    try:
                        await client.disconnect()
                    except:
                        pass
    
    async def _change_2fa_manual(self, client, session_path: str, old_password: str, 
                                 new_password: str, user_info: str, proxy_used: str) -> Tuple[bool, str]:
        """
        手动修改2FA密码（备用方法）
        """
        try:
            from telethon.tl.functions.account import GetPasswordRequest, UpdatePasswordSettingsRequest
            from telethon.tl.types import PasswordInputSettings
            
            # 获取密码配置
            pwd_info = await client(GetPasswordRequest())
            
            # 使用 Telethon 客户端的内置密码处理
            if old_password:
                password_bytes = old_password.encode('utf-8')
            else:
                password_bytes = b''
            
            # 生成新密码
            new_password_bytes = new_password.encode('utf-8')
            
            # 创建密码设置
            new_settings = PasswordInputSettings(
                new_password_hash=new_password_bytes,
                hint=f"Modified {datetime.now().strftime('%Y-%m-%d')}"
            )
            
            # 尝试更新
            await client(UpdatePasswordSettingsRequest(
                password=password_bytes,
                new_settings=new_settings
            ))
            
            # 更新文件
            update_success = await self._update_password_files(session_path, new_password, 'session')
            
            if update_success:
                return True, f"{user_info} | {proxy_used} | 密码修改成功，文件已更新"
            else:
                return True, f"{user_info} | {proxy_used} | 密码修改成功，但文件更新失败"
            
        except Exception as e:
            return False, f"{user_info} | {proxy_used} | 手动修改失败: {str(e)[:50]}"
    

    def create_proxy_dict(self, proxy_info: Dict) -> Optional[Dict]:
        """创建代理字典（复用SpamBotChecker的实现）"""
        if not proxy_info:
            return None
        
        try:
            if PROXY_SUPPORT:
                if proxy_info['type'] == 'socks5':
                    proxy_type = socks.SOCKS5
                elif proxy_info['type'] == 'socks4':
                    proxy_type = socks.SOCKS4
                else:
                    proxy_type = socks.HTTP
                
                proxy_dict = {
                    'proxy_type': proxy_type,
                    'addr': proxy_info['host'],
                    'port': proxy_info['port']
                }
                
                if proxy_info.get('username') and proxy_info.get('password'):
                    proxy_dict['username'] = proxy_info['username']
                    proxy_dict['password'] = proxy_info['password']
            else:
                proxy_dict = (proxy_info['host'], proxy_info['port'])
            
            return proxy_dict
            
        except Exception as e:
            print(f"❌ 创建代理配置失败: {e}")
            return None
    
    async def _update_password_files(self, file_path: str, new_password: str, file_type: str) -> bool:
        """
        更新文件中的密码
        
        Args:
            file_path: 文件路径（session或tdata路径）
            new_password: 新密码
            file_type: 文件类型（'session' 或 'tdata'）
            
        Returns:
            是否更新成功
        """
        try:
            if file_type == 'session':
                # 更新Session对应的JSON文件
                json_path = file_path.replace('.session', '.json')
                if os.path.exists(json_path):
                    try:
                        with open(json_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # 更新密码字段
                        updated = False
                        for field in ['twoFA', '2fa', 'password', 'two_fa', 'twofa']:
                            if field in data:
                                data[field] = new_password
                                updated = True
                                print(f"✅ 文件已更新: {os.path.basename(json_path)} - {field}字段已更新为新密码")
                                break
                        
                        if updated:
                            with open(json_path, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=2)
                            return True
                        else:
                            print(f"⚠️ JSON文件中未找到密码字段: {os.path.basename(json_path)}")
                            return False
                            
                    except Exception as e:
                        print(f"❌ 更新JSON文件失败 {os.path.basename(json_path)}: {e}")
                        return False
                else:
                    print(f"⚠️ JSON文件不存在: {json_path}")
                    return False
                    
            elif file_type == 'tdata':
                # 更新TData目录中的密码文件
                d877_path = os.path.join(file_path, "D877F783D5D3EF8C")
                if not os.path.exists(d877_path):
                    print(f"⚠️ TData目录结构无效: {file_path}")
                    return False
                
                updated = False
                found_files = []
                
                # 方法1: 在整个 tdata 目录搜索现有密码文件
                for password_file_name in ['2fa.txt', 'twofa.txt', 'password.txt']:
                    for root, dirs, files in os.walk(file_path):
                        for file in files:
                            if file.lower() == password_file_name.lower():
                                password_file = os.path.join(root, file)
                                try:
                                    with open(password_file, 'w', encoding='utf-8') as f:
                                        f.write(new_password)
                                    print(f"✅ TData密码文件已更新: {file}")
                                    found_files.append(file)
                                    updated = True
                                except Exception as e:
                                    print(f"❌ 更新密码文件失败 {file}: {e}")
                
                # 方法2: 如果没有找到任何密码文件，创建新的 2fa.txt（与 tdata 同级）
                if not found_files:
                    try:
                        # 获取 tdata 的父目录（与 tdata 同级）
                        parent_dir = os.path.dirname(file_path)
                        new_password_file = os.path.join(parent_dir, "2fa.txt")
                        
                        with open(new_password_file, 'w', encoding='utf-8') as f:
                            f.write(new_password)
                        print(f"✅ TData密码文件已创建: 2fa.txt (位置: 与 tdata 目录同级)")
                        updated = True
                    except Exception as e:
                        print(f"❌ 创建密码文件失败: {e}")
                
                return updated
            
            return False
            
        except Exception as e:
            print(f"❌ 更新文件密码失败: {e}")
            return False
    
    async def batch_change_passwords(self, files: List[Tuple[str, str]], file_type: str, 
                                    old_password: Optional[str], new_password: str,
                                    progress_callback=None) -> Dict[str, List[Tuple[str, str, str]]]:
        """
        批量修改密码
        
        Args:
            files: 文件列表 [(路径, 名称), ...]
            file_type: 文件类型（'tdata' 或 'session'）
            old_password: 手动输入的旧密码（备选）
            new_password: 新密码
            progress_callback: 进度回调函数
            
        Returns:
            结果字典 {'成功': [...], '失败': [...]}
        """
        results = {
            "成功": [],
            "失败": []
        }
        
        total = len(files)
        processed = 0
        start_time = time.time()
        
        async def process_single_file(file_path, file_name):
            nonlocal processed
            try:
                # 1. 如果是 TData 格式，需要先转换为 Session
                if file_type == 'tdata':
                    print(f"🔄 TData格式需要先转换为Session: {file_name}")
                    
                    # 使用 FormatConverter 转换
                    converter = FormatConverter(self.db)
                    status, info, name = await converter.convert_tdata_to_session(
                        file_path, 
                        file_name,
                        config.API_ID,
                        config.API_HASH
                    )
                    
                    if status != "转换成功":
                        results["失败"].append((file_path, file_name, f"转换失败: {info}"))
                        processed += 1
                        return
                    
                    # 转换成功，使用生成的 session 文件
                    sessions_dir = os.path.join(os.getcwd(), "sessions")
                    phone = file_name  # TData 的名称通常是手机号
                    session_path = os.path.join(sessions_dir, f"{phone}.session")
                    
                    if not os.path.exists(session_path):
                        results["失败"].append((file_path, file_name, "转换后的Session文件未找到"))
                        processed += 1
                        return
                    
                    print(f"✅ TData已转换为Session: {phone}.session")
                    actual_file_path = session_path
                    actual_file_type = 'session'
                else:
                    actual_file_path = file_path
                    actual_file_type = file_type
                
                # 2. 尝试自动检测密码
                detected_password = self.password_detector.detect_password(file_path, file_type)
                
                # 3. 如果检测失败，使用手动输入的备选密码
                current_old_password = detected_password if detected_password else old_password
                
                if not current_old_password:
                    results["失败"].append((file_path, file_name, "未找到旧密码"))
                    processed += 1
                    return
                
                # 4. 修改密码（使用 Session 格式）
                success, info = await self.change_2fa_password(
                    actual_file_path, current_old_password, new_password, file_name
                )
                
                if success:
                    # 如果原始是 TData，需要更新原始 TData 文件
                    if file_type == 'tdata':
                        tdata_update = await self._update_password_files(
                            file_path, new_password, 'tdata'
                        )
                        if tdata_update:
                            info += " | TData文件已更新"
                    
                    results["成功"].append((file_path, file_name, info))
                    print(f"✅ 修改成功 {processed + 1}/{total}: {file_name}")
                else:
                    results["失败"].append((file_path, file_name, info))
                    print(f"❌ 修改失败 {processed + 1}/{total}: {file_name} - {info}")
                
                processed += 1
                
                # 调用进度回调
                if progress_callback:
                    elapsed = time.time() - start_time
                    speed = processed / elapsed if elapsed > 0 else 0
                    await progress_callback(processed, total, results, speed, elapsed)
                
            except Exception as e:
                results["失败"].append((file_path, file_name, f"异常: {str(e)[:50]}"))
                processed += 1
                print(f"❌ 处理失败 {processed}/{total}: {file_name} - {str(e)}")
        
        # 批量并发处理（限制并发数）
        batch_size = 5
        for i in range(0, len(files), batch_size):
            batch = files[i:i + batch_size]
            tasks = [process_single_file(file_path, file_name) for file_path, file_name in batch]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # 批次间短暂休息
            await asyncio.sleep(0.5)
        
        return results
    
    def create_result_files(self, results: Dict, task_id: str, file_type: str = 'session') -> List[Tuple[str, str, str, int]]:
        """
        创建结果文件（修复版 - 分离 ZIP 和 TXT）
        
        Returns:
            [(zip文件路径, txt文件路径, 状态名称, 数量), ...]
        """
        result_files = []
        
        for status, items in results.items():
            if not items:
                continue
            
            print(f"📦 正在创建 {status} 结果文件，包含 {len(items)} 个账号")
            
            # 为每个状态创建唯一的临时目录
            timestamp_short = str(int(time.time()))[-6:]
            status_temp_dir = os.path.join(config.RESULTS_DIR, f"{status}_{timestamp_short}")
            os.makedirs(status_temp_dir, exist_ok=True)
            
            # 确保每个账号有唯一目录名
            used_names = set()
            
            try:
                for index, (file_path, file_name, info) in enumerate(items):
                    if file_type == "session":
                        # 复制 session 文件
                        dest_path = os.path.join(status_temp_dir, file_name)
                        if os.path.exists(file_path):
                            shutil.copy2(file_path, dest_path)
                            print(f"📄 复制Session文件: {file_name}")
                        
                        # 查找对应的 json 文件
                        json_name = file_name.replace('.session', '.json')
                        json_path = os.path.join(os.path.dirname(file_path), json_name)
                        if os.path.exists(json_path):
                            json_dest = os.path.join(status_temp_dir, json_name)
                            shutil.copy2(json_path, json_dest)
                            print(f"📄 复制JSON文件: {json_name}")
                    
                    elif file_type == "tdata":
                        # 使用原始文件夹名称（通常是手机号）
                        original_name = file_name
                        
                        # 确保名称唯一性
                        unique_name = original_name
                        counter = 1
                        while unique_name in used_names:
                            unique_name = f"{original_name}_{counter}"
                            counter += 1
                        
                        used_names.add(unique_name)
                        
                        # 创建 手机号/ 目录（与转换模块一致）
                        phone_dir = os.path.join(status_temp_dir, unique_name)
                        os.makedirs(phone_dir, exist_ok=True)
                        
                        # 1. 复制 tdata 目录
                        target_dir = os.path.join(phone_dir, "tdata")
                        
                        # 复制 TData 文件（使用正确的递归复制）
                        if os.path.exists(file_path) and os.path.isdir(file_path):
                            # 遍历 TData 目录
                            for item in os.listdir(file_path):
                                item_path = os.path.join(file_path, item)
                                dest_item_path = os.path.join(target_dir, item)
                                
                                if os.path.isdir(item_path):
                                    # 递归复制目录
                                    shutil.copytree(item_path, dest_item_path, dirs_exist_ok=True)
                                else:
                                    # 复制文件
                                    os.makedirs(target_dir, exist_ok=True)
                                    shutil.copy2(item_path, dest_item_path)
                            
                            print(f"📂 复制TData: {unique_name}/tdata/")
                        
                        # 2. 复制密码文件（从 tdata 的父目录，即与 tdata 同级）
                        parent_dir = os.path.dirname(file_path)
                        for password_file_name in ['2fa.txt', 'twofa.txt', 'password.txt']:
                            password_file_path = os.path.join(parent_dir, password_file_name)
                            if os.path.exists(password_file_path):
                                # 复制到 手机号/ 目录下（与 tdata 同级）
                                dest_password_path = os.path.join(phone_dir, password_file_name)
                                shutil.copy2(password_file_path, dest_password_path)
                                print(f"📄 复制密码文件: {unique_name}/{password_file_name}")
                
                # 创建 ZIP 文件 - 新格式
                zip_filename = f"修改2FA_{status}_{len(items)}个.zip"
                zip_path = os.path.join(config.RESULTS_DIR, zip_filename)
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files_list in os.walk(status_temp_dir):
                        for file in files_list:
                            file_path_full = os.path.join(root, file)
                            # 使用相对路径，避免重复
                            arcname = os.path.relpath(file_path_full, status_temp_dir)
                            zipf.write(file_path_full, arcname)
                
                print(f"✅ 创建ZIP文件: {zip_filename}")
                
                # 创建 TXT 报告 - 新格式
                txt_filename = f"修改2FA_{status}_{len(items)}个_报告.txt"
                txt_path = os.path.join(config.RESULTS_DIR, txt_filename)
                
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(f"2FA密码修改报告 - {status}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"总数: {len(items)}个\n\n")
                    f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    
                    f.write("详细列表:\n")
                    f.write("-" * 50 + "\n\n")
                    
                    for idx, (file_path, file_name, info) in enumerate(items, 1):
                        f.write(f"{idx}. 账号: {file_name}\n")
                        f.write(f"   详细信息: {info}\n")
                        f.write(f"   处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    
                    # 如果是失败列表，添加解决方案
                    if status == "失败":
                        f.write("\n" + "=" * 50 + "\n")
                        f.write("失败原因分析和解决方案:\n")
                        f.write("-" * 50 + "\n\n")
                        f.write("1. 账号未授权\n")
                        f.write("   - TData文件可能未登录或已失效\n")
                        f.write("   - 建议重新登录账号\n\n")
                        f.write("2. 旧密码错误\n")
                        f.write("   - 检查密码文件内容是否正确\n")
                        f.write("   - 确认JSON中的密码字段是否准确\n\n")
                        f.write("3. 网络连接失败\n")
                        f.write("   - 检查代理设置是否正确\n")
                        f.write("   - 尝试使用本地连接或更换代理\n\n")
                
                print(f"✅ 创建TXT报告: {txt_filename}")
                
                result_files.append((zip_path, txt_path, status, len(items)))
                
            except Exception as e:
                print(f"❌ 创建{status}结果文件失败: {e}")
                import traceback
                traceback.print_exc()
            finally:
                # 清理临时目录
                if os.path.exists(status_temp_dir):
                    shutil.rmtree(status_temp_dir, ignore_errors=True)
        
        return result_files
    
    def cleanup_expired_tasks(self, timeout_seconds: int = 300):
        """
        清理过期的待处理任务（默认5分钟超时）
        
        Args:
            timeout_seconds: 超时时间（秒）
        """
        current_time = time.time()
        expired_users = []
        
        for user_id, task_info in self.pending_2fa_tasks.items():
            task_start_time = task_info.get('start_time', 0)
            if current_time - task_start_time > timeout_seconds:
                expired_users.append(user_id)
        
        # 清理过期任务
        for user_id in expired_users:
            task_info = self.pending_2fa_tasks[user_id]
            
            # 清理临时文件
            extract_dir = task_info.get('extract_dir')
            temp_zip = task_info.get('temp_zip')
            
            if extract_dir and os.path.exists(extract_dir):
                try:
                    shutil.rmtree(extract_dir, ignore_errors=True)
                    print(f"🗑️ 清理过期任务的解压目录: {extract_dir}")
                except:
                    pass
            
            if temp_zip and os.path.exists(temp_zip):
                try:
                    shutil.rmtree(os.path.dirname(temp_zip), ignore_errors=True)
                    print(f"🗑️ 清理过期任务的临时文件: {temp_zip}")
                except:
                    pass
            
            # 删除任务信息
            del self.pending_2fa_tasks[user_id]
            print(f"⏰ 清理过期任务: user_id={user_id}")

# ================================
# 统一版 APIFormatConverter（Python 3.8/3.9 缩进已对齐）
# ================================
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta, timezone
import os, shutil, time, threading

class APIFormatConverter:
    def __init__(self, *args, **kwargs):
        """
        支持无参/带参：
          APIFormatConverter()
          APIFormatConverter(db)
          APIFormatConverter(db, base_url)
          APIFormatConverter(db=db, base_url=base_url)
        """
        db = kwargs.pop('db', None)
        base_url = kwargs.pop('base_url', None)
        if len(args) >= 1 and db is None:
            db = args[0]
        if len(args) >= 2 and base_url is None:
            base_url = args[1]

        self.db = db
        self.base_url = (base_url or os.getenv("BASE_URL") or "http://127.0.0.1:8080").rstrip('/')

        # 运行态
        self.flask_app = None
        self.active_sessions = {}
        self.code_watchers: Dict[str, threading.Thread] = {}
        self.fresh_watch: Dict[str, bool] = {}          # 是否 fresh（由刷新触发）
        self.history_window_sec: Dict[str, int] = {}    # fresh 时回扫窗口（秒）

        # DB 表结构
        try:
            self.init_api_database()
        except Exception as e:
            print("⚠️ 初始化API数据库时出错: %s" % e)

        print("🔗 API格式转换器已初始化，BASE_URL=%s, db=%s" % (self.base_url, "OK" if self.db else "None"))

    # ---------- DB 初始化/迁移 ----------
    def init_api_database(self):
        import sqlite3
        conn = sqlite3.connect(self.db.db_name)
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS api_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT UNIQUE,
                api_key TEXT UNIQUE,
                verification_url TEXT,
                two_fa_password TEXT,
                session_data TEXT,
                tdata_path TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT,
                last_used TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS verification_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT,
                code TEXT,
                code_type TEXT,
                received_at TEXT,
                used INTEGER DEFAULT 0,
                expires_at TEXT
            )
        """)

        # 迁移缺列
        def ensure_col(col, ddl):
            c.execute("PRAGMA table_info(api_accounts)")
            cols = [r[1] for r in c.fetchall()]
            if col not in cols:
                c.execute("ALTER TABLE api_accounts ADD COLUMN %s" % ddl)

        ensure_col("verification_url", "verification_url TEXT")
        ensure_col("two_fa_password", "two_fa_password TEXT")
        ensure_col("session_data", "session_data TEXT")
        ensure_col("tdata_path", "tdata_path TEXT")
        ensure_col("status", "status TEXT DEFAULT 'active'")
        ensure_col("created_at", "created_at TEXT")
        ensure_col("last_used", "last_used TEXT")

        conn.commit()
        conn.close()
        print("✅ API数据库表检查/迁移完成")

    # ---------- 工具 ----------
    def mark_all_codes_used(self, phone: str):
        import sqlite3
        conn = sqlite3.connect(self.db.db_name)
        c = conn.cursor()
        c.execute("UPDATE verification_codes SET used = 1 WHERE phone = ? AND used = 0", (phone,))
        conn.commit()
        conn.close()

    def generate_api_key(self, phone: str) -> str:
        import hashlib, uuid
        data = "%s_%s" % (phone, uuid.uuid4())
        return hashlib.sha256(data.encode()).hexdigest()[:32]

    def generate_verification_url(self, api_key: str) -> str:
        return "%s/verify/%s" % (self.base_url, api_key)

    def save_api_account(
        self,
        phone: str,
        api_key: str,
        verification_url: str,
        two_fa_password: str,
        session_data: str,
        tdata_path: str,
        account_info: dict
    ):
        import sqlite3
        conn = sqlite3.connect(self.db.db_name)
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO api_accounts
            (phone, api_key, verification_url, two_fa_password, session_data, tdata_path, status, created_at, last_used)
            VALUES(?, ?, ?, ?, ?, ?, 'active', ?, ?)
        """, (
            phone, api_key, verification_url, two_fa_password or "", session_data or "", tdata_path or "",
            datetime.now().isoformat(), datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

    def get_account_by_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        import sqlite3
        conn = sqlite3.connect(self.db.db_name)
        c = conn.cursor()
        c.execute("""
            SELECT phone, api_key, verification_url, two_fa_password, session_data, tdata_path
            FROM api_accounts WHERE api_key=?
        """, (api_key,))
        row = c.fetchone()
        conn.close()
        if not row:
            return None
        return {
            "phone": row[0],
            "api_key": row[1],
            "verification_url": row[2],
            "two_fa_password": row[3] or "",
            "session_data": row[4] or "",
            "tdata_path": row[5] or ""
        }

    def save_verification_code(self, phone: str, code: str, code_type: str):
        import sqlite3
        conn = sqlite3.connect(self.db.db_name)
        c = conn.cursor()
        expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()
        c.execute("""
            INSERT INTO verification_codes (phone, code, code_type, received_at, expires_at)
            VALUES (?, ?, ?, ?, ?)
        """, (phone, code, code_type, datetime.now().isoformat(), expires_at))
        conn.commit()
        conn.close()
        print("📱 收到验证码: %s - %s" % (phone, code))

    def get_latest_verification_code(self, phone: str) -> Optional[Dict[str, Any]]:
        import sqlite3
        conn = sqlite3.connect(self.db.db_name)
        c = conn.cursor()
        c.execute("""
            SELECT code, code_type, received_at
            FROM verification_codes
            WHERE phone=? AND used=0 AND expires_at > ?
            ORDER BY received_at DESC
            LIMIT 1
        """, (phone, datetime.now().isoformat()))
        row = c.fetchone()
        conn.close()
        if not row:
            return None
        return {"code": row[0], "code_type": row[1], "received_at": row[2]}

    # ---------- 账号信息提取 ----------
    async def extract_account_info_from_session(self, session_file: str) -> dict:
        """从Session文件提取账号信息"""
        try:
            client = TelegramClient(session_file, config.API_ID, config.API_HASH)
            await client.connect()
            
            if not await client.is_user_authorized():
                await client.disconnect()
                return {"error": "Session未授权"}
            
            me = await client.get_me()
            await client.disconnect()
            
            return {
                "phone": me.phone if me.phone else "unknown",
                "user_id": me.id
            }
            
        except Exception as e:
            return {"error": f"提取失败: {str(e)}"}
    async def extract_account_info_from_tdata(self, tdata_path: str) -> dict:
        if not OPENTELE_AVAILABLE:
            return {"error": "opentele库未安装"}
        try:
            tdesk = TDesktop(tdata_path)
            if not tdesk.isLoaded():
                return {"error": "TData未授权或无效"}
            temp_session = "temp_api_%d" % int(time.time())
            client = await tdesk.ToTelethon(session=temp_session, flag=UseCurrentSession)
            await client.connect()
            me = await client.get_me()
            await client.disconnect()
            # 清理临时session
            for suf in (".session", ".session-journal"):
                p = "%s%s" % (temp_session, suf)
                if os.path.exists(p):
                    try:
                        os.remove(p)
                    except Exception:
                        pass
            return {
                "phone": me.phone,
                "user_id": me.id,
                "username": me.username,
                "first_name": me.first_name,
                "last_name": me.last_name,
                "is_premium": getattr(me, 'premium', False)
            }
        except Exception as e:
            return {"error": "提取失败: %s" % str(e)}

    # ---------- 阶段2：转换为 API 并持久化复制 ----------
    async def convert_to_api_format(
        self,
        files: List[Tuple[str, str]],
        file_type: str,
        override_two_fa: Optional[str] = None
    ) -> List[dict]:
        api_accounts = []
        password_detector = PasswordDetector()
        sessions_dir = os.path.join(os.getcwd(), "sessions")
        os.makedirs(sessions_dir, exist_ok=True)

        for file_path, file_name in files:
            try:
                if file_type == "session":
                    info = await self.extract_account_info_from_session(file_path)
                else:
                    info = await self.extract_account_info_from_tdata(file_path)

                if "error" in info:
                    print("❌ 提取失败: %s - %s" % (file_name, info["error"]))
                    continue

                phone = info.get("phone")
                if not phone:
                    print("⚠️ 无法获取手机号: %s" % file_name)
                    continue

                two_fa = override_two_fa or (password_detector.detect_password(file_path, file_type) or "")

                persisted_session = ""
                persisted_tdata = ""

                if file_type == "session":
                    dest = os.path.join(sessions_dir, "%s.session" % phone)
                    try:
                        shutil.copy2(file_path, dest)
                    except Exception:
                        try:
                            if os.path.exists(dest):
                                os.remove(dest)
                            shutil.copy2(file_path, dest)
                        except Exception as e2:
                            print("❌ 复制session失败: %s" % e2)
                            continue
                    persisted_session = dest
                    json_src = file_path.replace(".session", ".json")
                    if os.path.exists(json_src):
                        try:
                            shutil.copy2(json_src, os.path.join(sessions_dir, "%s.json" % phone))
                        except Exception:
                            pass
                else:
                    phone_dir = os.path.join(sessions_dir, phone)
                    tdest = os.path.join(phone_dir, "tdata")
                    try:
                        if os.path.exists(tdest):
                            shutil.rmtree(tdest, ignore_errors=True)
                        os.makedirs(phone_dir, exist_ok=True)
                        shutil.copytree(file_path, tdest)
                    except Exception as e:
                        print("❌ 复制TData失败: %s" % e)
                        continue
                    persisted_tdata = tdest

                api_key = self.generate_api_key(phone)
                vurl = self.generate_verification_url(api_key)

                self.save_api_account(
                    phone=phone,
                    api_key=api_key,
                    verification_url=vurl,
                    two_fa_password=two_fa,
                    session_data=persisted_session,
                    tdata_path=persisted_tdata,
                    account_info=info
                )

                api_accounts.append({
                    "phone": phone,
                    "api_key": api_key,
                    "verification_url": vurl,
                    "two_fa_password": two_fa,
                    "account_info": info,
                    "created_at": datetime.now().isoformat(),
                    "format_version": "1.0"
                })
                print("✅ 转换成功: %s -> %s" % (phone, vurl))
            except Exception as e:
                print("❌ 处理失败: %s - %s" % (file_name, e))
                continue

        return api_accounts

    def create_api_result_files(self, api_accounts: List[dict], task_id: str) -> List[str]:
        out_dir = os.path.join(os.getcwd(), "api_results")
        os.makedirs(out_dir, exist_ok=True)
        out_txt = os.path.join(out_dir, f"TG_API_{len(api_accounts)}个账号.txt")
        with open(out_txt, "w", encoding="utf-8") as f:
            for it in (api_accounts or []):
                f.write("%s\t%s\n" % (it["phone"], it["verification_url"]))
        return [out_txt]

    # ---------- 自动监听 777000 ----------
    def start_code_watch(self, api_key: str, timeout: int = 300, fresh: bool = False, history_window_sec: int = 0):
        try:
            acc = self.get_account_by_api_key(api_key)
            if not acc:
                return False, "无效的API密钥"

            # 记录模式与回扫窗口；fresh 时清未用旧码
            self.fresh_watch[api_key] = bool(fresh)
            self.history_window_sec[api_key] = int(history_window_sec or 0)
            if fresh:
                try:
                    self.mark_all_codes_used(acc.get("phone", ""))
                except Exception:
                    pass

            # 已在监听则不重复启动（但已更新 fresh/window 配置）
            if api_key in self.code_watchers and self.code_watchers[api_key].is_alive():
                return True, "已在监听"

            def runner():
                import asyncio
                asyncio.run(self._watch_code_async(acc, timeout=timeout, api_key=api_key))

            th = threading.Thread(target=runner, daemon=True)
            self.code_watchers[api_key] = th
            th.start()
            return True, "已开始监听"
        except Exception as e:
            return False, "启动失败: %s" % e

    async def _watch_code_async(self, acc: Dict[str, Any], timeout: int = 300, api_key: str = ""):
        if not TELETHON_AVAILABLE:
            print("❌ Telethon 未安装，自动监听不可用")
            return

        phone = acc.get("phone", "")
        session_path = acc.get("session_data") or ""
        tdata_path = acc.get("tdata_path") or ""

        client = None
        temp_session_name = None
        try:
            is_fresh = bool(self.fresh_watch.get(api_key, False))
            window_sec = int(self.history_window_sec.get(api_key, 0) or 0)  # 刷新后回扫窗口（秒）

            if session_path and os.path.exists(session_path):
                client = TelegramClient(session_path, config.API_ID, config.API_HASH)
            elif tdata_path and os.path.exists(tdata_path) and OPENTELE_AVAILABLE:
                tdesk = TDesktop(tdata_path)
                if not tdesk.isLoaded():
                    print("⚠️ TData 无法加载: %s" % phone)
                    return
                temp_session_name = "watch_%s_%d" % (phone, int(time.time()))
                client = await tdesk.ToTelethon(session=temp_session_name, flag=UseCurrentSession, api=API.TelegramDesktop)
            else:
                print("⚠️ 无可用会话（缺少 session 或 tdata），放弃监听: %s" % phone)
                return

            await client.connect()
            if not await client.is_user_authorized():
                print("⚠️ 会话未授权: %s" % phone)
                await client.disconnect()
                return

            import re as _re
            import asyncio as _aio
            from telethon import events

            def extract_code(text: str):
                if not text:
                    return None
                m = _re.search(r"\b(\d{5,6})\b", text)
                if m:
                    return m.group(1)
                digits = _re.findall(r"\d", text)
                if len(digits) >= 6:
                    return "".join(digits[:6])
                if len(digits) >= 5:
                    return "".join(digits[:5])
                return None

            # 历史回扫：fresh 模式仅回扫最近 window_sec；否则回扫10分钟内
            try:
                entity = await client.get_entity(777000)
                if is_fresh and window_sec > 0:
                    cutoff = datetime.now(timezone.utc) - timedelta(seconds=window_sec)
                    async for msg in client.iter_messages(entity, limit=10):
                        msg_dt = msg.date
                        if msg_dt.tzinfo is None:
                            msg_dt = msg_dt.replace(tzinfo=timezone.utc)
                        if msg_dt >= cutoff:
                            code = extract_code(getattr(msg, "raw_text", "") or getattr(msg, "message", ""))
                            if code:
                                self.save_verification_code(phone, code, "app")
                                return
                elif not is_fresh:
                    async for msg in client.iter_messages(entity, limit=5):
                        msg_dt = msg.date
                        if msg_dt.tzinfo is None:
                            msg_dt = msg_dt.replace(tzinfo=timezone.utc)
                        if datetime.now(timezone.utc) - msg_dt <= timedelta(minutes=10):
                            code = extract_code(getattr(msg, "raw_text", "") or getattr(msg, "message", ""))
                            if code:
                                self.save_verification_code(phone, code, "app")
                                return
            except Exception as e:
                print("⚠️ 历史读取失败: %s" % e)

            got = _aio.Event()

            @client.on(events.NewMessage(from_users=777000))
            async def on_code(evt):
                code = extract_code(evt.raw_text or "")
                # 预处理文本避免 f-string 里的反斜杠问题
                n_preview = (evt.raw_text or "")
                n_preview = n_preview.replace("\n", " ")
                n_preview = n_preview[:120]
                print("[WATCH] new msg: %s | code=%s" % (n_preview, code))
                if code:
                    self.save_verification_code(phone, code, "app")
                    got.set()

            try:
                await _aio.wait_for(got.wait(), timeout=timeout)
            except _aio.TimeoutError:
                print("⏱️ 监听超时（%ds）: %s" % (timeout, phone))
        except Exception as e:
            print("❌ 监听异常 %s: %s" % (phone, e))
        finally:
            if client:
                try:
                    await client.disconnect()
                except Exception:
                    pass
            if temp_session_name:
                for suf in (".session", ".session-journal"):
                    p = "%s%s" % (temp_session_name, suf)
                    try:
                        if os.path.exists(p):
                            os.remove(p)
                    except Exception:
                        pass

    # ---------- Web ----------
def start_web_server(self):
    # 不依赖外部 FLASK_AVAILABLE 变量，直接按需导入
    try:
        from flask import Flask, jsonify, request, render_template_string
    except Exception as e:
        print("❌ Flask 未安装或导入失败: %s" % e)
        return

    if getattr(self, "flask_app", None):
        # 已经启动过
        return

    self.flask_app = Flask(__name__)

    @self.flask_app.route('/verify/<api_key>')
    def verification_page(api_key):
        try:
            account = self.get_account_by_api_key(api_key)
            if not account:
                return "❌ 无效的API密钥", 404

            # 若类里有自定义模板方法则调用；否则使用最简模板兜底，避免 500
            if hasattr(self, "render_verification_template"):
                return self.render_verification_template(
                    account['phone'],
                    api_key,
                    account.get('two_fa_password') or ""
                )

            minimal = r'''<!doctype html><meta charset="utf-8">
<title>Verify {{phone}}</title>
<div style="font-family:system-ui;padding:24px;background:#0b0f14;color:#e5e7eb">
  <h2 style="margin:0 0 8px">Top9 验证码接收</h2>
  <div>Phone: {{phone}}</div>
  <div id="status" style="margin:12px 0;padding:10px;border:1px solid #243244;border-radius:8px">读取验证码中…</div>
  <div id="code" style="font-size:40px;font-weight:800;letter-spacing:6px"></div>
</div>
<script>
fetch('/api/start_watch/{{api_key}}',{method:'POST'}).catch(()=>{});
function tick(){
  fetch('/api/get_code/{{api_key}}').then(r=>r.json()).then(d=>{
    if(d.success){document.getElementById('code').textContent=d.code;document.getElementById('status').textContent='验证码已接收';}
    else{document.getElementById('status').textContent='读取验证码中…'}
  }).catch(()=>{});
}
tick(); setInterval(tick,3000);
</script>'''
            return render_template_string(minimal, phone=account['phone'], api_key=api_key)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return "Template error: %s" % str(e), 500

    @self.flask_app.route('/api/get_code/<api_key>')
    def api_get_code(api_key):
        from flask import jsonify
        account = self.get_account_by_api_key(api_key)
        if not account:
            return jsonify({"error": "无效的API密钥"}), 404
        latest = self.get_latest_verification_code(account['phone'])
        if latest:
            return jsonify({
                "success": True,
                "code": latest['code'],
                "type": latest['code_type'],
                "received_at": latest['received_at']
            })
        return jsonify({"success": False, "message": "暂无验证码"})

    @self.flask_app.route('/api/submit_code', methods=['POST'])
    def api_submit_code():
        from flask import request, jsonify
        data = request.json or {}
        phone = data.get('phone')
        code = data.get('code')
        ctype = data.get('type', 'sms')
        if not phone or not code:
            return jsonify({"error": "缺少必要参数"}), 400
        self.save_verification_code(str(phone), str(code), str(ctype))
        return jsonify({"success": True})

    @self.flask_app.route('/api/start_watch/<api_key>', methods=['POST', 'GET'])
    def api_start_watch(api_key):
        # 解析 fresh/window_sec/timeout，容错处理
        from flask import request, jsonify
        q = request.args or {}
        fresh = str(q.get('fresh', '0')).lower() in ('1', 'true', 'yes', 'y', 'on')

        def _safe_float(v, default=0.0):
            try:
                if v is None:
                    return float(default)
                s = str(v).strip()
                import re
                m = re.search(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', s)
                if not m:
                    return float(default)
                return float(m.group(0))
            except Exception:
                return float(default)

        def _safe_int(v, default=0):
            try:
                return int(_safe_float(v, default))
            except Exception:
                return int(default)

        timeout = _safe_int(q.get('timeout', None), 300)
        window_sec = _safe_int(q.get('window_sec', None), 0)
        ok, msg = self.start_code_watch(api_key, timeout=timeout, fresh=fresh, history_window_sec=window_sec)
        return jsonify({"ok": ok, "message": msg, "timeout": timeout, "window_sec": window_sec})

    @self.flask_app.route('/healthz')
    def healthz():
        from flask import jsonify
        return jsonify({"ok": True, "base_url": self.base_url}), 200

    @self.flask_app.route('/debug/account/<api_key>')
    def debug_account(api_key):
        from flask import jsonify
        acc = self.get_account_by_api_key(api_key)
        return jsonify(acc or {}), (200 if acc else 404)

    # 独立线程启动，避免嵌套函数缩进问题
    t = threading.Thread(target=self._run_server, daemon=True)
    t.start()

def _run_server(self):
    host = os.getenv("API_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("API_SERVER_PORT", "8080"))
    print("🌐 验证码接收服务器启动: http://%s:%d (BASE_URL=%s)" % (host, port, self.base_url))
    # 这里直接用 self.flask_app.run；Flask 已在 start_web_server 中导入并实例化
    self.flask_app.run(host=host, port=port, debug=False)
# ========== APIFormatConverter 缩进安全补丁 v2（放在类定义之后、实例化之前）==========
import os, json, threading

# 确保类已定义
try:
    APIFormatConverter
except NameError:
    raise RuntimeError("请把本补丁放在 class APIFormatConverter 定义之后")

# 环境变量助手：去首尾空格/引号
def _afc_env(self, key: str, default: str = "") -> str:
    val = os.getenv(key)
    if val is None:
        return default
    return str(val).strip().strip('"').strip("'")

# 渲染模板：深色主题、内容居中放大、2FA/验证码/手机号复制（HTTPS+回退）、支持 .env 文案、标题模板
def _afc_render_verification_template(self, phone: str, api_key: str, two_fa_password: str = "") -> str:
    from flask import render_template_string

    # 文案/标题
    brand = _afc_env(self, "VERIFY_BRAND", "Top9")
    badge = _afc_env(self, "VERIFY_BADGE", brand)
    page_heading = _afc_env(self, "VERIFY_PAGE_HEADING", "验证码接收")
    page_title_tpl = _afc_env(self, "VERIFY_PAGE_TITLE", "{brand} · {heading} · {phone}")
    page_title = page_title_tpl.format(brand=(badge or brand), heading=page_heading, phone=phone)

    ad_html_default = _afc_env(
        self, "VERIFY_FOOTER_HTML",
        _afc_env(self, "VERIFY_AD_HTML", "Top9 · 安全、极速 · 联系我们：<a href='https://example.com' target='_blank' rel='noopener'>example.com</a>")
    )

    txt = {
        "brand_badge": badge,
        "left_title": _afc_env(self, "VERIFY_LEFT_TITLE", "Telegram Login API"),
        "left_cn": _afc_env(self, "VERIFY_LEFT_CN", "安全、快速的 Telegram 登录验证服务"),
        "left_en": _afc_env(self, "VERIFY_LEFT_EN", "Secure and Fast Telegram Authentication Service"),
        "hero_title": _afc_env(self, "VERIFY_HERO_TITLE", brand),
        "hero_subtitle": _afc_env(self, "VERIFY_HERO_SUBTITLE", "BRANDED AUTH PORTAL"),

        "page_heading": page_heading,
        "page_subtext": _afc_env(self, "VERIFY_PAGE_SUBTEXT", "打开此页已自动开始监听 App 内验证码（777000）。"),
        "phone_label": _afc_env(self, "VERIFY_PHONE_LABEL", "PHONE"),
        "copy_btn": _afc_env(self, "VERIFY_COPY_BTN", "复制"),
        "refresh_btn": _afc_env(self, "VERIFY_REFRESH_BTN", "刷新"),
        "twofa_label": _afc_env(self, "VERIFY_2FA_LABEL", "2FA"),
        "copy_2fa_btn": _afc_env(self, "VERIFY_COPY_2FA_BTN", "复制2FA"),

        "status_wait": _afc_env(self, "VERIFY_STATUS_WAIT", "读取验证码中 · READING THE VERIFICATION CODE."),
        "status_ok": _afc_env(self, "VERIFY_STATUS_OK", "验证码已接收 · VERIFICATION CODE RECEIVED."),

        "footer_html": ad_html_default,

        "toast_copied_phone": _afc_env(self, "VERIFY_TOAST_COPIED_PHONE", "已复制手机号"),
        "toast_copied_code": _afc_env(self, "VERIFY_TOAST_COPIED_CODE", "已复制验证码"),
        "toast_copied_2fa": _afc_env(self, "VERIFY_TOAST_COPIED_2FA", "已复制 2FA"),
        "toast_refresh_ok": _afc_env(self, "VERIFY_TOAST_REFRESH_OK", "已刷新，将只获取2分钟内的验证码"),
        "toast_refresh_fail": _afc_env(self, "VERIFY_TOAST_REFRESH_FAIL", "刷新失败"),
        "toast_no_code": _afc_env(self, "VERIFY_TOAST_NO_CODE", "暂无验证码可复制"),
    }
    txt_json = json.dumps(txt, ensure_ascii=False)

    template = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ page_title }}</title>
  <style>
    :root{
      --bg:#0b0f14; --bg2:#0f1621;
      --panel:#111827; --panel2:#0f172a;
      --text:#e5e7eb; --muted:#9ca3af; --border:#243244;
      --brand1:#06b6d4; --brand2:#3b82f6; --ok:#34d399; --warn:#fbbf24;
      --accent:#7dd3fc;
    }
    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0; padding:20px; min-height:100%;
      font-family:Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Arial;
      color:var(--text);
      background:
        radial-gradient(1200px 600px at -10% -10%, rgba(6,182,212,.10), transparent),
        radial-gradient(900px 500px at 110% 110%, rgba(59,130,246,.10), transparent),
        linear-gradient(180deg, var(--bg), var(--bg2));
      display:flex; align-items:center; justify-content:center;
    }
    .wrap{ width:100%; max-width:1200px; display:grid; grid-template-columns: 380px 1fr; gap:22px; }
    @media(max-width:1100px){ .wrap{ grid-template-columns:1fr; } }

    .brand{
      background:linear-gradient(180deg,#0f172a,#0b1220);
      border:1px solid var(--border); border-radius:18px; padding:26px; position:relative;
      box-shadow:0 18px 60px rgba(0,0,0,.45); overflow:hidden;
    }
    .badge{ display:inline-block; padding:8px 14px; border-radius:999px; border:1px solid rgba(6,182,212,.4);
            color:#7dd3fc; background:rgba(6,182,212,.12); font-weight:800; letter-spacing:.5px; }
    .brand h2{ margin:16px 0 10px; font-size:28px; }
    .brand p{ margin:0; color:var(--muted); line-height:1.6; }
    .hero{ margin-top:26px; text-align:center; border:1px dashed var(--border); border-radius:14px; padding:16px; background:rgba(2,6,23,.45); }
    .hero .big{ font-size:46px; font-weight:900; letter-spacing:2px; color:#93c5fd; }

    .panel{ background:var(--panel); border:1px solid var(--border); border-radius:18px; padding:22px; box-shadow:0 18px 60px rgba(0,0,0,.45); }
    .inner{ max-width:820px; margin:0 auto; } /* 右侧内容更居中 */
    .head{ display:flex; align-items:center; justify-content:space-between; gap:12px; }
    .title{ font-size:24px; font-weight:900; letter-spacing:.3px; }
    .muted{ color:var(--muted); font-size:14px; }

    .row{ display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
    .row.center{ justify-content:center; }
    .pill{ background:rgba(148,163,184,.12); color:#cbd5e1; padding:8px 12px; border-radius:999px; font-size:13px; border:1px solid var(--border); }
    .btn{ border:none; background:linear-gradient(135deg,var(--brand1),var(--brand2)); color:#fff; padding:10px 16px; border-radius:12px; cursor:pointer; font-weight:800; box-shadow:0 12px 24px rgba(59,130,246,.25); }

    .phone{
      margin-top:16px; background:var(--panel2); border:1px solid var(--border); border-radius:14px; padding:14px 16px;
      display:flex; align-items:center; justify-content:center; gap:14px; flex-wrap:wrap;
    }
    .phone .number{ font-size:24px; font-weight:900; letter-spacing:1px; color:#e6f0ff; }
    .btn.secondary{ background:#0b1220; border:1px solid var(--border); color:#9ac5ff; box-shadow:none; }

    .twofa{ margin-top:10px; display:flex; align-items:center; justify-content:center; gap:10px; flex-wrap:wrap; }
    .twofa code{ background:#0b1220; border:1px solid var(--border); padding:16px 20px; border-radius:14px; font-size:24px; font-weight:700; letter-spacing:2px; min-width:120px; text-align:center; }

    .status{ margin:18px auto 0; padding:14px 16px; border-radius:14px; text-align:center; font-weight:900; border:1px solid var(--border); max-width:820px; }
    .status.wait{ background:rgba(245,158,11,.12); color:#fbbf24; }
    .status.ok{ background:rgba(34,197,94,.12); color:var(--ok); }

    .code-wrap{ margin:18px auto 0; padding:20px; border-radius:18px; background:#0b1220; border:2px solid #1e2a3a; display:flex; align-items:center; justify-content:space-between; gap:16px; max-width:820px; }
    .code{ flex:1; display:flex; justify-content:center; gap:14px; font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace; }
    .digit{ width:86px; height:94px; border-radius:14px; background:#0c1422; border:2px solid #233247; color:#7dd3fc; font-size:52px; font-weight:900; display:flex; align-items:center; justify-content:center; box-shadow: inset 0 1px 0 rgba(255,255,255,.05), 0 6px 18px rgba(2,6,23,.45); }

    .meta{ margin-top:10px; text-align:center; color:#9ca3af; font-size:13px; }

    .footer{ margin-top:20px; border-top:1px solid var(--border); padding-top:12px; text-align:center; color:#9ca3af; font-size:12px; }
    .ad{ margin-top:10px; color:#cbd5e1; }

    .toast{
      position:fixed; left:50%; bottom:26px;
      transform:translateX(-50%) translateY(20px);
      background:rgba(15,23,42,.95); color:#e5e7eb;
      border:1px solid var(--border); padding:10px 14px;
      border-radius:10px; font-weight:800; font-size:14px;
      box-shadow:0 12px 30px rgba(0,0,0,.45);
      opacity:0; pointer-events:none; z-index:9999;
      transition:opacity .18s ease, transform .18s ease;
    }
    .toast.show{ opacity:1; transform:translateX(-50%) translateY(0); }
  </style>
</head>
<body>
  <div class="wrap">
    <section class="brand">
      <div class="badge">{{ txt.brand_badge }}</div>
      <h2>{{ txt.left_title }}</h2>
      <p>{{ txt.left_cn }}<br>{{ txt.left_en }}</p>
      <div class="hero">
        <div class="big">{{ txt.hero_title }}</div>
        <div class="muted">{{ txt.hero_subtitle }}</div>
      </div>
    </section>

    <section class="panel">
      <div class="inner">
        <div class="head">
          <div>
            <div class="title">{{ txt.page_heading }}</div>
            <div class="muted">{{ txt.page_subtext }}</div>
          </div>
          <button class="btn" id="refresh-btn">{{ txt.refresh_btn }}</button>
        </div>

        <div class="phone">
          <span class="pill">{{ txt.phone_label }}</span>
          <strong class="number">{{ phone }}</strong>
          <button class="btn secondary" id="copy-phone">{{ txt.copy_btn }}</button>
          {% if two_fa_password %}
          <span class="pill">{{ txt.twofa_label }}</span>
          <code id="twofa-text">{{ two_fa_password }}</code>
          <button class="btn secondary" id="copy-2fa">{{ txt.copy_2fa_btn }}</button>
          {% endif %}
        </div>

        <div id="status" class="status wait">{{ txt.status_wait }}</div>

        <div class="code-wrap" id="code-wrap" style="display:none;">
          <div class="code" id="code-boxes"></div>
          <button class="btn" id="copy-code">{{ txt.copy_btn }}</button>
        </div>

        <div class="meta" id="meta" style="display:none;"></div>

        <div class="footer">
          <div class="ad">{{ txt.footer_html | safe }}</div>
        </div>
      </div>
    </section>
  </div>

  <div id="toast" class="toast" role="status" aria-live="polite"></div>

  <script>
    const TXT = {{ txt_json | safe }};

    fetch('/api/start_watch/{{ api_key }}', { method: 'POST' }).catch(()=>{});

    let codeValue = '';
    let pollingTimer = null;
    let stopTimer = null;
    let toastTimer = null;

    function showToast(text, duration){
      try{
        const t = document.getElementById('toast');
        if (!t) return;
        t.textContent = text || '';
        t.classList.add('show');
        if (toastTimer) clearTimeout(toastTimer);
        toastTimer = setTimeout(()=>{ t.classList.remove('show'); }, duration || 1500);
      }catch(e){}
    }

    function notify(msg){
      try{ if(typeof showToast==='function'){ showToast(msg); } else { alert(msg); } }
      catch(e){ alert(msg); }
    }
    async function copyTextUniversal(text){
      try{
        if(!text){ notify('内容为空'); return false; }
        text = String(text);
        if (window.isSecureContext && navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(text);
          notify('已复制');
          return true;
        }
        const ta = document.createElement('textarea');
        ta.value = text;
        ta.setAttribute('readonly','');
        ta.style.position = 'fixed';
        ta.style.top = '-9999px';
        ta.style.left = '-9999px';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        const ua = navigator.userAgent.toLowerCase();
        if (/ipad|iphone|ipod/.test(ua)) {
          const range = document.createRange();
          range.selectNodeContents(ta);
          const sel = window.getSelection();
          sel.removeAllRanges(); sel.addRange(range);
          ta.setSelectionRange(0, 999999);
        } else {
          ta.select();
        }
        const ok = document.execCommand('copy');
        document.body.removeChild(ta);
        if (ok) { notify('已复制'); return true; }
        throw new Error('execCommand copy failed');
      } catch (e) {
        console.warn('Copy failed:', e);
        notify('复制失败，请手动选择并复制');
        return false;
      }
    }

    function renderDigits(code){
      const box = document.getElementById('code-boxes');
      box.innerHTML = '';
      const s = (code || '').trim();
      
      // 直接设置到按钮的 data 属性
      const copyBtn = document.getElementById('copy-code');
      if (copyBtn) {
        copyBtn.setAttribute('data-code', s);
      }
      
      for(const ch of s){
        const d = document.createElement('div');
        d.className = 'digit';
        d.textContent = ch;
        box.appendChild(d);
      }
    }

    function setStatus(ok, text){
      const s = document.getElementById('status');
      s.className = 'status ' + (ok ? 'ok' : 'wait');
      s.textContent = text || (ok ? TXT.status_ok : TXT.status_wait);
    }

    function checkCode(){
      fetch('/api/get_code/{{ api_key }}')
        .then(r => r.json())
        .then(d => {
          if(d.success){
            if(d.code && d.code !== codeValue){
              codeValue = d.code;
              renderDigits(codeValue);
              document.getElementById('code-wrap').style.display = 'flex';
              document.getElementById('meta').style.display = 'block';
              document.getElementById('meta').textContent = '接收时间：' + new Date(d.received_at).toLocaleString();
              setStatus(true);
            }
          }else{
            setStatus(false);
          }
        }).catch(()=>{});
    }

    function startPolling(){
      if(pollingTimer) clearInterval(pollingTimer);
      if(stopTimer) clearTimeout(stopTimer);
      checkCode();
      pollingTimer = setInterval(checkCode, 3000);
      stopTimer = setTimeout(()=>{ clearInterval(pollingTimer); }, 300000);
    }

    document.getElementById('refresh-btn').addEventListener('click', ()=>{
      const s = document.getElementById('status');
      s.className = 'status wait';
      s.textContent = TXT.status_wait;
      document.getElementById('code-wrap').style.display = 'none';
      document.getElementById('meta').style.display = 'none';
      document.getElementById('meta').textContent = '';
      fetch('/api/start_watch/{{ api_key }}?fresh=1&window_sec=120', { method: 'POST' })
        .then(()=>{ showToast(TXT.toast_refresh_ok); setTimeout(checkCode, 500); })
        .catch(()=>{ showToast(TXT.toast_refresh_fail); });
    });

    (function(){
      const btn = document.getElementById('copy-phone');
      if (!btn) return;
      btn.addEventListener('click', ()=>{
        const el = document.querySelector('.phone .number');
        const v = (el && (el.textContent || el.innerText || '')).trim();
        copyTextUniversal(v);
      });
    })();

    (function(){
      const btn = document.getElementById('copy-2fa');
      if (!btn) return;
      btn.addEventListener('click', ()=>{
        const el = document.getElementById('twofa-text');
        const v = (el && (el.textContent || el.innerText || '')).trim();
        copyTextUniversal(v);
      });
    })();

    // 复制验证码
    (function(){
      const btn = document.getElementById('copy-code');
      if (!btn) return;
      btn.addEventListener('click', ()=>{
        // 直接从页面元素获取验证码
        const digits = document.querySelectorAll('.digit');
        let code = '';
        digits.forEach(digit => {
          code += digit.textContent || digit.innerText || '';
        });
        
        console.log('获取到的验证码:', code); // 调试用
        
        if (code && code.length > 0) {
          copyTextUniversal(code);
        } else {
          notify('暂无验证码可复制');
        }
      });
    })();

    startPolling();
  </script>
</body>
</html>'''
    return render_template_string(
        template,
        phone=phone,
        api_key=api_key,
        two_fa_password=two_fa_password,
        txt=txt,
        txt_json=txt_json,
        page_title=page_title
    )

# Web 服务器（按需导入 Flask）
def _afc_start_web_server(self):
    try:
        from flask import Flask, jsonify, request, render_template_string
    except Exception as e:
        print("❌ Flask 导入失败: %s" % e)
        return

    if getattr(self, "flask_app", None):
        return

    self.flask_app = Flask(__name__)

    @self.flask_app.route('/verify/<api_key>')
    def _verify(api_key):
        try:
            account = self.get_account_by_api_key(api_key)
            if not account:
                return "❌ 无效的API密钥", 404
            return self.render_verification_template(
                account['phone'], api_key, account.get('two_fa_password') or ""
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
            return "Template error: %s" % str(e), 500

    @self.flask_app.route('/api/get_code/<api_key>')
    def _get_code(api_key):
        account = self.get_account_by_api_key(api_key)
        if not account:
            return jsonify({"error":"无效的API密钥"}), 404
        latest = self.get_latest_verification_code(account['phone'])
        if latest:
            return jsonify({"success":True,"code":latest["code"],"type":latest["code_type"],"received_at":latest["received_at"]})
        return jsonify({"success":False,"message":"暂无验证码"})

    @self.flask_app.route('/api/submit_code', methods=['POST'])
    def _submit():
        data = request.json or {}
        phone = data.get('phone'); code = data.get('code'); ctype = data.get('type','sms')
        if not phone or not code:
            return jsonify({"error":"缺少必要参数"}), 400
        self.save_verification_code(str(phone), str(code), str(ctype))
        return jsonify({"success":True})

    @self.flask_app.route('/api/start_watch/<api_key>', methods=['POST','GET'])
    def _start_watch(api_key):
        q = request.args or {}
        def _safe_float(v, default=0.0):
            try:
                if v is None: return float(default)
                import re; m = re.search(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?', str(v).strip())
                return float(m.group(0)) if m else float(default)
            except Exception:
                return float(default)
        def _safe_int(v, default=0):
            try: return int(_safe_float(v, default))
            except Exception: return int(default)

        fresh = str(q.get('fresh','0')).lower() in ('1','true','yes','y','on')
        timeout = _safe_int(q.get('timeout', None), 300)
        window_sec = _safe_int(q.get('window_sec', None), 0)
        ok, msg = self.start_code_watch(api_key, timeout=timeout, fresh=fresh, history_window_sec=window_sec)
        return jsonify({"ok":ok,"message":msg,"timeout":timeout,"window_sec":window_sec})

    @self.flask_app.route('/healthz')
    def _healthz():
        return jsonify({"ok":True,"base_url":self.base_url}), 200

    t = threading.Thread(target=self._run_server, daemon=True)
    t.start()

def _afc_run_server(self):
    host = os.getenv("API_SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("API_SERVER_PORT", "8080"))
    print("🌐 验证码接收服务器启动: http://%s:%d (BASE_URL=%s)" % (host, port, self.base_url))
    self.flask_app.run(host=host, port=port, debug=False)

# 把方法安全挂到类上（先定义，后挂载；用 hasattr 避免引用未定义名字）
if not hasattr(APIFormatConverter, "_env"):
    APIFormatConverter._env = _afc_env
if not hasattr(APIFormatConverter, "render_verification_template"):
    APIFormatConverter.render_verification_template = _afc_render_verification_template
if not hasattr(APIFormatConverter, "start_web_server"):
    APIFormatConverter.start_web_server = _afc_start_web_server
if not hasattr(APIFormatConverter, "_run_server"):
    APIFormatConverter._run_server = _afc_run_server
# ========== 补丁结束 ==========


# ================================
# 增强版机器人
# ================================

class EnhancedBot:
    """增强版机器人"""
    
    def __init__(self):
        print("🤖 初始化增强版机器人...")
        
        global config
        config = Config()
        if not config.validate():
            print("❌ 配置验证失败")
            sys.exit(1)
        
        self.db = Database(config.DB_NAME)
        self.proxy_manager = ProxyManager(config.PROXY_FILE)
        self.proxy_tester = ProxyTester(self.proxy_manager)
        self.checker = SpamBotChecker(self.proxy_manager)
        self.processor = FileProcessor(self.checker, self.db)
        self.converter = FormatConverter(self.db)
        self.two_factor_manager = TwoFactorManager(self.proxy_manager, self.db)
        import inspect
        print("DEBUG APIFormatConverter source:", inspect.getsourcefile(APIFormatConverter))
        print("DEBUG APIFormatConverter signature:", str(inspect.signature(APIFormatConverter)))
        # 初始化 API 格式转换器（带兜底，兼容无参老版本）
        try:
            # 首选：带参构造（新版本）
            self.api_converter = APIFormatConverter(self.db, base_url=config.BASE_URL)
        except TypeError as e:
            print(f"⚠️ APIFormatConverter 带参构造失败：{e}，切换到兼容模式（无参+手动注入）")
            self.api_converter = APIFormatConverter()   # 老版本：无参
            self.api_converter.db = self.db
            self.api_converter.base_url = config.BASE_URL


        # API转换待处理任务池：上传ZIP后先问网页展示的2FA，等待用户回复
        self.pending_api_tasks: Dict[int, Dict[str, Any]] = {}

        # 启动验证码接收服务器（Flask）
        try:
            self.api_converter.start_web_server()
        except Exception as e:
            print(f"⚠️ 验证码服务器启动失败: {e}")

        # 初始化账号分类器
        self.classifier = AccountClassifier() if CLASSIFY_AVAILABLE else None
        self.pending_classify_tasks: Dict[int, Dict[str, Any]] = {}
        
        # 广播消息待处理任务
        self.pending_broadcasts: Dict[int, Dict[str, Any]] = {}
        
        # 人工开通会员待处理任务
        self.pending_manual_open: Dict[int, int] = {}

        self.updater = Updater(config.TOKEN, use_context=True)
        self.dp = self.updater.dispatcher
        
        self.setup_handlers()
        
        print("✅ 增强版机器人初始化完成")
    
    def setup_handlers(self):
        self.dp.add_handler(CommandHandler("start", self.start_command))
        self.dp.add_handler(CommandHandler("help", self.help_command))
        self.dp.add_handler(CommandHandler("addadmin", self.add_admin_command))
        self.dp.add_handler(CommandHandler("removeadmin", self.remove_admin_command))
        self.dp.add_handler(CommandHandler("listadmins", self.list_admins_command))
        self.dp.add_handler(CommandHandler("proxy", self.proxy_command))
        self.dp.add_handler(CommandHandler("testproxy", self.test_proxy_command))
        self.dp.add_handler(CommandHandler("cleanproxy", self.clean_proxy_command))
        self.dp.add_handler(CommandHandler("convert", self.convert_command))
        # 新增：API格式转换命令
        self.dp.add_handler(CommandHandler("api", self.api_command))
        # 新增：账号分类命令
        self.dp.add_handler(CommandHandler("classify", self.classify_command))
        # 新增：返回主菜单（优先于通用回调）
        self.dp.add_handler(CallbackQueryHandler(self.on_back_to_main, pattern=r"^back_to_main$"))
        
        # 专用：广播消息回调处理器（必须在通用回调之前注册）
        self.dp.add_handler(CallbackQueryHandler(self.handle_broadcast_callbacks_router, pattern=r"^broadcast_"))

        # 通用回调处理（需放在特定回调之后）
        self.dp.add_handler(CallbackQueryHandler(self.handle_callbacks))
        self.dp.add_handler(MessageHandler(Filters.document, self.handle_file))
        # 新增：广播媒体上传处理
        self.dp.add_handler(MessageHandler(Filters.photo, self.handle_photo))
        self.dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_text))
    
    def safe_send_message(self, update, text, parse_mode=None, reply_markup=None):
        """安全发送消息"""
        try:
            # 检查 update.message 是否存在
            if update.message:
                return update.message.reply_text(
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup
                )
            # 如果 update.message 不存在（例如来自回调查询），使用 bot.send_message
            elif update.effective_chat:
                return self.updater.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup
                )
            else:
                print("❌ 无法发送消息: update 对象缺少 message 和 effective_chat")
                return None
        except RetryAfter as e:
            print(f"⚠️ 频率限制，等待 {e.retry_after} 秒")
            time.sleep(e.retry_after + 1)
            try:
                if update.message:
                    return update.message.reply_text(
                        text=text,
                        parse_mode=parse_mode,
                        reply_markup=reply_markup
                    )
                elif update.effective_chat:
                    return self.updater.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=text,
                        parse_mode=parse_mode,
                        reply_markup=reply_markup
                    )
            except:
                return None
        except Exception as e:
            print(f"❌ 发送消息失败: {e}")
            return None
    
    def safe_edit_message(self, query, text, parse_mode=None, reply_markup=None):
        """安全编辑消息"""
        try:
            return query.edit_message_text(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
        except RetryAfter as e:
            print(f"⚠️ 频率限制，等待 {e.retry_after} 秒")
            time.sleep(e.retry_after + 1)
            try:
                return query.edit_message_text(
                    text=text,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup
                )
            except:
                return None
        except BadRequest as e:
            if "message is not modified" in str(e).lower():
                return None
            print(f"❌ 编辑消息失败: {e}")
            return None
        except Exception as e:
            print(f"❌ 编辑消息失败: {e}")
            return None
    
    def create_status_count_separate_buttons(self, results: Dict[str, List], processed: int, total: int) -> InlineKeyboardMarkup:
        """创建状态|数量分离按钮布局"""
        buttons = []
        
        status_info = [
            ("无限制", "🟢", len(results['无限制'])),
            ("垃圾邮件", "🟡", len(results['垃圾邮件'])),
            ("冻结", "🔴", len(results['冻结'])),
            ("封禁", "🟠", len(results['封禁'])),
            ("连接错误", "⚫", len(results['连接错误']))
        ]
        
        # 每一行显示：状态名称 | 数量
        for status, emoji, count in status_info:
            row = [
                InlineKeyboardButton(f"{emoji} {status}", callback_data=f"status_{status}"),
                InlineKeyboardButton(f"{count}", callback_data=f"count_{status}")
            ]
            buttons.append(row)
        
        return InlineKeyboardMarkup(buttons)
    def start_command(self, update: Update, context: CallbackContext):
        """处理 /start 命令"""
        user_id = update.effective_user.id
        self.show_main_menu(update, user_id)
    
    def show_main_menu(self, update: Update, user_id: int):
        """显示主菜单（统一方法）"""
        # 获取用户信息
        if update.callback_query:
            first_name = update.callback_query.from_user.first_name or "用户"
        else:
            first_name = update.effective_user.first_name or "用户"
        
        # 获取会员状态（使用 check_membership 方法）
        is_member, level, expiry = self.db.check_membership(user_id)
        
        if self.db.is_admin(user_id):
            member_status = "👑 管理员"
        elif is_member:
            member_status = f"🎁 {level}"
        else:
            member_status = "❌ 无会员"
        
        welcome_text = f"""
<b>🔍 Telegram账号机器人 V8.0</b>

👤 <b>用户信息</b>
• 昵称: {first_name}
• ID: <code>{user_id}</code>
• 会员: {member_status}
• 到期: {expiry}

📡 <b>代理状态</b>
• 代理模式: {'🟢启用' if self.proxy_manager.is_proxy_mode_active(self.db) else '🔴本地连接'}
• 代理数量: {len(self.proxy_manager.proxies)}个
• 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        

        # 创建横排2x2布局的主菜单按钮（在原有两行后新增一行“🔗 API转换”）
        buttons = [
            [
                InlineKeyboardButton("🚀 账号检测", callback_data="start_check"),
                InlineKeyboardButton("🔄 格式转换", callback_data="format_conversion")
            ],
            [
                InlineKeyboardButton("🔐 修改2FA", callback_data="change_2fa"),
                InlineKeyboardButton("🛡️ 防止找回", callback_data="prevent_recovery")
            ],
            [
                InlineKeyboardButton("🔗 API转换", callback_data="api_conversion"),
                InlineKeyboardButton("📦 账号拆分", callback_data="classify_menu")
            ],
            [
                InlineKeyboardButton("💳 开通/兑换会员", callback_data="vip_menu")
            ],
            [
                InlineKeyboardButton("ℹ️ 帮助", callback_data="help")
            ]
        ]

        # 管理员按钮
        if self.db.is_admin(user_id):
            buttons.append([
                InlineKeyboardButton("👑 管理员面板", callback_data="admin_panel"),
                InlineKeyboardButton("📡 代理管理", callback_data="proxy_panel")
            ])

        # 底部功能按钮（如果已把“帮助”放到第三行左侧，可将这里的帮助去掉或改为“⚙️ 状态”）
        buttons.append([
            InlineKeyboardButton("⚙️ 状态", callback_data="status")
        ])

        
        keyboard = InlineKeyboardMarkup(buttons)
        
        # 判断是编辑消息还是发送新消息
        if update.callback_query:
            update.callback_query.answer()
            try:
                update.callback_query.edit_message_text(
                    text=welcome_text,
                    reply_markup=keyboard,
                    parse_mode='HTML'
                )
            except Exception as e:
                print(f"⚠️ 编辑消息失败: {e}")
        else:
            self.safe_send_message(update, welcome_text, 'HTML', keyboard)
    
    def api_command(self, update: Update, context: CallbackContext):
        """API格式转换命令"""
        user_id = update.effective_user.id

        # 权限检查
        is_member, level, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 需要会员权限才能使用API转换功能")
            return

        if not 'FLASK_AVAILABLE' in globals() or not FLASK_AVAILABLE:
            self.safe_send_message(update, "❌ API转换功能不可用\n\n原因: Flask库未安装\n💡 请安装: pip install flask jinja2")
            return

        text = """
🔗 <b>API格式转换功能</b>

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
请上传包含TData或Session文件的ZIP压缩包...
        """

        buttons = [
            [InlineKeyboardButton("🔙 返回主菜单", callback_data="back_to_main")]
        ]

        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_send_message(update, text, 'HTML', keyboard)

        # 设置用户状态
        self.db.save_user(
            user_id,
            update.effective_user.username or "",
            update.effective_user.first_name or "",
            "waiting_api_file"
        ) 

    def handle_api_conversion(self, query):
        """处理API转换选项"""
        query.answer()
        user_id = query.from_user.id

        # 权限检查
        is_member, level, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_edit_message(query, "❌ 需要会员权限才能使用API转换功能")
            return

        if not 'FLASK_AVAILABLE' in globals() or not FLASK_AVAILABLE:
            self.safe_edit_message(query, "❌ API转换功能不可用\n\n原因: Flask库未安装\n💡 请安装: pip install flask jinja2")
            return

        text = """
🔗 <b>API格式转换</b>

<b>🎯 核心功能</b>
• 📱 提取手机号信息
• 🔐 自动检测2FA密码
• 🌐 生成验证码接收链接
• 📋 输出标准API格式

<b>🌐 验证码接收特性</b>
• 每个账号生成独立验证链接
• 实时显示验证码，自动刷新
• 支持HTTP API调用获取验证码
• 5分钟自动过期保护

<b>📤 使用方法</b>
1. 上传ZIP文件（包含TData或Session）
2. 系统自动分析账号信息
3. 生成API格式文件和验证链接
4. 下载结果使用

请上传您的文件...
        """

        self.safe_edit_message(query, text, 'HTML')

        # 设置用户状态
        self.db.save_user(
            user_id,
            query.from_user.username or "",
            query.from_user.first_name or "",
            "waiting_api_file"
        )        
    def help_command(self, update: Update, context: CallbackContext):
        """处理 /help 命令和帮助按钮"""
        help_text = """
📖 <b>使用帮助</b>

<b>🚀 主要功能</b>
• 代理连接模式自动检测账号状态
• 实时进度显示和自动文件发送
• 支持Session和TData格式
• Tdata与Session格式互转

<b>📁 支持格式</b>
• Session + JSON文件
• TData文件夹
• ZIP压缩包

<b>🔄 格式转换</b>
• Tdata → Session: 转换为Session格式
• Session → Tdata: 转换为Tdata格式
• 批量并发处理，提高效率

<b>📡 代理功能</b>
• 自动读取proxy.txt文件
• 支持HTTP/SOCKS4/SOCKS5代理
• 代理失败自动切换到本地连接

<b>📋 使用流程</b>
1. 准备proxy.txt文件（可选）
2. 点击"🚀 开始检测"或"🔄 格式转换"
3. 上传ZIP文件
4. 观看实时进度
5. 自动接收分类文件
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 返回主菜单", callback_data="back_to_main")]
        ])
        
        if update.callback_query:
            update.callback_query.answer()
            update.callback_query.edit_message_text(
                text=help_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
        else:
            update.message.reply_text(
                text=help_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
        if self.db.is_admin(user_id):
            help_text += f"""

<b>👑 管理员命令</b>
• /addadmin [ID/用户名] - 添加管理员
• /removeadmin [ID] - 移除管理员
• /listadmins - 查看管理员列表
• /proxy - 代理状态管理
• /testproxy - 测试代理连接性能
• /cleanproxy - 清理失效代理（自动优化）
• /convert - 格式转换功能

<b>⚡ 速度优化功能</b>
• 快速模式: {config.PROXY_FAST_MODE}
• 并发检测: {config.PROXY_CHECK_CONCURRENT} 个
• 智能重试: {config.PROXY_RETRY_COUNT} 次
• 自动清理: {config.PROXY_AUTO_CLEANUP}
            """
        
        self.safe_send_message(update, help_text, 'HTML')
    
    def add_admin_command(self, update: Update, context: CallbackContext):
        """添加管理员命令"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 仅管理员可以使用此命令")
            return
        
        if not context.args:
            self.safe_send_message(update, 
                "📝 使用方法:\n"
                "/addadmin [用户ID]\n"
                "/addadmin [用户名]\n\n"
                "示例:\n"
                "/addadmin 123456789\n"
                "/addadmin @username"
            )
            return
        
        target = context.args[0].strip()
        
        # 尝试解析为用户ID
        try:
            target_user_id = int(target)
            target_username = "未知"
            target_first_name = "未知"
        except ValueError:
            # 尝试按用户名查找
            target = target.replace("@", "")
            user_info = self.db.get_user_by_username(target)
            if not user_info:
                self.safe_send_message(update, f"❌ 找不到用户名 @{target}\n请确保用户已使用过机器人")
                return
            
            target_user_id, target_username, target_first_name = user_info
        
        # 检查是否已经是管理员
        if self.db.is_admin(target_user_id):
            self.safe_send_message(update, f"⚠️ 用户 {target_user_id} 已经是管理员")
            return
        
        # 添加管理员
        if self.db.add_admin(target_user_id, target_username, target_first_name, user_id):
            self.safe_send_message(update, 
                f"✅ 成功添加管理员\n\n"
                f"👤 用户ID: {target_user_id}\n"
                f"📝 用户名: @{target_username}\n"
                f"🏷️ 昵称: {target_first_name}\n"
                f"⏰ 添加时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
        else:
            self.safe_send_message(update, "❌ 添加管理员失败")
    
    def remove_admin_command(self, update: Update, context: CallbackContext):
        """移除管理员命令"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 仅管理员可以使用此命令")
            return
        
        if not context.args:
            self.safe_send_message(update, 
                "📝 使用方法:\n"
                "/removeadmin [用户ID]\n\n"
                "示例:\n"
                "/removeadmin 123456789"
            )
            return
        
        try:
            target_user_id = int(context.args[0])
        except ValueError:
            self.safe_send_message(update, "❌ 请提供有效的用户ID")
            return
        
        # 不能移除配置文件中的管理员
        if target_user_id in config.ADMIN_IDS:
            self.safe_send_message(update, "❌ 无法移除配置文件中的管理员")
            return
        
        # 不能移除自己
        if target_user_id == user_id:
            self.safe_send_message(update, "❌ 无法移除自己的管理员权限")
            return
        
        if not self.db.is_admin(target_user_id):
            self.safe_send_message(update, f"⚠️ 用户 {target_user_id} 不是管理员")
            return
        
        if self.db.remove_admin(target_user_id):
            self.safe_send_message(update, f"✅ 已移除管理员: {target_user_id}")
        else:
            self.safe_send_message(update, "❌ 移除管理员失败")
    
    def list_admins_command(self, update: Update, context: CallbackContext):
        """查看管理员列表命令"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 仅管理员可以使用此命令")
            return
        
        admins = self.db.get_all_admins()
        
        if not admins:
            self.safe_send_message(update, "📝 暂无管理员")
            return
        
        admin_text = "<b>👑 管理员列表</b>\n\n"
        
        for i, (admin_id, username, first_name, added_time) in enumerate(admins, 1):
            admin_text += f"<b>{i}.</b> "
            if admin_id in config.ADMIN_IDS:
                admin_text += f"👑 <code>{admin_id}</code> (超级管理员)\n"
            else:
                admin_text += f"🔧 <code>{admin_id}</code>\n"
            
            if username and username != "配置文件管理员":
                admin_text += f"   📝 @{username}\n"
            if first_name and first_name != "":
                admin_text += f"   🏷️ {first_name}\n"
            if added_time != "系统内置":
                admin_text += f"   ⏰ {added_time}\n"
            admin_text += "\n"
        
        admin_text += f"<b>📊 总计: {len(admins)} 个管理员</b>"
        
        self.safe_send_message(update, admin_text, 'HTML')
    
    def proxy_command(self, update: Update, context: CallbackContext):
        """代理管理命令"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 仅管理员可以使用此命令")
            return
        
        # 获取当前代理状态
        proxy_enabled_db = self.db.get_proxy_enabled()
        proxy_mode_active = self.proxy_manager.is_proxy_mode_active(self.db)
        
        # 统计住宅代理数量
        residential_count = sum(1 for p in self.proxy_manager.proxies if p.get('is_residential', False))
        
        proxy_text = f"""
<b>📡 代理管理面板</b>

<b>📊 当前状态</b>
• 系统配置: {'🟢USE_PROXY=true' if config.USE_PROXY else '🔴USE_PROXY=false'}
• 代理开关: {'🟢已启用' if proxy_enabled_db else '🔴已禁用'}
• 代理文件: {config.PROXY_FILE}
• 可用代理: {len(self.proxy_manager.proxies)}个
• 住宅代理: {residential_count}个
• 普通超时: {config.PROXY_TIMEOUT}秒
• 住宅超时: {config.RESIDENTIAL_PROXY_TIMEOUT}秒
• 实际模式: {'🟢代理模式' if proxy_mode_active else '🔴本地模式'}

<b>📝 代理格式支持</b>
• HTTP: ip:port
• HTTP认证: ip:port:username:password  
• SOCKS5: socks5:ip:port:username:password
• SOCKS4: socks4:ip:port
• ABCProxy住宅代理: host.abcproxy.vip:port:username:password
        """
        
        # 创建交互按钮
        buttons = []
        
        # 代理开关控制按钮
        if proxy_enabled_db:
            buttons.append([InlineKeyboardButton("🔴 关闭代理", callback_data="proxy_disable")])
        else:
            buttons.append([InlineKeyboardButton("🟢 开启代理", callback_data="proxy_enable")])
        
        # 其他操作按钮
        buttons.extend([
            [
                InlineKeyboardButton("🔄 刷新代理列表", callback_data="proxy_reload"),
                InlineKeyboardButton("📊 查看代理状态", callback_data="proxy_status")
            ],
            [
                InlineKeyboardButton("🧪 测试代理", callback_data="proxy_test"),
                InlineKeyboardButton("📈 代理统计", callback_data="proxy_stats")
            ],
            [InlineKeyboardButton("🔙 返回管理面板", callback_data="admin_panel")]
        ])
        
        keyboard = InlineKeyboardMarkup(buttons)
        
        if context.args:
            if context.args[0] == "reload":
                self.proxy_manager.load_proxies()
                self.safe_send_message(update, f"✅ 已重新加载代理文件\n📡 新代理数量: {len(self.proxy_manager.proxies)}个")
                return
            elif context.args[0] == "status":
                self.show_proxy_detailed_status(update)
                return
        
        self.safe_send_message(update, proxy_text, 'HTML', keyboard)
    
    def show_proxy_detailed_status(self, update: Update):
        """显示代理详细状态"""
        if self.proxy_manager.proxies:
            status_text = "<b>📡 代理详细状态</b>\n\n"
            for i, proxy in enumerate(self.proxy_manager.proxies[:10], 1):  # 只显示前10个
                status_text += f"{i}. {proxy['host']}:{proxy['port']} ({proxy['type']})\n"
            
            if len(self.proxy_manager.proxies) > 10:
                status_text += f"\n... 还有 {len(self.proxy_manager.proxies) - 10} 个代理"
            
            # 添加代理设置信息
            enabled, updated_time, updated_by = self.db.get_proxy_setting_info()
            status_text += f"\n\n<b>📊 代理开关状态</b>\n"
            status_text += f"• 当前状态: {'🟢启用' if enabled else '🔴禁用'}\n"
            status_text += f"• 更新时间: {updated_time}\n"
            if updated_by:
                status_text += f"• 操作人员: {updated_by}\n"
            
            self.safe_send_message(update, status_text, 'HTML')
        else:
            self.safe_send_message(update, "❌ 没有可用的代理")
    
    def test_proxy_command(self, update: Update, context: CallbackContext):
        """测试代理命令"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 仅管理员可以使用此命令")
            return
        
        if not self.proxy_manager.proxies:
            self.safe_send_message(update, "❌ 没有可用的代理进行测试")
            return
        
        # 异步处理代理测试
        def process_test():
            asyncio.run(self.process_proxy_test(update, context))
        
        thread = threading.Thread(target=process_test)
        thread.start()
        
        self.safe_send_message(
            update, 
            f"🧪 开始测试 {len(self.proxy_manager.proxies)} 个代理...\n"
            f"⚡ 快速模式: {'开启' if config.PROXY_FAST_MODE else '关闭'}\n"
            f"🚀 并发数: {config.PROXY_CHECK_CONCURRENT}\n\n"
            "请稍等，测试结果将自动发送..."
        )
    
    async def process_proxy_test(self, update, context):
        """处理代理测试"""
        try:
            # 发送进度消息
            progress_msg = self.safe_send_message(
                update,
                "🧪 <b>代理测试中...</b>\n\n📊 正在初始化测试环境...",
                'HTML'
            )
            
            # 进度回调函数
            async def test_progress_callback(tested, total, stats):
                try:
                    progress = int(tested / total * 100)
                    elapsed = time.time() - stats['start_time']
                    speed = tested / elapsed if elapsed > 0 else 0
                    
                    progress_text = f"""
🧪 <b>代理测试进行中...</b>

📊 <b>测试进度</b>
• 进度: {progress}% ({tested}/{total})
• 速度: {speed:.1f} 代理/秒
• 可用: {stats['working']} 个
• 失效: {stats['failed']} 个
• 平均响应: {stats['avg_response_time']:.2f}s

⏱️ 已耗时: {elapsed:.1f} 秒
                    """
                    
                    if progress_msg:
                        try:
                            progress_msg.edit_text(progress_text, parse_mode='HTML')
                        except:
                            pass
                except:
                    pass
            
            # 执行测试
            working_proxies, failed_proxies, stats = await self.proxy_tester.test_all_proxies(test_progress_callback)
            
            # 显示最终结果
            total_time = time.time() - stats['start_time']
            test_speed = stats['total'] / total_time if total_time > 0 else 0
            
            final_text = f"""
✅ <b>代理测试完成！</b>

📊 <b>测试结果</b>
• 总计代理: {stats['total']} 个
• 🟢 可用代理: {stats['working']} 个 ({stats['working']/stats['total']*100:.1f}%)
• 🔴 失效代理: {stats['failed']} 个 ({stats['failed']/stats['total']*100:.1f}%)
• 📈 平均响应: {stats['avg_response_time']:.2f} 秒
• ⚡ 测试速度: {test_speed:.1f} 代理/秒
• ⏱️ 总耗时: {total_time:.1f} 秒

💡 使用 /cleanproxy 命令可自动清理失效代理
            """
            
            if progress_msg:
                try:
                    progress_msg.edit_text(final_text, parse_mode='HTML')
                except:
                    pass
            
        except Exception as e:
            self.safe_send_message(update, f"❌ 代理测试失败: {e}")
    
    def clean_proxy_command(self, update: Update, context: CallbackContext):
        """清理代理命令"""
        user_id = update.effective_user.id
        
        if not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 仅管理员可以使用此命令")
            return
        
        if not self.proxy_manager.proxies:
            self.safe_send_message(update, "❌ 没有可用的代理进行清理")
            return
        
        # 检查是否有确认参数
        auto_confirm = len(context.args) > 0 and context.args[0].lower() in ['yes', 'y', 'confirm']
        
        if not auto_confirm:
            # 显示确认界面
            confirm_text = f"""
⚠️ <b>代理清理确认</b>

📊 <b>当前状态</b>
• 代理文件: {config.PROXY_FILE}
• 代理数量: {len(self.proxy_manager.proxies)} 个
• 自动清理: {'启用' if config.PROXY_AUTO_CLEANUP else '禁用'}

🔧 <b>清理操作</b>
• 备份原始代理文件
• 测试所有代理连接性
• 自动删除失效代理
• 更新代理文件为可用代理
• 生成详细分类报告

⚠️ <b>注意事项</b>
• 此操作将修改代理文件
• 失效代理将被自动删除
• 原始文件会自动备份

确认执行清理吗？
            """
            
            buttons = [
                [
                    InlineKeyboardButton("✅ 确认清理", callback_data="confirm_proxy_cleanup"),
                    InlineKeyboardButton("❌ 取消", callback_data="cancel_proxy_cleanup")
                ],
                [InlineKeyboardButton("🧪 仅测试不清理", callback_data="test_only_proxy")]
            ]
            
            keyboard = InlineKeyboardMarkup(buttons)
            self.safe_send_message(update, confirm_text, 'HTML', keyboard)
        else:
            # 直接执行清理
            self._execute_proxy_cleanup(update, context, True)
    
    def _execute_proxy_cleanup(self, update, context, confirmed: bool):
        """执行代理清理"""
        if not confirmed:
            self.safe_send_message(update, "❌ 代理清理已取消")
            return
        
        # 异步处理代理清理
        def process_cleanup():
            asyncio.run(self.process_proxy_cleanup(update, context))
        
        thread = threading.Thread(target=process_cleanup)
        thread.start()
        
        self.safe_send_message(
            update, 
            f"🧹 开始清理 {len(self.proxy_manager.proxies)} 个代理...\n"
            f"⚡ 快速模式: {'开启' if config.PROXY_FAST_MODE else '关闭'}\n"
            f"🚀 并发数: {config.PROXY_CHECK_CONCURRENT}\n\n"
            "请稍等，清理过程可能需要几分钟..."
        )
    
    async def process_proxy_cleanup(self, update, context):
        """处理代理清理过程"""
        try:
            # 发送进度消息
            progress_msg = self.safe_send_message(
                update,
                "🧹 <b>代理清理中...</b>\n\n📊 正在备份原始文件...",
                'HTML'
            )
            
            # 执行清理
            success, result_msg = await self.proxy_tester.cleanup_and_update_proxies(auto_confirm=True)
            
            if success:
                # 显示成功结果
                if progress_msg:
                    try:
                        progress_msg.edit_text(
                            f"🎉 <b>代理清理成功！</b>\n\n{result_msg}",
                            parse_mode='HTML'
                        )
                    except:
                        pass
                
                # 发送额外的总结信息
                summary_text = f"""
📈 <b>优化效果预估</b>

⚡ <b>速度提升</b>
• 清理前代理数: {len(self.proxy_manager.proxies)} 个（包含失效）
• 清理后代理数: {len([p for p in self.proxy_manager.proxies])} 个可用代理
• 预计检测速度提升: 2-5倍

🎯 <b>建议</b>
• 定期运行 /testproxy 检查代理状态
• 使用 /cleanproxy 定期清理失效代理
• 在 .env 中调整 PROXY_CHECK_CONCURRENT 优化并发数

💡 现在可以开始使用优化后的代理进行账号检测了！
                """
                
                self.safe_send_message(update, summary_text, 'HTML')
            else:
                # 显示失败结果
                if progress_msg:
                    try:
                        progress_msg.edit_text(
                            f"❌ <b>代理清理失败</b>\n\n{result_msg}",
                            parse_mode='HTML'
                        )
                    except:
                        pass
                
        except Exception as e:
            self.safe_send_message(update, f"❌ 代理清理过程失败: {e}")
    
    def convert_command(self, update: Update, context: CallbackContext):
        """格式转换命令"""
        user_id = update.effective_user.id
        
        # 检查权限
        is_member, level, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 需要会员权限才能使用格式转换功能")
            return
        
        if not OPENTELE_AVAILABLE:
            self.safe_send_message(update, "❌ 格式转换功能不可用\n\n原因: opentele库未安装\n💡 请安装: pip install opentele")
            return
        
        text = """
🔄 <b>格式转换功能</b>

<b>📁 支持的转换</b>
1️⃣ <b>Tdata → Session</b>
   • 将Telegram Desktop的tdata格式转换为Session格式
   • 适用于需要使用Session的工具

2️⃣ <b>Session → Tdata</b>
   • 将Session格式转换为Telegram Desktop的tdata格式
   • 适用于Telegram Desktop客户端

<b>⚡ 功能特点</b>
• 批量并发转换，提高效率
• 实时进度显示
• 自动分类成功和失败
• 完善的错误处理

<b>📤 操作说明</b>
请选择要执行的转换类型：
        """
        
        buttons = [
            [InlineKeyboardButton("📤 Tdata → Session", callback_data="convert_tdata_to_session")],
            [InlineKeyboardButton("📥 Session → Tdata", callback_data="convert_session_to_tdata")],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data="back_to_main")]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_send_message(update, text, 'HTML', keyboard)
    
    def handle_proxy_callbacks(self, query, data):
        """处理代理相关回调"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可以操作")
            return
        
        if data == "proxy_enable":
            # 启用代理
            if self.db.set_proxy_enabled(True, user_id):
                query.answer("✅ 代理已启用")
                self.refresh_proxy_panel(query)
            else:
                query.answer("❌ 启用失败")
        
        elif data == "proxy_disable":
            # 禁用代理
            if self.db.set_proxy_enabled(False, user_id):
                query.answer("✅ 代理已禁用")
                self.refresh_proxy_panel(query)
            else:
                query.answer("❌ 禁用失败")
        
        elif data == "proxy_reload":
            # 重新加载代理列表
            old_count = len(self.proxy_manager.proxies)
            self.proxy_manager.load_proxies()
            new_count = len(self.proxy_manager.proxies)
            
            query.answer(f"✅ 重新加载完成: {old_count}→{new_count}个代理")
            self.refresh_proxy_panel(query)
        
        elif data == "proxy_status":
            # 查看详细状态
            self.show_proxy_status_popup(query)
        
        elif data == "proxy_test":
            # 测试代理连接
            self.test_proxy_connection(query)
        
        elif data == "proxy_stats":
            # 显示代理统计
            self.show_proxy_statistics(query)
        
        elif data == "proxy_cleanup":
            # 清理失效代理
            self.show_cleanup_confirmation(query)
        
        elif data == "proxy_optimize":
            # 显示速度优化信息
            self.show_speed_optimization_info(query)
    
    def refresh_proxy_panel(self, query):
        """刷新代理面板"""
        proxy_enabled_db = self.db.get_proxy_enabled()
        proxy_mode_active = self.proxy_manager.is_proxy_mode_active(self.db)
        
        # 统计住宅代理数量
        residential_count = sum(1 for p in self.proxy_manager.proxies if p.get('is_residential', False))
        
        proxy_text = f"""
<b>📡 代理管理面板</b>

<b>📊 当前状态</b>
• 系统配置: {'🟢USE_PROXY=true' if config.USE_PROXY else '🔴USE_PROXY=false'}
• 代理开关: {'🟢已启用' if proxy_enabled_db else '🔴已禁用'}
• 代理文件: {config.PROXY_FILE}
• 可用代理: {len(self.proxy_manager.proxies)}个
• 住宅代理: {residential_count}个
• 普通超时: {config.PROXY_TIMEOUT}秒
• 住宅超时: {config.RESIDENTIAL_PROXY_TIMEOUT}秒
• 实际模式: {'🟢代理模式' if proxy_mode_active else '🔴本地模式'}

<b>📝 代理格式支持</b>
• HTTP: ip:port
• HTTP认证: ip:port:username:password  
• SOCKS5: socks5:ip:port:username:password
• SOCKS4: socks4:ip:port
• ABCProxy住宅代理: host.abcproxy.vip:port:username:password
        """
        
        # 创建交互按钮
        buttons = []
        
        # 代理开关控制按钮
        if proxy_enabled_db:
            buttons.append([InlineKeyboardButton("🔴 关闭代理", callback_data="proxy_disable")])
        else:
            buttons.append([InlineKeyboardButton("🟢 开启代理", callback_data="proxy_enable")])
        
        # 其他操作按钮
        buttons.extend([
            [
                InlineKeyboardButton("🔄 刷新代理列表", callback_data="proxy_reload"),
                InlineKeyboardButton("📊 查看代理状态", callback_data="proxy_status")
            ],
            [
                InlineKeyboardButton("🧪 测试代理", callback_data="proxy_test"),
                InlineKeyboardButton("📈 代理统计", callback_data="proxy_stats")
            ],
            [InlineKeyboardButton("🔙 返回管理面板", callback_data="admin_panel")]
        ])
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, proxy_text, 'HTML', keyboard)
    
    def show_proxy_status_popup(self, query):
        """显示代理状态弹窗"""
        if self.proxy_manager.proxies:
            status_text = f"📡 可用代理: {len(self.proxy_manager.proxies)}个\n"
            enabled, updated_time, updated_by = self.db.get_proxy_setting_info()
            status_text += f"🔧 代理开关: {'启用' if enabled else '禁用'}\n"
            status_text += f"⏰ 更新时间: {updated_time}"
        else:
            status_text = "❌ 没有可用的代理"
        
        query.answer(status_text, show_alert=True)
    
    def test_proxy_connection(self, query):
        """测试代理连接"""
        if not self.proxy_manager.proxies:
            query.answer("❌ 没有可用的代理进行测试", show_alert=True)
            return
        
        # 简单测试：尝试获取一个代理
        proxy = self.proxy_manager.get_next_proxy()
        if proxy:
            query.answer(f"🧪 测试代理: {proxy['host']}:{proxy['port']} ({proxy['type']})", show_alert=True)
        else:
            query.answer("❌ 获取测试代理失败", show_alert=True)
    
    def show_proxy_statistics(self, query):
        """显示代理统计信息"""
        proxies = self.proxy_manager.proxies
        if not proxies:
            query.answer("❌ 没有代理数据", show_alert=True)
            return
        
        # 统计代理类型
        type_count = {}
        for proxy in proxies:
            proxy_type = proxy['type']
            type_count[proxy_type] = type_count.get(proxy_type, 0) + 1
        
        stats_text = f"📊 代理统计\n总数: {len(proxies)}个\n\n"
        for proxy_type, count in type_count.items():
            stats_text += f"{proxy_type.upper()}: {count}个\n"
        
        enabled, _, _ = self.db.get_proxy_setting_info()
        stats_text += f"\n状态: {'🟢启用' if enabled else '🔴禁用'}"
        
        query.answer(stats_text, show_alert=True)
    
    def show_cleanup_confirmation(self, query):
        """显示清理确认对话框"""
        query.answer()
        confirm_text = f"""
⚠️ <b>快速清理确认</b>

📊 <b>当前状态</b>
• 代理数量: {len(self.proxy_manager.proxies)} 个
• 快速模式: {'开启' if config.PROXY_FAST_MODE else '关闭'}
• 自动清理: {'启用' if config.PROXY_AUTO_CLEANUP else '禁用'}

🔧 <b>将执行以下操作</b>
• 备份原始代理文件
• 快速测试所有代理
• 自动删除失效代理
• 更新为可用代理

确认执行清理吗？
        """
        
        buttons = [
            [
                InlineKeyboardButton("✅ 确认清理", callback_data="confirm_proxy_cleanup"),
                InlineKeyboardButton("❌ 取消", callback_data="proxy_panel")
            ]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, confirm_text, 'HTML', keyboard)
    
    def show_speed_optimization_info(self, query):
        """显示速度优化信息"""
        query.answer()
        current_concurrent = config.PROXY_CHECK_CONCURRENT if config.PROXY_FAST_MODE else config.MAX_CONCURRENT_CHECKS
        current_timeout = config.PROXY_CHECK_TIMEOUT if config.PROXY_FAST_MODE else config.CHECK_TIMEOUT
        
        optimization_text = f"""
⚡ <b>速度优化配置</b>

<b>🚀 当前设置</b>
• 快速模式: {'🟢开启' if config.PROXY_FAST_MODE else '🔴关闭'}
• 并发数: {current_concurrent} 个
• 检测超时: {current_timeout} 秒
• 智能重试: {config.PROXY_RETRY_COUNT} 次
• 自动清理: {'🟢启用' if config.PROXY_AUTO_CLEANUP else '🔴禁用'}

<b>📈 优化效果</b>
• 标准模式: ~1-2 账号/秒
• 快速模式: ~3-8 账号/秒
• 预计提升: 3-5倍

<b>🔧 环境变量配置</b>
• PROXY_FAST_MODE={config.PROXY_FAST_MODE}
• PROXY_CHECK_CONCURRENT={config.PROXY_CHECK_CONCURRENT}
• PROXY_CHECK_TIMEOUT={config.PROXY_CHECK_TIMEOUT}
• PROXY_AUTO_CLEANUP={config.PROXY_AUTO_CLEANUP}
• PROXY_RETRY_COUNT={config.PROXY_RETRY_COUNT}

<b>💡 优化建议</b>
• 定期清理失效代理以提升速度
• 使用高质量代理获得最佳性能
• 根据网络状况调整并发数和超时
        """
        
        buttons = [
            [InlineKeyboardButton("🔙 返回代理面板", callback_data="proxy_panel")]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, optimization_text, 'HTML', keyboard)
    
    def show_proxy_panel(self, update: Update, query):
        """显示代理管理面板"""
        user_id = query.from_user.id
        
        # 权限检查（仅管理员可访问）
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可以访问代理管理面板")
            return
        
        query.answer()
        
        # 获取代理状态信息
        proxy_enabled_db = self.db.get_proxy_enabled()
        proxy_mode_active = self.proxy_manager.is_proxy_mode_active(self.db)
        
        # 统计住宅代理数量
        residential_count = sum(1 for p in self.proxy_manager.proxies if p.get('is_residential', False))
        
        # 构建代理管理面板信息
        proxy_text = f"""
<b>📡 代理管理面板</b>

<b>📊 当前状态</b>
• 系统配置: {'🟢USE_PROXY=true' if config.USE_PROXY else '🔴USE_PROXY=false'}
• 代理开关: {'🟢已启用' if proxy_enabled_db else '🔴已禁用'}
• 代理文件: {config.PROXY_FILE}
• 可用代理: {len(self.proxy_manager.proxies)}个
• 住宅代理: {residential_count}个
• 普通超时: {config.PROXY_TIMEOUT}秒
• 住宅超时: {config.RESIDENTIAL_PROXY_TIMEOUT}秒
• 实际模式: {'🟢代理模式' if proxy_mode_active else '🔴本地模式'}

<b>📝 代理格式支持</b>
• HTTP: ip:port
• HTTP认证: ip:port:username:password  
• SOCKS5: socks5:ip:port:username:password
• SOCKS4: socks4:ip:port
• ABCProxy住宅代理: host.abcproxy.vip:port:username:password

<b>🛠️ 操作说明</b>
• 启用/禁用：控制代理开关状态
• 重新加载：从文件重新读取代理列表
• 测试代理：检测代理连接性能
• 查看状态：显示详细代理信息
• 代理统计：查看使用数据统计
        """
        
        # 创建操作按钮
        buttons = []
        
        # 代理开关控制按钮
        if proxy_enabled_db:
            buttons.append([InlineKeyboardButton("🔴 禁用代理", callback_data="proxy_disable")])
        else:
            buttons.append([InlineKeyboardButton("🟢 启用代理", callback_data="proxy_enable")])
        
        # 代理管理操作按钮
        buttons.extend([
            [
                InlineKeyboardButton("🔄 重新加载代理", callback_data="proxy_reload"),
                InlineKeyboardButton("📊 代理状态", callback_data="proxy_status")
            ],
            [
                InlineKeyboardButton("🧪 测试代理", callback_data="proxy_test"),
                InlineKeyboardButton("📈 代理统计", callback_data="proxy_stats")
            ],
            [
                InlineKeyboardButton("🧹 清理失效代理", callback_data="proxy_cleanup"),
                InlineKeyboardButton("⚡ 速度优化", callback_data="proxy_optimize")
            ],
            [InlineKeyboardButton("🔙 返回管理面板", callback_data="admin_panel")]
        ])
        
        keyboard = InlineKeyboardMarkup(buttons)
        
        # 发送/编辑消息显示代理管理面板
        try:
            self.safe_edit_message(query, proxy_text, 'HTML', keyboard)
        except Exception as e:
            # 如果编辑失败，尝试发送新消息
            self.safe_send_message(update, proxy_text, 'HTML', keyboard)
    
    def handle_callbacks(self, update: Update, context: CallbackContext):
        query = update.callback_query
        data = query.data
        user_id = query.from_user.id  # ← 添加这一行
        if data == "start_check":
            self.handle_start_check(query)
        elif data == "format_conversion":
            self.handle_format_conversion(query)
        elif data == "change_2fa":
            self.handle_change_2fa(query)
        elif data == "convert_tdata_to_session":
            self.handle_convert_tdata_to_session(query)
        elif data == "convert_session_to_tdata":
            self.handle_convert_session_to_tdata(query)
        elif data == "api_conversion":
            self.handle_api_conversion(query)
        elif data.startswith("classify_") or data == "classify_menu":
            self.handle_classify_callbacks(update, context, query, data)
        elif query.data == "back_to_main":
            self.show_main_menu(update, user_id)
            # 返回主菜单 - 横排2x2布局
            query.answer()
            user = query.from_user
            user_id = user.id
            first_name = user.first_name or "用户"
            is_member, level, expiry = self.db.check_membership(user_id)
            
            if self.db.is_admin(user_id):
                member_status = "👑 管理员"
            elif is_member:
                member_status = f"🎁 {level}"
            else:
                member_status = "❌ 无会员"
            
            welcome_text = f"""
<b>🔍 Telegram账号机器人 V8.0</b>

👤 <b>用户信息</b>
• 昵称: {first_name}
• ID: <code>{user_id}</code>
• 会员: {member_status}
• 到期: {expiry}

📡 <b>代理状态</b>
• 代理模式: {'🟢启用' if self.proxy_manager.is_proxy_mode_active(self.db) else '🔴本地连接'}
• 代理数量: {len(self.proxy_manager.proxies)}个
• 快速模式: {'🟢开启' if config.PROXY_FAST_MODE else '🔴关闭'}
• 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            # 创建横排2x2布局的主菜单按钮
            buttons = [
                [
                    InlineKeyboardButton("🚀 账号检测", callback_data="start_check"),
                    InlineKeyboardButton("🔄 格式转换", callback_data="format_conversion")
                ],
                [
                    InlineKeyboardButton("🔐 修改2FA", callback_data="change_2fa"),
                    InlineKeyboardButton("🛡️ 防止找回", callback_data="prevent_recovery")
                ]
            ]
            
            # 管理员按钮
            if self.db.is_admin(user_id):
                buttons.append([
                    InlineKeyboardButton("👑 管理员面板", callback_data="admin_panel"),
                    InlineKeyboardButton("📡 代理管理", callback_data="proxy_panel")
                ])
            
            # 底部功能按钮
            buttons.append([
                InlineKeyboardButton("ℹ️ 帮助", callback_data="help"),
                InlineKeyboardButton("⚙️ 状态", callback_data="status")
            ])
            
            keyboard = InlineKeyboardMarkup(buttons)
            query.edit_message_text(
                text=welcome_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
        elif data == "help":
            self.handle_help_callback(query)
        elif data == "status":
            self.handle_status_callback(query)
        elif data == "admin_panel":
            self.handle_admin_panel(query)
        elif data == "proxy_panel":
            self.show_proxy_panel(update, query)
        elif data.startswith("proxy_"):
            self.handle_proxy_callbacks(query, data)
        elif data == "confirm_proxy_cleanup":
            query.answer()
            self._execute_proxy_cleanup(update, context, True)
        elif data == "cancel_proxy_cleanup":
            query.answer()
            self.safe_edit_message(query, "❌ 代理清理已取消")
        elif data == "test_only_proxy":
            # 仅测试不清理
            query.answer()
            def process_test():
                asyncio.run(self.process_proxy_test(update, context))
            thread = threading.Thread(target=process_test)
            thread.start()
            self.safe_edit_message(query, "🧪 开始测试代理（仅测试不清理）...")
        elif data == "admin_users":
            self.handle_admin_users(query)
        elif data == "admin_stats":
            self.handle_admin_stats(query)
        elif data == "admin_manage":
            self.handle_admin_manage(query)
        elif data == "admin_search":
            self.handle_admin_search(query)
        elif data == "admin_recent":
            self.handle_admin_recent(query)
        elif data.startswith("user_detail_"):
            user_id_to_view = int(data.split("_")[2])
            self.handle_user_detail(query, user_id_to_view)
        elif data.startswith("grant_membership_"):
            user_id_to_grant = int(data.split("_")[2])
            self.handle_grant_membership(query, user_id_to_grant)
        elif data.startswith("make_admin_"):
            user_id_to_make = int(data.split("_")[2])
            self.handle_make_admin(query, user_id_to_make)
        # VIP会员回调
        elif data == "vip_menu":
            self.handle_vip_menu(query)
        elif data == "vip_redeem":
            self.handle_vip_redeem(query)
        elif data == "admin_card_menu":
            self.handle_admin_card_menu(query)
        elif data.startswith("admin_card_days_"):
            days = int(data.split("_")[-1])
            self.handle_admin_card_generate(query, days)
        elif data == "admin_manual_menu":
            self.handle_admin_manual_menu(query)
        elif data.startswith("admin_manual_days_"):
            days = int(data.split("_")[-1])
            self.handle_admin_manual_grant(query, update, days)
        # 广播消息回调
        elif data.startswith("broadcast_"):
            self.handle_broadcast_callbacks(update, context, query, data)
        elif data.startswith("broadcast_alert_"):
            # 处理广播按钮回调 - 显示提示信息
            # 注意：实际的alert文本需要从按钮配置中获取，这里只是示例
            query.answer("✨ 感谢您的关注！", show_alert=True)
        elif data.startswith("status_") or data.startswith("count_"):
            query.answer("ℹ️ 这是状态信息")
    
    def handle_start_check(self, query):
        """处理开始检测"""
        query.answer()
        user_id = query.from_user.id
        
        # 检查权限
        is_member, level, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_edit_message(query, "❌ 需要会员权限才能使用检测功能")
            return
        
        if not TELETHON_AVAILABLE:
            self.safe_edit_message(query, "❌ 检测功能不可用\n\n原因: Telethon库未安装")
            return
        
        proxy_info = ""
        if config.USE_PROXY:
            proxy_count = len(self.proxy_manager.proxies)
            proxy_info = f"\n📡 代理模式: 启用 ({proxy_count}个代理)"
        
        text = f"""
📤 <b>请上传您的账号文件</b>

📁 <b>支持格式</b>
• ZIP压缩包 (推荐)
• 包含 Session + JSON 文件
• 包含 TData 文件夹{proxy_info}

请选择您的ZIP文件并上传...
        """
        
        self.safe_edit_message(query, text, 'HTML')
        
        # 设置用户状态
        self.db.save_user(user_id, query.from_user.username or "", 
                         query.from_user.first_name or "", "waiting_file")
    
    def handle_format_conversion(self, query):
        """处理格式转换选项"""
        query.answer()
        user_id = query.from_user.id
        
        # 检查权限
        is_member, level, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_edit_message(query, "❌ 需要会员权限才能使用格式转换功能")
            return
        
        if not OPENTELE_AVAILABLE:
            self.safe_edit_message(query, "❌ 格式转换功能不可用\n\n原因: opentele库未安装\n💡 请安装: pip install opentele")
            return
        
        text = """
🔄 <b>格式转换功能</b>

<b>📁 支持的转换</b>
1️⃣ <b>Tdata → Session</b>
   • 将Telegram Desktop的tdata格式转换为Session格式
   • 适用于需要使用Session的工具

2️⃣ <b>Session → Tdata</b>
   • 将Session格式转换为Telegram Desktop的tdata格式
   • 适用于Telegram Desktop客户端

<b>⚡ 功能特点</b>
• 批量并发转换，提高效率
• 实时进度显示
• 自动分类成功和失败
• 完善的错误处理

<b>📤 操作说明</b>
请选择要执行的转换类型：
        """
        
        buttons = [
            [InlineKeyboardButton("📤 Tdata → Session", callback_data="convert_tdata_to_session")],
            [InlineKeyboardButton("📥 Session → Tdata", callback_data="convert_session_to_tdata")],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data="back_to_main")]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def handle_convert_tdata_to_session(self, query):
        """处理Tdata转Session"""
        query.answer()
        user_id = query.from_user.id
        
        text = """
📤 <b>Tdata → Session 转换</b>

<b>📁 请准备以下文件</b>
• ZIP压缩包，包含Tdata文件夹
• 每个Tdata文件夹应包含 D877F783D5D3EF8C 目录

<b>🔧 转换说明</b>
• 系统将自动识别所有Tdata文件夹
• 批量转换为Session格式
• 生成对应的.session和.json文件

<b>⚡ 高性能处理</b>
• 并发转换，提高速度
• 实时显示进度
• 自动分类成功/失败

请上传您的ZIP文件...
        """
        
        self.safe_edit_message(query, text, 'HTML')
        
        # 设置用户状态
        self.db.save_user(user_id, query.from_user.username or "", 
                         query.from_user.first_name or "", "waiting_convert_tdata")
    
    def handle_convert_session_to_tdata(self, query):
        """处理Session转Tdata"""
        query.answer()
        user_id = query.from_user.id
        
        text = """
📥 <b>Session → Tdata 转换</b>

<b>📁 请准备以下文件</b>
• ZIP压缩包，包含.session文件
• 可选：对应的.json配置文件

<b>🔧 转换说明</b>
• 系统将自动识别所有Session文件
• 批量转换为Tdata格式
• 生成对应的Tdata文件夹

<b>⚡ 高性能处理</b>
• 并发转换，提高速度
• 实时显示进度
• 自动分类成功/失败

请上传您的ZIP文件...
        """
        
        self.safe_edit_message(query, text, 'HTML')
        
        # 设置用户状态
        self.db.save_user(user_id, query.from_user.username or "", 
                         query.from_user.first_name or "", "waiting_convert_session")
    
    def handle_change_2fa(self, query):
        """处理修改2FA"""
        query.answer()
        user_id = query.from_user.id
        
        # 检查权限
        is_member, level, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_edit_message(query, "❌ 需要会员权限才能使用2FA修改功能")
            return
        
        if not TELETHON_AVAILABLE:
            self.safe_edit_message(query, "❌ 2FA修改功能不可用\n\n原因: Telethon库未安装")
            return
        
        text = """
🔐 <b>批量修改2FA密码功能</b>

<b>✨ 核心功能</b>
• 🔍 <b>密码自动识别</b>
  - TData格式：自动识别 2fa.txt、twofa.txt、password.txt
  - Session格式：自动识别 JSON 中的 twoFA、2fa、password 字段
  - 智能备选：识别失败时使用手动输入的备选密码

• ✏️ <b>交互式密码输入</b>
  - 上传文件后系统提示输入密码
  - 支持两种格式：仅新密码（推荐）或 旧密码+新密码
  - 系统优先自动检测旧密码，无需手动输入
  - 5分钟输入超时保护

• 🔄 <b>自动更新密码文件</b>
  - Session格式：自动更新JSON文件中所有密码字段
  - TData格式：自动更新2fa.txt等密码文件
  - 修改成功后文件立即同步更新
  - 无需手动编辑配置文件

<b>⚠️ 注意事项</b>
• 系统会首先尝试自动识别现有密码
• 推荐使用"仅新密码"格式，让系统自动检测旧密码
• 如果自动识别失败，将使用您输入的旧密码
• 请在5分钟内输入密码，否则任务将自动取消
• 请确保账号已登录且session文件有效
• 修改成功后密码文件将自动更新并包含在结果ZIP中

🚀请上传您的ZIP文件...
        """
        
        self.safe_edit_message(query, text, 'HTML')
        
        # 设置用户状态 - 等待上传文件
        self.db.save_user(user_id, query.from_user.username or "", 
                         query.from_user.first_name or "", "waiting_2fa_file")
    
    def handle_help_callback(self, query):
        query.answer()
        help_text = """
<b>📖 详细说明</b>

<b>🚀 增强功能</b>
• 代理连接模式自动检测
• 状态|数量分离实时显示
• 检测完成后自动发送分类文件

<b>📡 代理优势</b>
• 提高检测成功率
• 避免IP限制
• 自动故障转移
        """
        
        self.safe_edit_message(query, help_text, 'HTML')
    
    def handle_status_callback(self, query):
        query.answer()
        user_id = query.from_user.id
        
        status_text = f"""
<b>⚙️ 系统状态</b>

<b>🤖 机器人信息</b>
• 版本: 8.0 (完整版)
• 状态: ✅正常运行
• 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        
        self.safe_edit_message(query, status_text, 'HTML')
    
    def handle_admin_panel(self, query):
        """管理员面板"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        # 获取统计信息
        stats = self.db.get_user_statistics()
        admin_count = len(self.db.get_all_admins()) if self.db.get_all_admins() else 0
        
        admin_text = f"""
<b>👑 管理员控制面板</b>

<b>📊 系统统计</b>
• 总用户数: {stats.get('total_users', 0)}
• 今日活跃: {stats.get('today_active', 0)}
• 本周活跃: {stats.get('week_active', 0)}
• 有效会员: {stats.get('active_members', 0)}
• 体验会员: {stats.get('trial_members', 0)}
• 近期新用户: {stats.get('recent_users', 0)}

<b>👑 管理员信息</b>
• 管理员数量: {admin_count}个
• 您的权限: {'👑 超级管理员' if user_id in config.ADMIN_IDS else '🔧 普通管理员'}
• 系统时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>🔧 快速操作</b>
点击下方按钮进行管理操作
        """
        
        # 创建管理按钮
        buttons = [
            [
                InlineKeyboardButton("👥 用户管理", callback_data="admin_users"),
                InlineKeyboardButton("📊 用户统计", callback_data="admin_stats")
            ],
            [
                InlineKeyboardButton("📡 代理管理", callback_data="proxy_panel"),
                InlineKeyboardButton("👑 管理员管理", callback_data="admin_manage")
            ],
            [
                InlineKeyboardButton("🔍 搜索用户", callback_data="admin_search"),
                InlineKeyboardButton("📋 最近用户", callback_data="admin_recent")
            ],
            [
                InlineKeyboardButton("💳 卡密开通", callback_data="admin_card_menu"),
                InlineKeyboardButton("👤 人工开通", callback_data="admin_manual_menu")
            ],
            [
                InlineKeyboardButton("📢 群发通知", callback_data="broadcast_menu")
            ],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data="back_to_main")]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, admin_text, 'HTML', keyboard)
    def handle_admin_users(self, query):
        """用户管理界面"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        query.answer()
        
        # 获取活跃用户列表
        active_users = self.db.get_active_users(days=7, limit=15)
        
        text = "<b>👥 用户管理</b>\n\n<b>📋 最近活跃用户（7天内）</b>\n\n"
        
        if active_users:
            for i, (uid, username, first_name, register_time, last_active, status) in enumerate(active_users[:10], 1):
                # 检查会员状态
                is_member, level, _ = self.db.check_membership(uid)
                member_icon = "🎁" if is_member else "❌"
                admin_icon = "👑" if self.db.is_admin(uid) else ""
                
                display_name = first_name or username or f"用户{uid}"
                if len(display_name) > 15:
                    display_name = display_name[:15] + "..."
                
                text += f"{i}. {admin_icon}{member_icon} <code>{uid}</code> - {display_name}\n"
                if last_active:
                    try:
                        last_time = datetime.strptime(last_active, '%Y-%m-%d %H:%M:%S')
                        time_diff = datetime.now() - last_time
                        if time_diff.days == 0:
                            time_str = f"{time_diff.seconds//3600}小时前"
                        else:
                            time_str = f"{time_diff.days}天前"
                        text += f"   🕒 {time_str}\n"
                    except:
                        text += f"   🕒 {last_active}\n"
                text += "\n"
        else:
            text += "暂无活跃用户\n"
        
        text += f"\n📊 <b>图例</b>\n👑 = 管理员 | 🎁 = 会员 | ❌ = 普通用户"
        
        buttons = [
            [
                InlineKeyboardButton("🔍 搜索用户", callback_data="admin_search"),
                InlineKeyboardButton("📋 最近注册", callback_data="admin_recent")
            ],
            [
                InlineKeyboardButton("📊 用户统计", callback_data="admin_stats"),
                InlineKeyboardButton("🔄 刷新列表", callback_data="admin_users")
            ],
            [InlineKeyboardButton("🔙 返回管理面板", callback_data="admin_panel")]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, text, 'HTML', keyboard)

    def handle_admin_stats(self, query):
        """用户统计界面"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        query.answer()
        
        stats = self.db.get_user_statistics()
        
        # 计算比率
        total = stats.get('total_users', 0)
        active_rate = (stats.get('week_active', 0) / total * 100) if total > 0 else 0
        member_rate = (stats.get('active_members', 0) / total * 100) if total > 0 else 0
        
        text = f"""
<b>📊 用户统计报告</b>

<b>🔢 基础数据</b>
• 总用户数: {stats.get('total_users', 0)}
• 今日活跃: {stats.get('today_active', 0)}
• 本周活跃: {stats.get('week_active', 0)} ({active_rate:.1f}%)
• 近期新用户: {stats.get('recent_users', 0)} (7天内)

<b>💎 会员数据</b>
• 有效会员: {stats.get('active_members', 0)} ({member_rate:.1f}%)
• 体验会员: {stats.get('trial_members', 0)}
• 转换率: {member_rate:.1f}%

<b>📈 活跃度分析</b>
• 周活跃率: {active_rate:.1f}%
• 日活跃率: {(stats.get('today_active', 0) / total * 100) if total > 0 else 0:.1f}%

<b>⏰ 统计时间</b>
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        buttons = [
            [
                InlineKeyboardButton("👥 用户管理", callback_data="admin_users"),
                InlineKeyboardButton("🔄 刷新统计", callback_data="admin_stats")
            ],
            [InlineKeyboardButton("🔙 返回管理面板", callback_data="admin_panel")]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, text, 'HTML', keyboard)

    def handle_admin_manage(self, query):
        """管理员管理界面"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        query.answer()
        
        # 获取管理员列表
        admins = self.db.get_all_admins()
        
        text = "<b>👑 管理员管理</b>\n\n<b>📋 当前管理员列表</b>\n\n"
        
        if admins:
            for i, (admin_id, username, first_name, added_time) in enumerate(admins, 1):
                is_super = admin_id in config.ADMIN_IDS
                admin_type = "👑 超级管理员" if is_super else "🔧 普通管理员"
                
                display_name = first_name or username or f"管理员{admin_id}"
                if len(display_name) > 15:
                    display_name = display_name[:15] + "..."
                
                text += f"{i}. {admin_type}\n"
                text += f"   ID: <code>{admin_id}</code>\n"
                text += f"   昵称: {display_name}\n"
                if username and username != "配置文件管理员":
                    text += f"   用户名: @{username}\n"
                text += f"   添加时间: {added_time}\n\n"
        else:
            text += "暂无管理员\n"
        
        text += f"\n<b>💡 说明</b>\n• 超级管理员来自配置文件\n• 普通管理员可通过命令添加"
        
        buttons = [
            [InlineKeyboardButton("🔙 返回管理面板", callback_data="admin_panel")]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, text, 'HTML', keyboard)

    def handle_admin_search(self, query):
        """搜索用户界面"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        query.answer()
        
        text = """
<b>🔍 用户搜索</b>

<b>搜索说明：</b>
• 输入用户ID（纯数字）
• 输入用户名（@username 或 username）
• 输入昵称关键词

<b>示例：</b>
• <code>123456789</code> - 按ID搜索
• <code>@username</code> - 按用户名搜索
• <code>张三</code> - 按昵称搜索

请发送要搜索的内容...
        """
        
        # 设置用户状态为等待搜索输入
        self.db.save_user(
            user_id,
            query.from_user.username or "",
            query.from_user.first_name or "",
            "waiting_admin_search"
        )
        
        buttons = [
            [InlineKeyboardButton("❌ 取消搜索", callback_data="admin_users")]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, text, 'HTML', keyboard)

    def handle_admin_recent(self, query):
        """最近注册用户"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        query.answer()
        
        recent_users = self.db.get_recent_users(limit=15)
        
        text = "<b>📋 最近注册用户</b>\n\n"
        
        if recent_users:
            for i, (uid, username, first_name, register_time, last_active, status) in enumerate(recent_users, 1):
                # 检查会员状态
                is_member, level, _ = self.db.check_membership(uid)
                member_icon = "🎁" if is_member else "❌"
                admin_icon = "👑" if self.db.is_admin(uid) else ""
                
                display_name = first_name or username or f"用户{uid}"
                if len(display_name) > 15:
                    display_name = display_name[:15] + "..."
                
                text += f"{i}. {admin_icon}{member_icon} <code>{uid}</code> - {display_name}\n"
                
                if register_time:
                    try:
                        reg_time = datetime.strptime(register_time, '%Y-%m-%d %H:%M:%S')
                        time_diff = datetime.now() - reg_time
                        if time_diff.days == 0:
                            time_str = f"{time_diff.seconds//3600}小时前注册"
                        else:
                            time_str = f"{time_diff.days}天前注册"
                        text += f"   📅 {time_str}\n"
                    except:
                        text += f"   📅 {register_time}\n"
                text += "\n"
        else:
            text += "暂无用户数据\n"
        
        text += f"\n📊 <b>图例</b>\n👑 = 管理员 | 🎁 = 会员 | ❌ = 普通用户"
        
        buttons = [
            [
                InlineKeyboardButton("👥 用户管理", callback_data="admin_users"),
                InlineKeyboardButton("🔄 刷新列表", callback_data="admin_recent")
            ],
            [InlineKeyboardButton("🔙 返回管理面板", callback_data="admin_panel")]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, text, 'HTML', keyboard)

    def handle_user_detail(self, query, target_user_id: int):
        """显示用户详细信息"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        query.answer()
        
        user_info = self.db.get_user_membership_info(target_user_id)
        
        if not user_info:
            self.safe_edit_message(query, f"❌ 找不到用户 {target_user_id}")
            return
        
        # 格式化显示
        username = user_info.get('username', '')
        first_name = user_info.get('first_name', '')
        register_time = user_info.get('register_time', '')
        last_active = user_info.get('last_active', '')
        membership_level = user_info.get('membership_level', '')
        expiry_time = user_info.get('expiry_time', '')
        is_admin = user_info.get('is_admin', False)
        
        # 计算活跃度
        activity_status = "🔴 从未活跃"
        if last_active:
            try:
                last_time = datetime.strptime(last_active, '%Y-%m-%d %H:%M:%S')
                time_diff = datetime.now() - last_time
                if time_diff.days == 0:
                    activity_status = f"🟢 {time_diff.seconds//3600}小时前活跃"
                elif time_diff.days <= 7:
                    activity_status = f"🟡 {time_diff.days}天前活跃"
                else:
                    activity_status = f"🔴 {time_diff.days}天前活跃"
            except:
                activity_status = f"🔴 {last_active}"
        
        # 会员状态
        member_status = "❌ 无会员"
        if membership_level and membership_level != "无会员":
            if expiry_time:
                try:
                    expiry_dt = datetime.strptime(expiry_time, '%Y-%m-%d %H:%M:%S')
                    if expiry_dt > datetime.now():
                        member_status = f"🎁 {membership_level}（有效至 {expiry_time}）"
                    else:
                        member_status = f"⏰ {membership_level}（已过期）"
                except:
                    member_status = f"🎁 {membership_level}"
        
        text = f"""
<b>👤 用户详细信息</b>

<b>📋 基本信息</b>
• 用户ID: <code>{target_user_id}</code>
• 昵称: {first_name or '未设置'}
• 用户名: @{username} 
• 权限: {'👑 管理员' if is_admin else '👤 普通用户'}

<b>📅 时间信息</b>
• 注册时间: {register_time or '未知'}
• 最后活跃: {last_active or '从未活跃'}
• 活跃状态: {activity_status}

<b>💎 会员信息</b>
• 会员状态: {member_status}

<b>🔧 管理操作</b>
点击下方按钮进行管理操作
        """
        
        buttons = [
            [InlineKeyboardButton("🎁 授予体验会员", callback_data=f"grant_membership_{target_user_id}")]
        ]
        
        # 如果不是管理员，显示设为管理员按钮
        if not is_admin:
            buttons.append([InlineKeyboardButton("👑 设为管理员", callback_data=f"make_admin_{target_user_id}")])
        
        buttons.append([InlineKeyboardButton("🔙 返回", callback_data="admin_users")])
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, text, 'HTML', keyboard)

    def handle_grant_membership(self, query, target_user_id: int):
        """授予用户体验会员"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        # 检查用户是否存在
        user_info = self.db.get_user_membership_info(target_user_id)
        if not user_info:
            query.answer("❌ 用户不存在")
            return
        
        # 授予体验会员
        success = self.db.save_membership(target_user_id, "体验会员")
        
        if success:
            query.answer("✅ 体验会员授予成功")
            # 刷新用户详情页面
            self.handle_user_detail(query, target_user_id)
        else:
            query.answer("❌ 授予失败")

    def handle_make_admin(self, query, target_user_id: int):
        """设置用户为管理员"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        # 检查用户是否存在
        user_info = self.db.get_user_membership_info(target_user_id)
        if not user_info:
            query.answer("❌ 用户不存在")
            return
        
        username = user_info.get('username', '')
        first_name = user_info.get('first_name', '')
        
        # 添加为管理员
        success = self.db.add_admin(target_user_id, username, first_name, user_id)
        
        if success:
            query.answer("✅ 管理员设置成功")
            # 刷新用户详情页面
            self.handle_user_detail(query, target_user_id)
        else:
            query.answer("❌ 设置失败")
    def handle_proxy_panel(self, query):
        """代理面板"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        # 直接调用刷新代理面板
        self.refresh_proxy_panel(query)

    def handle_file(self, update: Update, context: CallbackContext):
        """处理文件上传"""
        user_id = update.effective_user.id
        document = update.message.document

        if not document or not document.file_name.lower().endswith('.zip'):
            self.safe_send_message(update, "❌ 请上传ZIP格式的压缩包")
            return

        try:
            conn = sqlite3.connect(config.DB_NAME)
            c = conn.cursor()
            c.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            conn.close()

            # 放行的状态，新增 waiting_api_file
            if not row or row[0] not in [
                "waiting_file",
                "waiting_convert_tdata",
                "waiting_convert_session",
                "waiting_2fa_file",
                "waiting_api_file",
                "waiting_classify_file",
            ]:
                self.safe_send_message(update, "❌ 请先点击 🚀开始检测、🔄格式转换、🔐修改2FA、🔗API转换 或 📦账号分类 按钮")
                return

            user_status = row[0]
        except Exception:
            self.safe_send_message(update, "❌ 系统错误，请重试")
            return

        is_member, _, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 需要会员权限")
            return

        if document.file_size > 100 * 1024 * 1024:
            self.safe_send_message(update, "❌ 文件过大 (限制100MB)")
            return

        # 根据用户状态选择处理方式
        if user_status == "waiting_file":
            # 异步处理账号检测
            def process_file():
                asyncio.run(self.process_enhanced_check(update, context, document))
            thread = threading.Thread(target=process_file)
            thread.start()

        elif user_status in ["waiting_convert_tdata", "waiting_convert_session"]:
            # 异步处理格式转换
            def process_conversion():
                asyncio.run(self.process_format_conversion(update, context, document, user_status))
            thread = threading.Thread(target=process_conversion)
            thread.start()

        elif user_status == "waiting_2fa_file":
            # 异步处理2FA密码修改
            def process_2fa():
                asyncio.run(self.process_2fa_change(update, context, document))
            thread = threading.Thread(target=process_2fa)
            thread.start()

        elif user_status == "waiting_api_file":
            # 新增：API转换处理
            def process_api_conversion():
                asyncio.run(self.process_api_conversion(update, context, document))
            thread = threading.Thread(target=process_api_conversion)
            thread.start()
        elif user_status == "waiting_classify_file":
            # 账号分类处理
            def process_classify():
                asyncio.run(self.process_classify_stage1(update, context, document))
            thread = threading.Thread(target=process_classify, daemon=True)
            thread.start()
        elif user_status == "waiting_api_file":
            # API转换：阶段1（解析并询问2FA）
            def process_api_conversion():
                asyncio.run(self.process_api_conversion(update, context, document))
            thread = threading.Thread(target=process_api_conversion)
            thread.start()
        # 清空用户状态
        self.db.save_user(
            user_id,
            update.effective_user.username or "",
            update.effective_user.first_name or "",
            ""
        )


    async def process_api_conversion(self, update, context, document):
        """API格式转换 - 阶段1：解析文件并询问网页展示的2FA"""
        user_id = update.effective_user.id
        start_time = time.time()
        task_id = f"{user_id}_{int(start_time)}"

        progress_msg = self.safe_send_message(update, "📥 <b>正在处理您的文件...</b>", 'HTML')
        if not progress_msg:
            return

        temp_zip = None
        try:
            temp_dir = tempfile.mkdtemp(prefix="temp_api_")
            temp_zip = os.path.join(temp_dir, document.file_name)
            document.get_file().download(temp_zip)

            files, extract_dir, file_type = self.processor.scan_zip_file(temp_zip, user_id, task_id)
            if not files:
                try:
                    progress_msg.edit_text("❌ <b>未找到有效文件</b>\n\n请确保ZIP包含Session或TData格式的文件", parse_mode='HTML')
                except:
                    pass
                return

            total_files = len(files)
            try:
                progress_msg.edit_text(
                    f"✅ <b>已找到 {total_files} 个账号文件</b>\n"
                    f"📊 类型: {file_type.upper()}\n\n"
                    f"🔐 请输入将在网页上显示的 2FA 密码：\n"
                    f"• 直接发送 2FA 密码，例如: <code>My2FA@2024</code>\n"
                    f"• 或回复 <code>跳过</code> 使用自动识别\n\n"
                    f"⏰ 5分钟超时",
                    parse_mode='HTML'
                )
            except:
                pass

            # 记录待处理任务，等待用户输入2FA
            self.pending_api_tasks[user_id] = {
                "files": files,
                "file_type": file_type,
                "extract_dir": extract_dir,
                "task_id": task_id,
                "progress_msg": progress_msg,
                "start_time": start_time,
                "temp_zip": temp_zip
            }
        except Exception as e:
            print(f"❌ API阶段1失败: {e}")
            try:
                progress_msg.edit_text(f"❌ 失败: {str(e)}", parse_mode='HTML')
            except:
                pass
            if temp_zip and os.path.exists(temp_zip):
                try:
                    shutil.rmtree(os.path.dirname(temp_zip), ignore_errors=True)
                except:
                    pass
    async def continue_api_conversion(self, update, context, user_id: int, two_fa_input: Optional[str]):
        """API格式转换 - 阶段2：执行转换并生成仅含链接的TXT"""
        result_files = []
        task = self.pending_api_tasks.get(user_id)
        if not task:
            self.safe_send_message(update, "❌ 没有待处理的API转换任务")
            return

        files = task["files"]
        file_type = task["file_type"]
        extract_dir = task["extract_dir"]
        task_id = task["task_id"]
        progress_msg = task["progress_msg"]
        temp_zip = task["temp_zip"]
        start_time = task["start_time"]

        override_two_fa = None if (not two_fa_input or two_fa_input.strip().lower() in ["跳过", "skip"]) else two_fa_input.strip()

        # 更新提示
        try:
            tip = "🔄 <b>开始转换为API格式...</b>\n\n"
            if override_two_fa:
                tip += f"🔐 网页2FA: <code>{override_two_fa}</code>\n"
            else:
                tip += "🔐 网页2FA: 自动识别\n"
            progress_msg.edit_text(tip, parse_mode='HTML')
        except:
            pass

        try:
            # =================== 变量初始化 ===================
            total_files = len(files)
            api_accounts = []
            failed_accounts = []
            failure_reasons = {}
            
            # =================== 性能参数计算 ===================  
            max_concurrent = 15 if total_files > 100 else 10 if total_files > 50 else 5
            batch_size = min(20, max(5, total_files // 5))  # 统一的批次计算
            semaphore = asyncio.Semaphore(max_concurrent)
            
            print(f"🚀 并发转换参数: 文件={total_files}, 批次={batch_size}, 并发={max_concurrent}")
            
            # =================== 进度提示 ===================
            try:
                progress_msg.edit_text(
                    f"🔄 <b>开始API转换...</b>\n\n"
                    f"📊 总文件: {total_files} 个\n"
                    f"📁 类型: {file_type.upper()}\n"
                    f"🔐 2FA设置: {'自定义' if override_two_fa else '自动检测'}\n"
                    f"🚀 并发数: {max_concurrent} | 批次: {batch_size}\n\n"
                    f"正在处理...",
                    parse_mode='HTML'
                )
            except:
                pass

            # =================== 并发批处理循环 ===================
            for i in range(0, total_files, batch_size):
                batch_files = files[i:i + batch_size]
                
                # 更新进度
                try:
                    processed = i
                    progress = int(processed / total_files * 100)
                    elapsed = time.time() - start_time
                    speed = processed / elapsed if elapsed > 0 and processed > 0 else 0
                    remaining = (total_files - processed) / speed if speed > 0 else 0
                    
                    # 生成失败原因统计
                    failure_stats = ""
                    if failure_reasons:
                        failure_stats = "\n\n❌ <b>失败统计</b>\n"
                        for reason, count in failure_reasons.items():
                            failure_stats += f"• {reason}: {count}个\n"
                    
                    progress_text = f"""
🔄 <b>API转换进行中...</b>

📊 <b>转换进度</b>
• 进度: {progress}% ({processed}/{total_files})
• ✅ 成功: {len(api_accounts)} 个
• ❌ 失败: {len(failed_accounts)} 个
• 平均速度: {speed:.1f} 个/秒
• 预计剩余: {remaining/60:.1f} 分钟

⚡ <b>处理状态</b>
• 文件类型: {file_type.upper()}
• 2FA模式: {'自定义' if override_two_fa else '自动检测'}
• 已用时: {elapsed:.1f} 秒{failure_stats}
                    """
                    
                    progress_msg.edit_text(progress_text, parse_mode='HTML')
                except:
                    pass
                
                # 并发处理当前批次 - 高速版
                # 并发处理当前批次
                async def process_single_file(file_path, file_name):
                    try:
                        single_result = await self.api_converter.convert_to_api_format(
                            [(file_path, file_name)], file_type, override_two_fa
                        )
                        
                        if single_result and len(single_result) > 0:
                            return ("success", single_result[0], file_name)
                        else:
                            reason = await self.get_conversion_failure_reason(file_path, file_type)
                            return ("failed", reason, file_name)
                            
                    except Exception as e:
                        error_msg = str(e).lower()
                        if "auth" in error_msg:
                            reason = "未授权"
                        elif "timeout" in error_msg:
                            reason = "连接超时"
                        else:
                            reason = "转换异常"
                        
                        return ("failed", reason, file_name)
                
                # 创建并发任务
                tasks = [process_single_file(file_path, file_name) for file_path, file_name in batch_files]
                
                # 并发执行所有任务
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # 处理结果
                for result in results:
                    if isinstance(result, Exception):
                        failed_accounts.append(("未知文件", "并发异常"))
                        failure_reasons["并发异常"] = failure_reasons.get("并发异常", 0) + 1
                        continue
                    
                    status, data, file_name = result
                    if status == "success":
                        api_accounts.append(data)
                    else:  # failed
                        failed_accounts.append((file_name, data))
                        failure_reasons[data] = failure_reasons.get(data, 0) + 1
                
                # 短暂延迟
                await asyncio.sleep(0.1)  # 减少延迟提升速度

            # 仅生成TXT
            result_files = self.api_converter.create_api_result_files(api_accounts, task_id)
            elapsed_time = time.time() - start_time

            # 生成详细的失败原因统计
            failure_detail = ""
            if failure_reasons:
                failure_detail = "\n\n❌ <b>失败原因详细</b>\n"
                for reason, count in failure_reasons.items():
                    percentage = (count / total_files * 100) if total_files > 0 else 0
                    failure_detail += f"• {reason}: {count}个 ({percentage:.1f}%)\n"
            
            success_rate = (len(api_accounts) / total_files * 100) if total_files > 0 else 0
            
            # 发送结果（TXT）
            summary_text = f"""
🎉 <b>API格式转换完成！</b>

📊 <b>转换统计</b>
• 总计: {total_files} 个
• ✅ 成功: {len(api_accounts)} 个 ({success_rate:.1f}%)
• ❌ 失败: {len(failed_accounts)} 个 ({100-success_rate:.1f}%)
• ⏱️ 用时: {int(elapsed_time)} 秒
• 🚀 速度: {total_files/elapsed_time:.1f} 个/秒{failure_detail}

📄 正在发送TXT文件...
            """
            try:
                progress_msg.edit_text(summary_text, parse_mode='HTML')
            except:
                pass

            for file_path in result_files:
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'rb') as f:
                            caption = "📋 API链接（手机号 + 链接）"
                            context.bot.send_document(
                                chat_id=update.effective_chat.id,
                                document=f,
                                filename=os.path.basename(file_path),
                                caption=caption,
                                parse_mode='HTML'
                            )
                        print(f"📤 已发送TXT: {os.path.basename(file_path)}")
                        await asyncio.sleep(0.5)
                    except Exception as e:
                        print(f"❌ 发送TXT失败: {e}")

            # 完成提示
            self.safe_send_message(
                update,
                "✅ 如需再次使用 /start （转换失败的账户不会发送）\n"
            )

        except Exception as e:
            print(f"❌ API阶段2失败: {e}")
            try:
                progress_msg.edit_text(f"❌ 失败: {str(e)}", parse_mode='HTML')
            except:
                pass
        finally:
            # 清理
            if temp_zip and os.path.exists(temp_zip):
                try:
                    shutil.rmtree(os.path.dirname(temp_zip), ignore_errors=True)
                except:
                    pass
            if user_id in self.pending_api_tasks:
                del self.pending_api_tasks[user_id]
            # 可选：清理生成的TXT（如果你不想保留）
            try:
                for file_path in result_files:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"🗑️ 已删除TXT: {os.path.basename(file_path)}")
            except Exception as _:
                pass
    async def get_conversion_failure_reason(self, file_path: str, file_type: str) -> str:
        """获取转换失败的具体原因"""
        try:
            if file_type == "session":
                if not os.path.exists(file_path):
                    return "文件不存在"
                
                if os.path.getsize(file_path) < 100:
                    return "文件损坏"
                
                return "转换失败"
            
            elif file_type == "tdata":
                if not os.path.exists(file_path):
                    return "目录不存在"
                
                return "转换失败"
            
            return "未知错误"
            
        except Exception:
            return "检测失败"
            
    async def process_enhanced_check(self, update, context, document):
        """增强版检测处理"""
        user_id = update.effective_user.id
        start_time = time.time()
        task_id = f"{user_id}_{int(start_time)}"
        
        print(f"🚀 开始增强版检测任务: {task_id}")
        print(f"📡 代理模式: {'启用' if config.USE_PROXY else '禁用'}")
        print(f"🔢 可用代理: {len(self.proxy_manager.proxies)}个")
        
        # 安全发送进度消息
        progress_msg = self.safe_send_message(
            update,
            "📥 <b>正在处理您的文件...</b>",
            'HTML'
        )
        
        if not progress_msg:
            print("❌ 无法发送进度消息")
            return
        
        # 创建临时文件用于下载
        temp_zip = None
        try:
            # 下载上传的文件到临时位置
            temp_dir = tempfile.mkdtemp(prefix="temp_download_")
            temp_zip = os.path.join(temp_dir, document.file_name)
            
            document.get_file().download(temp_zip)
            print(f"📥 临时下载文件: {temp_zip}")
            
            # 扫描并正确保存文件
            files, extract_dir, file_type = self.processor.scan_zip_file(temp_zip, user_id, task_id)
            
            if not files:
                try:
                    progress_msg.edit_text(
                        "❌ <b>未找到有效的账号文件</b>\n\n"
                        "请确保ZIP文件包含:\n"
                        "• Session + JSON 文件\n"
                        "• TData 文件夹",
                        parse_mode='HTML'
                    )
                except:
                    pass
                return
            
            total_accounts = len(files)
            proxy_status = f"📡 {'代理模式' if config.USE_PROXY else '本地模式'}"
            print(f"📊 找到 {total_accounts} 个账号文件，类型: {file_type}")
            
            # 开始检测提示
            try:
                progress_msg.edit_text(
                    f"🔍 <b>开始检测 {total_accounts} 个账号...</b>\n\n"
                    f"📊 文件类型: {file_type.upper()}\n"
                    f"{proxy_status}\n"
                    f"⚡ 并发线程: {config.MAX_CONCURRENT_CHECKS}个\n\n"
                    f"请稍等，状态|数量分离按钮将实时显示检测进度...",
                    parse_mode='HTML'
                )
            except:
                pass
            
            # 实时更新回调函数
            async def enhanced_callback(processed, total, results, speed, elapsed):
                try:
                    progress = int(processed / total * 100)
                    remaining_time = (total - processed) / speed if speed > 0 else 0
                    
                    text = f"""
⚡ <b>检测进行中...</b>

📊 <b>检测进度</b>
• 进度: {progress}% ({processed}/{total})
• 格式: {file_type.upper()}
• 模式: {'📡代理模式' if config.USE_PROXY else '🏠本地模式'}
• 速度: {speed:.1f} 账号/秒
• 预计剩余: {remaining_time/60:.1f} 分钟

⚡ <b>优化状态</b>
• 快速模式: {'🟢开启' if config.PROXY_FAST_MODE else '🔴关闭'}
• 并发数: {config.PROXY_CHECK_CONCURRENT if config.PROXY_FAST_MODE else config.MAX_CONCURRENT_CHECKS}
• 检测超时: {config.PROXY_CHECK_TIMEOUT if config.PROXY_FAST_MODE else config.CHECK_TIMEOUT}秒
                    """
                    
                    # 创建状态|数量分离按钮
                    keyboard = self.create_status_count_separate_buttons(results, processed, total)
                    
                    # 安全编辑消息
                    try:
                        progress_msg.edit_text(text, parse_mode='HTML', reply_markup=keyboard)
                    except RetryAfter as e:
                        print(f"⚠️ 编辑消息频率限制，等待 {e.retry_after} 秒")
                        await asyncio.sleep(e.retry_after + 1)
                        try:
                            progress_msg.edit_text(text, parse_mode='HTML', reply_markup=keyboard)
                        except:
                            pass
                    except BadRequest as e:
                        if "message is not modified" not in str(e).lower():
                            print(f"❌ 编辑消息失败: {e}")
                    except Exception as e:
                        print(f"❌ 增强版按钮更新失败: {e}")
                    
                except Exception as e:
                    print(f"❌ 增强版回调失败: {e}")
            
            # 开始检测
            results = await self.processor.check_accounts_with_realtime_updates(
                files, file_type, enhanced_callback
            )
            
            print("📦 开始生成结果文件...")
            
            # 生成结果文件
            result_files = self.processor.create_result_zips(results, task_id, file_type)
            
            print(f"✅ 生成了 {len(result_files)} 个结果文件")
            
            # 最终结果显示
            total_time = time.time() - start_time
            final_speed = total_accounts / total_time if total_time > 0 else 0
            
            # 统计代理使用情况
            proxy_stats = ""
            if config.USE_PROXY:
                proxy_used_count = sum(1 for _, _, info in sum(results.values(), []) if "代理" in info)
                local_used_count = total_accounts - proxy_used_count
                proxy_stats = f"\n📡 代理连接: {proxy_used_count}个\n🏠 本地连接: {local_used_count}个"
            
            final_text = f"""
✅ <b>检测完成！正在自动发送文件...</b>

📊 <b>最终结果</b>
• 总计账号: {total_accounts}个
• 🟢 无限制: {len(results['无限制'])}个
• 🟡 垃圾邮件: {len(results['垃圾邮件'])}个
• 🔴 冻结: {len(results['冻结'])}个
• 🟠 封禁: {len(results['封禁'])}个
• ⚫ 连接错误: {len(results['连接错误'])}个{proxy_stats}

⚡ <b>性能统计</b>
• 检测时间: {int(total_time)}秒 ({total_time/60:.1f}分钟)
• 平均速度: {final_speed:.1f} 账号/秒
• 优化模式: {'🟢快速模式' if config.PROXY_FAST_MODE else '🔴标准模式'}
• 并发数: {config.PROXY_CHECK_CONCURRENT if config.PROXY_FAST_MODE else config.MAX_CONCURRENT_CHECKS}

🚀 正在自动发送分类文件，请稍等...
            """
            
            # 最终状态按钮
            final_keyboard = self.create_status_count_separate_buttons(results, total_accounts, total_accounts)
            
            try:
                progress_msg.edit_text(final_text, parse_mode='HTML', reply_markup=final_keyboard)
            except:
                pass
            
            # 自动发送所有分类文件
            sent_count = 0
            for file_path, status, count in result_files:
                if os.path.exists(file_path):
                    try:
                        print(f"📤 正在发送: {status}_{count}个.zip")
                        
                        with open(file_path, 'rb') as f:
                            context.bot.send_document(
                                chat_id=update.effective_chat.id,
                                document=f,
                                filename=f"{status}_{count}个.zip",
                                caption=f"📋 <b>{status}</b> - {count}个账号\n\n"
                                       f"⏰ 检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                                       f"🔧 检测模式: {'代理模式' if config.USE_PROXY else '本地模式'}",
                                parse_mode='HTML'
                            )
                        
                        sent_count += 1
                        print(f"✅ 发送成功: {status}_{count}个.zip")
                        
                        # 延迟避免发送过快
                        await asyncio.sleep(1.0)
                        
                    except RetryAfter as e:
                        print(f"⚠️ 发送文件频率限制，等待 {e.retry_after} 秒")
                        await asyncio.sleep(e.retry_after + 1)
                        # 重试发送
                        try:
                            with open(file_path, 'rb') as f:
                                context.bot.send_document(
                                    chat_id=update.effective_chat.id,
                                    document=f,
                                    filename=f"{status}_{count}个.zip",
                                    caption=f"📋 <b>{status}</b> - {count}个账号",
                                    parse_mode='HTML'
                                )
                            sent_count += 1
                        except Exception as e2:
                            print(f"❌ 重试发送失败: {e2}")
                    except Exception as e:
                        print(f"❌ 发送文件失败: {status} - {e}")
            
            # 发送完成总结
            if sent_count > 0:
                summary_text = f"""
🎉 <b>所有文件发送完成！</b>

📋 <b>发送总结</b>
• 成功发送: {sent_count} 个文件
• 检测模式: {'📡代理模式' if config.USE_PROXY else '🏠本地模式'}
• 检测时间: {int(total_time)}秒

感谢使用增强版机器人！如需再次检测，请点击 /start
                """
                
                try:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=summary_text,
                        parse_mode='HTML'
                    )
                except:
                    pass
            else:
                try:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="❌ 没有文件可以发送"
                    )
                except:
                    pass
            
            print("✅ 增强版检测任务完成")
            
        except Exception as e:
            print(f"❌ 处理失败: {e}")
            try:
                progress_msg.edit_text(f"❌ 处理失败: {str(e)}")
            except:
                pass
        finally:
            # 清理临时下载文件
            if temp_zip and os.path.exists(temp_zip):
                try:
                    shutil.rmtree(os.path.dirname(temp_zip), ignore_errors=True)
                    print(f"🗑️ 清理临时文件: {temp_zip}")
                except:
                    pass
    
    async def process_format_conversion(self, update, context, document, user_status):
        """处理格式转换"""
        user_id = update.effective_user.id
        start_time = time.time()
        task_id = f"{user_id}_{int(start_time)}"
        
        conversion_type = "tdata_to_session" if user_status == "waiting_convert_tdata" else "session_to_tdata"
        print(f"🔄 开始格式转换任务: {task_id} | 类型: {conversion_type}")
        
        # 发送进度消息
        progress_msg = self.safe_send_message(
            update,
            "📥 <b>正在处理您的文件...</b>",
            'HTML'
        )
        
        if not progress_msg:
            print("❌ 无法发送进度消息")
            return
        
        temp_zip = None
        try:
            # 下载文件
            temp_dir = tempfile.mkdtemp(prefix="temp_conversion_")
            temp_zip = os.path.join(temp_dir, document.file_name)
            
            document.get_file().download(temp_zip)
            print(f"📥 下载文件: {temp_zip}")
            
            # 扫描文件
            files, extract_dir, file_type = self.processor.scan_zip_file(temp_zip, user_id, task_id)
            
            if not files:
                try:
                    progress_msg.edit_text(
                        "❌ <b>未找到有效文件</b>\n\n请确保ZIP包含正确的格式",
                        parse_mode='HTML'
                    )
                except:
                    pass
                return
            
            # 验证文件类型
            if conversion_type == "tdata_to_session" and file_type != "tdata":
                try:
                    progress_msg.edit_text(
                        f"❌ <b>文件类型错误</b>\n\n需要Tdata文件，但找到的是{file_type}格式",
                        parse_mode='HTML'
                    )
                except:
                    pass
                return
            
            if conversion_type == "session_to_tdata" and file_type != "session":
                try:
                    progress_msg.edit_text(
                        f"❌ <b>文件类型错误</b>\n\n需要Session文件，但找到的是{file_type}格式",
                        parse_mode='HTML'
                    )
                except:
                    pass
                return
            
            total_files = len(files)
            
            try:
                progress_msg.edit_text(
                    f"🔄 <b>开始转换...</b>\n\n📁 找到 {total_files} 个文件\n⏳ 正在初始化...",
                    parse_mode='HTML'
                )
            except:
                pass
            
            # 定义进度回调
            async def conversion_callback(processed, total, results, speed, elapsed):
                try:
                    success_count = len(results.get("转换成功", []))
                    error_count = len(results.get("转换错误", []))
                    
                    progress_text = f"""
🔄 <b>格式转换进行中...</b>

📊 <b>当前进度</b>
• 已处理: {processed}/{total}
• 速度: {speed:.1f} 个/秒
• 用时: {int(elapsed)} 秒

✅ <b>转换成功</b>: {success_count}
❌ <b>转换错误</b>: {error_count}

⏱️ 预计剩余: {int((total - processed) / speed) if speed > 0 else 0} 秒
                    """
                    
                    progress_msg.edit_text(progress_text, parse_mode='HTML')
                except Exception as e:
                    print(f"⚠️ 更新进度失败: {e}")
            
            # 执行批量转换
            results = await self.converter.batch_convert_with_progress(
                files, 
                conversion_type,
                config.API_ID,
                config.API_HASH,
                conversion_callback
            )
            
            # 创建结果文件
            result_files = self.converter.create_conversion_result_zips(results, task_id, conversion_type)
            
            elapsed_time = time.time() - start_time
            
            # 发送结果统计
            success_count = len(results["转换成功"])
            error_count = len(results["转换错误"])
            
            summary_text = f"""
🎉 <b>转换完成！</b>

📊 <b>转换统计</b>
• 总数: {total_files}
• ✅ 成功: {success_count}
• ❌ 失败: {error_count}
• ⏱️ 用时: {int(elapsed_time)} 秒
• 🚀 速度: {total_files/elapsed_time:.1f} 个/秒

📦 正在打包结果文件...
            """
            
            try:
                progress_msg.edit_text(summary_text, parse_mode='HTML')
            except:
                pass
            
            # 发送结果文件
            # 发送结果文件（分离发送 ZIP 和 TXT）
            for zip_path, txt_path, status, count in result_files:
                try:
                    # 1. 发送 ZIP 文件
                    if os.path.exists(zip_path):
                        with open(zip_path, 'rb') as f:
                            caption = f"📦 <b>{status}</b> ({count}个账号)\n\n⏰ 处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                            update.message.reply_document(
                                document=f,
                                filename=os.path.basename(zip_path),
                                caption=caption,
                                parse_mode='HTML'
                            )
                        print(f"📤 发送ZIP文件: {os.path.basename(zip_path)}")
                        await asyncio.sleep(1.0)
                    
                    # 2. 发送 TXT 报告
                    if os.path.exists(txt_path):
                        with open(txt_path, 'rb') as f:
                            caption = f"📋 <b>{status} 详细报告</b>\n\n包含 {count} 个账号的详细信息"
                            update.message.reply_document(
                                document=f,
                                filename=os.path.basename(txt_path),
                                caption=caption,
                                parse_mode='HTML'
                            )
                        print(f"📤 发送TXT报告: {os.path.basename(txt_path)}")
                        await asyncio.sleep(1.0)
                        
                except Exception as e:
                    print(f"❌ 发送文件失败: {e}")
            
            # 最终消息
            success_rate = (success_count / total_files * 100) if total_files > 0 else 0
            
            final_text = f"""
✅ <b>转换任务完成！</b>

📊 <b>转换统计</b>
• 总计: {total_files}个
• ✅ 成功: {success_count}个 ({success_rate:.1f}%)
• ❌ 失败: {error_count}个 ({100-success_rate:.1f}%)
• ⏱️ 总用时: {int(elapsed_time)}秒 ({elapsed_time/60:.1f}分钟)
• 🚀 平均速度: {total_files/elapsed_time:.2f}个/秒


📥 {'所有结果文件已发送！'}
            """
            
            self.safe_send_message(update, final_text, 'HTML')
            
            # 清理临时文件
            if extract_dir and os.path.exists(extract_dir):
                shutil.rmtree(extract_dir, ignore_errors=True)
                print(f"🗑️ 清理解压目录: {extract_dir}")
            
            # 清理结果文件（修复：正确解包4个值）
            for zip_path, txt_path, status, count in result_files:
                try:
                    if os.path.exists(zip_path):
                        os.remove(zip_path)
                        print(f"🗑️ 清理结果ZIP: {os.path.basename(zip_path)}")
                except Exception as e:
                    print(f"⚠️ 清理ZIP失败: {e}")
                
                try:
                    if os.path.exists(txt_path):
                        os.remove(txt_path)
                        print(f"🗑️ 清理结果TXT: {os.path.basename(txt_path)}")
                except Exception as e:
                    print(f"⚠️ 清理TXT失败: {e}")
        
        except Exception as e:
            print(f"❌ 转换失败: {e}")
            import traceback
            traceback.print_exc()
            
            try:
                progress_msg.edit_text(
                    f"❌ <b>转换失败</b>\n\n错误: {str(e)}",
                    parse_mode='HTML'
                )
            except:
                pass
        
        finally:
            # 清理临时下载文件
            if temp_zip and os.path.exists(temp_zip):
                try:
                    shutil.rmtree(os.path.dirname(temp_zip), ignore_errors=True)
                    print(f"🗑️ 清理临时文件: {temp_zip}")
                except:
                    pass
    
    async def process_2fa_change(self, update, context, document):
        """处理2FA密码修改 - 交互式版本"""
        user_id = update.effective_user.id
        start_time = time.time()
        task_id = f"{user_id}_{int(start_time)}"
        
        print(f"🔐 开始2FA密码修改任务: {task_id}")
        
        # 发送进度消息
        progress_msg = self.safe_send_message(
            update,
            "📥 <b>正在处理您的文件...</b>",
            'HTML'
        )
        
        if not progress_msg:
            print("❌ 无法发送进度消息")
            return
        
        temp_zip = None
        try:
            # 下载文件
            temp_dir = tempfile.mkdtemp(prefix="temp_2fa_")
            temp_zip = os.path.join(temp_dir, document.file_name)
            
            document.get_file().download(temp_zip)
            print(f"📥 下载文件: {temp_zip}")
            
            # 扫描文件
            files, extract_dir, file_type = self.processor.scan_zip_file(temp_zip, user_id, task_id)
            
            if not files:
                try:
                    progress_msg.edit_text(
                        "❌ <b>未找到有效文件</b>\n\n请确保ZIP包含Session或TData格式的账号文件",
                        parse_mode='HTML'
                    )
                except:
                    pass
                return
            
            total_files = len(files)
            
            # 保存任务信息，等待用户输入密码
            self.two_factor_manager.pending_2fa_tasks[user_id] = {
                'files': files,
                'file_type': file_type,
                'extract_dir': extract_dir,
                'task_id': task_id,
                'progress_msg': progress_msg,
                'start_time': start_time,
                'temp_zip': temp_zip
            }
            
            # 请求用户输入密码
            try:
                progress_msg.edit_text(
                    f"📁 <b>已找到 {total_files} 个账号文件</b>\n\n"
                    f"📊 文件类型: {file_type.upper()}\n\n"
                    f"🔐 <b>请输入密码信息：</b>\n\n"
                    f"<b>格式1（推荐）：</b> 仅新密码\n"
                    f"<code>NewPassword123</code>\n"
                    f"<i>系统会自动检测旧密码</i>\n\n"
                    f"<b>格式2：</b> 旧密码 新密码\n"
                    f"<code>OldPass456 NewPassword123</code>\n"
                    f"<i>如果自动检测失败，将使用您提供的旧密码</i>\n\n"
                    f"💡 <b>提示：</b>\n"
                    f"• 推荐使用格式1，让系统自动检测\n"
                    f"• 密码可包含字母、数字、特殊字符\n"
                    f"• 两个密码之间用空格分隔\n\n"
                    f"⏰ 请在5分钟内发送密码...",
                    parse_mode='HTML'
                )
            except:
                pass
            
            print(f"⏳ 等待用户 {user_id} 输入密码...")
            
        except Exception as e:
            print(f"❌ 处理文件失败: {e}")
            import traceback
            traceback.print_exc()
            
            try:
                progress_msg.edit_text(
                    f"❌ <b>处理文件失败</b>\n\n错误: {str(e)}",
                    parse_mode='HTML'
                )
            except:
                pass
            
            # 清理临时下载文件
            if temp_zip and os.path.exists(temp_zip):
                try:
                    shutil.rmtree(os.path.dirname(temp_zip), ignore_errors=True)
                except:
                    pass
    
    async def complete_2fa_change_with_passwords(self, update, context, old_password: Optional[str], new_password: str):
        """完成2FA密码修改任务（使用用户提供的密码）"""
        user_id = update.effective_user.id
        
        # 检查是否有待处理的任务
        if user_id not in self.two_factor_manager.pending_2fa_tasks:
            self.safe_send_message(update, "❌ 没有待处理的2FA修改任务")
            return
        
        task_info = self.two_factor_manager.pending_2fa_tasks[user_id]
        files = task_info['files']
        file_type = task_info['file_type']
        extract_dir = task_info['extract_dir']
        task_id = task_info['task_id']
        progress_msg = task_info['progress_msg']
        start_time = task_info['start_time']
        temp_zip = task_info['temp_zip']
        
        total_files = len(files)
        
        try:
            # 更新消息，开始处理
            try:
                progress_msg.edit_text(
                    f"🔄 <b>开始修改密码...</b>\n\n"
                    f"📊 找到 {total_files} 个文件\n"
                    f"🔐 新密码: {new_password[:3]}***{new_password[-3:] if len(new_password) > 6 else ''}\n"
                    f"⏳ 正在处理，请稍候...",
                    parse_mode='HTML'
                )
            except:
                pass
            
            # 定义进度回调
            async def change_callback(processed, total, results, speed, elapsed):
                try:
                    success_count = len(results.get("成功", []))
                    fail_count = len(results.get("失败", []))
                    
                    progress_text = f"""
🔐 <b>2FA密码修改进行中...</b>

📊 <b>当前进度</b>
• 已处理: {processed}/{total}
• 速度: {speed:.1f} 个/秒
• 用时: {int(elapsed)} 秒

✅ <b>修改成功</b>: {success_count}
❌ <b>修改失败</b>: {fail_count}

⏱️ 预计剩余: {int((total - processed) / speed) if speed > 0 else 0} 秒
                    """
                    
                    try:
                        progress_msg.edit_text(progress_text, parse_mode='HTML')
                    except:
                        pass
                except Exception as e:
                    print(f"⚠️ 更新进度失败: {e}")
            
            # 执行批量修改
            results = await self.two_factor_manager.batch_change_passwords(
                files,
                file_type,
                old_password,
                new_password,
                change_callback
            )
            
                       # 创建结果文件（传入 file_type 参数）
                    
            result_files = self.two_factor_manager.create_result_files(results, task_id, file_type)
            
            elapsed_time = time.time() - start_time
            
            # 发送结果统计
            success_count = len(results["成功"])
            fail_count = len(results["失败"])
            
            summary_text = f"""
🎉 <b>2FA密码修改完成！</b>

📊 <b>修改统计</b>
• 总数: {total_files}
• ✅ 成功: {success_count}
• ❌ 失败: {fail_count}
• ⏱️ 用时: {int(elapsed_time)} 秒
• 🚀 速度: {total_files/elapsed_time:.1f} 个/秒

📦 正在发送结果文件...
            """
            
            try:
                progress_msg.edit_text(summary_text, parse_mode='HTML')
            except:
                pass
            
            # 发送结果文件（分离发送 ZIP 和 TXT）
            sent_count = 0
            for zip_path, txt_path, status, count in result_files:
                try:
                    # 1. 发送 ZIP 文件
                    if os.path.exists(zip_path):
                        try:
                            with open(zip_path, 'rb') as f:
                                caption = f"📦 <b>{status}</b> ({count}个账号)\n\n⏰ 处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                                context.bot.send_document(
                                    chat_id=update.effective_chat.id,
                                    document=f,
                                    filename=os.path.basename(zip_path),
                                    caption=caption,
                                    parse_mode='HTML'
                                )
                            print(f"📤 发送ZIP文件: {os.path.basename(zip_path)}")
                            sent_count += 1
                            await asyncio.sleep(1.0)
                        except Exception as e:
                            print(f"❌ 发送ZIP文件失败: {e}")
                    
                    # 2. 发送 TXT 报告
                    if os.path.exists(txt_path):
                        try:
                            with open(txt_path, 'rb') as f:
                                caption = f"📋 <b>{status} 详细报告</b>\n\n包含 {count} 个账号的详细信息"
                                context.bot.send_document(
                                    chat_id=update.effective_chat.id,
                                    document=f,
                                    filename=os.path.basename(txt_path),
                                    caption=caption,
                                    parse_mode='HTML'
                                )
                            print(f"📤 发送TXT报告: {os.path.basename(txt_path)}")
                            sent_count += 1
                            await asyncio.sleep(1.0)
                        except Exception as e:
                            print(f"❌ 发送TXT文件失败: {e}")
                    
                    # 3. 清理文件
                    try:
                        if os.path.exists(zip_path):
                            os.remove(zip_path)
                            print(f"🗑️ 清理结果文件: {os.path.basename(zip_path)}")
                        if os.path.exists(txt_path):
                            os.remove(txt_path)
                            print(f"🗑️ 清理报告文件: {os.path.basename(txt_path)}")
                    except Exception as e:
                        print(f"⚠️ 清理文件失败: {e}")
                        
                except Exception as e:
                    print(f"❌ 处理结果文件失败 {status}: {e}")
            
            # 发送完成总结
            if sent_count > 0:
                final_summary_text = f"""
🎉 <b>所有文件发送完成！</b>

📋 <b>发送总结</b>
• 发送文件: {sent_count} 个
• 总计账号: {len(files)} 个
• ✅ 成功: {success_count} 个
• ❌ 失败: {fail_count} 个
• ⏱️ 用时: {int(elapsed_time)}秒

如需再次使用，请点击 /start
                """
                
                try:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=final_summary_text,
                        parse_mode='HTML'
                    )
                except Exception as e:
                    print(f"❌ 发送总结失败: {e}")
            else:
                try:
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="❌ 没有文件可以发送"
                    )
                except Exception as e:
                    print(f"❌ 发送消息失败: {e}")
            
            # 清理临时文件
            if extract_dir and os.path.exists(extract_dir):
                shutil.rmtree(extract_dir, ignore_errors=True)
                print(f"🗑️ 清理解压目录: {extract_dir}")
            
        except Exception as e:
            print(f"❌ 2FA修改失败: {e}")
            import traceback
            traceback.print_exc()
            
            if progress_msg:
                try:
                    progress_msg.edit_text(
                        f"❌ <b>2FA修改失败</b>\n\n错误: {str(e)}",
                        parse_mode='HTML'
                    )
                except:
                    pass
            
            # 清理临时文件
            if extract_dir and os.path.exists(extract_dir):
                shutil.rmtree(extract_dir, ignore_errors=True)
            if temp_zip and os.path.exists(temp_zip):
                try:
                    shutil.rmtree(os.path.dirname(temp_zip), ignore_errors=True)
                except:
                    pass
        
        finally:
            # 清理任务信息
            if user_id in self.two_factor_manager.pending_2fa_tasks:
                del self.two_factor_manager.pending_2fa_tasks[user_id]
                print(f"🗑️ 清理任务信息: user_id={user_id}")
    
    def handle_photo(self, update: Update, context: CallbackContext):
        """处理图片上传（用于广播媒体）"""
        user_id = update.effective_user.id
        
        # 检查用户状态
        try:
            conn = sqlite3.connect(config.DB_NAME)
            c = conn.cursor()
            c.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            conn.close()
            
            if not row or row[0] != "waiting_broadcast_media":
                # 不是在等待广播媒体上传，忽略
                return
        except:
            return
        
        # 检查是否有待处理的广播任务
        if user_id not in self.pending_broadcasts:
            self.safe_send_message(update, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 获取最大尺寸的图片
        photo = update.message.photo[-1]
        
        # 保存图片 file_id
        task['media_file_id'] = photo.file_id
        task['media_type'] = 'photo'
        
        # 清空用户状态
        self.db.save_user(user_id, "", "", "")
        
        # 发送成功消息并返回编辑器
        self.safe_send_message(
            update,
            "✅ <b>图片已保存</b>\n\n返回编辑器继续设置",
            'HTML'
        )
        
        # 模拟 query 对象返回编辑器
        class FakeQuery:
            def __init__(self, user, chat):
                self.from_user = user
                self.message = type('obj', (object,), {'chat_id': chat.id, 'message_id': None})()
            def answer(self):
                pass
        
        fake_query = FakeQuery(update.effective_user, update.effective_chat)
        
        # 发送新消息显示编辑器
        self.show_broadcast_wizard_editor_as_new_message(update, context)
    
    def show_broadcast_wizard_editor_as_new_message(self, update, context):
        """以新消息的形式显示广播编辑器"""
        user_id = update.effective_user.id
        
        if user_id not in self.pending_broadcasts:
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 状态指示器
        media_status = "✅" if task.get('media_file_id') else "⚪"
        text_status = "✅" if task.get('content') else "⚪"
        buttons_status = "✅" if task.get('buttons') else "⚪"
        
        text = f"""
<b>📝 创建群发通知</b>

<b>📊 当前状态</b>
{media_status} 媒体: {'已设置' if task.get('media_file_id') else '未设置'}
{text_status} 文本: {'已设置' if task.get('content') else '未设置'}
{buttons_status} 按钮: {len(task.get('buttons', []))} 个

<b>💡 操作提示</b>
• 文本为必填项
• 媒体和按钮为可选项
• 设置完成后点击"下一步"
        """
        
        # 两栏布局按钮
        keyboard = InlineKeyboardMarkup([
            # 第一行：媒体操作
            [
                InlineKeyboardButton("📸 媒体", callback_data="broadcast_media"),
                InlineKeyboardButton("👁️ 查看", callback_data="broadcast_media_view"),
                InlineKeyboardButton("🗑️ 清除", callback_data="broadcast_media_clear")
            ],
            # 第二行：文本操作
            [
                InlineKeyboardButton("📝 文本", callback_data="broadcast_text"),
                InlineKeyboardButton("👁️ 查看", callback_data="broadcast_text_view")
            ],
            # 第三行：按钮操作
            [
                InlineKeyboardButton("🔘 按钮", callback_data="broadcast_buttons"),
                InlineKeyboardButton("👁️ 查看", callback_data="broadcast_buttons_view"),
                InlineKeyboardButton("🗑️ 清除", callback_data="broadcast_buttons_clear")
            ],
            # 第四行：预览和导航
            [
                InlineKeyboardButton("🔍 完整预览", callback_data="broadcast_preview")
            ],
            [
                InlineKeyboardButton("🔙 返回", callback_data="broadcast_cancel"),
                InlineKeyboardButton("➡️ 下一步", callback_data="broadcast_next")
            ]
        ])
        
        self.safe_send_message(update, text, 'HTML', keyboard)
    
    def handle_text(self, update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        text = update.message.text
        
        # 检查广播消息输入
        try:
            conn = sqlite3.connect(config.DB_NAME)
            c = conn.cursor()
            c.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            conn.close()
            
            if row:
                user_status = row[0]
                
                if user_status == "waiting_broadcast_title":
                    self.handle_broadcast_title_input(update, context, user_id, text)
                    return
                elif user_status == "waiting_broadcast_content":
                    self.handle_broadcast_content_input(update, context, user_id, text)
                    return
                elif user_status == "waiting_broadcast_buttons":
                    self.handle_broadcast_buttons_input(update, context, user_id, text)
                    return
                # VIP会员相关状态
                elif user_status == "waiting_redeem_code":
                    self.handle_redeem_code_input(update, user_id, text)
                    return
                elif user_status == "waiting_manual_user":
                    self.handle_manual_user_input(update, user_id, text)
                    return
        except Exception as e:
            print(f"❌ 检查广播状态失败: {e}")
        
        # 新增：处理 API 转换等待的 2FA 输入
        if user_id in getattr(self, "pending_api_tasks", {}):
            two_fa_input = (text or "").strip()
            def go_next():
                asyncio.run(self.continue_api_conversion(update, context, user_id, two_fa_input))
            threading.Thread(target=go_next, daemon=True).start()
            return        
        # 检查是否是2FA密码输入
        if user_id in self.two_factor_manager.pending_2fa_tasks:
            # 用户正在等待输入密码
            parts = text.strip().split()
            
            if len(parts) == 1:
                # 格式1：仅新密码，让系统自动检测旧密码
                new_password = parts[0]
                old_password = None
                
                print(f"🔐 用户 {user_id} 输入新密码（自动检测旧密码）")
                
                # 异步处理密码修改
                def process_password_change():
                    asyncio.run(self.complete_2fa_change_with_passwords(update, context, old_password, new_password))
                
                thread = threading.Thread(target=process_password_change)
                thread.start()
                
            elif len(parts) == 2:
                # 格式2：旧密码 新密码
                old_password = parts[0]
                new_password = parts[1]
                
                print(f"🔐 用户 {user_id} 输入旧密码和新密码")
                
                # 异步处理密码修改
                def process_password_change():
                    asyncio.run(self.complete_2fa_change_with_passwords(update, context, old_password, new_password))
                
                thread = threading.Thread(target=process_password_change)
                thread.start()
                
            else:
                # 格式错误
                self.safe_send_message(
                    update,
                    "❌ <b>格式错误</b>\n\n"
                    "请使用以下格式之一：\n\n"
                    "1️⃣ 仅新密码（推荐）\n"
                    "<code>NewPassword123</code>\n\n"
                    "2️⃣ 旧密码 新密码\n"
                    "<code>OldPass456 NewPassword123</code>\n\n"
                    "两个密码之间用空格分隔",
                    'HTML'
                )
            
            return
        
        # 检查是否是账号分类数量输入
        try:
            conn = sqlite3.connect(config.DB_NAME)
            c = conn.cursor()
            c.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            conn.close()
            
            if row:
                user_status = row[0]
                
                # 单个数量拆分
                if user_status == "waiting_classify_qty_single":
                    try:
                        qty = int(text.strip())
                        if qty <= 0:
                            self.safe_send_message(update, "❌ 请输入大于0的正整数")
                            return
                        
                        # 处理单个数量拆分
                        def process_single_qty():
                            asyncio.run(self._classify_split_single_qty(update, context, user_id, qty))
                        threading.Thread(target=process_single_qty, daemon=True).start()
                        return
                    except ValueError:
                        self.safe_send_message(update, "❌ 请输入有效的正整数")
                        return
                
                # 多个数量拆分
                elif user_status == "waiting_classify_qty_multi":
                    try:
                        parts = text.strip().split()
                        quantities = [int(p) for p in parts]
                        if any(q <= 0 for q in quantities):
                            self.safe_send_message(update, "❌ 所有数量必须大于0")
                            return
                        
                        # 处理多个数量拆分
                        def process_multi_qty():
                            asyncio.run(self._classify_split_multi_qty(update, context, user_id, quantities))
                        threading.Thread(target=process_multi_qty, daemon=True).start()
                        return
                    except ValueError:
                        self.safe_send_message(update, "❌ 请输入有效的正整数，用空格分隔\n例如: 10 20 30")
                        return
        except Exception as e:
            print(f"❌ 检查分类状态失败: {e}")
        # 管理员搜索用户
        if user_status == "waiting_admin_search":
            if not self.db.is_admin(user_id):
                self.safe_send_message(update, "❌ 权限不足")
                return
            
            search_query = text.strip()
            if len(search_query) < 2:
                self.safe_send_message(update, "❌ 搜索关键词太短，请至少输入2个字符")
                return
            
            # 执行搜索
            search_results = self.db.search_user(search_query)
            
            if not search_results:
                self.safe_send_message(update, f"🔍 未找到匹配 '{search_query}' 的用户")
                # 清空状态
                self.db.save_user(user_id, update.effective_user.username or "", update.effective_user.first_name or "", "")
                return
            
            # 显示搜索结果
            result_text = f"🔍 <b>搜索结果：'{search_query}'</b>\n\n"
            
            for i, (uid, username, first_name, register_time, last_active, status) in enumerate(search_results[:10], 1):
                is_member, level, _ = self.db.check_membership(uid)
                member_icon = "🎁" if is_member else "❌"
                admin_icon = "👑" if self.db.is_admin(uid) else ""
                
                display_name = first_name or username or f"用户{uid}"
                if len(display_name) > 20:
                    display_name = display_name[:20] + "..."
                
                result_text += f"{i}. {admin_icon}{member_icon} <code>{uid}</code>\n"
                result_text += f"   👤 {display_name}\n"
                if username:
                    result_text += f"   📱 @{username}\n"
                
                # 活跃状态
                if last_active:
                    try:
                        last_time = datetime.strptime(last_active, '%Y-%m-%d %H:%M:%S')
                        time_diff = datetime.now() - last_time
                        if time_diff.days == 0:
                            result_text += f"   🕒 {time_diff.seconds//3600}小时前活跃\n"
                        else:
                            result_text += f"   🕒 {time_diff.days}天前活跃\n"
                    except:
                        result_text += f"   🕒 {last_active}\n"
                else:
                    result_text += f"   🕒 从未活跃\n"
                
                result_text += "\n"
            
            if len(search_results) > 10:
                result_text += f"\n... 还有 {len(search_results) - 10} 个结果未显示"
            
            # 创建详情按钮（只显示前5个用户的详情按钮）
            buttons = []
            for i, (uid, username, first_name, _, _, _) in enumerate(search_results[:5]):
                display_name = first_name or username or f"用户{uid}"
                if len(display_name) > 15:
                    display_name = display_name[:15] + "..."
                buttons.append([InlineKeyboardButton(f"📋 {display_name} 详情", callback_data=f"user_detail_{uid}")])
            
            buttons.append([InlineKeyboardButton("🔙 返回用户管理", callback_data="admin_users")])
            
            keyboard = InlineKeyboardMarkup(buttons)
            self.safe_send_message(update, result_text, 'HTML', keyboard)
            
            # 清空状态
            self.db.save_user(user_id, update.effective_user.username or "", update.effective_user.first_name or "", "")
            return        
        # 其他文本消息的处理
        text_lower = text.lower()
        if any(word in text_lower for word in ["你好", "hello", "hi"]):
            self.safe_send_message(update, "👋 你好！发送 /start 开始检测")
        elif "帮助" in text_lower or "help" in text_lower:
            self.safe_send_message(update, "📖 发送 /help 查看帮助")
    
    # ================================
    # 账号分类功能
    # ================================
    
    def classify_command(self, update: Update, context: CallbackContext):
        """账号分类命令入口"""
        user_id = update.effective_user.id
        
        # 权限检查
        is_member, _, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 需要会员权限才能使用账号分类功能")
            return
        
        if not CLASSIFY_AVAILABLE or not self.classifier:
            self.safe_send_message(update, "❌ 账号分类功能不可用\n\n请检查 account_classifier.py 模块和 phonenumbers 库是否正确安装")
            return
        
        self.handle_classify_menu(update.callback_query if hasattr(update, 'callback_query') else None, update)
    
    def handle_classify_menu(self, query, update=None):
        """显示账号分类菜单"""
        if update is None:
            update = query.message if query else None
        
        user_id = query.from_user.id if query else update.effective_user.id
        
        # 权限检查
        is_member, _, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            if query:
                self.safe_edit_message(query, "❌ 需要会员权限")
            else:
                self.safe_send_message(update, "❌ 需要会员权限")
            return
        
        if not CLASSIFY_AVAILABLE or not self.classifier:
            msg = "❌ 账号分类功能不可用\n\n请检查依赖库是否正确安装"
            if query:
                self.safe_edit_message(query, msg)
            else:
                self.safe_send_message(update, msg)
            return
        
        text = """
📦 <b>账号文件分类</b>

🎯 <b>功能说明</b>
支持上传包含多个账号的ZIP文件（TData目录或Session+JSON文件），自动识别并分类打包：

📋 <b>支持的分类方式</b>
1️⃣ <b>按国家区号拆分</b>
   • 自动识别手机号→区号→国家
   • 每个国家生成一个ZIP
   • 命名：国家+区号+数量

2️⃣ <b>按数量拆分</b>
   • 支持单个或多个数量
   • 混合国家命名"混合+000+数量
   • 全未知命名"未知+000+数量

💡 <b>使用步骤</b>
1. 点击下方按钮开始
2. 上传包含账号的ZIP文件
3. 选择拆分方式
4. 等待处理并接收结果

⚠️ <b>注意事项</b>
• 支持TData和Session两种格式
• 文件大小限制100MB
• 自动识别手机号和国家信息
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📤 开始上传", callback_data="classify_start")],
            [InlineKeyboardButton("◀️ 返回主菜单", callback_data="back_to_main")]
        ])
        
        if query:
            query.answer()
            try:
                query.edit_message_text(text, parse_mode='HTML', reply_markup=keyboard)
            except:
                pass
        else:
            self.safe_send_message(update, text, 'HTML', keyboard)
    def on_back_to_main(self, update: Update, context: CallbackContext):
        """处理“返回主菜单”按钮"""
        query = update.callback_query
        if query:
            try:
                query.answer()
            except:
                pass
            # 使用统一方法渲染主菜单（包含“📦 账号分类”按钮）
            self.show_main_menu(update, query.from_user.id)        
    def _classify_buttons_split_type(self) -> InlineKeyboardMarkup:
        """生成拆分方式选择按钮"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("🌍 按国家拆分", callback_data="classify_split_country")],
            [InlineKeyboardButton("🔢 按数量拆分", callback_data="classify_split_quantity")],
            [InlineKeyboardButton("❌ 取消", callback_data="back_to_main")]
        ])
    
    def _classify_buttons_qty_mode(self) -> InlineKeyboardMarkup:
        """生成数量模式选择按钮"""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton("1️⃣ 单个数量", callback_data="classify_qty_single")],
            [InlineKeyboardButton("🔢 多个数量", callback_data="classify_qty_multi")],
            [InlineKeyboardButton("◀️ 返回", callback_data="classify_menu")]
        ])
    
    async def process_classify_stage1(self, update, context, document):
        """账号分类 - 阶段1：扫描文件并选择拆分方式"""
        user_id = update.effective_user.id
        start_time = time.time()
        task_id = f"{user_id}_{int(start_time)}"
        
        progress_msg = self.safe_send_message(update, "📥 <b>正在处理您的文件...</b>", 'HTML')
        if not progress_msg:
            return
        
        temp_zip = None
        try:
            temp_dir = tempfile.mkdtemp(prefix="temp_classify_")
            temp_zip = os.path.join(temp_dir, document.file_name)
            document.get_file().download(temp_zip)
            
            # 使用FileProcessor扫描
            files, extract_dir, file_type = self.processor.scan_zip_file(temp_zip, user_id, task_id)
            
            if not files:
                try:
                    progress_msg.edit_text(
                        "❌ <b>未找到有效文件</b>\n\n请确保ZIP包含Session或TData格式的账号文件",
                        parse_mode='HTML'
                    )
                except:
                    pass
                return
            
            # 构建元数据
            metas = self.classifier.build_meta_from_pairs(files, file_type)
            total_count = len(metas)
            
            # 统计识别情况
            recognized = sum(1 for m in metas if m.phone)
            unknown = total_count - recognized
            
            # 保存任务信息
            self.pending_classify_tasks[user_id] = {
                'metas': metas,
                'file_type': file_type,
                'extract_dir': extract_dir,
                'task_id': task_id,
                'progress_msg': progress_msg,
                'start_time': start_time,
                'temp_zip': temp_zip
            }
            
            # 提示选择拆分方式
            text = f"""
✅ <b>文件扫描完成！</b>

📊 <b>统计信息</b>
• 总账号数: {total_count} 个
• 已识别: {recognized} 个
• 未识别: {unknown} 个
• 文件类型: {file_type.upper()}

🎯 <b>请选择拆分方式：</b>
            """
            
            try:
                progress_msg.edit_text(
                    text,
                    parse_mode='HTML',
                    reply_markup=self._classify_buttons_split_type()
                )
            except:
                pass
        
        except Exception as e:
            print(f"❌ 分类阶段1失败: {e}")
            import traceback
            traceback.print_exc()
            try:
                progress_msg.edit_text(f"❌ 处理失败: {str(e)}", parse_mode='HTML')
            except:
                pass
            if temp_zip and os.path.exists(temp_zip):
                try:
                    shutil.rmtree(os.path.dirname(temp_zip), ignore_errors=True)
                except:
                    pass
    
    def _classify_cleanup(self, user_id):
        """清理分类任务"""
        if user_id in self.pending_classify_tasks:
            task = self.pending_classify_tasks[user_id]
            # 清理临时文件
            if 'temp_zip' in task and task['temp_zip'] and os.path.exists(task['temp_zip']):
                try:
                    shutil.rmtree(os.path.dirname(task['temp_zip']), ignore_errors=True)
                except:
                    pass
            if 'extract_dir' in task and task['extract_dir'] and os.path.exists(task['extract_dir']):
                try:
                    shutil.rmtree(task['extract_dir'], ignore_errors=True)
                except:
                    pass
            del self.pending_classify_tasks[user_id]
        
        # 清空数据库状态
        self.db.save_user(user_id, "", "", "")
    
    async def _classify_send_bundles(self, update, context, bundles, prefix=""):
        """统一发送ZIP包并节流"""
        sent_count = 0
        for zip_path, display_name, count in bundles:
            if os.path.exists(zip_path):
                try:
                    with open(zip_path, 'rb') as f:
                        caption = f"📦 <b>{prefix}{display_name}</b>\n包含 {count} 个账号"
                        context.bot.send_document(
                            chat_id=update.effective_chat.id,
                            document=f,
                            filename=display_name,
                            caption=caption,
                            parse_mode='HTML'
                        )
                    sent_count += 1
                    print(f"📤 已发送: {display_name}")
                    await asyncio.sleep(1.0)  # 节流
                    
                    # 发送后删除
                    try:
                        os.remove(zip_path)
                    except:
                        pass
                except Exception as e:
                    print(f"❌ 发送文件失败: {display_name} - {e}")
        
        return sent_count
    
    async def _classify_split_single_qty(self, update, context, user_id, qty):
        """按单个数量拆分"""
        if user_id not in self.pending_classify_tasks:
            self.safe_send_message(update, "❌ 没有待处理的分类任务")
            return
        
        task = self.pending_classify_tasks[user_id]
        metas = task['metas']
        task_id = task['task_id']
        progress_msg = task['progress_msg']
        
        try:
            total = len(metas)
            if qty > total:
                self.safe_send_message(update, f"❌ 数量 {qty} 超过总账号数 {total}")
                return
            
            # 更新提示
            try:
                progress_msg.edit_text(
                    f"🔄 <b>开始按数量拆分...</b>\n\n每包 {qty} 个账号\n总账号: {total} 个",
                    parse_mode='HTML'
                )
            except:
                pass
            
            # 计算需要多少个包
            num_bundles = (total + qty - 1) // qty
            sizes = [qty] * (num_bundles - 1) + [total - (num_bundles - 1) * qty]
            
            out_dir = os.path.join(config.RESULTS_DIR, f"classify_{task_id}")
            bundles = self.classifier.split_by_quantities(metas, sizes, out_dir)
            
            # 发送结果
            try:
                progress_msg.edit_text("📤 <b>正在发送结果...</b>", parse_mode='HTML')
            except:
                pass
            
            sent = await self._classify_send_bundles(update, context, bundles)
            
            # 完成提示
            self.safe_send_message(
                update,
                f"✅ <b>分类完成！</b>\n\n"
                f"• 总账号: {total} 个\n"
                f"• 已发送: {sent} 个文件\n"
                f"• 每包数量: {qty} 个\n\n"
                f"如需再次使用，请点击 /start",
                'HTML'
            )
            
            # 清理
            try:
                if os.path.exists(out_dir):
                    shutil.rmtree(out_dir, ignore_errors=True)
            except:
                pass
        
        except Exception as e:
            print(f"❌ 单数量拆分失败: {e}")
            import traceback
            traceback.print_exc()
            self.safe_send_message(update, f"❌ 拆分失败: {str(e)}")
        finally:
            self._classify_cleanup(user_id)
    
    async def _classify_split_multi_qty(self, update, context, user_id, quantities):
        """按多个数量拆分"""
        if user_id not in self.pending_classify_tasks:
            self.safe_send_message(update, "❌ 没有待处理的分类任务")
            return
        
        task = self.pending_classify_tasks[user_id]
        metas = task['metas']
        task_id = task['task_id']
        progress_msg = task['progress_msg']
        
        try:
            total = len(metas)
            total_requested = sum(quantities)
            
            # 更新提示
            try:
                progress_msg.edit_text(
                    f"🔄 <b>开始按数量拆分...</b>\n\n"
                    f"数量序列: {' '.join(map(str, quantities))}\n"
                    f"总账号: {total} 个\n"
                    f"请求数量: {total_requested} 个",
                    parse_mode='HTML'
                )
            except:
                pass
            
            out_dir = os.path.join(config.RESULTS_DIR, f"classify_{task_id}")
            bundles = self.classifier.split_by_quantities(metas, quantities, out_dir)
            
            # 余数提示
            remainder = total - total_requested
            remainder_msg = ""
            if remainder > 0:
                remainder_msg = f"\n\n⚠️ 剩余 {remainder} 个账号未分配"
            elif remainder < 0:
                remainder_msg = f"\n\n⚠️ 请求数量超出，最后一包可能不足"
            
            # 发送结果
            try:
                progress_msg.edit_text("📤 <b>正在发送结果...</b>", parse_mode='HTML')
            except:
                pass
            
            sent = await self._classify_send_bundles(update, context, bundles)
            
            # 完成提示
            self.safe_send_message(
                update,
                f"✅ <b>分类完成！</b>\n\n"
                f"• 总账号: {total} 个\n"
                f"• 已发送: {sent} 个文件\n"
                f"• 数量序列: {' '.join(map(str, quantities))}{remainder_msg}\n\n"
                f"如需再次使用，请点击 /start",
                'HTML'
            )
            
            # 清理
            try:
                if os.path.exists(out_dir):
                    shutil.rmtree(out_dir, ignore_errors=True)
            except:
                pass
        
        except Exception as e:
            print(f"❌ 多数量拆分失败: {e}")
            import traceback
            traceback.print_exc()
            self.safe_send_message(update, f"❌ 拆分失败: {str(e)}")
        finally:
            self._classify_cleanup(user_id)
    
    def handle_classify_callbacks(self, update, context, query, data):
        """处理分类相关的回调"""
        user_id = query.from_user.id
        
        if data == "classify_menu":
            self.handle_classify_menu(query)
        
        elif data == "classify_start":
            # 设置状态并提示上传
            self.db.save_user(
                user_id,
                query.from_user.username or "",
                query.from_user.first_name or "",
                "waiting_classify_file"
            )
            query.answer()
            try:
                query.edit_message_text(
                    "📤 <b>请上传账号文件</b>\n\n"
                    "支持格式：\n"
                    "• Session + JSON 文件的ZIP包\n"
                    "• TData 文件夹的ZIP包\n\n"
                    "⚠️ 文件大小限制100MB\n"
                    "⏰ 5分钟超时",
                    parse_mode='HTML'
                )
            except:
                pass
        
        elif data == "classify_split_country":
            # 按国家拆分
            if user_id not in self.pending_classify_tasks:
                query.answer("❌ 任务已过期")
                return
            
            task = self.pending_classify_tasks[user_id]
            metas = task['metas']
            task_id = task['task_id']
            progress_msg = task['progress_msg']
            
            query.answer()
            
            def process_country():
                asyncio.run(self._classify_split_by_country(update, context, user_id))
            threading.Thread(target=process_country, daemon=True).start()
        
        elif data == "classify_split_quantity":
            # 按数量拆分 - 询问模式
            query.answer()
            try:
                query.edit_message_text(
                    "🔢 <b>选择数量模式：</b>\n\n"
                    "1️⃣ <b>单个数量</b>\n"
                    "   按固定数量切分，例如每包10个\n\n"
                    "🔢 <b>多个数量</b>\n"
                    "   按多个数量依次切分，例如 10 20 30",
                    parse_mode='HTML',
                    reply_markup=self._classify_buttons_qty_mode()
                )
            except:
                pass
        
        elif data == "classify_qty_single":
            # 单个数量模式 - 等待输入
            self.db.save_user(
                user_id,
                query.from_user.username or "",
                query.from_user.first_name or "",
                "waiting_classify_qty_single"
            )
            query.answer()
            try:
                query.edit_message_text(
                    "🔢 <b>请输入每包的账号数量</b>\n\n"
                    "例如: <code>10</code>\n\n"
                    "系统将按此数量切分，最后一包为余数\n"
                    "⏰ 5分钟超时",
                    parse_mode='HTML'
                )
            except:
                pass
        
        elif data == "classify_qty_multi":
            # 多个数量模式 - 等待输入
            self.db.save_user(
                user_id,
                query.from_user.username or "",
                query.from_user.first_name or "",
                "waiting_classify_qty_multi"
            )
            query.answer()
            try:
                query.edit_message_text(
                    "🔢 <b>请输入多个数量（空格分隔）</b>\n\n"
                    "例如: <code>10 20 30</code>\n\n"
                    "系统将依次切分：第1包10个，第2包20个，第3包30个\n"
                    "余数将提示但不打包\n"
                    "⏰ 5分钟超时",
                    parse_mode='HTML'
                )
            except:
                pass
    
    async def _classify_split_by_country(self, update, context, user_id):
        """按国家拆分"""
        if user_id not in self.pending_classify_tasks:
            self.safe_send_message(update, "❌ 没有待处理的分类任务")
            return
        
        task = self.pending_classify_tasks[user_id]
        metas = task['metas']
        task_id = task['task_id']
        progress_msg = task['progress_msg']
        
        try:
            # 更新提示
            try:
                progress_msg.edit_text(
                    "🔄 <b>开始按国家拆分...</b>\n\n正在分组并打包...",
                    parse_mode='HTML'
                )
            except:
                pass
            
            out_dir = os.path.join(config.RESULTS_DIR, f"classify_{task_id}")
            bundles = self.classifier.split_by_country(metas, out_dir)
            
            # 发送结果
            try:
                progress_msg.edit_text("📤 <b>正在发送结果...</b>", parse_mode='HTML')
            except:
                pass
            
            sent = await self._classify_send_bundles(update, context, bundles)
            
            # 完成提示
            self.safe_send_message(
                update,
                f"✅ <b>分类完成！</b>\n\n"
                f"• 总账号: {len(metas)} 个\n"
                f"• 已发送: {sent} 个文件\n"
                f"• 分类方式: 按国家区号\n\n"
                f"如需再次使用，请点击 /start",
                'HTML'
            )
            
            # 清理
            try:
                if os.path.exists(out_dir):
                    shutil.rmtree(out_dir, ignore_errors=True)
            except:
                pass
        
        except Exception as e:
            print(f"❌ 国家拆分失败: {e}")
            import traceback
            traceback.print_exc()
            self.safe_send_message(update, f"❌ 拆分失败: {str(e)}")
        finally:
            self._classify_cleanup(user_id)
    
    # ================================
    # VIP会员功能
    # ================================
    
    def handle_vip_menu(self, query):
        """显示VIP会员菜单"""
        user_id = query.from_user.id
        query.answer()
        
        # 获取会员状态
        is_member, level, expiry = self.db.check_membership(user_id)
        
        if self.db.is_admin(user_id):
            member_status = "👑 管理员（永久有效）"
        elif is_member:
            member_status = f"💎 {level}\n• 到期时间: {expiry}"
        else:
            member_status = "❌ 暂无会员"
        
        text = f"""
<b>💳 会员中心</b>

<b>📊 当前状态</b>
{member_status}

<b>💡 功能说明</b>
• 兑换卡密即可开通会员
• 会员时长自动累加
• 支持多次兑换叠加

<b>🎯 操作选项</b>
请选择您要执行的操作
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🎟️ 兑换卡密", callback_data="vip_redeem")],
            [InlineKeyboardButton("🔙 返回主菜单", callback_data="back_to_main")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def handle_vip_redeem(self, query):
        """处理兑换卡密"""
        user_id = query.from_user.id
        query.answer()
        
        # 设置用户状态
        self.db.save_user(
            user_id,
            query.from_user.username or "",
            query.from_user.first_name or "",
            "waiting_redeem_code"
        )
        
        text = """
<b>🎟️ 兑换卡密</b>

<b>📋 请输入卡密（10位以内）</b>

💡 提示：
• 请输入您获得的卡密
• 卡密不区分大小写
• 兑换成功后时长自动累加

⏰ <i>5分钟内未输入将自动取消</i>
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ 取消", callback_data="vip_menu")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def handle_redeem_code_input(self, update, user_id: int, code: str):
        """处理用户输入的兑换码"""
        # 清除状态
        self.db.save_user(user_id, "", "", "")
        
        # 验证兑换码
        code = code.strip()
        if len(code) > 10:
            self.safe_send_message(update, "❌ 卡密长度不能超过10位")
            return
        
        # 执行兑换
        success, message, days = self.db.redeem_code(user_id, code)
        
        if success:
            # 获取新的会员状态
            is_member, level, expiry = self.db.check_membership(user_id)
            
            text = f"""
✅ <b>兑换成功！</b>

<b>📋 兑换信息</b>
• 卡密: <code>{code.upper()}</code>
• 会员等级: {level}
• 增加天数: {days}天

<b>💎 当前会员状态</b>
• 会员等级: {level}
• 到期时间: {expiry}

感谢您的支持！
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 返回主菜单", callback_data="back_to_main")]
            ])
            
            self.safe_send_message(update, text, 'HTML', keyboard)
        else:
            text = f"""
❌ <b>兑换失败</b>

{message}

请检查您的卡密是否正确
            """
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 重新兑换", callback_data="vip_redeem")],
                [InlineKeyboardButton("🔙 返回会员中心", callback_data="vip_menu")]
            ])
            
            self.safe_send_message(update, text, 'HTML', keyboard)
    
    def handle_admin_card_menu(self, query):
        """管理员卡密开通菜单"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        query.answer()
        
        text = """
<b>💳 卡密开通</b>

<b>📋 功能说明</b>
• 选择天数生成卡密
• 每次生成1个卡密
• 卡密为8位大写字母数字组合
• 每个卡密仅可使用一次

<b>🎯 选择有效期</b>
请选择要生成的卡密有效期
        """
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("1天", callback_data="admin_card_days_1"),
                InlineKeyboardButton("7天", callback_data="admin_card_days_7")
            ],
            [
                InlineKeyboardButton("30天", callback_data="admin_card_days_30"),
                InlineKeyboardButton("60天", callback_data="admin_card_days_60")
            ],
            [
                InlineKeyboardButton("90天", callback_data="admin_card_days_90"),
                InlineKeyboardButton("360天", callback_data="admin_card_days_360")
            ],
            [InlineKeyboardButton("🔙 返回管理面板", callback_data="admin_panel")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def handle_admin_card_generate(self, query, days: int):
        """管理员生成卡密"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        query.answer()
        
        # 生成卡密
        success, code, message = self.db.create_redeem_code("会员", days, None, user_id)
        
        if success:
            text = f"""
✅ <b>卡密生成成功！</b>

<b>📋 卡密信息</b>
• 卡密: <code>{code}</code>
• 等级: 会员
• 有效期: {days}天
• 状态: 未使用

<b>💡 提示</b>
• 请妥善保管卡密
• 每个卡密仅可使用一次
• 点击卡密可复制
            """
        else:
            text = f"""
❌ <b>生成失败</b>

{message}
            """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 继续生成", callback_data="admin_card_menu")],
            [InlineKeyboardButton("🔙 返回管理面板", callback_data="admin_panel")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def handle_admin_manual_menu(self, query):
        """管理员人工开通菜单"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        query.answer()
        
        # 设置用户状态
        self.db.save_user(
            user_id,
            query.from_user.username or "",
            query.from_user.first_name or "",
            "waiting_manual_user"
        )
        
        text = """
<b>👤 人工开通会员</b>

<b>📋 请输入要开通的用户</b>

支持以下格式：
• 用户ID：<code>123456789</code>
• 用户名：<code>@username</code> 或 <code>username</code>

<b>💡 提示</b>
• 用户必须先与机器人交互过
• 输入后会显示天数选择
• 会员时长自动累加

⏰ <i>5分钟内未输入将自动取消</i>
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ 取消", callback_data="admin_panel")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def handle_manual_user_input(self, update, admin_id: int, text: str):
        """处理管理员输入的用户信息"""
        # 清除状态
        self.db.save_user(admin_id, "", "", "")
        
        # 解析用户输入
        text = text.strip()
        target_user_id = None
        
        # 尝试作为用户ID解析
        if text.isdigit():
            target_user_id = int(text)
        else:
            # 尝试作为用户名解析
            username = text.replace("@", "")
            target_user_id = self.db.get_user_id_by_username(username)
        
        if not target_user_id:
            self.safe_send_message(
                update,
                "❌ <b>用户不存在</b>\n\n"
                "该用户未与机器人交互过，请确认：\n"
                "• 用户ID或用户名正确\n"
                "• 用户已发送过 /start 命令",
                'HTML'
            )
            return
        
        # 获取用户信息
        user_info = self.db.get_user_membership_info(target_user_id)
        if not user_info:
            self.safe_send_message(
                update,
                "❌ <b>用户不存在</b>\n\n"
                "该用户未与机器人交互过",
                'HTML'
            )
            return
        
        # 保存到待处理列表
        self.pending_manual_open[admin_id] = target_user_id
        
        # 获取用户会员信息
        is_member, level, expiry = self.db.check_membership(target_user_id)
        
        username = user_info.get('username', '')
        first_name = user_info.get('first_name', '')
        display_name = first_name or username or f"用户{target_user_id}"
        
        if is_member:
            member_status = f"💎 {level}\n• 到期: {expiry}"
        else:
            member_status = "❌ 暂无会员"
        
        text = f"""
<b>👤 确认用户信息</b>

<b>📋 用户信息</b>
• 昵称: {display_name}
• ID: <code>{target_user_id}</code>
• 用户名: @{username if username else '无'}

<b>💎 当前会员状态</b>
{member_status}

<b>🎯 选择开通天数</b>
请选择要为该用户开通的会员天数
        """
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("1天", callback_data="admin_manual_days_1"),
                InlineKeyboardButton("7天", callback_data="admin_manual_days_7")
            ],
            [
                InlineKeyboardButton("30天", callback_data="admin_manual_days_30"),
                InlineKeyboardButton("60天", callback_data="admin_manual_days_60")
            ],
            [
                InlineKeyboardButton("90天", callback_data="admin_manual_days_90"),
                InlineKeyboardButton("360天", callback_data="admin_manual_days_360")
            ],
            [InlineKeyboardButton("❌ 取消", callback_data="admin_panel")]
        ])
        
        self.safe_send_message(update, text, 'HTML', keyboard)
    
    def handle_admin_manual_grant(self, query, update, days: int):
        """管理员执行人工开通"""
        admin_id = query.from_user.id
        
        if not self.db.is_admin(admin_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        # 检查是否有待处理的用户
        if admin_id not in self.pending_manual_open:
            query.answer("❌ 没有待处理的用户")
            return
        
        target_user_id = self.pending_manual_open[admin_id]
        
        # 执行授予
        success = self.db.grant_membership_days(target_user_id, days, "会员")
        
        if success:
            # 获取新的会员状态
            is_member, level, expiry = self.db.check_membership(target_user_id)
            
            # 获取用户信息
            user_info = self.db.get_user_membership_info(target_user_id)
            username = user_info.get('username', '')
            first_name = user_info.get('first_name', '')
            display_name = first_name or username or f"用户{target_user_id}"
            
            text = f"""
✅ <b>开通成功！</b>

<b>📋 开通信息</b>
• 目标用户: {display_name}
• 用户ID: <code>{target_user_id}</code>
• 增加天数: {days}天

<b>💎 当前会员状态</b>
• 会员等级: {level}
• 到期时间: {expiry}
            """
            
            query.answer("✅ 开通成功")
            
            # 尝试通知用户
            try:
                context = update._bot
                context.send_message(
                    chat_id=target_user_id,
                    text=f"""
🎉 <b>恭喜！您已获得会员</b>

管理员为您开通了 {days}天 会员

<b>💎 当前会员状态</b>
• 会员等级: {level}
• 到期时间: {expiry}

感谢您的支持！
                    """,
                    parse_mode='HTML'
                )
            except:
                pass
        else:
            text = "❌ <b>开通失败</b>\n\n请稍后重试"
            query.answer("❌ 开通失败")
        
        # 清理待处理任务
        if admin_id in self.pending_manual_open:
            del self.pending_manual_open[admin_id]
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 继续开通", callback_data="admin_manual_menu")],
            [InlineKeyboardButton("🔙 返回管理面板", callback_data="admin_panel")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    # ================================
    # 广播消息功能
    # ================================
    
    def handle_broadcast_callbacks_router(self, update: Update, context: CallbackContext):
        """
        专用广播回调路由器 - 处理所有 broadcast_* 回调
        注册为独立的 CallbackQueryHandler，优先级高于通用处理器
        """
        query = update.callback_query
        data = query.data
        user_id = query.from_user.id
        
        # 始终先调用 query.answer() 避免 Telegram 超时和加载动画
        try:
            query.answer()
        except Exception as e:
            print(f"⚠️ query.answer() 失败: {e}")
        
        # 权限检查
        if not self.db.is_admin(user_id):
            try:
                query.answer("❌ 仅管理员可访问广播功能", show_alert=True)
            except:
                pass
            return
        
        # 分发表：将所有 broadcast_* 回调映射到对应的处理方法
        dispatch_table = {
            # 主菜单和向导
            "broadcast_menu": lambda: self.show_broadcast_menu(query),
            "broadcast_create": lambda: self.start_broadcast_wizard(query, update, context),
            "broadcast_history": lambda: self.show_broadcast_history(query),
            "broadcast_cancel": lambda: self.cancel_broadcast(query, user_id),
            "broadcast_edit": lambda: self.restart_broadcast_wizard(query, update, context),
            "broadcast_confirm_send": lambda: self.start_broadcast_sending(query, update, context),
            
            # 媒体操作
            "broadcast_media": lambda: self.handle_broadcast_media(query, update, context),
            "broadcast_media_view": lambda: self.handle_broadcast_media_view(query, update, context),
            "broadcast_media_clear": lambda: self.handle_broadcast_media_clear(query, update, context),
            
            # 文本操作
            "broadcast_text": lambda: self.handle_broadcast_text(query, update, context),
            "broadcast_text_view": lambda: self.handle_broadcast_text_view(query, update, context),
            
            # 按钮操作
            "broadcast_buttons": lambda: self.handle_broadcast_buttons(query, update, context),
            "broadcast_buttons_view": lambda: self.handle_broadcast_buttons_view(query, update, context),
            "broadcast_buttons_clear": lambda: self.handle_broadcast_buttons_clear(query, update, context),
            
            # 导航
            "broadcast_preview": lambda: self.handle_broadcast_preview(query, update, context),
            "broadcast_back": lambda: self.handle_broadcast_back(query, update, context),
            "broadcast_next": lambda: self.handle_broadcast_next(query, update, context),
        }
        
        # 处理简单的固定回调
        if data in dispatch_table:
            try:
                dispatch_table[data]()
            except Exception as e:
                print(f"❌ 广播回调处理失败 [{data}]: {e}")
                import traceback
                traceback.print_exc()
                try:
                    self.safe_edit_message(query, f"❌ 操作失败: {str(e)[:100]}")
                except:
                    pass
            return
        
        # 处理带参数的回调（历史详情、目标选择等）
        try:
            if data.startswith("broadcast_history_detail_"):
                broadcast_id = int(data.split("_")[-1])
                self.show_broadcast_detail(query, broadcast_id)
            elif data.startswith("broadcast_target_"):
                target = data.split("_", 2)[-1]  # 支持 broadcast_target_active_7d 这种格式
                self.handle_broadcast_target_selection(query, update, context, target)
            elif data.startswith("broadcast_alert_"):
                # 广播消息中的自定义回调按钮
                self.handle_broadcast_alert_button(query, data)
            else:
                print(f"⚠️ 未识别的广播回调: {data}")
                try:
                    query.answer("⚠️ 未识别的操作", show_alert=True)
                except:
                    pass
        except Exception as e:
            print(f"❌ 广播回调处理失败 [{data}]: {e}")
            import traceback
            traceback.print_exc()
            try:
                self.safe_edit_message(query, f"❌ 操作失败: {str(e)[:100]}")
            except:
                pass
    
    def handle_broadcast_callbacks(self, update, context, query, data):
        """
        旧版广播回调处理器 - 保持向后兼容
        现在通过 handle_broadcast_callbacks_router 调用
        """
        user_id = query.from_user.id
        
        # 权限检查
        if not self.db.is_admin(user_id):
            try:
                query.answer("❌ 仅管理员可访问广播功能", show_alert=True)
            except:
                pass
            return
        
        # 调用新的路由器（去掉 query.answer，因为路由器已经处理）
        if data == "broadcast_menu":
            self.show_broadcast_menu(query)
        elif data == "broadcast_create":
            self.start_broadcast_wizard(query, update, context)
        elif data == "broadcast_history":
            self.show_broadcast_history(query)
        elif data.startswith("broadcast_history_detail_"):
            broadcast_id = int(data.split("_")[-1])
            self.show_broadcast_detail(query, broadcast_id)
        elif data.startswith("broadcast_target_"):
            target = data.split("_")[-1]
            self.handle_broadcast_target_selection(query, update, context, target)
        elif data == "broadcast_confirm_send":
            self.start_broadcast_sending(query, update, context)
        elif data == "broadcast_edit":
            self.restart_broadcast_wizard(query, update, context)
        elif data == "broadcast_cancel":
            self.cancel_broadcast(query, user_id)
    
    def show_broadcast_menu(self, query):
        """显示广播菜单"""
        try:
            query.answer()
        except:
            pass
        
        text = """
<b>📢 群发通知管理</b>

<b>💡 功能说明</b>
• 支持HTML格式内容（粗体、斜体、链接等）
• 支持单张图片 + 文本组合
• 可添加自定义按钮（URL或回调）
• 智能节流避免触发限制
• 实时进度显示
• 完整历史记录

<b>🎯 选择操作</b>
点击下方按钮开始使用
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 创建群发", callback_data="broadcast_create")],
            [InlineKeyboardButton("📜 历史记录", callback_data="broadcast_history")],
            [InlineKeyboardButton("🔙 返回", callback_data="admin_panel")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    # ================================
    # 广播向导 - 新增媒体/文本/按钮操作方法
    # ================================
    
    def handle_broadcast_media(self, query, update, context):
        """处理媒体设置"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 更新用户状态
        self.db.save_user(
            user_id,
            query.from_user.username or "",
            query.from_user.first_name or "",
            "waiting_broadcast_media"
        )
        
        text = """
<b>📸 设置广播媒体</b>

<b>📋 请上传一张图片</b>

• 支持格式：JPG、PNG、GIF
• 图片将与文本一起发送
• 单次广播只支持一张图片

⏰ <i>5分钟内未上传将自动取消</i>
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ 取消", callback_data="broadcast_cancel")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def handle_broadcast_media_view(self, query, update, context):
        """查看当前设置的媒体"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        if 'media_file_id' not in task or not task['media_file_id']:
            try:
                query.answer("⚠️ 尚未设置媒体", show_alert=True)
            except:
                pass
            return
        
        # 发送媒体预览
        try:
            context.bot.send_photo(
                chat_id=user_id,
                photo=task['media_file_id'],
                caption="📸 当前广播媒体预览"
            )
            try:
                query.answer("✅ 已发送媒体预览")
            except:
                pass
        except Exception as e:
            try:
                query.answer(f"❌ 预览失败: {str(e)[:50]}", show_alert=True)
            except:
                pass
    
    def handle_broadcast_media_clear(self, query, update, context):
        """清除媒体设置"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        task['media_file_id'] = None
        task['media_type'] = None
        
        try:
            query.answer("✅ 已清除媒体设置")
        except:
            pass
        
        # 返回编辑界面
        self.show_broadcast_wizard_editor(query, update, context)
    
    def handle_broadcast_text(self, query, update, context):
        """处理文本设置"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 更新用户状态
        self.db.save_user(
            user_id,
            query.from_user.username or "",
            query.from_user.first_name or "",
            "waiting_broadcast_content"
        )
        
        text = """
<b>📝 设置广播文本</b>

<b>📄 请输入广播内容</b>

• 支持HTML格式：
  <code>&lt;b&gt;粗体&lt;/b&gt;</code>
  <code>&lt;i&gt;斜体&lt;/i&gt;</code>
  <code>&lt;a href="URL"&gt;链接&lt;/a&gt;</code>
  <code>&lt;code&gt;代码&lt;/code&gt;</code>

⏰ <i>5分钟内未输入将自动取消</i>
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ 取消", callback_data="broadcast_cancel")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def handle_broadcast_text_view(self, query, update, context):
        """查看当前设置的文本"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        if not task.get('content'):
            try:
                query.answer("⚠️ 尚未设置文本内容", show_alert=True)
            except:
                pass
            return
        
        # 显示文本预览
        preview = task['content'][:500]
        if len(task['content']) > 500:
            preview += "\n\n<i>... (内容过长，已截断)</i>"
        
        text = f"""
<b>📄 文本内容预览</b>

{preview}

<b>字符数:</b> {len(task['content'])}
        """
        
        self.safe_edit_message(query, text, 'HTML')
        try:
            query.answer("✅ 已显示文本预览")
        except:
            pass
    
    def handle_broadcast_buttons(self, query, update, context):
        """处理按钮设置"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 更新用户状态
        self.db.save_user(
            user_id,
            query.from_user.username or "",
            query.from_user.first_name or "",
            "waiting_broadcast_buttons"
        )
        
        text = """
<b>🔘 设置广播按钮</b>

<b>请输入自定义按钮（可选）</b>

• 每行一个按钮（最多4个）
• URL按钮格式：<code>文本|https://example.com</code>
• 回调按钮格式：<code>文本|callback:提示信息</code>

示例：
<code>官方网站|https://telegram.org
点我试试|callback:你点击了按钮！</code>

💡 <i>输入"跳过"或"skip"可跳过此步骤</i>
⏰ <i>5分钟内未输入将自动取消</i>
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ 取消", callback_data="broadcast_cancel")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def handle_broadcast_buttons_view(self, query, update, context):
        """查看当前设置的按钮"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        if not task.get('buttons'):
            try:
                query.answer("⚠️ 尚未设置按钮", show_alert=True)
            except:
                pass
            return
        
        # 显示按钮列表
        text = "<b>🔘 按钮列表</b>\n\n"
        for i, btn in enumerate(task['buttons'], 1):
            if btn['type'] == 'url':
                text += f"{i}. {btn['text']} → {btn['url']}\n"
            else:
                text += f"{i}. {btn['text']} (回调)\n"
        
        self.safe_edit_message(query, text, 'HTML')
        try:
            query.answer(f"✅ 共 {len(task['buttons'])} 个按钮")
        except:
            pass
    
    def handle_broadcast_buttons_clear(self, query, update, context):
        """清除按钮设置"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        task['buttons'] = []
        
        try:
            query.answer("✅ 已清除所有按钮")
        except:
            pass
        
        # 返回编辑界面
        self.show_broadcast_wizard_editor(query, update, context)
    
    def handle_broadcast_preview(self, query, update, context):
        """显示完整预览"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 检查必填项
        if not task.get('content'):
            try:
                query.answer("⚠️ 请先设置文本内容", show_alert=True)
            except:
                pass
            return
        
        # 发送预览消息
        try:
            # 构建按钮
            keyboard = None
            if task.get('buttons'):
                button_rows = []
                for btn in task['buttons']:
                    if btn['type'] == 'url':
                        button_rows.append([InlineKeyboardButton(btn['text'], url=btn['url'])])
                    else:
                        button_rows.append([InlineKeyboardButton(btn['text'], callback_data=btn['data'])])
                keyboard = InlineKeyboardMarkup(button_rows)
            
            # 发送预览
            if task.get('media_file_id'):
                context.bot.send_photo(
                    chat_id=user_id,
                    photo=task['media_file_id'],
                    caption=f"<b>📢 预览</b>\n\n{task['content']}",
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
            else:
                context.bot.send_message(
                    chat_id=user_id,
                    text=f"<b>📢 预览</b>\n\n{task['content']}",
                    parse_mode='HTML',
                    reply_markup=keyboard
                )
            
            try:
                query.answer("✅ 已发送预览")
            except:
                pass
        except Exception as e:
            try:
                query.answer(f"❌ 预览失败: {str(e)[:50]}", show_alert=True)
            except:
                pass
    
    def handle_broadcast_back(self, query, update, context):
        """返回上一步"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        # 返回编辑界面
        self.show_broadcast_wizard_editor(query, update, context)
    
    def handle_broadcast_next(self, query, update, context):
        """下一步：选择目标"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 检查必填项
        if not task.get('content'):
            try:
                query.answer("⚠️ 请先设置文本内容", show_alert=True)
            except:
                pass
            return
        
        # 进入目标选择
        self.show_target_selection(update, context, user_id)
    
    def handle_broadcast_alert_button(self, query, data):
        """处理广播消息中的自定义回调按钮"""
        # 从广播任务中查找对应的提示信息
        # 这里简化处理，直接显示通用提示
        try:
            query.answer("✨ 感谢您的关注！", show_alert=True)
        except:
            pass
    
    def show_broadcast_wizard_editor(self, query, update, context):
        """显示广播编辑器 - 两栏布局的 zh-CN UI"""
        user_id = query.from_user.id
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 状态指示器
        media_status = "✅" if task.get('media_file_id') else "⚪"
        text_status = "✅" if task.get('content') else "⚪"
        buttons_status = "✅" if task.get('buttons') else "⚪"
        
        text = f"""
<b>📝 创建群发通知</b>

<b>📊 当前状态</b>
{media_status} 媒体: {'已设置' if task.get('media_file_id') else '未设置'}
{text_status} 文本: {'已设置' if task.get('content') else '未设置'}
{buttons_status} 按钮: {len(task.get('buttons', []))} 个

<b>💡 操作提示</b>
• 文本为必填项
• 媒体和按钮为可选项
• 设置完成后点击"下一步"
        """
        
        # 两栏布局按钮
        keyboard = InlineKeyboardMarkup([
            # 第一行：媒体操作
            [
                InlineKeyboardButton("📸 媒体", callback_data="broadcast_media"),
                InlineKeyboardButton("👁️ 查看", callback_data="broadcast_media_view"),
                InlineKeyboardButton("🗑️ 清除", callback_data="broadcast_media_clear")
            ],
            # 第二行：文本操作
            [
                InlineKeyboardButton("📝 文本", callback_data="broadcast_text"),
                InlineKeyboardButton("👁️ 查看", callback_data="broadcast_text_view")
            ],
            # 第三行：按钮操作
            [
                InlineKeyboardButton("🔘 按钮", callback_data="broadcast_buttons"),
                InlineKeyboardButton("👁️ 查看", callback_data="broadcast_buttons_view"),
                InlineKeyboardButton("🗑️ 清除", callback_data="broadcast_buttons_clear")
            ],
            # 第四行：预览和导航
            [
                InlineKeyboardButton("🔍 完整预览", callback_data="broadcast_preview")
            ],
            [
                InlineKeyboardButton("🔙 返回", callback_data="broadcast_cancel"),
                InlineKeyboardButton("➡️ 下一步", callback_data="broadcast_next")
            ]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def start_broadcast_wizard(self, query, update, context):
        """开始广播创建向导 - 新版两栏 UI"""
        user_id = query.from_user.id
        try:
            query.answer()
        except:
            pass
        
        # 初始化广播任务
        self.pending_broadcasts[user_id] = {
            'step': 'editor',
            'started_at': time.time(),
            'title': f"广播_{int(time.time())}",  # 自动生成标题
            'content': '',
            'buttons': [],
            'media_file_id': None,
            'media_type': None,
            'target': '',
            'preview_message_id': None,
            'broadcast_id': None
        }
        
        # 显示编辑器界面
        self.show_broadcast_wizard_editor(query, update, context)
    
    def handle_broadcast_title_input(self, update, context, user_id, title):
        """处理标题输入"""
        if user_id not in self.pending_broadcasts:
            self.safe_send_message(update, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 检查超时
        if time.time() - task['started_at'] > 300:  # 5分钟
            del self.pending_broadcasts[user_id]
            self.db.save_user(user_id, "", "", "")
            self.safe_send_message(update, "❌ 操作超时，请重新开始")
            return
        
        # 验证标题
        title = title.strip()
        if not title:
            self.safe_send_message(update, "❌ 标题不能为空，请重新输入")
            return
        
        if len(title) > 100:
            self.safe_send_message(update, "❌ 标题过长（最多100字符），请重新输入")
            return
        
        # 保存标题并进入下一步
        task['title'] = title
        task['step'] = 'content'
        
        # 更新状态
        self.db.save_user(user_id, "", "", "waiting_broadcast_content")
        
        text = f"""
<b>📝 创建群发通知 - 步骤 2/4</b>

✅ 标题已设置: <code>{title}</code>

<b>📄 请输入通知内容</b>

• 支持HTML格式：
  <code>&lt;b&gt;粗体&lt;/b&gt;</code>
  <code>&lt;i&gt;斜体&lt;/i&gt;</code>
  <code>&lt;a href="URL"&gt;链接&lt;/a&gt;</code>
  <code>&lt;code&gt;代码&lt;/code&gt;</code>

⏰ <i>5分钟内未输入将自动取消</i>
        """
        
        self.safe_send_message(update, text, 'HTML')
    
    def handle_broadcast_content_input(self, update, context, user_id, content):
        """处理内容输入"""
        if user_id not in self.pending_broadcasts:
            self.safe_send_message(update, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 检查超时
        if time.time() - task['started_at'] > 300:
            del self.pending_broadcasts[user_id]
            self.db.save_user(user_id, "", "", "")
            self.safe_send_message(update, "❌ 操作超时，请重新开始")
            return
        
        # 验证内容
        content = content.strip()
        if not content:
            self.safe_send_message(update, "❌ 内容不能为空，请重新输入")
            return
        
        # 保存内容
        task['content'] = content
        
        # 清空用户状态
        self.db.save_user(user_id, "", "", "")
        
        # 返回编辑器
        self.safe_send_message(update, "✅ <b>内容已保存</b>\n\n返回编辑器继续设置", 'HTML')
        self.show_broadcast_wizard_editor_as_new_message(update, context)
    
    def handle_broadcast_buttons_input(self, update, context, user_id, buttons_text):
        """处理按钮输入"""
        if user_id not in self.pending_broadcasts:
            self.safe_send_message(update, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 检查超时
        if time.time() - task['started_at'] > 300:
            del self.pending_broadcasts[user_id]
            self.db.save_user(user_id, "", "", "")
            self.safe_send_message(update, "❌ 操作超时，请重新开始")
            return
        
        # 检查是否跳过
        buttons_text = buttons_text.strip()
        if buttons_text.lower() in ['跳过', 'skip', '']:
            task['buttons'] = []
            # 清空用户状态
            self.db.save_user(user_id, "", "", "")
            self.safe_send_message(update, "✅ <b>已跳过按钮设置</b>\n\n返回编辑器继续设置", 'HTML')
            self.show_broadcast_wizard_editor_as_new_message(update, context)
            return
        
        # 解析按钮
        buttons = []
        lines = buttons_text.split('\n')[:4]  # 最多4个按钮
        
        for line in lines:
            line = line.strip()
            if not line or '|' not in line:
                continue
            
            parts = line.split('|', 1)
            if len(parts) != 2:
                continue
            
            text = parts[0].strip()
            value = parts[1].strip()
            
            if not text or not value:
                continue
            
            # 判断按钮类型
            if value.startswith('callback:'):
                # 回调按钮
                callback_text = value[9:].strip()
                buttons.append({
                    'type': 'callback',
                    'text': text,
                    'data': f'broadcast_alert_{len(buttons)}',
                    'alert': callback_text
                })
            elif value.startswith('http://') or value.startswith('https://'):
                # URL按钮
                buttons.append({
                    'type': 'url',
                    'text': text,
                    'url': value
                })
            else:
                # 尝试作为URL处理
                if '.' in value:
                    buttons.append({
                        'type': 'url',
                        'text': text,
                        'url': f'https://{value}'
                    })
        
        task['buttons'] = buttons
        
        # 清空用户状态
        self.db.save_user(user_id, "", "", "")
        
        # 返回编辑器
        self.safe_send_message(update, f"✅ <b>已保存 {len(buttons)} 个按钮</b>\n\n返回编辑器继续设置", 'HTML')
        self.show_broadcast_wizard_editor_as_new_message(update, context)
    
    
    def show_target_selection(self, update, context, user_id):
        """显示目标用户选择"""
        if user_id not in self.pending_broadcasts:
            return
        
        task = self.pending_broadcasts[user_id]
        task['step'] = 'target'
        
        # 更新状态
        self.db.save_user(user_id, "", "", "")
        
        # 获取各类用户数量
        all_users = len(self.db.get_target_users('all'))
        members = len(self.db.get_target_users('members'))
        active_7d = len(self.db.get_target_users('active_7d'))
        new_7d = len(self.db.get_target_users('new_7d'))
        
        text = f"""
<b>📝 创建群发通知 - 步骤 4/4</b>

✅ 标题: <code>{task['title']}</code>
✅ 内容已设置
✅ 按钮: {len(task['buttons'])} 个

<b>🎯 请选择目标用户</b>

请选择要发送通知的用户群体：
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"👥 全部用户 ({all_users})", callback_data="broadcast_target_all")],
            [InlineKeyboardButton(f"💎 仅会员 ({members})", callback_data="broadcast_target_members")],
            [InlineKeyboardButton(f"🔥 活跃用户(7天) ({active_7d})", callback_data="broadcast_target_active_7d")],
            [InlineKeyboardButton(f"🆕 新用户(7天) ({new_7d})", callback_data="broadcast_target_new_7d")],
            [InlineKeyboardButton("❌ 取消", callback_data="broadcast_cancel")]
        ])
        
        self.safe_send_message(update, text, 'HTML', keyboard)
    
    def handle_broadcast_target_selection(self, query, update, context, target):
        """处理目标选择"""
        user_id = query.from_user.id
        query.answer()
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        task['target'] = target
        
        # 获取目标用户列表
        target_users = self.db.get_target_users(target)
        
        if not target_users:
            self.safe_edit_message(query, "❌ 未找到符合条件的用户")
            return
        
        # 目标名称映射
        target_names = {
            'all': '全部用户',
            'members': '仅会员',
            'active_7d': '活跃用户(7天)',
            'new_7d': '新用户(7天)'
        }
        
        # 生成预览
        buttons_preview = ""
        if task['buttons']:
            buttons_preview = "\n\n<b>🔘 按钮:</b>\n"
            for i, btn in enumerate(task['buttons'], 1):
                if btn['type'] == 'url':
                    buttons_preview += f"{i}. {btn['text']} → {btn['url']}\n"
                else:
                    buttons_preview += f"{i}. {btn['text']} (点击提示)\n"
        
        text = f"""
<b>📢 群发通知预览</b>

<b>📋 标题:</b> {task['title']}
<b>🎯 目标:</b> {target_names.get(target, target)} ({len(target_users)} 人)

<b>📄 内容:</b>
{task['content'][:200]}{'...' if len(task['content']) > 200 else ''}{buttons_preview}

<b>⚠️ 确认发送？</b>
• 预计耗时: {len(target_users) * 0.05:.1f} 秒
• 发送模式: 智能节流批量发送
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ 开始发送", callback_data="broadcast_confirm_send")],
            [InlineKeyboardButton("✏️ 返回修改", callback_data="broadcast_edit")],
            [InlineKeyboardButton("❌ 取消", callback_data="broadcast_cancel")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def start_broadcast_sending(self, query, update, context):
        """开始发送广播"""
        user_id = query.from_user.id
        query.answer()
        
        if user_id not in self.pending_broadcasts:
            self.safe_edit_message(query, "❌ 没有待处理的广播任务")
            return
        
        task = self.pending_broadcasts[user_id]
        
        # 插入广播记录
        buttons_json = json.dumps(task['buttons'], ensure_ascii=False)
        broadcast_id = self.db.insert_broadcast_record(
            task['title'],
            task['content'],
            buttons_json,
            task['target'],
            user_id
        )
        
        if not broadcast_id:
            self.safe_edit_message(query, "❌ 创建广播记录失败")
            return
        
        task['broadcast_id'] = broadcast_id
        
        # 启动异步发送
        def send_broadcast():
            asyncio.run(self.execute_broadcast_sending(update, context, user_id, broadcast_id))
        
        thread = threading.Thread(target=send_broadcast, daemon=True)
        thread.start()
        
        self.safe_edit_message(query, "📤 <b>开始发送广播...</b>\n\n正在初始化...", 'HTML')
    
    async def execute_broadcast_sending(self, update, context, admin_id, broadcast_id):
        """执行广播发送"""
        if admin_id not in self.pending_broadcasts:
            return
        
        task = self.pending_broadcasts[admin_id]
        start_time = time.time()
        
        # 获取目标用户
        target_users = self.db.get_target_users(task['target'])
        total = len(target_users)
        
        if total == 0:
            context.bot.send_message(
                chat_id=admin_id,
                text="❌ 未找到符合条件的用户",
                parse_mode='HTML'
            )
            del self.pending_broadcasts[admin_id]
            return
        
        # 构建按钮
        keyboard = None
        if task['buttons']:
            button_rows = []
            for btn in task['buttons']:
                if btn['type'] == 'url':
                    button_rows.append([InlineKeyboardButton(btn['text'], url=btn['url'])])
                else:
                    button_rows.append([InlineKeyboardButton(btn['text'], callback_data=btn['data'])])
            keyboard = InlineKeyboardMarkup(button_rows)
        
        # 发送统计
        success_count = 0
        failed_count = 0
        
        # 批量发送
        batch_size = 25
        progress_msg = None
        
        try:
            # 发送进度消息
            progress_msg = context.bot.send_message(
                chat_id=admin_id,
                text=f"📤 <b>广播发送中...</b>\n\n• 目标: {total} 人\n• 进度: 0/{total}\n• 成功: 0\n• 失败: 0",
                parse_mode='HTML'
            )
            
            for i in range(0, total, batch_size):
                batch = target_users[i:i + batch_size]
                batch_start = time.time()
                
                for user_id in batch:
                    try:
                        context.bot.send_message(
                            chat_id=user_id,
                            text=task['content'],
                            parse_mode='HTML',
                            reply_markup=keyboard
                        )
                        success_count += 1
                        self.db.add_broadcast_log(broadcast_id, user_id, 'success')
                    except RetryAfter as e:
                        # 处理速率限制
                        await asyncio.sleep(e.retry_after + 1)
                        try:
                            context.bot.send_message(
                                chat_id=user_id,
                                text=task['content'],
                                parse_mode='HTML',
                                reply_markup=keyboard
                            )
                            success_count += 1
                            self.db.add_broadcast_log(broadcast_id, user_id, 'success')
                        except Exception as retry_err:
                            failed_count += 1
                            self.db.add_broadcast_log(broadcast_id, user_id, 'failed', str(retry_err))
                    except BadRequest as e:
                        # 用户屏蔽机器人或其他错误
                        failed_count += 1
                        error_msg = str(e)
                        if 'bot was blocked' in error_msg.lower():
                            self.db.add_broadcast_log(broadcast_id, user_id, 'blocked', 'User blocked bot')
                        else:
                            self.db.add_broadcast_log(broadcast_id, user_id, 'failed', error_msg)
                    except Exception as e:
                        failed_count += 1
                        self.db.add_broadcast_log(broadcast_id, user_id, 'failed', str(e))
                
                # 更新进度
                processed = success_count + failed_count
                elapsed = time.time() - start_time
                speed = processed / elapsed if elapsed > 0 else 0
                eta = (total - processed) / speed if speed > 0 else 0
                
                if progress_msg and processed % batch_size == 0:
                    try:
                        progress_msg.edit_text(
                            f"📤 <b>广播发送中...</b>\n\n"
                            f"• 目标: {total} 人\n"
                            f"• 进度: {processed}/{total} ({processed/total*100:.1f}%)\n"
                            f"• 成功: {success_count}\n"
                            f"• 失败: {failed_count}\n"
                            f"• 速度: {speed:.1f} 人/秒\n"
                            f"• 预计剩余: {int(eta)} 秒",
                            parse_mode='HTML'
                        )
                    except:
                        pass
                
                # 批次间延迟
                if i + batch_size < total:
                    await asyncio.sleep(random.uniform(0.8, 1.2))
            
            # 完成
            duration = time.time() - start_time
            self.db.update_broadcast_progress(
                broadcast_id, success_count, failed_count, 'completed', duration
            )
            
            # 发送完成消息
            success_rate = (success_count / total * 100) if total > 0 else 0
            final_text = f"""
✅ <b>广播发送完成！</b>

<b>📊 发送统计</b>
• 目标用户: {total} 人
• ✅ 成功: {success_count} 人 ({success_rate:.1f}%)
• ❌ 失败: {failed_count} 人
• ⏱️ 总用时: {duration:.1f} 秒
• 🚀 平均速度: {total/duration:.1f} 人/秒

<b>📋 广播ID:</b> <code>{broadcast_id}</code>
            """
            
            context.bot.send_message(
                chat_id=admin_id,
                text=final_text,
                parse_mode='HTML'
            )
            
        except Exception as e:
            print(f"❌ 广播发送失败: {e}")
            import traceback
            traceback.print_exc()
            
            # 更新状态
            duration = time.time() - start_time
            self.db.update_broadcast_progress(
                broadcast_id, success_count, failed_count, 'failed', duration
            )
            
            context.bot.send_message(
                chat_id=admin_id,
                text=f"❌ <b>广播发送失败</b>\n\n错误: {str(e)}",
                parse_mode='HTML'
            )
        
        finally:
            # 清理任务
            if admin_id in self.pending_broadcasts:
                del self.pending_broadcasts[admin_id]
    
    def show_broadcast_history(self, query):
        """显示广播历史"""
        query.answer()
        
        history = self.db.get_broadcast_history(10)
        
        if not history:
            text = """
<b>📜 广播历史记录</b>

暂无广播记录
            """
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 返回", callback_data="broadcast_menu")]
            ])
            self.safe_edit_message(query, text, 'HTML', keyboard)
            return
        
        text = "<b>📜 广播历史记录</b>\n\n"
        
        buttons = []
        for record in history:
            broadcast_id, title, target, created_at, status, total, success, failed = record
            
            # 状态图标
            status_icon = {
                'pending': '⏳',
                'completed': '✅',
                'failed': '❌'
            }.get(status, '❓')
            
            # 目标名称
            target_names = {
                'all': '全部',
                'members': '会员',
                'active_7d': '活跃',
                'new_7d': '新用户'
            }
            target_name = target_names.get(target, target)
            
            text += f"{status_icon} <b>{title}</b>\n"
            text += f"   🎯 {target_name} | 👥 {total} | ✅ {success} | ❌ {failed}\n"
            text += f"   📅 {created_at}\n\n"
            
            buttons.append([
                InlineKeyboardButton(
                    f"📋 {title[:20]}{'...' if len(title) > 20 else ''}",
                    callback_data=f"broadcast_history_detail_{broadcast_id}"
                )
            ])
        
        buttons.append([InlineKeyboardButton("🔙 返回", callback_data="broadcast_menu")])
        keyboard = InlineKeyboardMarkup(buttons)
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def show_broadcast_detail(self, query, broadcast_id):
        """显示广播详情"""
        query.answer()
        
        detail = self.db.get_broadcast_detail(broadcast_id)
        
        if not detail:
            self.safe_edit_message(query, "❌ 未找到广播记录")
            return
        
        # 状态图标
        status_icon = {
            'pending': '⏳ 待发送',
            'completed': '✅ 已完成',
            'failed': '❌ 失败'
        }.get(detail['status'], '❓ 未知')
        
        # 目标名称
        target_names = {
            'all': '全部用户',
            'members': '仅会员',
            'active_7d': '活跃用户(7天)',
            'new_7d': '新用户(7天)'
        }
        target_name = target_names.get(detail['target'], detail['target'])
        
        # 按钮信息
        buttons_info = ""
        if detail['buttons_json']:
            try:
                buttons = json.loads(detail['buttons_json'])
                if buttons:
                    buttons_info = "\n\n<b>🔘 按钮:</b>\n"
                    for i, btn in enumerate(buttons, 1):
                        if btn['type'] == 'url':
                            buttons_info += f"{i}. {btn['text']} → {btn['url']}\n"
                        else:
                            buttons_info += f"{i}. {btn['text']} (回调)\n"
            except:
                pass
        
        success_rate = (detail['success'] / detail['total'] * 100) if detail['total'] > 0 else 0
        
        text = f"""
<b>📋 广播详情</b>

<b>🆔 ID:</b> <code>{detail['id']}</code>
<b>📋 标题:</b> {detail['title']}
<b>📅 创建时间:</b> {detail['created_at']}
<b>⚙️ 状态:</b> {status_icon}

<b>🎯 目标群体:</b> {target_name}
<b>👥 目标人数:</b> {detail['total']} 人

<b>📊 发送结果:</b>
• ✅ 成功: {detail['success']} 人 ({success_rate:.1f}%)
• ❌ 失败: {detail['failed']} 人
• ⏱️ 用时: {detail['duration_sec']:.1f} 秒

<b>📄 内容:</b>
{detail['content'][:300]}{'...' if len(detail['content']) > 300 else ''}{buttons_info}
        """
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 返回历史", callback_data="broadcast_history")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def cancel_broadcast(self, query, user_id):
        """取消广播"""
        query.answer()
        
        if user_id in self.pending_broadcasts:
            del self.pending_broadcasts[user_id]
        
        self.db.save_user(user_id, "", "", "")
        
        text = "❌ <b>已取消创建广播</b>"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 返回", callback_data="broadcast_menu")]
        ])
        
        self.safe_edit_message(query, text, 'HTML', keyboard)
    
    def restart_broadcast_wizard(self, query, update, context):
        """重新开始广播向导"""
        user_id = query.from_user.id
        
        if user_id in self.pending_broadcasts:
            del self.pending_broadcasts[user_id]
        
        self.start_broadcast_wizard(query, update, context)
    
    def run(self):
        print("🚀 启动增强版机器人（速度优化版）...")
        print(f"📡 代理模式: {'启用' if config.USE_PROXY else '禁用'}")
        print(f"🔢 可用代理: {len(self.proxy_manager.proxies)}个")
        print(f"⚡ 快速模式: {'开启' if config.PROXY_FAST_MODE else '关闭'}")
        print(f"🚀 并发数: {config.PROXY_CHECK_CONCURRENT if config.PROXY_FAST_MODE else config.MAX_CONCURRENT_CHECKS}个")
        print(f"⏱️ 检测超时: {config.PROXY_CHECK_TIMEOUT if config.PROXY_FAST_MODE else config.CHECK_TIMEOUT}秒")
        print(f"🔄 智能重试: {config.PROXY_RETRY_COUNT}次")
        print(f"🧹 自动清理: {'启用' if config.PROXY_AUTO_CLEANUP else '禁用'}")
        print("✅ 管理员系统: 启用")
        print("✅ 速度优化: 预计提升3-5倍")
        print("🛑 按 Ctrl+C 停止机器人")
        print("-" * 50)
        
        try:
            self.updater.start_polling()
            self.updater.idle()
        except KeyboardInterrupt:
            print("\n👋 机器人已停止")
        except Exception as e:
            print(f"\n❌ 运行错误: {e}")

# ================================
# 创建示例代理文件
# ================================

def create_sample_proxy_file():
    """创建示例代理文件"""
    proxy_file = "proxy.txt"
    if not os.path.exists(proxy_file):
        sample_content = """# 代理配置文件示例
# 支持的格式:
# HTTP代理: ip:port
# HTTP认证: ip:port:username:password
# SOCKS5: socks5:ip:port:username:password
# SOCKS4: socks4:ip:port
# ABCProxy住宅代理: host.abcproxy.vip:port:username:password

# 示例（请替换为真实代理）:
# 1.2.3.4:8080
# 1.2.3.4:8080:username:password
# socks5:1.2.3.4:1080:username:password
# socks4:1.2.3.4:1080

# ABCProxy住宅代理示例:
# f01a4db3d3952561.abcproxy.vip:4950:FlBaKtPm7l-zone-abc:00937128

# 注意:
# - 住宅代理（如ABCProxy）会自动检测并使用更长的超时时间（30秒）
# - 系统会自动优化住宅代理的连接参数
"""
        with open(proxy_file, 'w', encoding='utf-8') as f:
            f.write(sample_content)
        print(f"✅ 已创建示例代理文件: {proxy_file}")

# ================================
# Session文件管理系统
# ================================

def setup_session_directory():
    """确保sessions目录存在并移动任何残留的session文件和JSON文件"""
    sessions_dir = os.path.join(os.getcwd(), "sessions")
    
    # 创建sessions目录
    if not os.path.exists(sessions_dir):
        os.makedirs(sessions_dir)
        print(f"📁 创建sessions目录: {sessions_dir}")
    
    # 移动根目录中的session文件和JSON文件到sessions目录
    moved_count = 0
    current_dir = os.getcwd()
    
    # 系统必需文件，不移动
    system_files = ['tdata.session', 'tdata.session-journal']
    
    for filename in os.listdir(current_dir):
        # 检查是否是session文件或journal文件或对应的JSON文件
        should_move = False
        
        if filename.endswith('.session') or filename.endswith('.session-journal'):
            if filename not in system_files:
                should_move = True
        elif filename.endswith('.json'):
            # 检查是否是账号相关的JSON文件（通常以手机号命名）
            # 排除配置文件等
            if filename not in ['package.json', 'config.json', 'settings.json']:
                # 如果JSON文件名看起来像手机号或账号ID，则移动
                base_name = filename.replace('.json', '')
                if base_name.replace('_', '').isdigit() or len(base_name) > 8:
                    should_move = True
        
        if should_move:
            file_path = os.path.join(current_dir, filename)
            if os.path.isfile(file_path):
                new_path = os.path.join(sessions_dir, filename)
                try:
                    shutil.move(file_path, new_path)
                    print(f"📁 移动文件: {filename} -> sessions/")
                    moved_count += 1
                except Exception as e:
                    print(f"⚠️ 移动文件失败 {filename}: {e}")
    
    if moved_count > 0:
        print(f"✅ 已移动 {moved_count} 个文件到sessions目录")
    
    return sessions_dir

# ================================
# 启动脚本
# ================================

def main():
    print("🔍 Telegram账号检测机器人 V8.0")
    print("⚡ 群发通知完整版")
    print("=" * 50)
    
    # 设置session目录并清理残留文件
    setup_session_directory()
    
    # 创建示例代理文件
    create_sample_proxy_file()
    
    try:
        bot = EnhancedBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 再见！")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")

if __name__ == "__main__":
    main()
