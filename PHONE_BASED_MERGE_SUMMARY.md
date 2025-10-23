# Account Files Merge - Phone-based Naming and Deduplication

## Overview

This update enhances the Account Files Merge (🧩 账户合并) feature by implementing phone number-based naming and automatic deduplication of accounts.

## Changes Made

### 1. Phone Number Extraction

Added two helper functions to extract phone numbers from different sources:

#### `extract_phone_from_json(json_path: str) -> Optional[str]`
- Reads JSON files and extracts the `phone` field
- Removes non-digit characters (like `+` signs)
- Validates that the phone number is at least 10 digits
- Returns `None` if no valid phone number is found

#### `extract_phone_from_tdata_path(account_root: str, tdata_dir_name: str) -> Optional[str]`
- Examines the TData directory path structure
- Looks for phone numbers in parent directory names
- Checks all path components for phone-like patterns
- Returns `None` if no phone number is detected

### 2. Deduplication Logic

The updated `process_merge_files()` function now:

**For TData Accounts:**
- Extracts phone numbers from directory paths
- Groups accounts by phone number
- Keeps only the first occurrence of each phone number
- Accounts without phone numbers fall back to `account_N` naming

**For Session+JSON Pairs:**
- Extracts phone numbers from JSON files
- Groups pairs by phone number
- Keeps only the first occurrence of each phone number
- Pairs without phone numbers use original basename

### 3. Output Archive Structure

**TData Archive (`tdata_only_<timestamp>.zip`):**
```
tdata_only_1234567890.zip
├── 1234567890/            # Phone number as directory name
│   └── tdata/
│       └── D877F783D5D3EF8C/
│           └── ...files...
├── 9876543210/            # Another phone number
│   └── tdata/
│       └── ...
└── account_1/             # Fallback for accounts without phone
    └── tdata/
        └── ...
```

**Session+JSON Archive (`session_json_<timestamp>.zip`):**
```
session_json_1234567890.zip
├── 1234567890.session     # Phone number as filename
├── 1234567890.json
├── 9876543210.session     # Another phone number
├── 9876543210.json
└── ...
```

### 4. Output Filenames

- **Before:** `tdata_accounts_<timestamp>.zip`
- **After:** `tdata_only_<timestamp>.zip`

- **Before:** `session_json_pairs_<timestamp>.zip`
- **After:** `session_json_<timestamp>.zip`

### 5. User Feedback

The summary message now includes deduplication statistics:

```
✅ 账户文件合并完成！

📊 处理结果
• 解压 ZIP 文件: 6 个
• TData 账户: 2 个
• Session+JSON 配对: 2 对
• 去重移除: 2 个

📦 生成文件
```

## Benefits

1. **Consistent Naming:** All accounts use phone numbers as canonical identifiers
2. **Deduplication:** Automatically removes duplicate accounts with the same phone number
3. **Easy Identification:** Users can immediately see which accounts they have
4. **Better Organization:** Phone-based naming makes it easier to manage accounts
5. **Backward Compatible:** Accounts without phone numbers still work with fallback naming

## Testing

Comprehensive test coverage includes:

### `test_phone_deduplication.py`
- Phone extraction from JSON files
- Phone extraction from TData paths
- Deduplication logic
- Output structure verification
- Filename format validation

### `test_phone_merge_integration.py`
- End-to-end workflow testing
- Multiple duplicate scenarios
- Archive structure verification
- Deduplication verification

### Existing Tests
- `test_merge_recursive.py` ✅ All pass
- `test_integration_merge.py` ✅ All pass

## Implementation Details

### Phone Number Format
- Accepts international format with `+` prefix
- Accepts plain digit format
- Minimum length: 10 digits
- Non-digit characters are automatically removed

### Deduplication Strategy
- First occurrence wins (preserves the first encountered account)
- Duplicates are logged but not included in output
- Users are informed of the number of duplicates removed

### Fallback Behavior
- **TData accounts without phone:** Use `account_N` naming (N = 1, 2, 3...)
- **Session+JSON without phone:** Use original basename from filename

## Code Changes

**Files Modified:**
- `TGapibot.py`: Added phone extraction and deduplication logic

**Files Added:**
- `test_phone_deduplication.py`: Unit tests for new features
- `test_phone_merge_integration.py`: Integration tests for complete workflow

**Total Lines Changed:**
- Added: ~150 lines
- Modified: ~20 lines
- Net change: ~170 lines

## Examples

### Example 1: Normal TData with Phone
**Input:** ZIP containing `1234567890/tdata/D877F783D5D3EF8C/...`
**Output:** `tdata_only_<timestamp>.zip` with `1234567890/tdata/...`

### Example 2: Duplicate TData
**Input:**
- ZIP1: `1234567890/tdata/D877F783D5D3EF8C/...`
- ZIP2: `1234567890/tdata/D877F783D5D3EF8C/...` (duplicate)

**Output:** 
- Only first occurrence included
- Summary shows "去重移除: 1 个"

### Example 3: Session+JSON with Phone
**Input:**
- `user1.session`
- `user1.json` (contains `"phone": "+1234567890"`)

**Output:** `session_json_<timestamp>.zip` with:
- `1234567890.session`
- `1234567890.json`

## Performance Impact

- **Minimal:** Phone extraction is fast (string operations)
- **Deduplication:** O(n) time complexity using dictionaries
- **No slowdown** in overall processing time

## Compatibility

✅ **Backward Compatible:**
- Existing workflows continue to work
- Accounts without phone numbers handled gracefully
- No breaking changes to API or database

## Future Enhancements

Potential improvements for future versions:
- Support for extracting phone from TData internal files
- Configurable deduplication strategy (first/last/newest)
- Phone number validation against country codes
- Merge statistics export to CSV

---

**Version:** 1.0  
**Date:** October 23, 2024  
**Status:** ✅ Complete and Tested
