"""Generate structured markdown documents from the Fourth Enterprise Platform Playbook XLSX.

Reads docs/playbook_data.json (pre-exported from XLSX) and generates:
1. sample_content/messaging/enterprise-platform-playbook.md (master doc, replaces existing)
2. sample_content/platform/workforce-management.md (pillar + modules + solutions)
3. sample_content/platform/inventory-management.md
4. sample_content/platform/fourth-iq.md
5. sample_content/platform/services-and-support.md
6. sample_content/messaging/packaging-solutions-matrix.md

Usage: python scripts/generate_playbook_docs.py
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
CONTENT_DIR = PROJECT_ROOT / "sample_content"
DATA_FILE = PROJECT_ROOT / "docs" / "playbook_data.json"


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def clean(text: str) -> str:
    """Clean cell text: fix encoding artifacts, normalize line breaks."""
    if not text:
        return ""
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2013", "--").replace("\u2014", "---")
    text = text.replace("\ufffd", "'")  # replacement char from encoding issues
    text = text.replace("\u00a0", " ")  # non-breaking space
    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip()


def parse_platform_sheet(rows):
    """Parse Platform sheet into structured dict."""
    # Row 0: title, Row 1: headers, Row 2: The Fourth Platform
    # Row 3: pillar headers, Rows 4-8: Pillars
    labels = ["name", "elevator_pitch", "overview", "vp1", "vp2", "vp3", "vp4", "business_value", "customer_examples"]

    platform = {}
    for j, label in enumerate(labels):
        platform[label] = clean(rows[2][j]) if j < len(rows[2]) else ""

    pillars = []
    for i in range(4, 9):
        pillar = {}
        for j, label in enumerate(labels):
            pillar[label] = clean(rows[i][j]) if j < len(rows[i]) else ""
        pillars.append(pillar)

    return platform, pillars


def parse_modules_sheet(rows):
    """Parse Modules sheet into structured dict grouped by pillar."""
    labels = ["name", "elevator_pitch", "narrative", "vp1", "vp2", "vp3", "vp4", "business_value", "solutions"]
    pillars = {}
    current_pillar = ""

    for row in rows:
        name = clean(row[0])
        if not name:
            continue
        if name in ("Workforce Management", "Inventory Management", "Services & Support"):
            current_pillar = name
            if current_pillar not in pillars:
                pillars[current_pillar] = []
            continue
        if name == "Module":
            continue
        module = {}
        for j, label in enumerate(labels):
            val = clean(row[j]) if j < len(row) else ""
            module[label] = val
        if current_pillar:
            pillars[current_pillar].append(module)

    return pillars


def parse_solutions_sheet(rows):
    """Parse Solutions sheet into structured dict grouped by pillar/module."""
    # Columns: Solution | Adv | Exp | What It Does | Why It Matters | Context | Value Propositions
    pillars = {}
    current_pillar = ""
    current_module = ""

    for i, row in enumerate(rows):
        name = clean(row[0])
        if not name:
            continue
        if name in ("Workforce Management", "Inventory Management", "Services & Support"):
            current_pillar = name
            if current_pillar not in pillars:
                pillars[current_pillar] = {}
            continue
        if name == "Solution":
            continue
        # Check if this is a module name (next row is "Solution" header)
        if i + 1 < len(rows) and clean(rows[i + 1][0]) == "Solution":
            current_module = name
            if current_pillar and current_module not in pillars.get(current_pillar, {}):
                pillars.setdefault(current_pillar, {})[current_module] = []
            continue
        # It's a solution row
        adv = clean(row[1]) if len(row) > 1 else ""
        exp = clean(row[2]) if len(row) > 2 else ""
        if adv and exp:
            tier = "Advanced + Expert"
        elif exp:
            tier = "Expert Only"
        elif adv:
            tier = "Advanced Only"
        else:
            tier = "Base"

        solution = {
            "name": name,
            "tier": tier,
            "adv": bool(adv),
            "exp": bool(exp),
            "what_it_does": clean(row[3]) if len(row) > 3 else "",
            "why_it_matters": clean(row[4]) if len(row) > 4 else "",
            "context": clean(row[5]) if len(row) > 5 else "",
            "value_propositions": clean(row[6]) if len(row) > 6 else "",
        }
        if current_pillar and current_module:
            pillars.setdefault(current_pillar, {}).setdefault(current_module, []).append(solution)

    return pillars


def format_value_props(vp1, vp2, vp3, vp4):
    """Format value propositions as markdown list."""
    lines = []
    for vp in [vp1, vp2, vp3, vp4]:
        if vp:
            lines.append(f"- **{vp}**" if ":" in vp else f"- {vp}")
    return "\n".join(lines)


def format_customer_quote(text):
    """Format customer examples as blockquotes."""
    if not text:
        return ""
    # Split on common attribution patterns
    lines = text.strip().split("\n")
    result = []
    for line in lines:
        line = line.strip()
        if line.startswith("-") or line.startswith("--"):
            result.append(f"\n> *{line}*")
        elif line:
            result.append(f"> {line}")
    return "\n".join(result)


def generate_master_playbook(platform, pillars, modules, solutions):
    """Generate the comprehensive enterprise-platform-playbook.md."""
    lines = []
    lines.append("# Fourth Enterprise Platform Playbook\n")

    # Platform Overview
    lines.append("## Platform Overview\n")
    lines.append(f"**{platform['elevator_pitch']}**\n")
    lines.append(f"{platform['overview']}\n")
    lines.append("### Value Propositions\n")
    lines.append(format_value_props(platform['vp1'], platform['vp2'], platform['vp3'], platform['vp4']))
    lines.append("")
    if platform['business_value']:
        lines.append("### Key Metrics\n")
        for metric in platform['business_value'].split(";"):
            metric = metric.strip()
            if metric:
                lines.append(f"- {metric}")
        lines.append("")

    # Platform Pillars
    lines.append("## Platform Pillars\n")
    pillar_names = {
        0: "Fourth iQ -- In-Store Operations",
        1: "Fourth iQ -- Above-Store Strategy",
        2: "Workforce Management",
        3: "Inventory Management",
        4: "Services & Support",
    }

    for idx, pillar in enumerate(pillars):
        pname = pillar_names[idx]
        lines.append(f"### {pname}\n")
        lines.append(f"**{pillar['elevator_pitch']}**\n")
        lines.append(f"{pillar['overview']}\n")
        lines.append("**Value Propositions:**\n")
        lines.append(format_value_props(pillar['vp1'], pillar['vp2'], pillar['vp3'], pillar['vp4']))
        lines.append("")
        if pillar['business_value']:
            lines.append(f"**Business Value:** {pillar['business_value']}\n")
        if pillar['customer_examples']:
            lines.append("**Customer Evidence:**\n")
            lines.append(format_customer_quote(pillar['customer_examples']))
            lines.append("")

    # Modules by Pillar
    lines.append("---\n")
    lines.append("## Modules\n")

    for pillar_name in ["Workforce Management", "Inventory Management", "Services & Support"]:
        lines.append(f"### {pillar_name} Modules\n")
        for mod in modules.get(pillar_name, []):
            lines.append(f"#### {mod['name']}\n")
            lines.append(f"**Elevator Pitch:** {mod['elevator_pitch']}\n")
            lines.append(f"{mod['narrative']}\n")
            lines.append("**Value Propositions:**\n")
            lines.append(format_value_props(mod['vp1'], mod['vp2'], mod['vp3'], mod['vp4']))
            lines.append("")
            if mod['business_value']:
                lines.append(f"**Business Value:** {mod['business_value']}\n")
            if mod['solutions']:
                sol_list = [s.strip() for s in mod['solutions'].replace("\n", " -- ").split(" -- ") if s.strip()]
                lines.append(f"**Solutions:** {', '.join(sol_list)}\n")

    # Solution Detail
    lines.append("---\n")
    lines.append("## Solution Detail\n")

    for pillar_name in ["Workforce Management", "Inventory Management", "Services & Support"]:
        lines.append(f"### {pillar_name} Solutions\n")
        for module_name, sols in solutions.get(pillar_name, {}).items():
            lines.append(f"#### {module_name}\n")
            lines.append("| Solution | Tier | What It Does | Why It Matters |")
            lines.append("|----------|------|-------------|----------------|")
            for sol in sols:
                what = sol['what_it_does'].replace("\n", " ").replace("|", "/")
                why = sol['why_it_matters'].replace("\n", " ").replace("|", "/")
                lines.append(f"| **{sol['name']}** | {sol['tier']} | {what} | {why} |")
            lines.append("")

    # Customer Proof Points
    lines.append("---\n")
    lines.append("## Customer Proof Points\n")
    for pillar in pillars:
        if pillar['customer_examples']:
            lines.append(f"### {pillar['name']}\n")
            lines.append(format_customer_quote(pillar['customer_examples']))
            lines.append("")

    # Key Metrics Summary
    lines.append("---\n")
    lines.append("## Key Metrics Summary\n")
    lines.append("| Area | Metric |")
    lines.append("|------|--------|")
    all_metrics = []
    if platform['business_value']:
        for m in platform['business_value'].split(";"):
            m = m.strip()
            if m:
                all_metrics.append(("Platform", m))
    for pillar in pillars:
        if pillar['business_value']:
            for m in pillar['business_value'].split(";"):
                m = m.strip()
                if m:
                    all_metrics.append((pillar['name'], m))
    for mod_pillar, mods in modules.items():
        for mod in mods:
            if mod['business_value']:
                for m in mod['business_value'].split(";"):
                    m = m.strip()
                    if m:
                        all_metrics.append((mod['name'], m))
    for area, metric in all_metrics:
        lines.append(f"| {area} | {metric} |")
    lines.append("")

    return "\n".join(lines)


def generate_pillar_doc(pillar_data, pillar_name, modules_data, solutions_data):
    """Generate a per-pillar markdown document."""
    lines = []
    lines.append(f"# Fourth {pillar_name}\n")
    lines.append(f"**{pillar_data['elevator_pitch']}**\n")
    lines.append("## Overview\n")
    lines.append(f"{pillar_data['overview']}\n")
    lines.append("## Value Propositions\n")
    lines.append(format_value_props(pillar_data['vp1'], pillar_data['vp2'], pillar_data['vp3'], pillar_data['vp4']))
    lines.append("")

    if pillar_data['business_value']:
        lines.append("## Business Value\n")
        for metric in pillar_data['business_value'].split(";"):
            metric = metric.strip()
            if metric:
                lines.append(f"- {metric}")
        lines.append("")

    if pillar_data['customer_examples']:
        lines.append("## Customer Evidence\n")
        lines.append(format_customer_quote(pillar_data['customer_examples']))
        lines.append("")

    # Modules
    lines.append("---\n")
    lines.append("## Modules\n")
    for mod in modules_data:
        lines.append(f"### {mod['name']}\n")
        lines.append(f"**{mod['elevator_pitch']}**\n")
        lines.append(f"{mod['narrative']}\n")
        lines.append("**Value Propositions:**\n")
        lines.append(format_value_props(mod['vp1'], mod['vp2'], mod['vp3'], mod['vp4']))
        lines.append("")
        if mod['business_value']:
            lines.append(f"**Business Value:** {mod['business_value']}\n")

        # Solutions for this module
        module_solutions = solutions_data.get(mod['name'], [])
        if module_solutions:
            lines.append(f"### {mod['name']} -- Solutions\n")
            lines.append("| Solution | Tier | What It Does | Why It Matters |")
            lines.append("|----------|------|-------------|----------------|")
            for sol in module_solutions:
                what = sol['what_it_does'].replace("\n", " ").replace("|", "/")
                why = sol['why_it_matters'].replace("\n", " ").replace("|", "/")
                lines.append(f"| **{sol['name']}** | {sol['tier']} | {what} | {why} |")
            lines.append("")

            # Context and value props for each solution (detailed)
            for sol in module_solutions:
                if sol['context'] or sol['value_propositions']:
                    lines.append(f"**{sol['name']}**\n")
                    if sol['context']:
                        lines.append(f"*Context:* {sol['context']}\n")
                    if sol['value_propositions']:
                        lines.append(f"*Value Propositions:* {sol['value_propositions']}\n")

    return "\n".join(lines)


def generate_fourth_iq_doc(iq_instore, iq_abovestore):
    """Generate the Fourth iQ document covering both in-store and above-store."""
    lines = []
    lines.append("# Fourth iQ AI Platform\n")
    lines.append("Fourth iQ is the AI engine built into every aspect of the Fourth Platform. It operates at two levels: in-store operations and above-store strategy.\n")

    lines.append("## Fourth iQ for In-Store Operations\n")
    lines.append(f"**{iq_instore['elevator_pitch']}**\n")
    lines.append(f"{iq_instore['overview']}\n")
    lines.append("### Value Propositions\n")
    lines.append(format_value_props(iq_instore['vp1'], iq_instore['vp2'], iq_instore['vp3'], iq_instore['vp4']))
    lines.append("")
    if iq_instore['business_value']:
        lines.append(f"**Business Value:** {iq_instore['business_value']}\n")

    lines.append("## Fourth iQ for Above-Store Strategy\n")
    lines.append(f"**{iq_abovestore['elevator_pitch']}**\n")
    lines.append(f"{iq_abovestore['overview']}\n")
    lines.append("### Value Propositions\n")
    lines.append(format_value_props(iq_abovestore['vp1'], iq_abovestore['vp2'], iq_abovestore['vp3'], iq_abovestore['vp4']))
    lines.append("")
    if iq_abovestore['business_value']:
        lines.append(f"**Business Value:** {iq_abovestore['business_value']}\n")

    return "\n".join(lines)


def generate_solutions_matrix(solutions):
    """Generate the packaging solutions matrix document."""
    lines = []
    lines.append("# Fourth Platform Solutions Matrix\n")
    lines.append("Complete reference of all solutions with packaging tier flags.\n")
    lines.append("| Pillar | Module | Solution | Advanced | Expert | What It Does |")
    lines.append("|--------|--------|----------|:--------:|:------:|-------------|")

    total = 0
    for pillar_name in ["Workforce Management", "Inventory Management", "Services & Support"]:
        for module_name, sols in solutions.get(pillar_name, {}).items():
            for sol in sols:
                adv = "Yes" if sol['adv'] else ""
                exp = "Yes" if sol['exp'] else ""
                what = sol['what_it_does'].replace("\n", " ").replace("|", "/")[:120]
                lines.append(f"| {pillar_name} | {module_name} | {sol['name']} | {adv} | {exp} | {what} |")
                total += 1

    lines.append(f"\n**Total Solutions: {total}**\n")

    # Summary by pillar
    lines.append("## Summary by Pillar\n")
    for pillar_name in ["Workforce Management", "Inventory Management", "Services & Support"]:
        pillar_sols = solutions.get(pillar_name, {})
        module_count = len(pillar_sols)
        sol_count = sum(len(sols) for sols in pillar_sols.values())
        lines.append(f"- **{pillar_name}:** {module_count} modules, {sol_count} solutions")
    lines.append("")

    return "\n".join(lines)


def main():
    data = load_data()

    platform, pillars = parse_platform_sheet(data["Platform"])
    modules = parse_modules_sheet(data["Modules"])
    solutions = parse_solutions_sheet(data["Solutions"])

    # Count solutions
    total_sols = sum(
        len(sols)
        for pillar_sols in solutions.values()
        for sols in pillar_sols.values()
    )
    total_mods = sum(len(mods) for mods in modules.values())
    print(f"Parsed: {len(pillars)} pillars, {total_mods} modules, {total_sols} solutions")

    # 1. Master playbook
    master = generate_master_playbook(platform, pillars, modules, solutions)
    out_path = CONTENT_DIR / "messaging" / "enterprise-platform-playbook.md"
    out_path.write_text(master, encoding="utf-8")
    print(f"  Written: {out_path} ({len(master.splitlines())} lines)")

    # 2. Per-pillar documents
    # Workforce Management (pillar index 2)
    wfm_doc = generate_pillar_doc(pillars[2], "Workforce Management",
                                   modules.get("Workforce Management", []),
                                   solutions.get("Workforce Management", {}))
    out_path = CONTENT_DIR / "platform" / "workforce-management.md"
    out_path.write_text(wfm_doc, encoding="utf-8")
    print(f"  Written: {out_path} ({len(wfm_doc.splitlines())} lines)")

    # Inventory Management (pillar index 3)
    inv_doc = generate_pillar_doc(pillars[3], "Inventory Management",
                                   modules.get("Inventory Management", []),
                                   solutions.get("Inventory Management", {}))
    out_path = CONTENT_DIR / "platform" / "inventory-management.md"
    out_path.write_text(inv_doc, encoding="utf-8")
    print(f"  Written: {out_path} ({len(inv_doc.splitlines())} lines)")

    # Fourth iQ (pillar indices 0 and 1)
    iq_doc = generate_fourth_iq_doc(pillars[0], pillars[1])
    # Overwrite the existing fourth-iq-ai-platform.md with real data
    out_path = CONTENT_DIR / "platform" / "fourth-iq-ai-platform.md"
    out_path.write_text(iq_doc, encoding="utf-8")
    print(f"  Written: {out_path} ({len(iq_doc.splitlines())} lines)")

    # Services & Support (pillar index 4)
    svc_doc = generate_pillar_doc(pillars[4], "Services & Support",
                                   modules.get("Services & Support", []),
                                   solutions.get("Services & Support", {}))
    out_path = CONTENT_DIR / "platform" / "services-and-support.md"
    out_path.write_text(svc_doc, encoding="utf-8")
    print(f"  Written: {out_path} ({len(svc_doc.splitlines())} lines)")

    # 3. Packaging solutions matrix
    matrix = generate_solutions_matrix(solutions)
    out_path = CONTENT_DIR / "messaging" / "packaging-solutions-matrix.md"
    out_path.write_text(matrix, encoding="utf-8")
    print(f"  Written: {out_path} ({len(matrix.splitlines())} lines)")

    print(f"\nDone! Generated 6 documents from the Enterprise Platform Playbook.")
    print(f"Verification: {len(pillars)} pillars, {total_mods} modules, {total_sols} solutions")


if __name__ == "__main__":
    main()
