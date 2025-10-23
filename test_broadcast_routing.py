#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for broadcast callback routing
Validates that all broadcast_* callbacks are properly routed
"""

import sys
import re

def test_broadcast_routing():
    """Test that all broadcast callback patterns are properly handled"""
    
    print("=" * 60)
    print("🧪 Broadcast Callback Routing Test")
    print("=" * 60)
    
    # Read TGapibot.py
    with open('TGapibot.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test 1: Check dedicated CallbackQueryHandler registration
    print("\n1️⃣ Testing CallbackQueryHandler registration...")
    pattern = r'CallbackQueryHandler\(self\.handle_broadcast_callbacks_router,\s*pattern=r"\^broadcast_"'
    if re.search(pattern, content):
        print("   ✅ Dedicated broadcast CallbackQueryHandler found")
    else:
        print("   ❌ Dedicated broadcast CallbackQueryHandler NOT found")
        return False
    
    # Test 2: Check handler order (broadcast before generic)
    print("\n2️⃣ Testing handler registration order...")
    lines = content.split('\n')
    broadcast_line = -1
    generic_line = -1
    
    for i, line in enumerate(lines):
        if 'handle_broadcast_callbacks_router' in line and 'CallbackQueryHandler' in line:
            broadcast_line = i
        if 'self.handle_callbacks)' in line and 'CallbackQueryHandler' in line and 'pattern' not in line:
            generic_line = i
    
    if broadcast_line > 0 and generic_line > 0:
        if broadcast_line < generic_line:
            print(f"   ✅ Broadcast handler (line {broadcast_line}) before generic handler (line {generic_line})")
        else:
            print(f"   ❌ ERROR: Generic handler (line {generic_line}) before broadcast handler (line {broadcast_line})")
            return False
    else:
        print("   ❌ Could not find handler registration lines")
        return False
    
    # Test 3: Check dispatch table exists
    print("\n3️⃣ Testing dispatch table...")
    required_actions = [
        'broadcast_menu',
        'broadcast_create',
        'broadcast_history',
        'broadcast_cancel',
        'broadcast_media',
        'broadcast_media_view',
        'broadcast_media_clear',
        'broadcast_text',
        'broadcast_text_view',
        'broadcast_buttons',
        'broadcast_buttons_view',
        'broadcast_buttons_clear',
        'broadcast_preview',
        'broadcast_back',
        'broadcast_next'
    ]
    
    missing_actions = []
    for action in required_actions:
        pattern = f'"{action}".*lambda'
        if not re.search(pattern, content):
            missing_actions.append(action)
    
    if not missing_actions:
        print(f"   ✅ All {len(required_actions)} required actions in dispatch table")
    else:
        print(f"   ❌ Missing actions: {', '.join(missing_actions)}")
        return False
    
    # Test 4: Check query.answer() safety
    print("\n4️⃣ Testing query.answer() safety...")
    router_func = content[content.find('def handle_broadcast_callbacks_router'):content.find('def handle_broadcast_callbacks_router') + 2000]
    
    if 'try:' in router_func and 'query.answer()' in router_func:
        print("   ✅ query.answer() wrapped in try/except")
    else:
        print("   ❌ query.answer() not properly wrapped")
        return False
    
    # Test 5: Check new methods exist
    print("\n5️⃣ Testing new broadcast methods...")
    required_methods = [
        'handle_broadcast_media',
        'handle_broadcast_media_view',
        'handle_broadcast_media_clear',
        'handle_broadcast_text',
        'handle_broadcast_text_view',
        'handle_broadcast_buttons',
        'handle_broadcast_buttons_view',
        'handle_broadcast_buttons_clear',
        'handle_broadcast_preview',
        'handle_broadcast_back',
        'handle_broadcast_next',
        'handle_broadcast_alert_button',
        'show_broadcast_wizard_editor'
    ]
    
    missing_methods = []
    for method in required_methods:
        if f'def {method}(' not in content:
            missing_methods.append(method)
    
    if not missing_methods:
        print(f"   ✅ All {len(required_methods)} required methods implemented")
    else:
        print(f"   ❌ Missing methods: {', '.join(missing_methods)}")
        return False
    
    # Test 6: Check photo handler
    print("\n6️⃣ Testing photo upload handler...")
    if 'MessageHandler(Filters.photo, self.handle_photo)' in content:
        print("   ✅ Photo handler registered")
    else:
        print("   ❌ Photo handler NOT registered")
        return False
    
    if 'def handle_photo(' in content:
        print("   ✅ handle_photo method exists")
    else:
        print("   ❌ handle_photo method NOT found")
        return False
    
    # Test 7: Check two-column UI implementation
    print("\n7️⃣ Testing two-column UI...")
    if 'show_broadcast_wizard_editor' in content:
        editor_func = content[content.find('def show_broadcast_wizard_editor'):content.find('def show_broadcast_wizard_editor') + 2000]
        
        # Check for button layout
        button_checks = [
            ('📸 媒体', 'Media button'),
            ('📝 文本', 'Text button'),
            ('🔘 按钮', 'Buttons button'),
            ('🔍 完整预览', 'Preview button'),
            ('➡️ 下一步', 'Next button'),
            ('🔙 返回', 'Back button')
        ]
        
        missing_buttons = []
        for label, desc in button_checks:
            if label not in editor_func:
                missing_buttons.append(desc)
        
        if not missing_buttons:
            print("   ✅ Two-column UI with all required buttons")
        else:
            print(f"   ❌ Missing UI buttons: {', '.join(missing_buttons)}")
            return False
    else:
        print("   ❌ show_broadcast_wizard_editor method NOT found")
        return False
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_broadcast_routing()
    sys.exit(0 if success else 1)
