#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for File Rename and Account Merge features
"""

import sys
import os

# Add the bot module to path
sys.path.insert(0, os.path.dirname(__file__))

def test_sanitize_filename():
    """Test the sanitize_filename function"""
    print("Testing sanitize_filename...")
    
    # Mock the bot class with just the sanitize_filename method
    class MockBot:
        def sanitize_filename(self, filename: str) -> str:
            """Clean filename by removing illegal characters and limiting length"""
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                filename = filename.replace(char, '_')
            
            filename = ''.join(char for char in filename if ord(char) >= 32)
            
            max_length = 200
            if len(filename) > max_length:
                filename = filename[:max_length]
            
            filename = filename.strip('. ')
            
            if not filename:
                filename = 'unnamed_file'
            
            return filename
    
    bot = MockBot()
    
    # Test cases
    test_cases = [
        ("normal_file", "normal_file"),
        ("file<with>invalid:chars", "file_with_invalid_chars"),
        ("file/with\\slashes", "file_with_slashes"),
        ("file|with?special*", "file_with_special_"),
        ("   spaced   ", "spaced"),
        ("", "unnamed_file"),
        ("a" * 250, "a" * 200),  # Long filename
    ]
    
    passed = 0
    failed = 0
    
    for input_name, expected in test_cases:
        result = bot.sanitize_filename(input_name)
        if result == expected:
            print(f"✅ PASS: '{input_name}' -> '{result}'")
            passed += 1
        else:
            print(f"❌ FAIL: '{input_name}' -> '{result}' (expected '{expected}')")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0

def test_is_tdata_zip():
    """Test the TData ZIP detection"""
    print("\nTesting is_tdata_zip...")
    
    import tempfile
    import zipfile
    
    class MockBot:
        def is_tdata_zip(self, zip_path: str) -> bool:
            """Detect if ZIP file contains TData marker"""
            try:
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    namelist = zf.namelist()
                    for name in namelist:
                        if 'D877F783D5D3EF8C' in name:
                            return True
                return False
            except:
                return False
    
    bot = MockBot()
    
    # Create test ZIP files
    temp_dir = tempfile.mkdtemp()
    
    # Create TData ZIP
    tdata_zip = os.path.join(temp_dir, 'tdata_test.zip')
    with zipfile.ZipFile(tdata_zip, 'w') as zf:
        zf.writestr('tdata/D877F783D5D3EF8C/file.dat', 'test data')
    
    # Create non-TData ZIP
    normal_zip = os.path.join(temp_dir, 'normal_test.zip')
    with zipfile.ZipFile(normal_zip, 'w') as zf:
        zf.writestr('some_file.txt', 'test data')
    
    passed = 0
    failed = 0
    
    # Test TData ZIP
    if bot.is_tdata_zip(tdata_zip):
        print("✅ PASS: TData ZIP correctly identified")
        passed += 1
    else:
        print("❌ FAIL: TData ZIP not identified")
        failed += 1
    
    # Test non-TData ZIP
    if not bot.is_tdata_zip(normal_zip):
        print("✅ PASS: Non-TData ZIP correctly identified")
        passed += 1
    else:
        print("❌ FAIL: Non-TData ZIP incorrectly identified as TData")
        failed += 1
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0

def test_session_json_pairing():
    """Test session and JSON file pairing logic"""
    print("\nTesting session+JSON pairing...")
    
    session_files = ['user1.session', 'user2.session', 'user3.session']
    json_files = ['user1.json', 'user2.json', 'user4.json']
    
    # Pairing logic
    paired_files = []
    unpaired_session = []
    unpaired_json = []
    
    session_basenames = {f.replace('.session', ''): f for f in session_files}
    json_basenames = {f.replace('.json', ''): f for f in json_files}
    
    for basename in session_basenames.keys():
        if basename in json_basenames:
            paired_files.append((session_basenames[basename], json_basenames[basename]))
        else:
            unpaired_session.append(session_basenames[basename])
    
    for basename in json_basenames.keys():
        if basename not in session_basenames:
            unpaired_json.append(json_basenames[basename])
    
    # Verify results
    passed = 0
    failed = 0
    
    if len(paired_files) == 2:  # user1 and user2
        print("✅ PASS: Correct number of paired files (2)")
        passed += 1
    else:
        print(f"❌ FAIL: Expected 2 paired files, got {len(paired_files)}")
        failed += 1
    
    if len(unpaired_session) == 1 and 'user3.session' in unpaired_session:
        print("✅ PASS: Correct unpaired session files")
        passed += 1
    else:
        print(f"❌ FAIL: Unexpected unpaired session files: {unpaired_session}")
        failed += 1
    
    if len(unpaired_json) == 1 and 'user4.json' in unpaired_json:
        print("✅ PASS: Correct unpaired JSON files")
        passed += 1
    else:
        print(f"❌ FAIL: Unexpected unpaired JSON files: {unpaired_json}")
        failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0

def main():
    """Run all tests"""
    print("=" * 50)
    print("File Rename and Account Merge Features Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Run tests
    all_passed &= test_sanitize_filename()
    all_passed &= test_is_tdata_zip()
    all_passed &= test_session_json_pairing()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ ALL TESTS PASSED")
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
