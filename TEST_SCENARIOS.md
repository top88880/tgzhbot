# Test Scenarios for File Rename and Account Merge Features

## File Rename Feature (📝 文件重命名)

### Scenario 1: Basic File Rename
1. Start the bot and click main menu
2. Click "📝 文件重命名" button
3. Upload any file (e.g., document.pdf)
4. Bot should acknowledge receipt and ask for new name
5. Send new filename (without extension): "my_renamed_document"
6. Bot should:
   - Rename the file
   - Send back the renamed file
   - Display success message

**Expected Result**: File is renamed from "document.pdf" to "my_renamed_document.pdf"

### Scenario 2: Special Characters in Filename
1. Click "📝 文件重命名"
2. Upload a file
3. Send filename with special chars: "test<file>name|with:chars"
4. Bot should sanitize it to: "test_file_name_with_chars"

**Expected Result**: All illegal characters are replaced with underscores

### Scenario 3: Empty Filename
1. Click "📝 文件重命名"
2. Upload a file
3. Send empty or whitespace-only text
4. Bot should reject and ask for valid filename

**Expected Result**: Error message displayed

### Scenario 4: File Without Extension
1. Click "📝 文件重命名"
2. Upload a file without extension (e.g., "README")
3. Send new name: "NEW_README"
4. Bot should preserve the lack of extension

**Expected Result**: File renamed to "NEW_README" (no extension)

### Scenario 5: Cancel Operation
1. Click "📝 文件重命名"
2. Click "❌ 取消" button
3. Bot should cancel and return to main menu

**Expected Result**: Task cancelled, temp files cleaned up

## Account Merge Feature (🧩 账户合并)

### Scenario 1: TData ZIP Files Only
1. Click "🧩 账户合并"
2. Upload 3 TData ZIP files (containing D877F783D5D3EF8C directory)
3. Click "✅ 完成合并"
4. Bot should:
   - Identify all as TData
   - Create "tdata_only_[timestamp].zip"
   - Send the packaged file

**Expected Result**: One ZIP file with 3 TData archives

### Scenario 2: Session+JSON Pairs
1. Click "🧩 账户合并"
2. Upload:
   - user1.session
   - user1.json
   - user2.session
   - user2.json
3. Click "✅ 完成合并"
4. Bot should:
   - Pair user1 files
   - Pair user2 files
   - Create "session_json_pairs_[timestamp].zip"

**Expected Result**: One ZIP with 2 paired accounts (4 files total)

### Scenario 3: Mixed Files
1. Click "🧩 账户合并"
2. Upload:
   - 2 TData ZIP files
   - user1.session + user1.json (paired)
   - user2.session (unpaired)
   - user3.json (unpaired)
   - random.zip (not TData)
3. Click "✅ 完成合并"
4. Bot should create 3 ZIPs:
   - tdata_only: 2 TData ZIPs
   - session_json_pairs: 1 pair (user1)
   - incomplete: user2.session, user3.json, random.zip

**Expected Result**: 3 separate ZIP files with proper categorization

### Scenario 4: No Files Uploaded
1. Click "🧩 账户合并"
2. Click "✅ 完成合并" immediately
3. Bot should show error

**Expected Result**: Error message "没有上传任何文件"

### Scenario 5: Unsupported File Type
1. Click "🧩 账户合并"
2. Upload a .txt file
3. Bot should reject it

**Expected Result**: Error message about unsupported file type

### Scenario 6: Multiple Uploads
1. Click "🧩 账户合并"
2. Upload file1.session
3. Wait for confirmation
4. Upload file1.json
5. Wait for confirmation
6. Upload file2.zip
7. Click "✅ 完成合并"

**Expected Result**: All 3 files processed correctly

### Scenario 7: Cancel Operation
1. Click "🧩 账户合并"
2. Upload some files
3. Click "❌ 取消"
4. Bot should cancel and clean up

**Expected Result**: Task cancelled, temp files cleaned up

## Integration Tests

### Test 1: Switch Between Features
1. Click "📝 文件重命名"
2. Click "❌ 取消"
3. Click "🧩 账户合并"
4. Upload a file
5. Click "❌ 取消"
6. Verify no lingering tasks

### Test 2: Concurrent Users (Admin Test)
1. User A starts rename
2. User B starts merge
3. Both should work independently
4. No task confusion

### Test 3: Timeout Handling
1. Click "📝 文件重命名"
2. Wait 6+ minutes without uploading
3. Upload file
4. Bot should reject (timeout)

### Test 4: Main Menu Integration
1. Start bot with /start
2. Verify "📝 文件重命名" and "🧩 账户合并" buttons visible
3. Other buttons still functional
4. No layout issues

## Performance Tests

### Test 1: Large File Rename
- Upload 50MB file
- Should complete within reasonable time
- No memory issues

### Test 2: Many Files Merge
- Upload 50 mixed files
- Should process all correctly
- Proper categorization

### Test 3: Concurrent Merges
- 3 users start merge simultaneously
- Each should complete independently
- No file conflicts

## Error Handling Tests

### Test 1: Disk Space
- Fill up disk (if possible)
- Try to upload large file
- Should show proper error

### Test 2: Invalid ZIP
- Upload corrupted ZIP to merge
- Should handle gracefully

### Test 3: Permission Issues
- Set readonly on temp dir (if possible)
- Try operations
- Should handle gracefully

## Cleanup Tests

### Test 1: Verify Temp Dir Cleanup
1. Complete rename operation
2. Check that temp_rename_* dirs are removed
3. Complete merge operation
4. Check that temp_merge_* dirs are removed

### Test 2: Verify Status Reset
1. Complete any operation
2. Check user status in database
3. Should be empty or reset

## Regression Tests

### Test 1: Existing Features Still Work
- Test "🚀 账号检测" still works
- Test "🔄 格式转换" still works
- Test "🔐 修改2FA" still works
- Test other features

### Test 2: File Handler Priority
- Test that ZIP files for other features still route correctly
- Rename/merge don't intercept other workflows

## Notes

- All temp files should be cleaned up after operations
- User statuses should be reset properly
- No memory leaks from file operations
- Proper error messages for all failure cases
- Emoji display correctly in all messages
