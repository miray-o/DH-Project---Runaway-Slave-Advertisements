import pandas as pd
import re
import matplotlib.pyplot as plt

# Read the data
df = pd.read_csv(
    "/Users/mirayozmutlu/Documents/GitHub/DH-Project---Runaway-Slave-Advertisements/_Pretends To Be Free_ - Runaway Slave Ads - Sheet1 (1).csv")


# Extract decade from date
def extract_decade(date_str):
    try:
        year_match = re.search(r'(\d{4})', str(date_str))
        if year_match:
            year = int(year_match.group(1))
            return (year // 10) * 10
    except:
        pass
    return None


df['decade'] = df['Date '].apply(extract_decade)
df = df.dropna(subset=['decade'])

# Count 'free' mentions per row
df['free_count'] = df['Content'].apply(lambda x: len(re.findall(r'\bfree\b', str(x), re.IGNORECASE)))

# Read name origins CSV once
name_origin_csv = pd.read_csv('name_origins_by_decade.csv')

# Aggregate by decade
decade_data = []
for decade in sorted(df['decade'].unique()):
    decade_df = df[df['decade'] == decade]
    total = len(decade_df)

    # Find the row for this decade
    decade_str = f"{int(decade)}s"
    origin_row = name_origin_csv[name_origin_csv['Decade'] == decade_str]

    if not origin_row.empty:
        # Extract percentages from CSV (remove '%' and convert to float)
        african_pct = float(origin_row['African_Pct'].values[0].strip('%'))
        western_pct = float(origin_row['Anglo_Western_Pct'].values[0].strip('%'))
    else:
        african_pct = 0
        western_pct = 0

    free_freq = decade_df['free_count'].sum() / total if total > 0 else 0

    decade_data.append({
        'Decade': decade_str,
        'African_Names_Pct': african_pct,
        'Western_Names_Pct': western_pct,
        'Free_Frequency': free_freq
    })

stats_df = pd.DataFrame(decade_data)

# Create line plot
fig, ax1 = plt.subplots(figsize=(12, 6))

# Plot percentages on left y-axis
ax1.plot(stats_df['Decade'], stats_df['African_Names_Pct'], marker='o', linewidth=2.5,
         label='African Names %', color='#FF6B6B', markersize=8)
ax1.plot(stats_df['Decade'], stats_df['Western_Names_Pct'], marker='s', linewidth=2.5,
         label='Western Names %', color='#4ECDC4', markersize=8)
ax1.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
ax1.set_xlabel('Decade', fontsize=12, fontweight='bold')
ax1.tick_params(axis='y', labelcolor='black')
ax1.grid(True, alpha=0.3)

# Create second y-axis for 'free' frequency
ax2 = ax1.twinx()
ax2.plot(stats_df['Decade'], stats_df['Free_Frequency'], marker='^', linewidth=2.5,
         label='"Free" Frequency', color='#95E1D3', markersize=8, linestyle='--')
ax2.set_ylabel('"Free" Mentions (per ad)', fontsize=12, fontweight='bold')
ax2.tick_params(axis='y', labelcolor='#95E1D3')

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=11)

plt.title('African Names, Western Names & "Free" Frequency by Decade', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()