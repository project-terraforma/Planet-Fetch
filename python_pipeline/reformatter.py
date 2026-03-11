import re
import json
from pathlib import Path

def parse_context(content):
    data = {
        'release': '',
        'total_records': '',
        'themes': {},
        'countries': []
    }
    
    # Extract Release Month
    match = re.search(r'DATA RELEASE MONTH:\s*(.*)', content)
    if match:
        data['release'] = match.group(1).strip()
    
    # Extract Global Total Records
    match = re.search(r'SECTION 4 — GLOBAL STATISTICS.*?Total Records:\s*([\d,]+)', content, re.DOTALL)
    if match:
        data['total_records'] = match.group(1).strip()
    
    # Split by Theme Blocks
    # Each theme starts with ### THEME_NAME
    theme_sections = re.split(r'### ', content)
    for section in theme_sections[1:]:
        lines = section.strip().split('\n')
        if not lines: continue
        
        theme_name = lines[0].strip().lower()
        if theme_name == "summary": continue # Skip global summary if it matches pattern
        
        theme_data = {
            'count': '0',
            'types': [],
            'datasets': [],
            'coverage': [],
            'classes': [],
            'subtypes': [],
            'distribution': []
        }
        
        # Total Count
        count_match = re.search(r'Total Records:\s*([\d,]+)', section)
        if count_match:
            theme_data['count'] = count_match.group(1).strip()
            
        # Types
        types_match = re.search(r'Types Included\n(.*?)(?:\n\n|\Z)', section, re.DOTALL)
        if types_match:
            theme_data['types'] = [t.strip('- ').strip() for t in types_match.group(1).split('\n') if t.strip()]
            
        # Top Datasets
        datasets_match = re.search(r'Top Datasets\n(.*?)(?:\n\n|\Z)', section, re.DOTALL)
        if datasets_match:
            theme_data['datasets'] = re.findall(r'- (.*?): ([\d,]+)', datasets_match.group(1))
            
        # Property Coverage
        coverage_match = re.search(r'Property Coverage\n(.*?)(?:\n\n|\Z)', section, re.DOTALL)
        if coverage_match:
            # Matches "- name: count (pct%)"
            theme_data['coverage'] = re.findall(r'- (.*?): ([\d,]+) \((.*?)\)', coverage_match.group(1))
            
        # Top Class Values
        class_match = re.search(r'Top Class Values\n(.*?)(?:\n\n|\Z)', section, re.DOTALL)
        if class_match:
            theme_data['classes'] = re.findall(r'- (.*?): ([\d,]+)', class_match.group(1))
            
        # Top Subtype Values
        subtype_match = re.search(r'Top Subtype Values\n(.*?)(?:\n\n|\Z)', section, re.DOTALL)
        if subtype_match:
            theme_data['subtypes'] = re.findall(r'- (.*?): ([\d,]+)', subtype_match.group(1))
            
        # Change Type Distribution
        dist_match = re.search(r'Change Type Distribution\n(.*?)(?:\n\n|\Z)', section, re.DOTALL)
        if dist_match:
            theme_data['distribution'] = re.findall(r'- (.*?): ([\d,]+)', dist_match.group(1))
            
        data['themes'][theme_name] = theme_data

    # Extract Countries from Section 4 specifically
    section_4_match = re.search(r'SECTION 4 .*? GLOBAL STATISTICS(.*?)(?:SECTION 5|$)', content, re.DOTALL | re.IGNORECASE)
    if section_4_match:
        section_4_content = section_4_match.group(1)
        country_section_match = re.search(r'Top Countries Overall\n(.*?)(?:\n\n-|$)', section_4_content, re.DOTALL)
        if country_section_match:
            country_matches = re.findall(r'-\s+([A-Z]{2}):\s*([\d,]+)', country_section_match.group(1))
            for country, count in country_matches:
                data['countries'].append({'name': country, 'count': count})
                
    return data

