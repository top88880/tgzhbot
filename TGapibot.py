#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram账号检测机器人 - V8.0
二级密码管理器修复完整版
"""

import os
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
    from login_api import LoginApiService, AIOHTTP_AVAILABLE as LOGIN_API_AVAILABLE
    print("✅ login_api模块导入成功")
except ImportError:
    LOGIN_API_AVAILABLE = False
    print("⚠️ login_api模块导入失败，Web Login API功能不可用")

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
        
        # 新增速度优化配置
        self.PROXY_CHECK_CONCURRENT = int(os.getenv("PROXY_CHECK_CONCURRENT", "50"))
        self.PROXY_CHECK_TIMEOUT = int(os.getenv("PROXY_CHECK_TIMEOUT", "3"))
        self.PROXY_AUTO_CLEANUP = os.getenv("PROXY_AUTO_CLEANUP", "true").lower() == "true"
        self.PROXY_FAST_MODE = os.getenv("PROXY_FAST_MODE", "true").lower() == "true"
        self.PROXY_RETRY_COUNT = int(os.getenv("PROXY_RETRY_COUNT", "2"))
        self.PROXY_BATCH_SIZE = int(os.getenv("PROXY_BATCH_SIZE", "20"))
        
        # Web Login API 配置
        self.API_SERVER_HOST = os.getenv("API_SERVER_HOST", "0.0.0.0")
        self.API_SERVER_PORT = int(os.getenv("API_SERVER_PORT", "8080"))
        self.PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "")
        
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
        print(f"🌐 Web Login API: {self.API_SERVER_HOST}:{self.API_SERVER_PORT}")
        if self.PUBLIC_BASE_URL:
            print(f"🔗 公开 URL: {self.PUBLIC_BASE_URL}")
    
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
API_SERVER_HOST=0.0.0.0
API_SERVER_PORT=8080
PUBLIC_BASE_URL=
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
        if self.is_admin(user_id):
            return True, "管理员", "永久有效"
        
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT level, trial_expiry_time FROM memberships WHERE user_id = ?", (user_id,))
            row = c.fetchone()
            conn.close()
            
            if not row:
                return False, "无会员", "未订阅"
            
            level, trial_expiry_time = row
            
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
                
                # 方法2: 如果没有找到任何密码文件，创建新的 2fa.txt
                if not found_files:
                    try:
                        # 在 D877F783D5D3EF8C 目录下创建 2fa.txt
                        new_password_file = os.path.join(d877_path, "2fa.txt")
                        with open(new_password_file, 'w', encoding='utf-8') as f:
                            f.write(new_password)
                        print(f"✅ TData密码文件已创建: 2fa.txt (位置: D877F783D5D3EF8C/)")
                        updated = True
                    except Exception as e:
                        print(f"❌ 创建密码文件失败: {e}")
                
                return updated
            
            return False
            
        except Exception as e:
            print(f"❌ 更新文件密码失败: {e}")
            return False
    
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
                    f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"总数: {len(items)}个\n\n")
                    
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
        
        # 初始化 Web Login API 服务
        self.login_api_service = None
        if LOGIN_API_AVAILABLE:
            try:
                self.login_api_service = LoginApiService(
                    host=config.API_SERVER_HOST,
                    port=config.API_SERVER_PORT,
                    public_base_url=config.PUBLIC_BASE_URL
                )
                self.login_api_service.start_background()
                print("✅ Web Login API 服务已启动")
            except Exception as e:
                print(f"⚠️ Web Login API 服务启动失败: {e}")
                self.login_api_service = None
        else:
            print("⚠️ Web Login API 服务不可用（aiohttp未安装）")
        
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
        self.dp.add_handler(CommandHandler("api", self.api_command))
        self.dp.add_handler(CallbackQueryHandler(self.handle_callbacks))
        self.dp.add_handler(MessageHandler(Filters.document, self.handle_file))
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
• 快速模式: {'🟢开启' if config.PROXY_FAST_MODE else '🔴关闭'}
• 并发数量: {config.PROXY_CHECK_CONCURRENT if config.PROXY_FAST_MODE else config.MAX_CONCURRENT_CHECKS}个

⚡ <b>速度优化</b>
• 检测超时: {config.PROXY_CHECK_TIMEOUT if config.PROXY_FAST_MODE else config.CHECK_TIMEOUT}秒
• 智能重试: {config.PROXY_RETRY_COUNT}次
• 自动清理: {'🟢启用' if config.PROXY_AUTO_CLEANUP else '🔴关闭'}
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
                InlineKeyboardButton("🌐 api转换", callback_data="api_convert")
            ],
            [
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
    
    def api_command(self, update: Update, context: CallbackContext):
        """API命令 - 扫描sessions文件夹并发布登录链接"""
        user_id = update.effective_user.id
        
        # 检查权限
        is_member, level, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 需要会员权限才能使用API功能")
            return
        
        # 检查 Web Login API 服务是否可用
        if not self.login_api_service:
            self.safe_send_message(
                update,
                "❌ Web Login API 服务不可用\n\n"
                "原因: aiohttp库未安装或服务启动失败\n"
                "💡 请安装: pip install aiohttp",
                'HTML'
            )
            return
        
        # 扫描 sessions 目录
        sessions_dir = os.path.join(os.getcwd(), "sessions")
        if not os.path.exists(sessions_dir):
            self.safe_send_message(
                update,
                "❌ sessions 目录不存在\n\n"
                "请先将 .session 文件放入 sessions 目录",
                'HTML'
            )
            return
        
        # 查找所有 .session 文件
        session_files = []
        for filename in os.listdir(sessions_dir):
            if filename.endswith('.session') and not filename.endswith('.session-journal'):
                session_path = os.path.join(sessions_dir, filename)
                session_files.append((session_path, filename))
        
        if not session_files:
            self.safe_send_message(
                update,
                "❌ sessions 目录中没有找到 .session 文件",
                'HTML'
            )
            return
        
        # 注册所有 sessions 并生成链接
        links_text = "🌐 <b>Web Login API 链接</b>\n\n"
        links_text += f"📊 找到 {len(session_files)} 个 session 文件\n\n"
        
        for session_path, filename in session_files:
            # 从文件名提取手机号
            phone = filename.replace('.session', '')
            
            # 注册到 Web Login API
            try:
                url = self.login_api_service.register_session(
                    session_path=session_path,
                    phone=phone,
                    api_id=config.API_ID,
                    api_hash=config.API_HASH
                )
                
                links_text += f"📱 <code>{phone}</code>\n"
                links_text += f"🔗 {url}\n\n"
                
            except Exception as e:
                print(f"❌ 注册 session 失败 {phone}: {e}")
                links_text += f"❌ <code>{phone}</code> - 注册失败\n\n"
        
        links_text += "💡 <b>使用说明:</b>\n"
        links_text += "• 点击链接访问登录页面\n"
        links_text += "• 页面会实时显示收到的验证码\n"
        links_text += "• 支持 API 接口查询验证码\n"
        
        self.safe_send_message(update, links_text, 'HTML')
    
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
        elif data == "api_convert":
            self.handle_api_convert(query)
        elif data == "convert_tdata_to_session":
            self.handle_convert_tdata_to_session(query)
        elif data == "convert_session_to_tdata":
            self.handle_convert_session_to_tdata(query)
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
• 并发数量: {config.PROXY_CHECK_CONCURRENT if config.PROXY_FAST_MODE else config.MAX_CONCURRENT_CHECKS}个

⚡ <b>速度优化</b>
• 检测超时: {config.PROXY_CHECK_TIMEOUT if config.PROXY_FAST_MODE else config.CHECK_TIMEOUT}秒
• 智能重试: {config.PROXY_RETRY_COUNT}次
• 自动清理: {'🟢启用' if config.PROXY_AUTO_CLEANUP else '🔴关闭'}
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
    
    def handle_api_convert(self, query):
        """处理API转换"""
        query.answer()
        user_id = query.from_user.id
        
        # 检查权限
        is_member, level, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_edit_message(query, "❌ 需要会员权限才能使用API转换功能")
            return
        
        # 检查 LoginApiService 是否可用
        if not self.login_api_service:
            self.safe_edit_message(query, "❌ Web Login API服务不可用\n\n原因: aiohttp库未安装或服务未启动\n💡 请安装: pip install aiohttp")
            return
        
        text = """
