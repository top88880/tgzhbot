# -*- coding: utf-8 -*-
import os
import re
import json
import zipfile
from dataclasses import dataclass
from typing import List, Tuple, Optional, Iterable, Dict
import phonenumbers
from phonenumbers import geocoder

PHONE_REGEX = re.compile(r"(?:\+?\d{6,16})")

@dataclass
class AccountMeta:
    path: str            # 文件或目录绝对路径
    display_name: str    # 显示/打包用名称（保留原名）
    phone: Optional[str] # 形如 +8613xxxxxx（E.164）
    country_code: Optional[int]
    country_name_zh: Optional[str]

class AccountClassifier:
    """账号分类/打包工具：支持 tdata 和 session+json 两种来源"""
    def __init__(self) -> None:
        pass

    # -------------- 基础提取 --------------
    def _normalize_phone(self, raw: str) -> Optional[str]:
        """从字符串中提取并标准化为 E.164；失败返回 None"""
        if not raw:
            return None
        m = PHONE_REGEX.search(raw)
        if not m:
            return None
        cand = m.group(0)
        if not cand.startswith("+"):
            cand = "+" + cand
        try:
            num = phonenumbers.parse(cand, None)
            if phonenumbers.is_possible_number(num):
                return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
        except Exception:
            return None
        return None

    def _infer_phone_from_json(self, json_path: str) -> Optional[str]:
        """尝试在 JSON 文件中寻找手机号字段"""
        try:
            with open(json_path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
            # 常见字段
            for k in ("phone", "phone_number", "tel", "user_phone"):
                if isinstance(data.get(k), str):
                    p = self._normalize_phone(data[k])
                    if p:
                        return p
            # 常见嵌套
            user = data.get("user")
            if isinstance(user, dict):
                for k in ("phone", "phone_number"):
                    if isinstance(user.get(k), str):
                        p = self._normalize_phone(user[k])
                        if p:
                            return p
        except Exception:
            pass
        return None

    def _detect_country(self, phone: Optional[str]) -> Tuple[Optional[int], Optional[str]]:
        """通过 phonenumbers 解析国家信息；失败返回 (None, None)"""
        if not phone:
            return None, None
        try:
            num = phonenumbers.parse(phone, None)
            code = num.country_code
            name = geocoder.country_name_for_number(num, "zh") or geocoder.country_name_for_number(num, "en")
            return code, (name or "未知")
        except Exception:
            return None, None

    # -------------- 元数据构造 --------------
    def build_meta_from_pairs(self, files: List[Tuple[str, str]], file_type: str) -> List[AccountMeta]:
        """
        将 FileProcessor.scan_zip_file 返回的列表 [(path, name)] 转为 AccountMeta 列表
        file_type: 'tdata' 或 'session'
        """
        metas: List[AccountMeta] = []
        for path, display_name in files:
            phone: Optional[str] = None

            # 1) 从名称里推断
            phone = self._normalize_phone(display_name)

            # 2) 目录/文件内查找 json 兜底
            if not phone:
                if os.path.isdir(path):
                    # tdata 目录下同级或下层可能会有描述 json
                    for root, _, fns in os.walk(path):
                        for fn in fns:
                            if fn.lower().endswith(".json"):
                                p = self._infer_phone_from_json(os.path.join(root, fn))
                                if p:
                                    phone = p
                                    break
                        if phone:
                            break
                else:
                    # session 同目录下可能有 .json
                    if path.lower().endswith(".json"):
                        phone = self._infer_phone_from_json(path)
                    else:
                        alt = path.replace(".session", ".json")
                        if os.path.exists(alt):
                            phone = self._infer_phone_from_json(alt)

            code, name = self._detect_country(phone)
            metas.append(AccountMeta(
                path=path,
                display_name=display_name,
                phone=phone,
                country_code=code,
                country_name_zh=name if name else None
            ))
        return metas

    # -------------- 命名与分组 --------------
    def country_key(self, m: AccountMeta) -> Tuple[str, str]:
        if m.country_code:
            return (m.country_name_zh or "未知"), str(m.country_code)
        return "未知", "000"

    def detect_bundle_country_label(self, metas: List[AccountMeta]) -> Tuple[str, str]:
        """用于按数量拆分时统一命名：若混合国家返回 ('混合','000')，全未知返回 ('未知','000')"""
        if not metas:
            return "未知", "000"
        codes: Dict[str, str] = {}  # code -> name
        code_list: List[str] = []
        for m in metas:
            name, code = self.country_key(m)
            codes[code] = name
            code_list.append(code)
        uniq = set(code_list)
        if len(uniq) == 1:
            code = next(iter(uniq))
            return codes.get(code, "未知"), code
        if uniq == {"000"}:
            return "未知", "000"
        return "混合", "000"

    # -------------- 打包 --------------
    def _zip_bundle(self, items: List[AccountMeta], out_dir: str, display_zip: str) -> str:
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, display_zip)
        with zipfile.ZipFile(dst, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for it in items:
                if os.path.isdir(it.path):
                    # 递归加入目录
                    root_base = os.path.dirname(it.path)
                    for rp, _, fns in os.walk(it.path):
                        for fn in fns:
                            full = os.path.join(rp, fn)
                            rel = os.path.relpath(full, root_base)
                            # 保持最上层目录名为 display_name
                            arcname = os.path.join(it.display_name, os.path.basename(rel))
                            zf.write(full, arcname=arcname)
                else:
                    zf.write(it.path, arcname=it.display_name)
        return dst

    # -------------- 对外：按国家拆分 --------------
    def split_by_country(self, metas: List[AccountMeta], out_dir: str) -> List[Tuple[str, str, int]]:
        from collections import defaultdict
        groups: Dict[Tuple[str, str], List[AccountMeta]] = defaultdict(list)
        for m in metas:
            groups[self.country_key(m)].append(m)

        results: List[Tuple[str, str, int]] = []
        for (name, code), items in groups.items():
            qty = len(items)
            zip_name = f"{name}+{code}+{qty}.zip"
            path = self._zip_bundle(items, out_dir, zip_name)
            results.append((path, zip_name, qty))
        return results

    # -------------- 对外：按数量拆分 --------------
    def split_by_quantities(
        self,
        metas: List[AccountMeta],
        sizes: Iterable[int],
        out_dir: str,
        country_label: Optional[Tuple[str, str]] = None
    ) -> List[Tuple[str, str, int]]:
        """按给定 sizes 依次切分，命名 {国家}+{区号}+{数量}.zip"""
        if country_label is None:
            country_label = self.detect_bundle_country_label(metas)
        name, code = country_label

        res: List[Tuple[str, str, int]] = []
        idx = 0
        metas_sorted = list(metas)
        total = len(metas_sorted)
        for s in sizes:
            if idx >= total:
                break
            batch = metas_sorted[idx: idx + s]
            real = len(batch)
            zip_name = f"{name}+{code}+{real}.zip"
            path = self._zip_bundle(batch, out_dir, zip_name)
            res.append((path, zip_name, real))
            idx += s
        return res
