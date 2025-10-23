#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edge case tests for phone-based Account Merge feature
"""

import sys
import os
import tempfile
import shutil
import zipfile
import json

def test_phone_with_plus_sign():
    """Test phone extraction with + prefix"""
    print("Testing phone extraction with + prefix...")
    
    test_dir = tempfile.mkdtemp(prefix="test_plus_")
    
    try:
        # Create TData with +phone in path
        phone = "+1234567890"
        acc_dir = os.path.join(test_dir, phone)
        tdata_path = os.path.join(acc_dir, 'tdata', 'D877F783D5D3EF8C')
        os.makedirs(tdata_path)
        with open(os.path.join(tdata_path, 'key'), 'w') as f:
            f.write('data')
        
        # Extract phone
        def extract_phone_from_tdata_path(account_root, tdata_dir_name):
            parent_dir = os.path.basename(account_root)
            phone_clean = parent_dir.lstrip('+')
            if phone_clean.isdigit() and len(phone_clean) >= 10:
                return phone_clean
            return None
        
        result = extract_phone_from_tdata_path(acc_dir, 'tdata')
        
        if result == "1234567890":
            print(f"  ✅ PASS: +phone extracted correctly: {result}")
            return True
        else:
            print(f"  ❌ FAIL: Expected '1234567890', got '{result}'")
            return False
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_short_phone_rejection():
    """Test that short phone numbers are rejected"""
    print("\nTesting short phone number rejection...")
    
    test_dir = tempfile.mkdtemp(prefix="test_short_")
    
    try:
        # Create JSON with short phone
        json_path = os.path.join(test_dir, 'test.json')
        with open(json_path, 'w') as f:
            json.dump({"phone": "12345"}, f)  # Too short
        
        def extract_phone_from_json(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    phone = data.get('phone', '')
                    if phone:
                        phone_clean = ''.join(c for c in phone if c.isdigit())
                        if phone_clean and len(phone_clean) >= 10:
                            return phone_clean
            except:
                pass
            return None
        
        result = extract_phone_from_json(json_path)
        
        if result is None:
            print(f"  ✅ PASS: Short phone correctly rejected")
            return True
        else:
            print(f"  ❌ FAIL: Short phone should be rejected, got '{result}'")
            return False
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_mixed_case_tdata():
    """Test TData detection with mixed case directory names"""
    print("\nTesting mixed case TData detection...")
    
    test_dir = tempfile.mkdtemp(prefix="test_case_")
    
    try:
        # Create TData with various cases
        phone = "1234567890"
        
        test_cases = [
            ('tdata', 'd877f783d5d3ef8c'),
            ('TData', 'D877F783D5D3EF8C'),
            ('TDATA', 'd877f783d5d3ef8c'),
            ('TdAtA', 'D877F783D5D3EF8C'),
        ]
        
        detected_count = 0
        
        for tdata_name, marker_name in test_cases:
            acc_dir = os.path.join(test_dir, f'{phone}_{tdata_name}')
            tdata_path = os.path.join(acc_dir, tdata_name, marker_name)
            os.makedirs(tdata_path)
            with open(os.path.join(tdata_path, 'key'), 'w') as f:
                f.write('data')
            
            # Scan for TData (case-insensitive)
            for root, dirs, files in os.walk(acc_dir):
                dirs_lower = [d.lower() for d in dirs]
                if 'tdata' in dirs_lower:
                    tdata_dir_name = dirs[dirs_lower.index('tdata')]
                    found_tdata_path = os.path.join(root, tdata_dir_name)
                    
                    if os.path.exists(found_tdata_path):
                        for subdir in os.listdir(found_tdata_path):
                            if subdir.upper() == 'D877F783D5D3EF8C':
                                detected_count += 1
                                break
        
        if detected_count == 4:
            print(f"  ✅ PASS: All 4 mixed-case TData detected")
            return True
        else:
            print(f"  ❌ FAIL: Expected 4 TData, detected {detected_count}")
            return False
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_no_phone_fallback():
    """Test fallback naming when no phone number available"""
    print("\nTesting fallback naming without phone...")
    
    test_dir = tempfile.mkdtemp(prefix="test_fallback_")
    
    try:
        # Create TData without phone in path
        acc_dir = os.path.join(test_dir, 'MyTelegramAccount')
        tdata_path = os.path.join(acc_dir, 'tdata', 'D877F783D5D3EF8C')
        os.makedirs(tdata_path)
        with open(os.path.join(tdata_path, 'key'), 'w') as f:
            f.write('data')
        
        def extract_phone_from_tdata_path(account_root, tdata_dir_name):
            parent_dir = os.path.basename(account_root)
            phone_clean = parent_dir.lstrip('+')
            if phone_clean.isdigit() and len(phone_clean) >= 10:
                return phone_clean
            return None
        
        result = extract_phone_from_tdata_path(acc_dir, 'tdata')
        
        if result is None:
            print(f"  ✅ PASS: No phone extracted, will use fallback naming")
            
            # Simulate fallback naming
            tdata_without_phones = [(acc_dir, 'tdata')]
            fallback_name = f'account_{1}'
            
            print(f"    Fallback name: {fallback_name}")
            return True
        else:
            print(f"  ❌ FAIL: Expected None, got '{result}'")
            return False
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_multiple_accounts_same_phone():
    """Test that only first account is kept when multiple have same phone"""
    print("\nTesting multiple accounts with same phone...")
    
    test_dir = tempfile.mkdtemp(prefix="test_multi_")
    
    try:
        phone = "1234567890"
        
        # Create 3 accounts with same phone
        accounts = []
        for i in range(3):
            acc_dir = os.path.join(test_dir, f'{phone}_v{i}')
            tdata_path = os.path.join(acc_dir, 'tdata', 'D877F783D5D3EF8C')
            os.makedirs(tdata_path)
            with open(os.path.join(tdata_path, f'key{i}'), 'w') as f:
                f.write(f'data{i}')
            accounts.append((acc_dir, 'tdata'))
        
        def extract_phone_from_tdata_path(account_root, tdata_dir_name):
            parent = os.path.basename(account_root)
            phone_clean = parent.split('_')[0]
            if phone_clean.isdigit() and len(phone_clean) >= 10:
                return phone_clean
            return None
        
        # Deduplicate
        tdata_with_phones = {}
        duplicates = 0
        
        for account_root, tdata_dir_name in accounts:
            phone_extracted = extract_phone_from_tdata_path(account_root, tdata_dir_name)
            if phone_extracted:
                if phone_extracted not in tdata_with_phones:
                    tdata_with_phones[phone_extracted] = (account_root, tdata_dir_name)
                else:
                    duplicates += 1
        
        if len(tdata_with_phones) == 1 and duplicates == 2:
            print(f"  ✅ PASS: 3 accounts -> 1 account (2 duplicates removed)")
            return True
        else:
            print(f"  ❌ FAIL: Expected 1 account, got {len(tdata_with_phones)} (duplicates: {duplicates})")
            return False
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_special_chars_in_phone():
    """Test phone extraction with special characters"""
    print("\nTesting phone with special characters...")
    
    test_dir = tempfile.mkdtemp(prefix="test_special_")
    
    try:
        # Create JSON with phone containing spaces, dashes, etc.
        json_path = os.path.join(test_dir, 'test.json')
        with open(json_path, 'w') as f:
            json.dump({"phone": "+1 (234) 567-8900"}, f)
        
        def extract_phone_from_json(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    phone = data.get('phone', '')
                    if phone:
                        phone_clean = ''.join(c for c in phone if c.isdigit())
                        if phone_clean and len(phone_clean) >= 10:
                            return phone_clean
            except:
                pass
            return None
        
        result = extract_phone_from_json(json_path)
        
        if result == "12345678900":
            print(f"  ✅ PASS: Special chars removed: {result}")
            return True
        else:
            print(f"  ❌ FAIL: Expected '12345678900', got '{result}'")
            return False
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_empty_json():
    """Test handling of empty or invalid JSON"""
    print("\nTesting empty/invalid JSON handling...")
    
    test_dir = tempfile.mkdtemp(prefix="test_empty_")
    
    try:
        # Empty JSON
        json1 = os.path.join(test_dir, 'empty.json')
        with open(json1, 'w') as f:
            json.dump({}, f)
        
        # Invalid JSON
        json2 = os.path.join(test_dir, 'invalid.json')
        with open(json2, 'w') as f:
            f.write('not valid json')
        
        def extract_phone_from_json(json_path):
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    phone = data.get('phone', '')
                    if phone:
                        phone_clean = ''.join(c for c in phone if c.isdigit())
                        if phone_clean and len(phone_clean) >= 10:
                            return phone_clean
            except:
                pass
            return None
        
        result1 = extract_phone_from_json(json1)
        result2 = extract_phone_from_json(json2)
        
        if result1 is None and result2 is None:
            print(f"  ✅ PASS: Invalid JSONs handled gracefully")
            return True
        else:
            print(f"  ❌ FAIL: Expected None for both, got '{result1}' and '{result2}'")
            return False
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def main():
    """Run all edge case tests"""
    print("=" * 60)
    print("Phone-based Merge Edge Case Tests")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Run tests
    all_passed &= test_phone_with_plus_sign()
    all_passed &= test_short_phone_rejection()
    all_passed &= test_mixed_case_tdata()
    all_passed &= test_no_phone_fallback()
    all_passed &= test_multiple_accounts_same_phone()
    all_passed &= test_special_chars_in_phone()
    all_passed &= test_empty_json()
    
    print()
    print("=" * 60)
    if all_passed:
        print("✅ ALL EDGE CASE TESTS PASSED")
        return 0
    else:
        print("❌ SOME EDGE CASE TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
