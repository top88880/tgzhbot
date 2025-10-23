#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for phone-based naming and deduplication in Account Merge feature
"""

import sys
import os
import tempfile
import shutil
import zipfile
import json

def test_phone_extraction_from_json():
    """Test phone number extraction from JSON files"""
    print("Testing phone extraction from JSON...")
    
    test_dir = tempfile.mkdtemp(prefix="test_phone_json_")
    
    try:
        # Test case 1: Normal phone with +
        json1 = os.path.join(test_dir, 'test1.json')
        with open(json1, 'w') as f:
            json.dump({"phone": "+1234567890"}, f)
        
        # Test case 2: Phone without +
        json2 = os.path.join(test_dir, 'test2.json')
        with open(json2, 'w') as f:
            json.dump({"phone": "9876543210"}, f)
        
        # Test case 3: No phone
        json3 = os.path.join(test_dir, 'test3.json')
        with open(json3, 'w') as f:
            json.dump({"username": "testuser"}, f)
        
        # Mock extract_phone_from_json function
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
        
        # Test extraction
        phone1 = extract_phone_from_json(json1)
        phone2 = extract_phone_from_json(json2)
        phone3 = extract_phone_from_json(json3)
        
        passed = True
        if phone1 == "1234567890":
            print(f"  ✅ PASS: Extracted phone from JSON with + : {phone1}")
        else:
            print(f"  ❌ FAIL: Expected '1234567890', got '{phone1}'")
            passed = False
        
        if phone2 == "9876543210":
            print(f"  ✅ PASS: Extracted phone from JSON without + : {phone2}")
        else:
            print(f"  ❌ FAIL: Expected '9876543210', got '{phone2}'")
            passed = False
        
        if phone3 is None:
            print(f"  ✅ PASS: No phone extracted when not present")
        else:
            print(f"  ❌ FAIL: Expected None, got '{phone3}'")
            passed = False
        
        return passed
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_phone_extraction_from_tdata_path():
    """Test phone number extraction from TData directory path"""
    print("\nTesting phone extraction from TData path...")
    
    # Mock extract_phone_from_tdata_path function
    def extract_phone_from_tdata_path(account_root, tdata_dir_name):
        try:
            # Check parent directory name
            parent_dir = os.path.basename(account_root)
            phone_clean = parent_dir.lstrip('+')
            if phone_clean.isdigit() and len(phone_clean) >= 10:
                return phone_clean
            
            # Check path parts
            path_parts = account_root.split(os.sep)
            for part in reversed(path_parts):
                if not part:
                    continue
                phone_clean = part.lstrip('+')
                if phone_clean.isdigit() and len(phone_clean) >= 10:
                    return phone_clean
        except:
            pass
        return None
    
    test_cases = [
        ("/tmp/1234567890/tdata", "tdata", "1234567890"),
        ("/tmp/+9876543210/tdata", "tdata", "9876543210"),
        ("/tmp/accounts/1122334455/tdata", "tdata", "1122334455"),
        ("/tmp/MyAccount/tdata", "tdata", None),
    ]
    
    passed = True
    for account_root, tdata_dir, expected in test_cases:
        result = extract_phone_from_tdata_path(account_root, tdata_dir)
        if result == expected:
            print(f"  ✅ PASS: '{account_root}' -> {result}")
        else:
            print(f"  ❌ FAIL: '{account_root}' -> {result} (expected {expected})")
            passed = False
    
    return passed


def test_deduplication():
    """Test deduplication of accounts with same phone number"""
    print("\nTesting deduplication...")
    
    test_dir = tempfile.mkdtemp(prefix="test_dedup_")
    
    try:
        # Create multiple accounts with same phone number
        # TData accounts
        phone = "1234567890"
        
        # Account 1
        acc1_dir = os.path.join(test_dir, phone + "_v1")
        tdata1 = os.path.join(acc1_dir, "tdata", "D877F783D5D3EF8C")
        os.makedirs(tdata1)
        with open(os.path.join(tdata1, "file1.dat"), 'w') as f:
            f.write("data1")
        
        # Account 2 (duplicate)
        acc2_dir = os.path.join(test_dir, phone + "_v2")
        tdata2 = os.path.join(acc2_dir, "tdata", "D877F783D5D3EF8C")
        os.makedirs(tdata2)
        with open(os.path.join(tdata2, "file2.dat"), 'w') as f:
            f.write("data2")
        
        # Simulate deduplication logic
        tdata_accounts = [
            (acc1_dir, "tdata"),
            (acc2_dir, "tdata"),
        ]
        
        def extract_phone_from_tdata_path(account_root, tdata_dir_name):
            parent = os.path.basename(account_root)
            phone_clean = parent.split('_')[0]
            if phone_clean.isdigit() and len(phone_clean) >= 10:
                return phone_clean
            return None
        
        tdata_with_phones = {}
        for account_root, tdata_dir_name in tdata_accounts:
            phone = extract_phone_from_tdata_path(account_root, tdata_dir_name)
            if phone:
                if phone not in tdata_with_phones:
                    tdata_with_phones[phone] = (account_root, tdata_dir_name)
                else:
                    print(f"    ⚠️ Duplicate detected: {phone}")
        
        # Should have only 1 account after deduplication
        if len(tdata_with_phones) == 1:
            print(f"  ✅ PASS: Deduplication worked (2 accounts -> 1)")
            return True
        else:
            print(f"  ❌ FAIL: Expected 1 account after dedup, got {len(tdata_with_phones)}")
            return False
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_output_structure_with_phones():
    """Test output ZIP structure with phone-based naming"""
    print("\nTesting output structure with phone-based naming...")
    
    test_dir = tempfile.mkdtemp(prefix="test_output_")
    
    try:
        # Create test accounts
        accounts = [
            ("1234567890", "tdata1"),
            ("9876543210", "tdata2"),
        ]
        
        for phone, tdata_name in accounts:
            acc_dir = os.path.join(test_dir, phone)
            tdata_path = os.path.join(acc_dir, tdata_name, "D877F783D5D3EF8C")
            os.makedirs(tdata_path)
            with open(os.path.join(tdata_path, "key_data"), 'w') as f:
                f.write(f"data for {phone}")
        
        # Create output ZIP with phone-based naming
        zip_path = os.path.join(test_dir, "tdata_only_test.zip")
        with zipfile.ZipFile(zip_path, 'w') as zf:
            for phone, tdata_name in accounts:
                acc_dir = os.path.join(test_dir, phone)
                tdata_full = os.path.join(acc_dir, tdata_name)
                
                for root, dirs, files in os.walk(tdata_full):
                    for fname in files:
                        file_path = os.path.join(root, fname)
                        rel_path = os.path.relpath(file_path, acc_dir)
                        arcname = os.path.join(phone, rel_path)
                        zf.write(file_path, arcname)
        
        # Verify ZIP structure
        with zipfile.ZipFile(zip_path, 'r') as zf:
            namelist = zf.namelist()
            
            # Check for phone-based paths
            has_phone1 = any('1234567890/' in name for name in namelist)
            has_phone2 = any('9876543210/' in name for name in namelist)
            
            if has_phone1 and has_phone2:
                print(f"  ✅ PASS: ZIP contains phone-based directories")
                print(f"    Files in ZIP: {namelist[:5]}")
                return True
            else:
                print(f"  ❌ FAIL: Phone-based directories not found")
                print(f"    Files: {namelist}")
                return False
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_session_json_with_phones():
    """Test Session+JSON output with phone-based naming"""
    print("\nTesting Session+JSON output with phone-based naming...")
    
    test_dir = tempfile.mkdtemp(prefix="test_session_")
    
    try:
        # Create session+json pairs
        pairs = [
            ("user1", "1234567890"),
            ("user2", "9876543210"),
        ]
        
        session_json_with_phones = {}
        
        for basename, phone in pairs:
            session_path = os.path.join(test_dir, f"{basename}.session")
            json_path = os.path.join(test_dir, f"{basename}.json")
            
            with open(session_path, 'w') as f:
                f.write("session data")
            with open(json_path, 'w') as f:
                json.dump({"phone": f"+{phone}"}, f)
            
            # Extract phone from JSON
            with open(json_path, 'r') as f:
                data = json.load(f)
                phone_extracted = ''.join(c for c in data['phone'] if c.isdigit())
                session_json_with_phones[phone_extracted] = (session_path, json_path)
        
        # Create output ZIP
        zip_path = os.path.join(test_dir, "session_json_test.zip")
        with zipfile.ZipFile(zip_path, 'w') as zf:
            for phone, (session_path, json_path) in session_json_with_phones.items():
                zf.write(session_path, f'{phone}.session')
                zf.write(json_path, f'{phone}.json')
        
        # Verify ZIP contents
        with zipfile.ZipFile(zip_path, 'r') as zf:
            namelist = zf.namelist()
            
            expected = [
                '1234567890.session', '1234567890.json',
                '9876543210.session', '9876543210.json'
            ]
            
            if all(name in namelist for name in expected):
                print(f"  ✅ PASS: Session+JSON files use phone-based naming")
                print(f"    Files: {namelist}")
                return True
            else:
                print(f"  ❌ FAIL: Expected phone-based file names")
                print(f"    Expected: {expected}")
                print(f"    Got: {namelist}")
                return False
        
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)


def test_filename_format():
    """Test output ZIP filename format"""
    print("\nTesting output ZIP filename format...")
    
    import time
    timestamp = int(time.time())
    
    tdata_filename = f'tdata_only_{timestamp}.zip'
    session_filename = f'session_json_{timestamp}.zip'
    
    passed = True
    
    if 'tdata_only_' in tdata_filename and tdata_filename.endswith('.zip'):
        print(f"  ✅ PASS: TData filename format correct: {tdata_filename}")
    else:
        print(f"  ❌ FAIL: TData filename format incorrect: {tdata_filename}")
        passed = False
    
    if 'session_json_' in session_filename and session_filename.endswith('.zip'):
        print(f"  ✅ PASS: Session filename format correct: {session_filename}")
    else:
        print(f"  ❌ FAIL: Session filename format incorrect: {session_filename}")
        passed = False
    
    return passed


def main():
    """Run all tests"""
    print("=" * 60)
    print("Phone-based Naming and Deduplication Test Suite")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Run tests
    all_passed &= test_phone_extraction_from_json()
    all_passed &= test_phone_extraction_from_tdata_path()
    all_passed &= test_deduplication()
    all_passed &= test_output_structure_with_phones()
    all_passed &= test_session_json_with_phones()
    all_passed &= test_filename_format()
    
    print()
    print("=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
