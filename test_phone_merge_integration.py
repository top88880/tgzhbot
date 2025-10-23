#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integration test for phone-based Account Merge feature
Tests the complete workflow with phone extraction and deduplication
"""

import sys
import os
import tempfile
import shutil
import zipfile
import json

def test_complete_phone_merge():
    """Test complete merge workflow with phone-based naming and deduplication"""
    print("Testing complete phone-based merge workflow...")
    
    test_dir = tempfile.mkdtemp(prefix="test_phone_merge_")
    
    try:
        # ==============================================================
        # Step 1: Create test data with various scenarios
        # ==============================================================
        
        # Scenario 1: TData account with phone number in path
        zip1_dir = os.path.join(test_dir, 'zip1_content')
        phone1 = "1234567890"
        acc1_path = os.path.join(zip1_dir, phone1)
        tdata1 = os.path.join(acc1_path, 'tdata', 'D877F783D5D3EF8C')
        os.makedirs(tdata1)
        with open(os.path.join(tdata1, 'key_data'), 'w') as f:
            f.write('encrypted data for account 1')
        
        zip1_path = os.path.join(test_dir, 'accounts1.zip')
        with zipfile.ZipFile(zip1_path, 'w') as zf:
            for root, dirs, files in os.walk(zip1_dir):
                for fname in files:
                    file_path = os.path.join(root, fname)
                    arcname = os.path.relpath(file_path, test_dir)
                    zf.write(file_path, arcname)
        
        # Scenario 2: Duplicate TData account with same phone (should be deduplicated)
        zip2_dir = os.path.join(test_dir, 'zip2_content')
        acc2_path = os.path.join(zip2_dir, phone1)  # Same phone!
        tdata2 = os.path.join(acc2_path, 'tdata', 'D877F783D5D3EF8C')
        os.makedirs(tdata2)
        with open(os.path.join(tdata2, 'key_data'), 'w') as f:
            f.write('duplicate data for account 1')
        
        zip2_path = os.path.join(test_dir, 'accounts2.zip')
        with zipfile.ZipFile(zip2_path, 'w') as zf:
            for root, dirs, files in os.walk(zip2_dir):
                for fname in files:
                    file_path = os.path.join(root, fname)
                    arcname = os.path.relpath(file_path, test_dir)
                    zf.write(file_path, arcname)
        
        # Scenario 3: TData account with different phone
        zip3_dir = os.path.join(test_dir, 'zip3_content')
        phone2 = "9876543210"
        acc3_path = os.path.join(zip3_dir, phone2)
        tdata3 = os.path.join(acc3_path, 'tdata', 'D877F783D5D3EF8C')
        os.makedirs(tdata3)
        with open(os.path.join(tdata3, 'key_data'), 'w') as f:
            f.write('encrypted data for account 2')
        
        zip3_path = os.path.join(test_dir, 'accounts3.zip')
        with zipfile.ZipFile(zip3_path, 'w') as zf:
            for root, dirs, files in os.walk(zip3_dir):
                for fname in files:
                    file_path = os.path.join(root, fname)
                    arcname = os.path.relpath(file_path, test_dir)
                    zf.write(file_path, arcname)
        
        # Scenario 4: Session+JSON with phone in JSON
        zip4_dir = os.path.join(test_dir, 'zip4_content')
        os.makedirs(zip4_dir)
        
        phone3 = "5551234567"
        with open(os.path.join(zip4_dir, 'user1.session'), 'w') as f:
            f.write('session binary data')
        with open(os.path.join(zip4_dir, 'user1.json'), 'w') as f:
            json.dump({"phone": f"+{phone3}"}, f)
        
        zip4_path = os.path.join(test_dir, 'sessions1.zip')
        with zipfile.ZipFile(zip4_path, 'w') as zf:
            zf.write(os.path.join(zip4_dir, 'user1.session'), 'user1.session')
            zf.write(os.path.join(zip4_dir, 'user1.json'), 'user1.json')
        
        # Scenario 5: Duplicate Session+JSON (should be deduplicated)
        zip5_dir = os.path.join(test_dir, 'zip5_content')
        os.makedirs(zip5_dir)
        
        with open(os.path.join(zip5_dir, 'user2.session'), 'w') as f:
            f.write('duplicate session data')
        with open(os.path.join(zip5_dir, 'user2.json'), 'w') as f:
            json.dump({"phone": f"+{phone3}"}, f)  # Same phone!
        
        zip5_path = os.path.join(test_dir, 'sessions2.zip')
        with zipfile.ZipFile(zip5_path, 'w') as zf:
            zf.write(os.path.join(zip5_dir, 'user2.session'), 'user2.session')
            zf.write(os.path.join(zip5_dir, 'user2.json'), 'user2.json')
        
        # Scenario 6: Session+JSON with different phone
        zip6_dir = os.path.join(test_dir, 'zip6_content')
        os.makedirs(zip6_dir)
        
        phone4 = "5559876543"
        with open(os.path.join(zip6_dir, 'user3.session'), 'w') as f:
            f.write('session data 3')
        with open(os.path.join(zip6_dir, 'user3.json'), 'w') as f:
            json.dump({"phone": f"+{phone4}"}, f)
        
        zip6_path = os.path.join(test_dir, 'sessions3.zip')
        with zipfile.ZipFile(zip6_path, 'w') as zf:
            zf.write(os.path.join(zip6_dir, 'user3.session'), 'user3.session')
            zf.write(os.path.join(zip6_dir, 'user3.json'), 'user3.json')
        
        # ==============================================================
        # Step 2: Simulate merge process
        # ==============================================================
        
        files = ['accounts1.zip', 'accounts2.zip', 'accounts3.zip', 
                 'sessions1.zip', 'sessions2.zip', 'sessions3.zip']
        
        extract_dir = os.path.join(test_dir, 'extracted')
        os.makedirs(extract_dir)
        
        # Extract all ZIPs
        for filename in files:
            zip_path = os.path.join(test_dir, filename)
            zip_extract_dir = os.path.join(extract_dir, filename.replace('.zip', ''))
            os.makedirs(zip_extract_dir)
            
            with zipfile.ZipFile(zip_path, 'r') as zf:
                zf.extractall(zip_extract_dir)
        
        # Scan for accounts
        tdata_accounts = []
        session_json_pairs = []
        
        def scan_directory(dir_path):
            for root, dirs, filenames in os.walk(dir_path):
                # TData detection
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
        
        print(f"  Found {len(tdata_accounts)} TData accounts (before dedup)")
        print(f"  Found {len(session_json_pairs)} Session+JSON pairs (before dedup)")
        
        # Extract phone numbers and deduplicate
        def extract_phone_from_tdata_path(account_root, tdata_dir_name):
            parent_dir = os.path.basename(account_root)
            phone_clean = parent_dir.lstrip('+')
            if phone_clean.isdigit() and len(phone_clean) >= 10:
                return phone_clean
            return None
        
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
        
        # Deduplicate TData accounts
        tdata_with_phones = {}
        tdata_without_phones = []
        
        for account_root, tdata_dir_name in tdata_accounts:
            phone = extract_phone_from_tdata_path(account_root, tdata_dir_name)
            if phone:
                if phone not in tdata_with_phones:
                    tdata_with_phones[phone] = (account_root, tdata_dir_name)
                else:
                    print(f"    ⚠️ Duplicate TData: {phone}")
            else:
                tdata_without_phones.append((account_root, tdata_dir_name))
        
        # Deduplicate Session+JSON pairs
        session_json_with_phones = {}
        
        for session_path, json_path, basename in session_json_pairs:
            phone = extract_phone_from_json(json_path)
            if phone:
                if phone not in session_json_with_phones:
                    session_json_with_phones[phone] = (session_path, json_path)
                else:
                    print(f"    ⚠️ Duplicate Session+JSON: {phone}")
            else:
                if basename not in session_json_with_phones:
                    session_json_with_phones[basename] = (session_path, json_path)
        
        total_tdata = len(tdata_with_phones) + len(tdata_without_phones)
        total_session_json = len(session_json_with_phones)
        
        print(f"  After dedup: {total_tdata} TData accounts")
        print(f"  After dedup: {total_session_json} Session+JSON pairs")
        
        # ==============================================================
        # Step 3: Create output archives
        # ==============================================================
        
        result_dir = os.path.join(test_dir, 'results')
        os.makedirs(result_dir)
        
        import time
        timestamp = int(time.time())
        
        # Create TData archive
        tdata_zip_path = os.path.join(result_dir, f'tdata_only_{timestamp}.zip')
        with zipfile.ZipFile(tdata_zip_path, 'w') as zf:
            for phone, (account_root, tdata_dir_name) in tdata_with_phones.items():
                tdata_full_path = os.path.join(account_root, tdata_dir_name)
                
                for root, dirs, filenames in os.walk(tdata_full_path):
                    for fname in filenames:
                        file_path = os.path.join(root, fname)
                        rel_path = os.path.relpath(file_path, account_root)
                        arcname = os.path.join(phone, rel_path)
                        zf.write(file_path, arcname)
        
        # Create Session+JSON archive
        session_json_zip_path = os.path.join(result_dir, f'session_json_{timestamp}.zip')
        with zipfile.ZipFile(session_json_zip_path, 'w') as zf:
            for phone, (session_path, json_path) in session_json_with_phones.items():
                zf.write(session_path, f'{phone}.session')
                zf.write(json_path, f'{phone}.json')
        
        # ==============================================================
        # Step 4: Verify output
        # ==============================================================
        
        passed = True
        
        # Verify TData archive
        print("\n  Verifying TData output archive...")
        with zipfile.ZipFile(tdata_zip_path, 'r') as zf:
            namelist = zf.namelist()
            
            # Should have 2 unique accounts (phone1 and phone2)
            has_phone1 = any(phone1 in name for name in namelist)
            has_phone2 = any(phone2 in name for name in namelist)
            
            if has_phone1 and has_phone2:
                print(f"    ✅ Both unique TData accounts present")
            else:
                print(f"    ❌ Missing TData accounts")
                passed = False
            
            # Should not have 'account_' prefix
            has_account_prefix = any('account_' in name for name in namelist)
            if not has_account_prefix:
                print(f"    ✅ No 'account_' prefix found (all have phone numbers)")
            else:
                print(f"    ⚠️  Warning: Some accounts without phone numbers")
            
            print(f"    TData files: {namelist[:3]}...")
        
        # Verify Session+JSON archive
        print("\n  Verifying Session+JSON output archive...")
        with zipfile.ZipFile(session_json_zip_path, 'r') as zf:
            namelist = zf.namelist()
            
            # Should have 2 unique phone numbers (phone3 and phone4)
            expected_files = [
                f'{phone3}.session', f'{phone3}.json',
                f'{phone4}.session', f'{phone4}.json'
            ]
            
            all_present = all(fname in namelist for fname in expected_files)
            
            if all_present:
                print(f"    ✅ All unique Session+JSON pairs present")
            else:
                print(f"    ❌ Missing Session+JSON files")
                print(f"    Expected: {expected_files}")
                print(f"    Got: {namelist}")
                passed = False
            
            # Should not have original user1, user2, user3 names
            has_original_names = any('user' in name for name in namelist)
            if not has_original_names:
                print(f"    ✅ All files renamed to phone numbers")
            else:
                print(f"    ❌ Original filenames still present")
                passed = False
            
            print(f"    Session+JSON files: {namelist}")
        
        # Verify deduplication
        print("\n  Verifying deduplication...")
        tdata_dupes_removed = len(tdata_accounts) - total_tdata
        session_dupes_removed = len(session_json_pairs) - total_session_json
        
        if tdata_dupes_removed == 1:
            print(f"    ✅ 1 duplicate TData removed")
        else:
            print(f"    ❌ Expected 1 TData duplicate removed, got {tdata_dupes_removed}")
            passed = False
        
        if session_dupes_removed == 1:
            print(f"    ✅ 1 duplicate Session+JSON removed")
        else:
            print(f"    ❌ Expected 1 Session+JSON duplicate removed, got {session_dupes_removed}")
            passed = False
        
        # Verify filenames
        print("\n  Verifying output filenames...")
        tdata_filename = os.path.basename(tdata_zip_path)
        session_filename = os.path.basename(session_json_zip_path)
        
        if 'tdata_only_' in tdata_filename:
            print(f"    ✅ TData filename correct: {tdata_filename}")
        else:
            print(f"    ❌ TData filename incorrect: {tdata_filename}")
            passed = False
        
        if 'session_json_' in session_filename:
            print(f"    ✅ Session+JSON filename correct: {session_filename}")
        else:
            print(f"    ❌ Session+JSON filename incorrect: {session_filename}")
            passed = False
        
        if passed:
            print("\n✅ PASS: Complete phone-based merge workflow test passed")
        else:
            print("\n❌ FAIL: Complete phone-based merge workflow test failed")
        
        return passed
        
    finally:
        # Cleanup
        shutil.rmtree(test_dir, ignore_errors=True)


def main():
    """Run integration test"""
    print("=" * 60)
    print("Phone-based Account Merge Integration Test")
    print("=" * 60)
    print()
    
    success = test_complete_phone_merge()
    
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