def generate_v1_refined(data):
    lines = [
        f"OVERTURE MAPS FOUNDATION DATA CONTEXT",
        f"RELEASE: {data['release']}",
        f"GENERATED: 2026-03-11",
        "",
        "================================================================================",
        "GLOBAL STATISTICS",
        f"  - Total Records: {data['total_records']}",
        f"  - Themes Count: {len(data['themes'])}",
        "",
        "DETAILED THEME BREAKDOWN"
    ]
    for theme, info in sorted(data['themes'].items()):
        lines.append(f"  - {theme.upper()}: {info['count']} records")
        if info['datasets']:
            lines.append(f"    * Top Sources: " + ", ".join([f"{d[0]} ({d[1]})" for d in info['datasets'][:3]]))
        if info['coverage']:
            lines.append(f"    * Highlights: " + ", ".join([f"{c[0]} ({c[2]})" for c in info['coverage'][:3]]))
    
    lines.append("")
    lines.append("TOP COUNTRIES OVERALL")
    for c in data['countries']:
        lines.append(f"  - {c['name']}: {c['count']}")
    
    lines.append("")
    lines.append("================================================================================")
    lines.append("STRICT ANALYST MODE: Use only the figures above for verification.")
    
    return "\n".join(lines)

def generate_v2_hierarchical(data):
    lines = [
        f"Overture Maps Context [{data['release']}]",
        "└── Global Summary",
        f"    ├── Total Records: {data['total_records']}",
        f"    └── Themes: {len(data['themes'])}",
        "└── Theme Hierarchy"
    ]
    
    for theme, info in sorted(data['themes'].items()):
        lines.append(f"    ├── {theme.upper()} ({info['count']})")
        if info['types']:
            lines.append(f"    │   ├── Types: " + ", ".join(info['types']))
        if info['datasets']:
            lines.append(f"    │   ├── Top Source: {info['datasets'][0][0]} ({info['datasets'][0][1]})")
            
    lines.append("└── Top Countries")
    for c in data['countries'][:10]:
        lines.append(f"    ├── {c['name']}: {c['count']}")
        
    return "\n".join(lines)

def generate_v3_tabular(data):
    lines = [
        f"# Overture Maps Release {data['release']} Summary",
        "",
        "## Core Metrics",
        f"**Total Records:** {data['total_records']} | **Themes:** {len(data['themes'])}",
        "",
        "## Theme Details",
        "| Theme | Total Count | Top Classes | Top Subtypes |",
        "| :--- | :--- | :--- | :--- |"
    ]
    for theme, info in sorted(data['themes'].items()):
        classes = ", ".join([c[0] for c in info['classes'][:2]])
        subtypes = ", ".join([s[0] for s in info['subtypes'][:2]])
        lines.append(f"| {theme} | {info['count']} | {classes} | {subtypes} |")
        
    lines.append("")
    lines.append("## Property Coverage highlights")
    lines.append("| Theme | Metric | Coverage |")
    lines.append("| :--- | :--- | :--- |")
    for theme, info in sorted(data['themes'].items()):
        for c in info['coverage'][:2]:
            lines.append(f"| {theme} | {c[0]} | {c[2]} |")
            
    lines.append("")
    lines.append("## Top Countries")
    lines.append("| Rank | Country | Records |")
    lines.append("| :---: | :--- | :---: |")
    for i, c in enumerate(data['countries'][:10], 1):
        lines.append(f"| {i} | {c['name']} | {c['count']} |")
        
    return "\n".join(lines)

def generate_v4_compressed(data):
    theme_str = "; ".join([f"{t}:{info['count']}" for t, info in data['themes'].items()])
    country_str = ",".join([f"{c['name']}:{c['count']}" for c in data['countries'][:10]])
    return f"REF:{data['release']}|TOT:{data['total_records']}|THEMES[{theme_str}]|TOP10_GEO[{country_str}]"

def main():
    project_root = Path(__file__).resolve().parent.parent
    contexts_dir = project_root / "contexts"
    
    for month_dir in contexts_dir.iterdir():
        if month_dir.is_dir():
            context_file = month_dir / "context.txt"
            if context_file.exists():
                print(f"Processing formats for {month_dir.name}...")
                content = context_file.read_text()
                data = parse_context(content)
                
                (month_dir / "v1_refined.txt").write_text(generate_v1_refined(data))
                (month_dir / "v2_hierarchical.txt").write_text(generate_v2_hierarchical(data))
                (month_dir / "v3_tabular.txt").write_text(generate_v3_tabular(data))
                (month_dir / "v4_compressed.txt").write_text(generate_v4_compressed(data))

if __name__ == "__main__":
    main()
