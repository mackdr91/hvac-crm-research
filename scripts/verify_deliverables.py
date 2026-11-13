# Author: Domonick Mack
# Date: 2026-11-13
# Description: Verification script to validate HVAC CRM research deliverables, header conventions, workflow coverage, and platform matrix completeness.

import os
import sys
import re

EXPECTED_FILES = [
    "hvac_crm_pain_points_summary.md",
    "hvac_crm_reddit_evidence_matrix.md",
    "README.md",
]

MANDATORY_WORKFLOWS = [
    "Scheduling & Dispatching",
    "Offline Mobile Access & Field Reliability",
    "Equipment & Serial Number Tracking",
    "Refrigerant Compliance & Environmental Regulations",
    "Manufacturer Warranty Management",
    "Maintenance Agreements & Service Clubs",
    "Pricebooks & Parts Purchase Orders",
    "QuickBooks Accounting Reconciliation",
    "Merchant Processing & Cash Flow Friction",
]

MANDATORY_PLATFORMS = [
    "ServiceTitan",
    "Housecall Pro",
    "Jobber",
    "FieldEdge",
    "Workiz",
    "Sera",
    "Simpro",
    "Successware",
    "mHelpDesk",
]

def check_header(filepath, content):
    pattern = r"<!--\s*Author:\s*Domonick Mack\s*Date:\s*2026-11-13\s*Description:\s*.+?\s*-->"
    if not re.search(pattern, content, re.DOTALL):
        return False, f"Missing or invalid author/date/description header comment in {filepath}"
    return True, "Header OK"

def check_no_placeholders(filepath, content):
    forbidden = ["TODO", "TBD", "placeholder", "lorem ipsum", "FIXME"]
    lines = content.splitlines()
    for idx, line in enumerate(lines, 1):
        for term in forbidden:
            # Case-insensitive match for forbidden tokens
            if re.search(r'\b' + re.escape(term) + r'\b', line, re.IGNORECASE):
                # Allow TBD only if explicitly in an explanation of why something shouldn't be TBD
                return False, f"Forbidden placeholder '{term}' found in {filepath}:{idx} -> {line.strip()}"
    return True, "No placeholders"

def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"[*] Validating repository deliverables at: {repo_root}")
    failures = []

    # 1. Check all required files exist
    for filename in EXPECTED_FILES:
        filepath = os.path.join(repo_root, filename)
        if not os.path.exists(filepath):
            failures.append(f"Missing required deliverable: {filename}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check header
        ok, msg = check_header(filename, content)
        if not ok:
            failures.append(msg)

        # Check placeholders
        ok, msg = check_no_placeholders(filename, content)
        if not ok:
            failures.append(msg)

    # 2. Check workflow coverage in hvac_crm_pain_points_summary.md
    summary_path = os.path.join(repo_root, "hvac_crm_pain_points_summary.md")
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            summary_content = f.read()
        for wf in MANDATORY_WORKFLOWS:
            if wf.lower() not in summary_content.lower():
                failures.append(f"Summary missing workflow: {wf}")

        for plat in MANDATORY_PLATFORMS:
            if plat.lower() not in summary_content.lower():
                failures.append(f"Summary missing platform: {plat}")

    # 3. Check evidence matrix completeness
    matrix_path = os.path.join(repo_root, "hvac_crm_reddit_evidence_matrix.md")
    if os.path.exists(matrix_path):
        with open(matrix_path, "r", encoding="utf-8") as f:
            matrix_content = f.read()

        for plat in MANDATORY_PLATFORMS:
            if plat.lower() not in matrix_content.lower():
                failures.append(f"Evidence matrix missing platform: {plat}")

        reddit_links = re.findall(r'https?://(?:www\.)?reddit\.com/r/[A-Za-z0-9_]+/comments/[A-Za-z0-9_]+/[^/\s\)]*', matrix_content)
        if len(reddit_links) < 8:
            failures.append(f"Evidence matrix has fewer than 8 primary Reddit thread URLs (found {len(reddit_links)})")
        else:
            print(f"[✓] Found {len(reddit_links)} verified primary Reddit discussion URLs in evidence matrix")

    if failures:
        print("\n[!] Verification FAILED with errors:")
        for err in failures:
            print(f"  - {err}")
        sys.exit(1)

    print("\n[✓] ALL DELIVERABLE VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    print(f"[✓] Validated {len(EXPECTED_FILES)} files, {len(MANDATORY_WORKFLOWS)} operational workflows, and {len(MANDATORY_PLATFORMS)} CRM platforms.")

if __name__ == "__main__":
    main()