🌐 <b>批量转换API功能</b>

<b>✨ 核心功能</b>
• 📱 <b>自动转换</b>
  - TData格式：自动转换为Session并生成API链接
  - Session格式：直接使用已有Session生成API链接
  - 智能识别：系统自动检测文件类型

• 🔗 <b>生成网页接码链接</b>
  - 每个账号生成唯一的网页链接
  - 用于后续登录时获取验证码
  - 链接永久有效，随时可查看

• 📊 <b>实时进度显示</b>
  - 显示转换和处理进度
  - 自动生成结果文件
  - 包含手机号和对应链接

<b>📤 操作说明</b>
请上传 tdata 或 session+json 的 ZIP 文件，系统将转换为 API 并生成网页接码链接；处理中会显示实时进度。

<b>📁 支持格式</b>
• TData 文件夹（包含 D877F783D5D3EF8C 目录）
• Session 文件（.session 格式）
• ZIP 压缩包

🚀 请上传您的ZIP文件...
        """
        
        buttons = [
            [InlineKeyboardButton("🔙 返回主菜单", callback_data="back_to_main")]
        ]
        
        keyboard = InlineKeyboardMarkup(buttons)
        self.safe_edit_message(query, text, 'HTML', keyboard)
        
        # 设置用户状态
        self.db.save_user(user_id, query.from_user.username or "", 
                         query.from_user.first_name or "", "waiting_api_convert_file")
    
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

<b>⚡ 检测设置</b>
• 标准并发: {config.MAX_CONCURRENT_CHECKS}个
• 快速并发: {config.PROXY_CHECK_CONCURRENT}个
• 标准超时: {config.CHECK_TIMEOUT}秒
• 快速超时: {config.PROXY_CHECK_TIMEOUT}秒
• SpamBot等待: {config.SPAMBOT_WAIT_TIME}秒
• 智能重试: {config.PROXY_RETRY_COUNT}次
• Telethon: {'✅可用' if TELETHON_AVAILABLE else '❌不可用'}

<b>📡 代理状态</b>
• 系统配置: {'🟢USE_PROXY=true' if config.USE_PROXY else '🔴USE_PROXY=false'}
• 代理开关: {'🟢已启用' if self.db.get_proxy_enabled() else '🔴已禁用'}
• 实际模式: {'🟢代理模式' if self.proxy_manager.is_proxy_mode_active(self.db) else '🔴本地模式'}
• 代理数量: {len(self.proxy_manager.proxies)}个
• 代理超时: {config.PROXY_TIMEOUT}秒
• 代理支持: {'✅完整' if PROXY_SUPPORT else '⚠️基础'}

<b>🚀 速度优化</b>
• 快速模式: {'✅启用' if config.PROXY_FAST_MODE else '❌禁用'}
• 自动清理: {'✅启用' if config.PROXY_AUTO_CLEANUP else '❌禁用'}
• 批量大小: {config.PROXY_BATCH_SIZE}个
• 预计提升: 3-5倍速度

<b>🛡️ 增强功能</b>
• 代理轮换: ✅启用
• 自动故障转移: ✅启用
• 智能重试: ✅启用
• 快速预检测: ✅启用
• 管理员系统: ✅启用
• 代理开关控制: ✅启用
"""
        
        self.safe_edit_message(query, status_text, 'HTML')
    
    def handle_admin_panel(self, query):
        """管理员面板"""
        user_id = query.from_user.id
        
        if not self.db.is_admin(user_id):
            query.answer("❌ 仅管理员可访问")
            return
        
        # 获取管理员统计信息
        admins = self.db.get_all_admins()
        admin_count = len(admins) if admins else 0
        
        admin_text = f"""
<b>👑 管理员控制面板</b>

<b>📊 管理员系统状态</b>
• 当前管理员: {admin_count}个
• 您的权限: {'👑 超级管理员' if user_id in config.ADMIN_IDS else '🔧 普通管理员'}
• 系统时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>🔧 管理员命令</b>
• /addadmin [ID/用户名] - 添加管理员
• /removeadmin [ID] - 移除管理员
• /listadmins - 查看管理员列表

<b>📡 代理管理</b>
• /proxy status - 查看代理状态
• /proxy reload - 重新加载代理

<b>ℹ️ 使用说明</b>
直接在聊天中输入上述命令即可执行相应操作
        """
        
        self.safe_edit_message(query, admin_text, 'HTML')
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
            
            if not row or row[0] not in ["waiting_file", "waiting_convert_tdata", "waiting_convert_session", "waiting_2fa_file", "waiting_api_convert_file"]:
                self.safe_send_message(update, "❌ 请先点击 🚀开始检测、🔄格式转换、🔐修改2FA 或 🌐api转换 按钮")
                return
            
            user_status = row[0]
        except:
            self.safe_send_message(update, "❌ 系统错误，请重试")
            return
        
        is_member, _, _ = self.db.check_membership(user_id)
        if not is_member and not self.db.is_admin(user_id):
            self.safe_send_message(update, "❌ 需要会员权限")
            return
        
        if document.file_size > 100 * 1024 * 1024:
            self.safe_send_message(update, f"❌ 文件过大 (限制100MB)")
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
        elif user_status == "waiting_api_convert_file":
            # 异步处理API转换
            def process_api():
                asyncio.run(self.process_api_conversion(update, context, document))
            
            thread = threading.Thread(target=process_api)
            thread.start()
        
        self.db.save_user(user_id, update.effective_user.username or "", 
                         update.effective_user.first_name or "", "")

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
            
            # 如果是 tdata_to_session 转换且有成功的，自动注册到 Web Login API
            api_links_text = ""
            if conversion_type == "tdata_to_session" and success_count > 0 and self.login_api_service:
                api_links_text = "\n\n🌐 <b>Web Login API 链接</b>\n"
                
                # 查找转换成功的 session 文件并注册
                sessions_dir = os.path.join(os.getcwd(), "sessions")
                registered_count = 0
                
                for file_path, file_name, info in results.get("转换成功", []):
                    try:
                        # 查找对应的 session 文件
                        # file_name 是 tdata 目录名，需要找到对应的 session
                        # session 文件在 results 中的 file_path 指向
                        session_files = []
                        if os.path.isdir(file_path):
                            # 如果是目录，查找其中的 session 文件
                            for item in os.listdir(file_path):
                                if item.endswith('.session'):
                                    session_files.append(os.path.join(file_path, item))
                        else:
                            # 如果直接是文件
                            if file_path.endswith('.session'):
                                session_files.append(file_path)
                        
                        # 也检查 sessions 目录
                        if os.path.exists(sessions_dir):
                            for item in os.listdir(sessions_dir):
                                if item.endswith('.session') and file_name in item:
                                    session_path = os.path.join(sessions_dir, item)
                                    if session_path not in session_files:
                                        session_files.append(session_path)
                        
                        # 注册找到的 session 文件
                        for session_path in session_files:
                            if os.path.exists(session_path):
                                phone = os.path.basename(session_path).replace('.session', '')
                                url = self.login_api_service.register_session(
                                    session_path=session_path,
                                    phone=phone,
                                    api_id=config.API_ID,
                                    api_hash=config.API_HASH
                                )
                                api_links_text += f"📱 {phone}\n🔗 {url}\n\n"
                                registered_count += 1
                                
                    except Exception as e:
                        print(f"⚠️ 注册 session 到 API 失败 {file_name}: {e}")
                
                if registered_count > 0:
                    api_links_text += f"✅ 已注册 {registered_count} 个账号到 Web Login API\n"
                else:
                    api_links_text = ""
            
            final_text = f"""
✅ <b>转换任务完成！</b>

📊 <b>转换统计</b>
• 总计: {total_files}个
• ✅ 成功: {success_count}个 ({success_rate:.1f}%)
• ❌ 失败: {error_count}个 ({100-success_rate:.1f}%)
• ⏱️ 总用时: {int(elapsed_time)}秒 ({elapsed_time/60:.1f}分钟)
• 🚀 平均速度: {total_files/elapsed_time:.2f}个/秒


📥 {'所有结果文件已发送！'}{api_links_text}
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
    
    async def process_api_conversion(self, update, context, document):
        """处理API转换 - 将TData或Session转换为API链接"""
        user_id = update.effective_user.id
        start_time = time.time()
        task_id = f"{user_id}_{int(start_time)}"
        
        print(f"🌐 开始API转换任务: {task_id}")
        
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
        extract_dir = None
        try:
            # 下载文件
            temp_dir = tempfile.mkdtemp(prefix="temp_api_")
            temp_zip = os.path.join(temp_dir, document.file_name)
            
            document.get_file().download(temp_zip)
            print(f"📥 下载文件: {temp_zip}")
            
            # 扫描文件
            files, extract_dir, file_type = self.processor.scan_zip_file(temp_zip, user_id, task_id)
            
            if not files:
                try:
                    progress_msg.edit_text(
                        "❌ <b>未找到有效文件</b>\n\n请确保ZIP包含TData或Session格式的账号文件",
                        parse_mode='HTML'
                    )
                except:
                    pass
                return
            
            total_files = len(files)
            
            try:
                progress_msg.edit_text(
                    f"🔄 <b>转换 API 进行中...</b>\n\n📁 找到 {total_files} 个文件\n📊 文件类型: {file_type.upper()}\n⏳ 正在初始化...",
                    parse_mode='HTML'
                )
            except:
                pass
            
            # 存储成功转换的session信息
            success_sessions = []
            
            # 如果是TData格式，需要先转换为Session
            if file_type == "tdata":
                print(f"📦 检测到TData格式，开始转换为Session...")
                
                # 定义进度回调
                async def conversion_callback(processed, total, results, speed, elapsed):
                    try:
                        success_count = len(results.get("转换成功", []))
                        error_count = len(results.get("转换错误", []))
                        
                        progress_text = f"""
