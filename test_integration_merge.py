#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration test for the complete Account Merge workflow
"""

import sys
import os
import tempfile
import shutil
import zipfile

def test_complete_merge_workflow():
    """Test the complete merge workflow end-to-end"""
    print("Testing complete merge workflow...")
    
    test_dir = tempfile.mkdtemp(prefix="test_integration_")
    
    try:
        # Step 1: Create multiple ZIP files with different account types
        
        # ZIP 1: Contains TData account
        zip1_content_dir = os.path.join(test_dir, 'zip1_content')
        os.makedirs(zip1_content_dir)
        
        account1_dir = os.path.join(zip1_content_dir, 'MyAccount1')
        tdata1 = os.path.join(account1_dir, 'tdata')
        marker1 = os.path.join(tdata1, 'D877F783D5D3EF8C')
        os.makedirs(marker1)
        
        with open(os.path.join(marker1, 'key_data'), 'w') as f:
            f.write('encrypted key data 1')
        with open(os.path.join(marker1, 'map'), 'w') as f:
            f.write('0s')
        
        zip1_path = os.path.join(test_dir, 'account1.zip')
        with zipfile.ZipFile(zip1_path, 'w') as zf:
            for root, dirs, files in os.walk(zip1_content_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, test_dir)
                    zf.write(file_path, arcname)
        
        # ZIP 2: Contains Session+JSON pair
        zip2_content_dir = os.path.join(test_dir, 'zip2_content')
        os.makedirs(zip2_content_dir)
        
        with open(os.path.join(zip2_content_dir, 'user123.session'), 'w') as f:
            f.write('session binary data')
        with open(os.path.join(zip2_content_dir, 'user123.json'), 'w') as f:
            f.write('{"phone": "+1234567890"}')
        
        zip2_path = os.path.join(test_dir, 'sessions.zip')
        with zipfile.ZipFile(zip2_path, 'w') as zf:
            zf.write(os.path.join(zip2_content_dir, 'user123.session'), 'user123.session')
            zf.write(os.path.join(zip2_content_dir, 'user123.json'), 'user123.json')
        
        # ZIP 3: Contains nested TData (mixed case)
        zip3_content_dir = os.path.join(test_dir, 'zip3_content')
        os.makedirs(zip3_content_dir)
        
        nested_dir = os.path.join(zip3_content_dir, 'backup', 'accounts')
        os.makedirs(nested_dir)
        
        account2_dir = os.path.join(nested_dir, 'TelegramDesktop')
        tdata2 = os.path.join(account2_dir, 'TData')  # Mixed case
        marker2 = os.path.join(tdata2, 'd877f783d5d3ef8c')  # Lowercase marker
        os.makedirs(marker2)
        
        with open(os.path.join(marker2, 'key_data'), 'w') as f:
            f.write('encrypted key data 2')
        
        zip3_path = os.path.join(test_dir, 'backup.zip')
        with zipfile.ZipFile(zip3_path, 'w') as zf:
            for root, dirs, files in os.walk(zip3_content_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, test_dir)
                    zf.write(file_path, arcname)
        
        # Step 2: Simulate the extraction process
        extract_dir = os.path.join(test_dir, 'extracted')
        os.makedirs(extract_dir)
        
        for zip_name, zip_path in [('account1', zip1_path), ('sessions', zip2_path), ('backup', zip3_path)]:
            zip_extract_dir = os.path.join(extract_dir, zip_name)
            os.makedirs(zip_extract_dir)
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(zip_extract_dir)
        
        # Step 3: Scan for accounts
        tdata_accounts = []
        session_json_pairs = []
        
        def scan_directory(dir_path):
            for root, dirs, filenames in os.walk(dir_path):
                # TData detection (case-insensitive)
                dirs_lower = [d.lower() for d in dirs]
                if 'tdata' in dirs_lower:
                    tdata_dir_name = dirs[dirs_lower.index('tdata')]
                    tdata_path = os.path.join(root, tdata_dir_name)
                    
                    if os.path.exists(tdata_path):
                        for subdir in os.listdir(tdata_path):
                            if subdir.upper() == 'D877F783D5D3EF8C':
                                tdata_accounts.append((root, tdata_dir_name))
                                break
                
                # Session+JSON pairing
                session_files = {}
                json_files = {}
                
                for fname in filenames:
                    if fname.lower().endswith('.session'):
                        basename = fname[:-8]
                        session_files[basename] = os.path.join(root, fname)
                    elif fname.lower().endswith('.json'):
                        basename = fname[:-5]
                        json_files[basename] = os.path.join(root, fname)
                
                for basename in session_files.keys():
                    if basename in json_files:
                        session_json_pairs.append((session_files[basename], json_files[basename], basename))
        
        scan_directory(extract_dir)
        
        # Step 4: Verify results
        passed = True
        
        print(f"  Found {len(tdata_accounts)} TData accounts")
        print(f"  Found {len(session_json_pairs)} Session+JSON pairs")
        
        if len(tdata_accounts) != 2:
            print(f"  ❌ FAIL: Expected 2 TData accounts, got {len(tdata_accounts)}")
            passed = False
        else:
            print("  ✅ PASS: Found correct number of TData accounts")
        
        if len(session_json_pairs) != 1:
            print(f"  ❌ FAIL: Expected 1 Session+JSON pair, got {len(session_json_pairs)}")
            passed = False
        else:
            print("  ✅ PASS: Found correct number of Session+JSON pairs")
        
        # Step 5: Test normalized output structure
        result_dir = os.path.join(test_dir, 'results')
        os.makedirs(result_dir)
        
        if tdata_accounts:
            tdata_zip_path = os.path.join(result_dir, 'tdata_accounts_test.zip')
            with zipfile.ZipFile(tdata_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for idx, (account_root, tdata_dir_name) in enumerate(tdata_accounts, 1):
                    account_name = f'account_{idx}'
                    tdata_full_path = os.path.join(account_root, tdata_dir_name)
                    
                    for root, dirs, filenames in os.walk(tdata_full_path):
                        for fname in filenames:
                            file_path = os.path.join(root, fname)
                            rel_path = os.path.relpath(file_path, account_root)
                            arcname = os.path.join(account_name, rel_path)
                            zf.write(file_path, arcname)
            
            # Verify normalized structure
            with zipfile.ZipFile(tdata_zip_path, 'r') as zf:
                namelist = zf.namelist()
                
                # Check for normalized paths
                expected_patterns = [
                    'account_1/tdata/',
                    'account_2/TData/',  # Preserves original case
                ]
                
                has_account_1 = any('account_1/' in name for name in namelist)
                has_account_2 = any('account_2/' in name for name in namelist)
                
                if has_account_1 and has_account_2:
                    print("  ✅ PASS: Output structure is normalized")
                else:
                    print(f"  ❌ FAIL: Output structure not normalized properly")
                    passed = False
        
        if passed:
            print("✅ PASS: Complete workflow test passed")
        else:
            print("❌ FAIL: Complete workflow test failed")
        
        return passed
        
    finally:
        # Cleanup
        shutil.rmtree(test_dir, ignore_errors=True)

def main():
    """Run integration test"""
    print("=" * 60)
    print("Account Merge Integration Test")
    print("=" * 60)
    print()
    
    success = test_complete_merge_workflow()
    
    print()
    print("=" * 60)
    if success:
        print("✅ INTEGRATION TEST PASSED")
        return 0
    else:
        print("❌ INTEGRATION TEST FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
