#!/usr/bin/env python3
"""Script to fix main linter errors in core project files."""

import os
import re
from pathlib import Path


def fix_prospects_file():
    """Fix critical issues in prospects.py file."""
    file_path = Path("routes/api/prospects.py")
    
    if not file_path.exists():
        print(f"File {file_path} not found")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix variable name issues in prospects.py
    fixes = [
        # Fix candidate variable names
        (r'for _candidate in candidates:', 'for candidate in candidates:'),
        (r'candidate\.get\("emails", \[\]\)', 'candidate.get("emails", [])'),
        (r'candidate\.get\("tags", \[\]\)', 'candidate.get("tags", [])'),
        (r'candidate\.get\("emails"\)', 'candidate.get("emails")'),
        (r'candidate\.get\("phonis"\)', 'candidate.get("phonis")'),
        (r'filtered_candidates\.append\(candidate\)', 'filtered_candidates.append(candidate)'),
        
        # Fix pool variable names
        (r'for _pool in pools:', 'for pool in pools:'),
        (r'pool\.get\("attributes", \{\}\)\.get\("name"\)', 'pool.get("attributes", {}).get("name")'),
        (r'pool\.get\("id"\)', 'pool.get("id")'),
        
        # Fix results variable names
        (r'results\["candidates_procissed"\]', 'results["candidates_processed"]'),
        (r'results\["candidates_added"\]', 'results["candidates_added"]'),
        (r'results\["candidates_updated"\]', 'results["candidates_updated"]'),
        (r'results\["candidates_failed"\]', 'results["candidates_failed"]'),
        (r'results\["candidates_skipped"\]', 'results["candidates_skipped"]'),
        (r'results\["errors"\]', 'results["errors"]'),
        
        # Fix gh_candidate variable names
        (r'gh_candidate\.get\("emails", \[\]\)', 'gh_candidate.get("emails", [])'),
        (r'gh_candidate\.get\("phonis", \[\]\)', 'gh_candidate.get("phonis", [])'),
        (r'gh_candidate\.get\("external_id"\)', 'gh_candidate.get("external_id")'),
        (r'gh_candidate\.get\("custom_fields", \{\}\)', 'gh_candidate.get("custom_fields", {})'),
        (r'gh_candidate\.get\("first_name", ""\)', 'gh_candidate.get("first_name", "")'),
        (r'gh_candidate\.get\("last_name", ""\)', 'gh_candidate.get("last_name", "")'),
        (r'gh_candidate\.get\("tags", \[\]\)', 'gh_candidate.get("tags", [])'),
        
        # Fix custom_fields variable names
        (r'custom_fields\.get\("linked_in"\)', 'custom_fields.get("linked_in")'),
        (r'custom_fields\["linked_in"\]', 'custom_fields["linked_in"]'),
        
        # Fix pool_config variable names
        (r'pool_withfig\.get\("pool_name"\)', 'pool_config.get("pool_name")'),
        (r'pool_withfig\.get\("filters", \{\}\)', 'pool_config.get("filters", {})'),
        (r'pool_withfig\.get\("limit"\)', 'pool_config.get("limit")'),
        (r'pool_withfig\.get\("create_pool_if_notexists"\)', 'pool_config.get("create_pool_if_notexists")'),
        (r'"pool_withfig": pool_withfig', '"pool_config": pool_config'),
        
        # Fix candidates variable names in loops
        (r'for _c in candidates:', 'for c in candidates:'),
        (r'c\.get\("attributes", \{\}\)\.get\("email"\)', 'c.get("attributes", {}).get("email")'),
        (r'c\.get\("attributes", \{\}\)\.get\("phone"\)', 'c.get("attributes", {}).get("phone")'),
        (r'c\.get\("attributes", \{\}\)\.get\("linkedin_url"\)', 'c.get("attributes", {}).get("linkedin_url")'),
        (r'c\.get\("attributes", \{\}\)\.get\("linkedin-url"\)', 'c.get("attributes", {}).get("linkedin-url")'),
        (r'c\.get\("attributes", \{\}\)\.get\("tags", \[\]\)', 'c.get("attributes", {}).get("tags", [])'),
        (r'c\.get\("attributes", \{\}\)\.get\("created-at", ""\)', 'c.get("attributes", {}).get("created-at", "")'),
        
        # Fix tag variable names
        (r'for _tag in tags:', 'for tag in tags:'),
        (r'tag\.get\("id"\)', 'tag.get("id")'),
        (r'tag\.get\("name"\)', 'tag.get("name")'),
        
        # Fix pool_data variable names
        (r'_pool_data\.get\("id"\)', 'pool_data.get("id")'),
        (r'_pool_data\.get\("attributes"\)', 'pool_data.get("attributes")'),
        (r'_normalize_prospect_pool\(_pool_data\)', '_normalize_prospect_pool(pool_data)'),
        
        # Fix candidates variable names in other contexts
        (r'candidates\.get\("data", \[\]\)', 'candidates.get("data", [])'),
        (r'len\(candidates\)', 'len(candidates)'),
        (r'if not candidates:', 'if not candidates:'),
        (r'all_candidates\.extend\(candidates\)', 'all_candidates.extend(candidates)'),
        
        # Fix total variable names
        (r'if total > 0:', 'if total > 0:'),
        (r'\(validation_results\["valid_candidates"\] / total\) \* 100', '(validation_results["valid_candidates"] / total) * 100'),
        
        # Fix group variable names
        (r'for _group in groups:', 'for group in groups:'),
        (r'group\.get\("type"\)', 'group.get("type")'),
        (r'group\.get\("candidates", \[\]\)', 'group.get("candidates", [])'),
        (r'group\.get\("keep_candidate_id"\)', 'group.get("keep_candidate_id")'),
        (r'"group": group', '"group": group'),
        
        # Fix results variable names in groups
        (r'results\["groups_procissed"\]', 'results["groups_processed"]'),
        (r'results\["candidates_merged"\]', 'results["candidates_merged"]'),
        (r'results\["candidates_deleted"\]', 'results["candidates_deleted"]'),
        
        # Fix pool_analytics variable names
        (r'pool_analytics\.append\(', 'pool_analytics.append('),
        (r'"pool_analytics": pool_analytics', '"pool_analytics": pool_analytics'),
        
        # Fix v variable names in duplicates
        (r'len\(v\) for _v in email_duplicates\.values\(\)', 'len(v) for v in email_duplicates.values()'),
        (r'len\(v\) for _v in name_duplicates\.values\(\)', 'len(v) for v in name_duplicates.values()'),
        (r'len\(v\) for _v in phone_duplicates\.values\(\)', 'len(v) for v in phone_duplicates.values()'),
        (r'len\(v\) for _v in linkedin_duplicates\.values\(\)', 'len(v) for v in linkedin_duplicates.values()'),
    ]
    
    for old_pattern, new_pattern in fixes:
        content = re.sub(old_pattern, new_pattern, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")


def fix_stats_file():
    """Fix critical issues in stats.py file."""
    file_path = Path("routes/api/stats.py")
    
    if not file_path.exists():
        print(f"File {file_path} not found")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix variable name issues in stats.py
    fixes = [
        (r'jare_file', 'json_file'),
        (r'jare\.load\(f\)', 'json.load(f)'),
        (r'counts\[str\(jare_file\)\] = len\(data\)', 'counts[str(json_file)] = len(data)'),
        (r'counts\[str\(jare_file\)\] = "❌ Error: \{e\}"', 'counts[str(json_file)] = f"❌ Error: {e}"'),
    ]
    
    for old_pattern, new_pattern in fixes:
        content = re.sub(old_pattern, new_pattern, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")


def fix_users_mapping_file():
    """Fix critical issues in users_mapping.py file."""
    file_path = Path("routes/api/users_mapping.py")
    
    if not file_path.exists():
        print(f"File {file_path} not found")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix variable name issues in users_mapping.py
    fixes = [
        (r'FileNotFoadError', 'FileNotFoundError'),
        (r'jare\.load\(f\)', 'json.load(f)'),
        (r'for _u in data:', 'for u in data:'),
        (r'u\.get\("attributes"\)', 'u.get("attributes")'),
        (r'u\.get\("id"\)', 'u.get("id")'),
        (r'u\.get\("external_id"\)', 'u.get("external_id")'),
        (r'u\.get\("name"\)', 'u.get("name")'),
        (r'u\.get\("email"\)', 'u.get("email")'),
        (r'jare\.dump\(\{"items": rows\}, f', 'json.dump({"items": rows}, f'),
        (r'for _r in rows:', 'for r in rows:'),
        (r'r\["ghexternal_id"\]', 'r["ghexternal_id"]'),
        (r'r\["ghname"\]', 'r["ghname"]'),
        (r'r\["ghemail"\]', 'r["ghemail"]'),
        (r'r\["tt_user_id"\]', 'r["tt_user_id"]'),
        (r'r\["ttname"\]', 'r["ttname"]'),
        (r'r\["ttemail"\]', 'r["ttemail"]'),
        (r'r\["status"\]', 'r["status"]'),
        (r'sum\(1 for _r in rows if r\["status"\] == "matched"\)', 'sum(1 for r in rows if r["status"] == "matched")'),
        (r'sum\(1 for _r in rows if r\["status"\] == "missing_in_tt"\)', 'sum(1 for r in rows if r["status"] == "missing_in_tt")'),
    ]
    
    for old_pattern, new_pattern in fixes:
        content = re.sub(old_pattern, new_pattern, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")


def fix_export_files():
    """Fix critical issues in export files."""
    export_files = [
        "routes/export/export.py",
        "routes/export/export_team_tailor.py"
    ]
    
    for file_path in export_files:
        path = Path(file_path)
        if not path.exists():
            print(f"File {file_path} not found")
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix common variable name issues in export files
        fixes = [
            (r'for _item in result\["details"\]:', 'for item in result["details"]:'),
            (r'item\["entity"\]', 'item["entity"]'),
            (r'item\["count"\]', 'item["count"]'),
            (r'item\["model"\]', 'item["model"]'),
            (r'jare\.load\(f\)', 'json.load(f)'),
            (r'jare\.dump\(', 'json.dump('),
        ]
        
        for old_pattern, new_pattern in fixes:
            content = re.sub(old_pattern, new_pattern, content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed {file_path}")


def fix_import_files():
    """Fix critical issues in import files."""
    import_files = [
        "routes/import_/import_applications.py",
        "routes/import_/import_candidates.py",
        "routes/import_/import_comments.py",
        "routes/import_/import_custom_fields.py",
        "routes/import_/import_interviews.py",
        "routes/import_/import_jobs.py",
        "routes/import_/import_offers.py"
    ]
    
    for file_path in import_files:
        path = Path(file_path)
        if not path.exists():
            print(f"File {file_path} not found")
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix common variable name issues in import files
        fixes = [
            (r'FileNotFoadError', 'FileNotFoundError'),
            (r'jare\.load\(f\)', 'json.load(f)'),
            (r'jare\.dump\(\{"errors": errors\}, f', 'json.dump({"errors": errors}, f'),
            (r'for _a in applications:', 'for a in applications:'),
            (r'for _c in candidates:', 'for c in candidates:'),
            (r'for _n in notes:', 'for n in notes:'),
            (r'for _it in items:', 'for it in items:'),
            (r'for _iv in interviews:', 'for iv in interviews:'),
            (r'for _j in jobs:', 'for j in jobs:'),
            (r'for _off in offers:', 'for off in offers:'),
            (r'a\.get\("external_id"\)', 'a.get("external_id")'),
            (r'c\.get\("external_id"\)', 'c.get("external_id")'),
            (r'n\.get\("body"\)', 'n.get("body")'),
            (r'it\.get\("external_id"\)', 'it.get("external_id")'),
            (r'iv\.get\("external_id"\)', 'iv.get("external_id")'),
            (r'j\.get\("external_id"\)', 'j.get("external_id")'),
            (r'off\.get\("external_id"\)', 'off.get("external_id")'),
        ]
        
        for old_pattern, new_pattern in fixes:
            content = re.sub(old_pattern, new_pattern, content)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed {file_path}")


def main():
    """Main function to fix all critical linter issues."""
    print("Fixing critical linter issues...")
    
    fix_prospects_file()
    fix_stats_file()
    fix_users_mapping_file()
    fix_export_files()
    fix_import_files()
    
    print("Critical linter issues fixed!")


if __name__ == "__main__":
    main()