🔄 <b>转换 API 进行中...</b>

📊 <b>当前进度</b>
• 已处理: {processed}/{total}
• 速度: {speed:.1f} 个/秒
• 用时: {int(elapsed)} 秒

✅ <b>转换成功</b>: {success_count}
❌ <b>转换错误</b>: {error_count}

⏱️ 预计剩余: {int((total - processed) / speed) if speed > 0 else 0} 秒
                        """
                        
                        try:
                            progress_msg.edit_text(progress_text, parse_mode='HTML')
                        except:
                            pass
                    except Exception as e:
                        print(f"⚠️ 更新进度失败: {e}")
                
                # 执行批量转换
                conversion_results = await self.converter.batch_convert_with_progress(
                    files, 
                    "tdata_to_session",
                    config.API_ID,
                    config.API_HASH,
                    conversion_callback
                )
                
                # 从转换成功的结果中提取session文件
                sessions_dir = os.path.join(os.getcwd(), "sessions")
                for file_path, file_name, info in conversion_results.get("转换成功", []):
                    # 查找转换后的session文件
                    session_file = os.path.join(sessions_dir, f"{file_name}.session")
                    if os.path.exists(session_file):
                        success_sessions.append((session_file, file_name))
                        print(f"✅ 转换成功: {file_name}")
                
                print(f"📊 转换完成: 成功 {len(success_sessions)} 个")
                
            elif file_type == "session":
                print(f"📱 检测到Session格式，直接使用...")
                # 直接使用session文件
                for file_path, file_name in files:
                    if file_path.endswith('.session'):
                        # 提取手机号（从文件名）
                        phone = os.path.basename(file_path).replace('.session', '')
                        success_sessions.append((file_path, phone))
                        print(f"✅ 找到Session: {phone}")
            
            # 为每个session注册到LoginAPI并生成链接
            print(f"🔗 开始注册 {len(success_sessions)} 个账号到 Web Login API...")
            
            api_links = []
            registered_count = 0
            
            for session_path, phone in success_sessions:
                try:
                    if os.path.exists(session_path):
                        url = self.login_api_service.register_session(
                            session_path=session_path,
                            phone=phone,
                            api_id=config.API_ID,
                            api_hash=config.API_HASH
                        )
                        api_links.append((phone, url))
                        registered_count += 1
                        print(f"🔗 注册成功: {phone} -> {url}")
                except Exception as e:
                    print(f"⚠️ 注册失败 {phone}: {e}")
            
            # 生成TXT文件
            if api_links:
                result_filename = f"批量转换API_获取成功_{registered_count}.txt"
                result_path = os.path.join(config.RESULTS_DIR, result_filename)
                
                try:
                    with open(result_path, 'w', encoding='utf-8') as f:
                        for phone, url in api_links:
                            f.write(f"{phone} {url}\n")
                    
                    print(f"📄 生成结果文件: {result_filename}")
                except Exception as e:
                    print(f"❌ 生成文件失败: {e}")
                    result_path = None
            else:
                result_path = None
            
            elapsed_time = time.time() - start_time
            
            # 发送结果统计
            summary_text = f"""
