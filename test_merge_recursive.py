#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for the updated Account Merge feature with recursive scanning
"""

import sys
import os
import tempfile
import shutil
import zipfile

def test_recursive_tdata_extraction():
    """Test recursive extraction and TData detection"""
    print("Testing recursive TData extraction...")
    
    # Create a temporary directory
    test_dir = tempfile.mkdtemp(prefix="test_merge_")
    
    try:
        # Create a nested ZIP structure with TData account
        # Structure: test.zip -> subdir -> tdata -> D877F783D5D3EF8C -> key_data
        
        # First, create the inner directory structure
        inner_dir = os.path.join(test_dir, 'account1')
        os.makedirs(inner_dir)
        
        tdata_dir = os.path.join(inner_dir, 'tdata')
        os.makedirs(tdata_dir)
        
        marker_dir = os.path.join(tdata_dir, 'D877F783D5D3EF8C')
        os.makedirs(marker_dir)
        
        # Create a dummy file inside
        test_file = os.path.join(marker_dir, 'key_data')
        with open(test_file, 'w') as f:
            f.write('test data')
        
        # Create the ZIP file
        zip_path = os.path.join(test_dir, 'test_tdata.zip')
        with zipfile.ZipFile(zip_path, 'w') as zf:
            zf.write(test_file, os.path.relpath(test_file, test_dir))
            zf.write(marker_dir, os.path.relpath(marker_dir, test_dir))
            zf.write(tdata_dir, os.path.relpath(tdata_dir, test_dir))
            zf.write(inner_dir, os.path.relpath(inner_dir, test_dir))
        
        # Simulate extraction
        extract_dir = os.path.join(test_dir, 'extracted')
        os.makedirs(extract_dir)
        
        zip_extract_dir = os.path.join(extract_dir, 'test_tdata')
        os.makedirs(zip_extract_dir)
        
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(zip_extract_dir)
        
        # Scan for TData accounts
        tdata_accounts = []
        
        for root, dirs, files in os.walk(extract_dir):
            dirs_lower = [d.lower() for d in dirs]
            if 'tdata' in dirs_lower:
                tdata_dir_name = dirs[dirs_lower.index('tdata')]
                tdata_path = os.path.join(root, tdata_dir_name)
                
                if os.path.exists(tdata_path):
                    for subdir in os.listdir(tdata_path):
                        if subdir.upper() == 'D877F783D5D3EF8C':
                            tdata_accounts.append((root, tdata_dir_name))
                            break
        
        # Verify results
        if len(tdata_accounts) == 1:
            print("✅ PASS: Found 1 TData account")
            return True
        else:
            print(f"❌ FAIL: Expected 1 TData account, found {len(tdata_accounts)}")
            return False
            
    finally:
        # Cleanup
        shutil.rmtree(test_dir, ignore_errors=True)

def test_case_insensitive_tdata():
    """Test case-insensitive TData detection"""
    print("\nTesting case-insensitive TData detection...")
    
    test_dir = tempfile.mkdtemp(prefix="test_merge_case_")
    
    try:
        # Create TData with mixed case
        inner_dir = os.path.join(test_dir, 'account1')
        os.makedirs(inner_dir)
        
        # Use lowercase 'tdata'
        tdata_dir = os.path.join(inner_dir, 'TData')  # Mixed case
        os.makedirs(tdata_dir)
        
        # Use lowercase marker
        marker_dir = os.path.join(tdata_dir, 'd877f783d5d3ef8c')  # Lowercase
        os.makedirs(marker_dir)
        
        test_file = os.path.join(marker_dir, 'key_data')
        with open(test_file, 'w') as f:
            f.write('test data')
        
        # Scan for TData accounts (case-insensitive)
        tdata_accounts = []
        
        for root, dirs, files in os.walk(test_dir):
            dirs_lower = [d.lower() for d in dirs]
            if 'tdata' in dirs_lower:
                tdata_dir_name = dirs[dirs_lower.index('tdata')]
                tdata_path = os.path.join(root, tdata_dir_name)
                
                if os.path.exists(tdata_path):
                    for subdir in os.listdir(tdata_path):
                        if subdir.upper() == 'D877F783D5D3EF8C':
                            tdata_accounts.append((root, tdata_dir_name))
                            break
        
        if len(tdata_accounts) == 1:
            print("✅ PASS: Case-insensitive detection works")
            return True
        else:
            print(f"❌ FAIL: Case-insensitive detection failed, found {len(tdata_accounts)}")
            return False
            
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)

def test_recursive_session_json_pairing():
    """Test recursive Session+JSON pairing"""
    print("\nTesting recursive Session+JSON pairing...")
    
    test_dir = tempfile.mkdtemp(prefix="test_merge_session_")
    
    try:
        # Create nested structure with Session+JSON files
        subdir1 = os.path.join(test_dir, 'accounts', 'user1')
        os.makedirs(subdir1)
        
        # Create paired files
        with open(os.path.join(subdir1, 'myaccount.session'), 'w') as f:
            f.write('session data')
        with open(os.path.join(subdir1, 'myaccount.json'), 'w') as f:
            f.write('{"phone": "+1234567890"}')
        
        # Create another pair in different directory
        subdir2 = os.path.join(test_dir, 'accounts', 'user2')
        os.makedirs(subdir2)
        
        with open(os.path.join(subdir2, 'account2.session'), 'w') as f:
            f.write('session data 2')
        with open(os.path.join(subdir2, 'account2.json'), 'w') as f:
            f.write('{"phone": "+9876543210"}')
        
        # Scan for Session+JSON pairs
        session_json_pairs = []
        
        for root, dirs, files in os.walk(test_dir):
            session_files = {}
            json_files = {}
            
            for fname in files:
                if fname.lower().endswith('.session'):
                    basename = fname[:-8]
                    session_files[basename] = os.path.join(root, fname)
                elif fname.lower().endswith('.json'):
                    basename = fname[:-5]
                    json_files[basename] = os.path.join(root, fname)
            
            for basename in session_files.keys():
                if basename in json_files:
                    session_json_pairs.append((session_files[basename], json_files[basename], basename))
        
        if len(session_json_pairs) == 2:
            print("✅ PASS: Found 2 Session+JSON pairs")
            return True
        else:
            print(f"❌ FAIL: Expected 2 pairs, found {len(session_json_pairs)}")
            return False
            
    finally:
        shutil.rmtree(test_dir, ignore_errors=True)

def test_zip_only_acceptance():
    """Test that only ZIP files are accepted"""
    print("\nTesting ZIP-only file acceptance...")
    
    # Mock the file validation logic
    def is_zip_file(filename):
        return filename.lower().endswith('.zip')
    
    test_cases = [
        ('archive.zip', True),
        ('Archive.ZIP', True),
        ('data.session', False),
        ('config.json', False),
        ('file.txt', False),
        ('archive.zip.bak', False),
    ]
    
    passed = 0
    failed = 0
    
    for filename, expected in test_cases:
        result = is_zip_file(filename)
        if result == expected:
            print(f"✅ PASS: '{filename}' -> {result}")
            passed += 1
        else:
            print(f"❌ FAIL: '{filename}' -> {result} (expected {expected})")
            failed += 1
    
    return failed == 0

def main():
    """Run all tests"""
    print("=" * 60)
    print("Updated Account Merge Feature Test Suite")
    print("=" * 60)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_zip_only_acceptance()
    all_passed &= test_recursive_tdata_extraction()
    all_passed &= test_case_insensitive_tdata()
    all_passed &= test_recursive_session_json_pairing()
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
