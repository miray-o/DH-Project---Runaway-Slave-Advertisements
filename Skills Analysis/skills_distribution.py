"""
Skills Analysis for Runaway Slave Advertisements
Analyzes literacy, mechanical, and musical skills as routes to economic independence
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
        r'named? ([A-Z][a-z]+)',
        r'called ([A-Z][a-z]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None


def check_literacy(content):
    """Check for literacy skills in advertisement"""
    content_lower = content.lower()

    literacy_patterns = [
        r'can read',
        r'can write',
        r'read and write',
        r'reads? (?:and )?(?:writes?)?(?:\s+(?:good|well|tolerably|pretty))?',
        r'writing',
        r'literate',
        r'cypher'  # Mathematical literacy
    ]

    for pattern in literacy_patterns:
        match = re.search(pattern, content_lower)
        if match:
            # Get context around the match
            context_match = re.search(f'.{{0,70}}{pattern}.{{0,70}}', content_lower)
            context = context_match.group(0).strip() if context_match else match.group(0)
            return True, context

    return False, None


def check_mechanical_skills(content):
    """Check for mechanical/trade skills in advertisement"""
    content_lower = content.lower()

    mechanical_patterns = [
        (r'carpenter|house-carpenter|ship-carpenter', 'Carpenter'),
        (r'blacksmith', 'Blacksmith'),
        (r'cooper', 'Cooper'),
        (r'shoemaker|cordwainer', 'Shoemaker'),
        (r'tailor', 'Tailor'),
        (r'wheelwright', 'Wheelwright'),
        (r'mason', 'Mason'),
        (r'farming work|farm work|all sorts of farming|husbandry|plantation(?:\s+work)?', 'Farming'),
        (r'sawyer', 'Sawyer'),
        (r'joiner', 'Joiner'),
        (r'barber', 'Barber'),
        (r'caulker', 'Caulker'),
        (r'weaver', 'Weaver')
    ]

    for pattern, skill_name in mechanical_patterns:
        match = re.search(pattern, content_lower)
        if match:
            # Get context around the match
            context_match = re.search(f'.{{0,70}}{pattern}.{{0,70}}', content_lower)
            context = context_match.group(0).strip() if context_match else match.group(0)
            return True, skill_name, context

    return False, None, None


def check_musical_skills(content):
    """Check for musical skills in advertisement"""
    content_lower = content.lower()

    musical_patterns = [
        (r'plays? (?:well )?(?:on |upon )?(?:the )?fiddle|fiddl(?:e|er|ing)', 'Fiddle'),
        (r'plays? (?:well )?(?:on |upon )?(?:the )?(?:flute|fife)', 'Flute/Fife'),
        (r'plays? (?:well )?(?:on |upon )?(?:the )?violin', 'Violin'),
        (r'drum(?:mer)?', 'Drum'),
    ]

    for pattern, skill_name in musical_patterns:
        match = re.search(pattern, content_lower)
        if match:
            # Get context around the match
            context_match = re.search(f'.{{0,70}}{pattern}.{{0,70}}', content_lower)
            context = context_match.group(0).strip() if context_match else match.group(0)
            return True, skill_name, context

    return False, None, None


def analyze_skills(csv_file):
    """Main analysis function"""
    print("=" * 100)
    print("SKILLS ANALYSIS: Runaway Slave Advertisements (NY/NJ, 18th Century)")
    print("Literacy, Mechanical, and Musical Skills as Routes to Economic Independence")
    print("=" * 100)
    print()

    # Read data
    df = pd.read_csv(csv_file)
    print(f"Total advertisements: {len(df)}\n")

    # Initialize data structures
    literacy_cases = []
    mechanical_cases = []
    musical_cases = []
    all_skilled_cases = []

    decade_totals = defaultdict(int)
    decade_literacy = defaultdict(int)
    decade_mechanical = defaultdict(int)
    decade_musical = defaultdict(int)
    decade_multi_skilled = defaultdict(int)

    mechanical_skill_types = defaultdict(int)
    musical_skill_types = defaultdict(int)

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

        # Check for skills
        has_literacy, literacy_context = check_literacy(content)
        has_mechanical, mechanical_type, mechanical_context = check_mechanical_skills(content)
        has_musical, musical_type, musical_context = check_musical_skills(content)

        # Count skills
        skill_count = sum([has_literacy, has_mechanical, has_musical])

        # Record literacy cases
        if has_literacy:
            decade_literacy[decade] += 1
            literacy_cases.append({
                'row': idx + 2,
                'date': date,
                'year': year,
                'decade': decade,
                'newspaper': row['Newspaper Name'],
                'name': name,
                'context': literacy_context,
                'full_content': content[:300]
            })

        # Record mechanical cases
        if has_mechanical:
            decade_mechanical[decade] += 1
            mechanical_skill_types[mechanical_type] += 1
            mechanical_cases.append({
                'row': idx + 2,
                'date': date,
                'year': year,
                'decade': decade,
                'newspaper': row['Newspaper Name'],
                'name': name,
                'skill_type': mechanical_type,
                'context': mechanical_context,
                'full_content': content[:300]
            })

        # Record musical cases
        if has_musical:
            decade_musical[decade] += 1
            musical_skill_types[musical_type] += 1
            musical_cases.append({
                'row': idx + 2,
                'date': date,
                'year': year,
                'decade': decade,
                'newspaper': row['Newspaper Name'],
                'name': name,
                'skill_type': musical_type,
                'context': musical_context,
                'full_content': content[:300]
            })

        # Record all skilled individuals
        if has_literacy or has_mechanical or has_musical:
            is_multi_skilled = skill_count >= 2
            if is_multi_skilled:
                decade_multi_skilled[decade] += 1

            all_skilled_cases.append({
                'row': idx + 2,
                'year': year,
                'decade': decade,
                'name': name,
                'literacy': 'Yes' if has_literacy else 'No',
                'mechanical': mechanical_type if has_mechanical else 'No',
                'musical': musical_type if has_musical else 'No',
                'multi_skilled': 'Yes' if is_multi_skilled else 'No',
                'skill_count': skill_count
            })

    # Print summary statistics
    print("SUMMARY STATISTICS")
    print("=" * 100)
    print(f"Total literacy cases: {len(literacy_cases)} ({len(literacy_cases) / len(df) * 100:.1f}%)")
    print(f"Total mechanical skills cases: {len(mechanical_cases)} ({len(mechanical_cases) / len(df) * 100:.1f}%)")
    print(f"Total musical skills cases: {len(musical_cases)} ({len(musical_cases) / len(df) * 100:.1f}%)")
    print(
        f"Total multi-skilled cases: {sum(decade_multi_skilled.values())} ({sum(decade_multi_skilled.values()) / len(df) * 100:.1f}%)")

    # Print decade breakdown
    print("\n\nTABLE 1: SKILLS BY DECADE (PERCENTAGES)")
    print("=" * 100)
    print(
        f"{'Decade':<10} {'Total':<8} {'Literacy':<12} {'Lit %':<10} {'Mechanical':<12} {'Mech %':<10} {'Musical':<12} {'Mus %':<10} {'Multi':<10} {'Multi %':<10}")
    print("-" * 100)

    decade_stats = []
    for decade in sorted(decade_totals.keys()):
        total = decade_totals[decade]
        lit = decade_literacy[decade]
        mech = decade_mechanical[decade]
        mus = decade_musical[decade]
        multi = decade_multi_skilled[decade]

        lit_pct = (lit / total * 100) if total > 0 else 0
        mech_pct = (mech / total * 100) if total > 0 else 0
        mus_pct = (mus / total * 100) if total > 0 else 0
        multi_pct = (multi / total * 100) if total > 0 else 0

        print(f"{decade}s{' ':<6} {total:<8} {lit:<12} {lit_pct:>5.1f}%{' ':<4} {mech:<12} {mech_pct:>5.1f}%{' ':<4} "
              f"{mus:<12} {mus_pct:>5.1f}%{' ':<4} {multi:<10} {multi_pct:>5.1f}%")

        decade_stats.append({
            'Decade': f"{decade}s",
            'Total_Ads': total,
            'Literacy_Count': lit,
            'Literacy_Pct': f"{lit_pct:.1f}%",
            'Mechanical_Count': mech,
            'Mechanical_Pct': f"{mech_pct:.1f}%",
            'Musical_Count': mus,
            'Musical_Pct': f"{mus_pct:.1f}%",
            'Multi_Skilled_Count': multi,
            'Multi_Skilled_Pct': f"{multi_pct:.1f}%"
        })

    # Print mechanical skills breakdown
    print("\n\nTABLE 2: MECHANICAL SKILLS DISTRIBUTION")
    print("=" * 100)
    print(f"{'Skill Type':<20} {'Count':<10} {'Percentage':<15}")
    print("-" * 100)

    total_mechanical = len(mechanical_cases)
    for skill_type, count in sorted(mechanical_skill_types.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_mechanical * 100) if total_mechanical > 0 else 0
        print(f"{skill_type:<20} {count:<10} {pct:>5.1f}%")

    # Print musical skills breakdown
    print("\n\nTABLE 3: MUSICAL SKILLS DISTRIBUTION")
    print("=" * 100)
    print(f"{'Skill Type':<20} {'Count':<10} {'Percentage':<15}")
    print("-" * 100)

    total_musical = len(musical_cases)
    for skill_type, count in sorted(musical_skill_types.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total_musical * 100) if total_musical > 0 else 0
        print(f"{skill_type:<20} {count:<10} {pct:>5.1f}%")

    # Print detailed literacy cases
    print("\n\nLITERACY CASES (Row Numbers)")
    print("=" * 100)
    print(f"Total cases: {len(literacy_cases)}\n")

    for i, case in enumerate(literacy_cases[:20], 1):  # First 20
        print(f"{i}. ROW {case['row']} ({case['year']})")
        if case['name']:
            print(f"   Name: {case['name']}")
        print(f"   Source: {case['newspaper']}")
        print(f"   Evidence: \"{case['context']}\"")
        print()

    if len(literacy_cases) > 20:
        print(f"   ... and {len(literacy_cases) - 20} more cases")

    # Print detailed mechanical cases
    print("\n\nMECHANICAL SKILLS CASES (Row Numbers)")
    print("=" * 100)
    print(f"Total cases: {len(mechanical_cases)}\n")

    for i, case in enumerate(mechanical_cases[:20], 1):  # First 20
        print(f"{i}. ROW {case['row']} ({case['year']}) - {case['skill_type']}")
        if case['name']:
            print(f"   Name: {case['name']}")
        print(f"   Source: {case['newspaper']}")
        print(f"   Evidence: \"{case['context']}\"")
        print()

    if len(mechanical_cases) > 20:
        print(f"   ... and {len(mechanical_cases) - 20} more cases")

    # Print detailed musical cases
    print("\n\nMUSICAL SKILLS CASES (Row Numbers)")
    print("=" * 100)
    print(f"Total cases: {len(musical_cases)}\n")

    for i, case in enumerate(musical_cases[:20], 1):  # First 20
        print(f"{i}. ROW {case['row']} ({case['year']}) - {case['skill_type']}")
        if case['name']:
            print(f"   Name: {case['name']}")
        print(f"   Source: {case['newspaper']}")
        print(f"   Evidence: \"{case['context']}\"")
        print()

    if len(musical_cases) > 20:
        print(f"   ... and {len(musical_cases) - 20} more cases")

    # Print multi-skilled individuals
    multi_skilled = [c for c in all_skilled_cases if c['multi_skilled'] == 'Yes']
    print("\n\nMULTI-SKILLED INDIVIDUALS (2+ Skill Types)")
    print("=" * 100)
    print(f"Total cases: {len(multi_skilled)}\n")

    for i, case in enumerate(multi_skilled, 1):
        skills = []
        if case['literacy'] == 'Yes':
            skills.append('Literacy')
        if case['mechanical'] != 'No':
            skills.append(f"Mechanical ({case['mechanical']})")
        if case['musical'] != 'No':
            skills.append(f"Musical ({case['musical']})")

        print(f"{i}. ROW {case['row']} ({case['year']}) - {case['name'] if case['name'] else 'Unknown'}")
        print(f"   Skills: {' + '.join(skills)}")
        print()

    # Save to CSV files
    df_decade_stats = pd.DataFrame(decade_stats)
    df_literacy = pd.DataFrame(literacy_cases)
    df_mechanical = pd.DataFrame(mechanical_cases)
    df_musical = pd.DataFrame(musical_cases)
    df_all_skilled = pd.DataFrame(all_skilled_cases)

    df_decade_stats.to_csv('skills_by_decade.csv', index=False)
    df_literacy.to_csv('literacy_cases_detailed.csv', index=False)
    df_mechanical.to_csv('mechanical_cases_detailed.csv', index=False)
    df_musical.to_csv('musical_cases_detailed.csv', index=False)
    df_all_skilled.to_csv('all_skilled_individuals.csv', index=False)

    print("\n\nFILES CREATED:")
    print("- skills_by_decade.csv")
    print("- literacy_cases_detailed.csv")
    print("- mechanical_cases_detailed.csv")
    print("- musical_cases_detailed.csv")
    print("- all_skilled_individuals.csv")

    return {
        'literacy_cases': literacy_cases,
        'mechanical_cases': mechanical_cases,
        'musical_cases': musical_cases,
        'multi_skilled': multi_skilled,
        'decade_stats': decade_stats
    }


if __name__ == "__main__":
    # Check if CSV file provided
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = "/Users/mirayozmutlu/Documents/GitHub/DH-Project---Runaway-Slave-Advertisements/_Pretends To Be Free_ - Runaway Slave Ads - Sheet1 (1).csv"

    try:
        results = analyze_skills(csv_file)
        print("\n\nAnalysis complete!")
    except FileNotFoundError:
        print(f"Error: Could not find file {csv_file}")
        print("Usage: python analyze_skills.py [path_to_csv_file]")
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback

        traceback.print_exc()