批量转换API｜统计数据

🟢 获取成功: {registered_count}

⏱️ 处理时间: {int(elapsed_time)} 秒
📊 文件类型: {file_type.upper()}

{'📦 正在发送结果文件...' if result_path else '❌ 没有成功转换的账号'}
            """
            
            try:
                progress_msg.edit_text(summary_text, parse_mode=None)
            except:
                pass
            
            # 发送TXT文件
            if result_path and os.path.exists(result_path):
                try:
                    with open(result_path, 'rb') as f:
                        caption = f"📋 批量转换API结果\n\n🟢 获取成功: {registered_count}个账号\n⏰ 处理时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        context.bot.send_document(
                            chat_id=update.effective_chat.id,
                            document=f,
                            filename=result_filename,
                            caption=caption
                        )
                    print(f"📤 发送结果文件: {result_filename}")
                    
                    # 清理结果文件
                    try:
                        os.remove(result_path)
                    except:
                        pass
                        
                except Exception as e:
                    print(f"❌ 发送文件失败: {e}")
            
            # 最终消息
            final_text = f"""
✅ <b>API转换完成！</b>

📊 <b>转换统计</b>
• 总计: {total_files}个
• 🟢 获取成功: {registered_count}个
• ⏱️ 总用时: {int(elapsed_time)}秒

