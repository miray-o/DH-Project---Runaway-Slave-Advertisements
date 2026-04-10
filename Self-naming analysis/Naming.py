"""
Self-Naming Analysis for Runaway Slave Advertisements
Analyzes patterns of self-naming, preferred names, and name origins
Based on "Pretends To Be Free" dataset from NY/NJ 18th century
"""

import pandas as pd
import re
from collections import defaultdict
import sys


def extract_year_decade(date_str):
    """Extract year and decade from date string"""
    try:
        year_match = re.search(r'(\d{4})', str(date_str))
        if year_match:
            year = int(year_match.group(1))
            decade = (year // 10) * 10
            return year, decade
    except:
        pass
    return None, None


def extract_name(content):
    """Extract name from advertisement content"""
    patterns = [
        r'named? ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'called ([A-Z][a-z]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None


def check_self_naming(content):
    """Check if advertisement contains self-naming patterns"""
    content_lower = content.lower()

    # Check for different self-naming patterns
    if re.search(r'calls? (?:himself|herself)', content_lower):
        # Extract what they call themselves
        match = re.search(r'calls? (?:himself|herself) ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', content)
        return True, 'calls himself/herself', match.group(1) if match else None

    elif re.search(r'goes by the name', content_lower):
        match = re.search(r'goes by the name (?:of )?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', content)
        return True, 'goes by the name', match.group(1) if match else None

    #elif re.search(r'pretends? to be (?:a )?free(?:man)?', content_lower):
        #return True, 'pretends to be free', None

    #elif re.search(r'pretends? to be (?:a )?freeman', content_lower):
        #return True, 'pretends to be a Freeman', None

    return False, None, None


def check_preferred_name(content):
    """Check if advertisement contains preferred/alternate name patterns"""
    content_lower = content.lower()

    # Check for alias patterns
    alias_match = re.search(r'named? ([A-Z][a-z]+),?\s+alias ([A-Z][a-z]+)', content)
    if alias_match:
        return True, 'alias', f"{alias_match.group(1)}/{alias_match.group(2)}"

    # Check for "commonly called"
    if re.search(r'but commonly called', content_lower):
        match = re.search(r'named? ([A-Z][a-z]+)(?:\s+[A-Z][a-z]+)?,?\s+but commonly called ([A-Z][a-z]+)', content)
        if match:
            return True, 'commonly called', f"{match.group(1)}/{match.group(2)}"

    # Check for "sometimes called"
    if re.search(r'sometimes calls? (?:himself|herself)', content_lower):
        match = re.search(r'sometimes calls? (?:himself|herself) ([A-Z][a-z]+)', content)
        if match:
            return True, 'sometimes called', match.group(1)

    if re.search(r'(?:but|and) sometimes called', content_lower):
        match = re.search(r'(?:but|and) sometimes called ([A-Z][a-z]+)', content)
        if match:
            return True, 'sometimes called', match.group(1)

    return False, None, None


def categorize_name_origin(name):
    """Categorize name by origin"""
    if not name:
        return 'Unknown'

    name_lower = name.lower()

    # African names (including day names)
    african_names = ['cuff', 'cuffy', 'coffee', 'quash', 'quashee', 'quaw', 'quamino',
                     'cudjoe', 'juba', 'mingo', 'sambo', 'quaco', 'billah', 'moosa',
                     'ishmael', 'alli', 'mahomet', 'pompaw', 'popaw', 'nim', 'sippee']

    # Classical names
    classical_names = ['scipio', 'cato', 'caesar', 'cesar', 'pompey', 'hercules',
                       'cicero', 'hannibal', 'chloe', 'venus', 'diana', 'jupiter', 'mars']

    # Biblical names
    biblical_names = ['isaac', 'abraham', 'samuel', 'james', 'joseph', 'moses', 'adam',
                      'daniel', 'jacob', 'peter', 'john', 'paul', 'sarah', 'rachel']

    # Geographic names
    geographic_names = ['london', 'boston', 'york', 'bristol', 'newport', 'cambridge']

    # Anglo/Western names
    anglo_names = ['thomas', 'william', 'george', 'charles', 'henry', 'edward', 'robert',
                   'mary', 'elizabeth', 'anne', 'jack', 'tom', 'will', 'dick', 'harry',
                   'frank', 'robin', 'ned', 'joe', 'bill']

    if name_lower in african_names:
        return 'African'
    elif name_lower in classical_names:
        return 'Classical'
    elif name_lower in biblical_names:
        return 'Biblical'
    elif name_lower in geographic_names:
        return 'Geographic'
    elif name_lower in anglo_names:
        return 'Anglo/Western'
    else:
        return 'Other'


def analyze_self_naming(csv_file):
    """Main analysis function"""
    print("=" * 100)
    print("SELF-NAMING ANALYSIS: Runaway Slave Advertisements (NY/NJ, 18th Century)")
    print("=" * 100)
    print()

    # Read data
    df = pd.read_csv(csv_file)
    print(f"Total advertisements: {len(df)}\n")

    # Initialize data structures
    self_named_cases = []
    preferred_name_cases = []
    name_origin_data = defaultdict(lambda: defaultdict(int))
    decade_totals = defaultdict(int)

    # Process each advertisement
    for idx, row in df.iterrows():
        content = str(row['Content'])
        date = str(row['Date '])

        year, decade = extract_year_decade(date)
        if not decade:
            continue

        decade_totals[decade] += 1

        # Extract name
        name = extract_name(content)

        # Check for self-naming
        is_self_named, self_naming_type, self_name = check_self_naming(content)
        if is_self_named:
            self_named_cases.append({
                'row': idx + 2,  # +2 for header and 1-indexing
                'date': date,
                'year': year,
                'decade': decade,
                'newspaper': row['Newspaper Name'],
                'issue': row['Issue No'],
                'name': name,
                'self_naming_type': self_naming_type,
                'self_name': self_name,
                'content': content[:300]
            })

        # Check for preferred names
        has_preferred, preferred_type, preferred_name = check_preferred_name(content)
        if has_preferred:
            preferred_name_cases.append({
                'row': idx + 2,
                'date': date,
                'year': year,
                'decade': decade,
                'newspaper': row['Newspaper Name'],
                'issue': row['Issue No'],
                'name': name,
                'preferred_type': preferred_type,
                'preferred_name': preferred_name,
                'content': content[:300]
            })

        # Categorize name origin
        if name:
            origin = categorize_name_origin(name)
            name_origin_data[decade][origin] += 1

    # Calculate percentages by decade
    print("TABLE 1: SELF-NAMING AND PREFERRED NAME PERCENTAGES BY DECADE")
    print("=" * 100)
    print(f"{'Decade':<10} {'Total':<8} {'Self-Named':<12} {'Self %':<10} {'Preferred':<12} {'Pref %':<10}")
    print("-" * 100)

    decade_stats = []
    for decade in sorted(decade_totals.keys()):
        total = decade_totals[decade]
        self_count = len([c for c in self_named_cases if c['decade'] == decade])
        pref_count = len([c for c in preferred_name_cases if c['decade'] == decade])

        self_pct = (self_count / total * 100) if total > 0 else 0
        pref_pct = (pref_count / total * 100) if total > 0 else 0

        print(
            f"{decade}s{' ':<6} {total:<8} {self_count:<12} {self_pct:>5.1f}%{' ':<4} {pref_count:<12} {pref_pct:>5.1f}%")

        decade_stats.append({
            'Decade': f"{decade}s",
            'Total_Ads': total,
            'Self_Named_Count': self_count,
            'Self_Named_Pct': f"{self_pct:.1f}%",
            'Preferred_Count': pref_count,
            'Preferred_Pct': f"{pref_pct:.1f}%"
        })

    # Print name origin statistics
    print("\n\nTABLE 2: NAME ORIGIN CATEGORIES BY DECADE")
    print("=" * 100)
    print(
        f"{'Decade':<10} {'Total':<8} {'African':<10} {'Biblical':<10} {'Classical':<12} {'Geographic':<12} {'Anglo/West':<12} {'Other':<10}")
    print("-" * 100)

    name_origin_stats = []
    for decade in sorted(decade_totals.keys()):
        total = decade_totals[decade]
        origins = name_origin_data[decade]

        african = origins.get('African', 0)
        biblical = origins.get('Biblical', 0)
        classical = origins.get('Classical', 0)
        geographic = origins.get('Geographic', 0)
        anglo = origins.get('Anglo/Western', 0)
        other = origins.get('Other', 0)

        african_pct = (african / total * 100) if total > 0 else 0
        biblical_pct = (biblical / total * 100) if total > 0 else 0
        classical_pct = (classical / total * 100) if total > 0 else 0
        geographic_pct = (geographic / total * 100) if total > 0 else 0
        anglo_pct = (anglo / total * 100) if total > 0 else 0
        other_pct = (other / total * 100) if total > 0 else 0

        print(f"{decade}s{' ':<6} {total:<8} {african_pct:>5.1f}%{' ':<4} {biblical_pct:>5.1f}%{' ':<4} "
              f"{classical_pct:>5.1f}%{' ':<6} {geographic_pct:>5.1f}%{' ':<6} {anglo_pct:>5.1f}%{' ':<6} {other_pct:>5.1f}%")

        name_origin_stats.append({
            'Decade': f"{decade}s",
            'Total': total,
            'African_Pct': f"{african_pct:.1f}%",
            'Biblical_Pct': f"{biblical_pct:.1f}%",
            'Classical_Pct': f"{classical_pct:.1f}%",
            'Geographic_Pct': f"{geographic_pct:.1f}%",
            'Anglo_Western_Pct': f"{anglo_pct:.1f}%",
            'Other_Pct': f"{other_pct:.1f}%"
        })

    # Print detailed lists
    print("\n\nSELF-NAMED CASES (Row Numbers)")
    print("=" * 100)
    print(f"Total cases found: {len(self_named_cases)}\n")

    for i, case in enumerate(self_named_cases, 1):
        print(f"{i}. ROW {case['row']} ({case['year']}) - {case['self_naming_type']}")
        if case['self_name']:
            print(f"   Self-name: {case['self_name']}")
        if case['name']:
            print(f"   Original name: {case['name']}")
        print(f"   Source: {case['newspaper']}, Issue {case['issue']}")

    print("\n\nPREFERRED/ALTERNATE NAME CASES (Row Numbers)")
    print("=" * 100)
    print(f"Total cases found: {len(preferred_name_cases)}\n")

    for i, case in enumerate(preferred_name_cases, 1):
        print(f"{i}. ROW {case['row']} ({case['year']}) - {case['preferred_type']}")
        print(f"   Names: {case['preferred_name']}")
        print(f"   Source: {case['newspaper']}, Issue {case['issue']}")

    # Save to CSV files
    df_decade_stats = pd.DataFrame(decade_stats)
    df_name_origins = pd.DataFrame(name_origin_stats)
    df_self_named = pd.DataFrame(self_named_cases)
    df_preferred = pd.DataFrame(preferred_name_cases)

    df_decade_stats.to_csv('self_naming_by_decade.csv', index=False)
    df_name_origins.to_csv('name_origins_by_decade.csv', index=False)
    df_self_named.to_csv('self_named_detailed.csv', index=False)
    df_preferred.to_csv('preferred_names_detailed.csv', index=False)

    print("\n\nFILES CREATED:")
    print("- self_naming_by_decade.csv")
    print("- name_origins_by_decade.csv")
    print("- self_named_detailed.csv")
    print("- preferred_names_detailed.csv")

    return {
        'self_named_cases': self_named_cases,
        'preferred_name_cases': preferred_name_cases,
        'decade_stats': decade_stats,
        'name_origin_stats': name_origin_stats
    }


if __name__ == "__main__":
    # Check if CSV file provided
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = "/Users/mirayozmutlu/Documents/GitHub/DH-Project---Runaway-Slave-Advertisements/_Pretends To Be Free_ - Runaway Slave Ads - Sheet1 (1).csv"

    try:
        results = analyze_self_naming(csv_file)
        print("\n\nAnalysis complete!")
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_file}")
        print("Usage: python analyze_self_naming.py [path_to_csv_file]")
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback

        traceback.print_exc()