{'📥 结果文件已发送！' if registered_count > 0 else ''}

如需再次使用，请点击 /start
            """
            
            self.safe_send_message(update, final_text, 'HTML')
            
        except Exception as e:
            print(f"❌ API转换失败: {e}")
            import traceback
            traceback.print_exc()
            
            try:
                progress_msg.edit_text(
                    f"❌ <b>API转换失败</b>\n\n错误: {str(e)}",
                    parse_mode='HTML'
                )
            except:
                pass
        
        finally:
            # 清理临时文件
            if extract_dir and os.path.exists(extract_dir):
                try:
                    shutil.rmtree(extract_dir, ignore_errors=True)
                    print(f"🗑️ 清理解压目录: {extract_dir}")
                except:
                    pass
            
            if temp_zip and os.path.exists(temp_zip):
                try:
                    shutil.rmtree(os.path.dirname(temp_zip), ignore_errors=True)
                    print(f"🗑️ 清理临时文件: {temp_zip}")
                except:
                    pass
    
    def handle_text(self, update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        text = update.message.text
        
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
        
        # 其他文本消息的处理
        text_lower = text.lower()
        if any(word in text_lower for word in ["你好", "hello", "hi"]):
            self.safe_send_message(update, "👋 你好！发送 /start 开始检测")
        elif "帮助" in text_lower or "help" in text_lower:
            self.safe_send_message(update, "📖 发送 /help 查看帮助")
    
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
    print("⚡ 二级密码管理器修复完整版")
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
