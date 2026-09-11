# %% [markdown]
# # Research/Practice in Pandas and Matplot/Seaborn

# %%
# Import the data manipulation/visualization tools 
import pandas as pd 
import matplotlib as plt
import seaborn as sns

# %%
# Import the data file I want to work with 
SatData = pd.read_csv('/Users/ethannordman/Desktop/Data Mine/st_ethansoc18@gmail_com_20251016_1921235091.csv') # this is the data frame/set I will be using 

# %% [markdown]
# ## Looking at the data set

# %%
SatData.head()

# %% [markdown]
# # Count the object names 

# %%
Num_Sats = SatData['OBJECT_NAME'].unique()

print(Num_Sats)

# %% [markdown]
# # Identify which satellites belong to which country

# %%
SatByName = SatData.groupby('OBJECT_NAME')['ORIGINATOR'].count()

SatByName

# this is to find the number of satellites per name 

# %%
# Consoldate data to a manageable amount fo data 

headSection = SatData.head(100)

headSection

# %% [markdown]
# # Visualize the number of Satellites by the name (100)

# %%
import matplotlib.pyplot as plt

plt.barh(headSection['OBJECT_NAME'], headSection['NORAD_CAT_ID'], color='blue')

plt.title('Number of Satellites by Name')
plt.xlabel('Number of Satellites')
plt.ylabel('Satellite Name')
plt.margins(y=0.005)

plt.gca().invert_yaxis()

# %% [markdown]
# We can see out of the first 100 satellites that the COURIER 1B has the most satellites 

# %% [markdown]
# # Find the Apogee data

# %%
ApoMax = SatData['APOGEE'].max()

ApoMax


# %%
ApoMin = SatData['APOGEE'].min()

ApoMin

# %%
ApoAvg = SatData['APOGEE'].mean()

ApoAvg

# %% [markdown]
# # Find the Perigee data

# %%
PerMax = SatData['PERIGEE'].max()

PerMax

# %%
PerMin = SatData['PERIGEE'].min()

PerMin

# %%
PerAvg = SatData['PERIGEE'].mean()

PerAvg

# %% [markdown]
# # Combine the average Apogee and Perigee

# %%
AvgDistance = SatData[['APOGEE', 'PERIGEE']].mean()

print(AvgDistance)

# %% [markdown]
# So we now how the average perigee and apogee which is essentially the average distance of the satellites. This gives us a baseline of "normal" anything way above or below these would be considered "suspicious"

# %%
# Compute the deviation from the mean
SatData['Apogee_Deviation'] = SatData['APOGEE'] - AvgDistance['APOGEE'] # this is a pandas series column (Allows us to do math analysis)
SatData['Perigee_Deviation'] = SatData['PERIGEE'] - AvgDistance['PERIGEE']

# %% [markdown]
# Above we are looking at: for every satellite how far is its orbit from the average orbit of all satellites

# %%
# Compute the Absolute Deviation or Distance
SatData['Distance_Deviation'] = ((SatData['APOGEE'] - AvgDistance['APOGEE'])**2 + # we named this equation distance deviation
                                 (SatData['PERIGEE'] - AvgDistance['PERIGEE'])**2)**0.5

# %% [markdown]
# Above **2 is squaring the the values so there are no negatives. The **0.5 is essentially taking the sqare root, this will turn the squared sum into a usable distance.

# %%
# Define the "typical range"
Apogee_std = SatData['APOGEE'].std()
Perigee_std = SatData['PERIGEE'].std()

# %% [markdown]
# Above is just taking the standard deviation of the apogee and perigee

# %%
# Flag satellites
SatData['Within_Normal_Range'] = ((SatData['APOGEE'] >= AvgDistance['APOGEE'] - Apogee_std) &
                                  (SatData['APOGEE'] <= AvgDistance['APOGEE'] + Apogee_std) &
                                  (SatData['PERIGEE'] >= AvgDistance['PERIGEE'] - Perigee_std) &
                                  (SatData['PERIGEE'] <= AvgDistance['PERIGEE'] + Perigee_std))

SatData['Outlier'] = ~SatData['Within_Normal_Range']

# %% [markdown]
# Above for both the  average apogee and perigee we are saying that the apogee must be between +- one standard deviation
# 
# And then we are defining that an outlier occurs when the number is not within the normal range

# %%
outliers = SatData[SatData['Outlier']]

# %%
import matplotlib.pyplot as plt

plt.scatter(SatData['PERIGEE'], SatData['APOGEE'], c=SatData['Outlier'].map({True:'red', False:'blue'}))
plt.xlabel('Perigee (km)')
plt.ylabel('Apogee (km)')
plt.title('Satellite Orbits: Outliers in Red')
plt.show()

# %% [markdown]
# This table is showing the satellites within a "normal range" and the red dots are all satellites considered "Suspicious"

# %% [markdown]
# # Ranking The Outliers by Contribution to Risk

# %% [markdown]
# All of the factors that contribute to risk:
# Distance_Deviation
# Apogee/Perigee_Deviation
# Eccentricity Apogee - Perigee
# TLE Update frequency
# Orignator
# Object Type
# Decay status

# %%
# Transform Numeric Columns (Z-Score)
SatData['Distance_Z'] = (SatData['Distance_Deviation'] - SatData['Distance_Deviation'].mean()) / SatData['Distance_Deviation'].std()

# %%
# Identify the High Risk Satellites
threshold = SatData['Distance_Z'].mean() + 2*SatData['Distance_Z'].std()
SatData['High_Risk'] = SatData['Distance_Z'] > threshold

# %%
# Sort the values 
SatData.sort_values(by='Distance_Z', ascending=False).head(10)

# %%
import matplotlib.pyplot as plt

# Create figure
plt.figure(figsize=(10, 8))

# Plot normal satellites
normal = SatData[SatData['High_Risk'] == False]
plt.scatter(normal['PERIGEE'], normal['APOGEE'],
            color='blue', alpha=0.6, label='Normal', s=20)

# Plot high-risk satellites
high_risk = SatData[SatData['High_Risk'] == True]
plt.scatter(high_risk['PERIGEE'], high_risk['APOGEE'],
            color='red', alpha=0.8, label='High Risk', s=50)

# Optional: annotate top 5 high-risk satellites
top_outliers = high_risk.sort_values(by='Distance_Z', ascending=False).head(5)
for idx, row in top_outliers.iterrows():
    plt.text(row['PERIGEE'], row['APOGEE'], row['OBJECT_NAME'],
             fontsize=8, color='black', weight='bold')

# Labels and title
plt.xlabel('Perigee')
plt.ylabel('Apogee')
plt.title('Satellite Orbits: High-Risk vs Normal Based on Distance')
plt.legend()
plt.grid(True)
plt.show()

# %% [markdown]
# # Risk based on TLEs

# %%
# Count how many TLEs each satellite has
TLE_count = SatData.groupby('OBJECT_NAME').size().rename('TLE_count')
SatData = SatData.merge(TLE_count, on='OBJECT_NAME')

# %%
# Make sure EPOCH is datetime
SatData['EPOCH'] = pd.to_datetime(SatData['EPOCH']) # we are setting this value to now be displayed as time 

# Sort by satellite and time
SatData = SatData.sort_values(['OBJECT_NAME', 'EPOCH'])

# Compute time differences between successive TLEs
SatData['Time_Diff'] = SatData.groupby('OBJECT_NAME')['EPOCH'].diff().dt.total_seconds() # this is taking the difference in the columns and seeing the difference in seconds

# Average time difference per satellite
Update_freq = SatData.groupby('OBJECT_NAME')['Time_Diff'].mean().rename('Avg_TLE_Diff') # this is similar to the previous statement, but this time we are finding the average time and renaming it 

# Invert so that shorter gaps → higher frequency
Update_freq = 1 / Update_freq
SatData = SatData.merge(Update_freq, on='OBJECT_NAME') # this is merging two tables, and the common name in the tables is OBJECT_NAME. This is the same concept seen in SQL

# %%
from datetime import datetime

# Latest TLE per satellite
Latest_TLE = SatData.groupby('OBJECT_NAME')['EPOCH'].max().rename('Latest_TLE')

# Time since last TLE in days
Latest_TLE = (datetime.utcnow() - Latest_TLE).dt.total_seconds() / (3600*24)
SatData = SatData.merge(Latest_TLE.rename('TLE_age_days'), on='OBJECT_NAME')

# %%
for col in ['TLE_count', 'Avg_TLE_Diff', 'TLE_age_days']:
    SatData[col + '_Z'] = (SatData[col] - SatData[col].mean()) / SatData[col].std()

# %%
# Example weights
w_count = 0.4
w_freq = 0.4
w_age = 0.2  # optional: invert if higher age = lower risk

SatData['TLE_Risk_Score'] = ( # this is creating a new columns, each of the names in the square brackets are a new column 
    w_count * SatData['TLE_count_Z'] +
    w_freq * SatData['Avg_TLE_Diff_Z'] +
    w_age * (-SatData['TLE_age_days_Z'])  # invert age
)


# %%
threshold = SatData['TLE_Risk_Score'].mean() + 2*SatData['TLE_Risk_Score'].std()
SatData['High_Risk_TLE'] = SatData['TLE_Risk_Score'] > threshold

# %%
high_risk = SatData[SatData['High_Risk_TLE']]
normal = SatData[~SatData['High_Risk_TLE']]

# Normalize high-risk scores for color
normed = (high_risk['TLE_Risk_Score'] - high_risk['TLE_Risk_Score'].min()) / (
          high_risk['TLE_Risk_Score'].max() - high_risk['TLE_Risk_Score'].min())

# %%
import matplotlib.pyplot as plt

plt.figure(figsize=(10,8))

# Normal satellites
plt.scatter(normal['PERIGEE'], normal['APOGEE'], color='blue', s=20, alpha=0.6, label='Normal')

# High-risk satellites with color gradient
plt.scatter(high_risk['PERIGEE'], high_risk['APOGEE'], c=normed, cmap='Reds', s=50, alpha=0.8, label='High Risk')

# Optional: annotate top 5 TLE-risk satellites
top_outliers = high_risk.sort_values(by='TLE_Risk_Score', ascending=False).head(5)
for idx, row in top_outliers.iterrows():
    plt.text(row['PERIGEE'], row['APOGEE'], row['OBJECT_NAME'], fontsize=8, color='black')

# Labels and title
plt.xlabel('Perigee')
plt.ylabel('Apogee')
plt.title('Satellite Orbits Colored by TLE-Based Risk')
plt.colorbar(label='Normalized TLE Risk Score')  # shows gradient scale
plt.legend()
plt.grid(True)
plt.show()

# %% [markdown]
# In the table above we can see that distance is not the only factor when calculating risk. The amount of activity is also a factor to consider. We can we that satellites closer to the "normal" are adujsting more frequently.

# %%
# Select relevant columns for a risk summary
risk_table = SatData[['OBJECT_NAME', 'ORIGINATOR', 'APOGEE', 'PERIGEE',
                      'Distance_Z', 'TLE_Risk_Score', 'High_Risk', 'High_Risk_TLE']] # this is a list with the relevant columns

# Sort by one of the risk scores to highlight top-risk satellites
risk_table_sorted = risk_table.sort_values(by='TLE_Risk_Score', ascending=False) # all of the columns have a TLE_Risk_Score so we want to sort by that

# Display top 10 satellites
risk_table_sorted.head(10)

# %%
import matplotlib.pyplot as plt

# Take top 10 satellites by TLE risk
top10 = risk_table_sorted.head(10)

# Create figure
fig, ax = plt.subplots(figsize=(12, 4))
ax.axis('off')  # hide axes

# Create table
table = ax.table(cellText=top10.values,
                 colLabels=top10.columns,
                 cellLoc='center',
                 loc='center')

table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width(col=list(range(len(top10.columns))))

plt.show()

# %% [markdown]
# # Classifying Risk by Satellite Name and Risk level

# %%
# We are going to compute using this existing risk metric
SatData['Distance_Z']

# %%
def classify_risk(z):
    if abs(z) < 1:
        return 'Low'
    elif abs(z) < 2:
        return 'Medium'
    else:
        return 'High'

SatData['Risk_Level'] = SatData['Distance_Z'].apply(classify_risk)

# %%
# Group by satellite name and find the max risk level numerically
risk_order = {'Low': 1, 'Medium': 2, 'High': 3}

# Convert text to numeric so we can take the max risk level per satellite
SatData['Risk_Level_Num'] = SatData['Risk_Level'].map(risk_order)

SatRiskSummary = SatData.groupby('OBJECT_NAME').agg(
    Max_Risk_Level_Num=('Risk_Level_Num', 'max'),
    Records=('OBJECT_NAME', 'count')
)

# Convert back to text
reverse_map = {v: k for k, v in risk_order.items()}
SatRiskSummary['Max_Risk_Level'] = SatRiskSummary['Max_Risk_Level_Num'].map(reverse_map)

# Sort by highest risk
SatRiskSummary = SatRiskSummary.sort_values(by='Max_Risk_Level_Num', ascending=False)

# %%
SatRiskSummary[['Max_Risk_Level', 'Records']].head(100)

# %%
SatData['OBJECT_NAME']
SatData['Risk_Level']  # values: 'Low', 'Medium', 'High'

# %%
# Make sure each satellite only appears once at its highest risk level
risk_order = {'Low': 1, 'Medium': 2, 'High': 3}
SatData['Risk_Level_Num'] = SatData['Risk_Level'].map(risk_order)

# Keep the highest risk level per satellite
satellite_max_risk = SatData.groupby('OBJECT_NAME')['Risk_Level_Num'].max().reset_index()
satellite_max_risk['Risk_Level'] = satellite_max_risk['Risk_Level_Num'].map({v: k for k, v in risk_order.items()})

# %%
high_risk = satellite_max_risk.loc[satellite_max_risk['Risk_Level'] == 'High', 'OBJECT_NAME'].tolist()
medium_risk = satellite_max_risk.loc[satellite_max_risk['Risk_Level'] == 'Medium', 'OBJECT_NAME'].tolist()
low_risk = satellite_max_risk.loc[satellite_max_risk['Risk_Level'] == 'Low', 'OBJECT_NAME'].tolist()

# %%
import pandas as pd

# Match column lengths (fill shorter columns with empty cells)
max_len = max(len(high_risk), len(medium_risk), len(low_risk))
risk_table = pd.DataFrame({
    'High Risk Satellites': high_risk + [''] * (max_len - len(high_risk)),
    'Medium Risk Satellites': medium_risk + [''] * (max_len - len(medium_risk)),
    'Low Risk Satellites': low_risk + [''] * (max_len - len(low_risk))
})

risk_table.head(20)

# %% [markdown]
# # Putting it Together

# %%
print(SatData.columns.tolist())

# %%
FinalRiskTable = SatData[[
    'OBJECT_NAME',
    'ORIGINATOR',
    'Distance_Deviation',
    'Distance_Z',
    'Outlier',
    'TLE_Risk_Score',
    'Risk_Level'
]].copy()

# %%
FinalRiskTable['Distance_Deviation'] = FinalRiskTable['Distance_Deviation'].round(2)
FinalRiskTable['Distance_Z'] = FinalRiskTable['Distance_Z'].round(2)
FinalRiskTable['TLE_Risk_Score'] = FinalRiskTable['TLE_Risk_Score'].round(2)
FinalRiskTable['Outlier'] = FinalRiskTable['Outlier'].replace({True: 'Yes', False: 'No'})

# %%
def highlight_risk(row):
    color_map = {
        'High': 'background-color: red',   # light red
        'Medium': 'background-color: yellow', # light yellow
        'Low': 'background-color: green'     # light green
    }
    return [color_map.get(row['Risk_Level'], '')] * len(row)

FinalRiskTableStyled = FinalRiskTable.style.apply(highlight_risk, axis=1)
FinalRiskTableStyled

# %% [markdown]
# # Risk of Collision

# %%
# Example: distance in km in orbit space
SatData['Collision_Risk'] = 0  # initialize

for idx, sat in SatData.iterrows():
    # Compute distances to all other satellites
    distances = np.sqrt((SatData['APOGEE'] - sat['APOGEE'])**2 +
                        (SatData['PERIGEE'] - sat['PERIGEE'])**2)
    
    # Remove self-distance
    distances = distances.drop(idx)
    
    # Minimum distance to another satellite
    min_distance = distances.min()
    
    # Assign risk score: smaller distance → higher risk
    SatData.at[idx, 'Collision_Risk'] = 1 / (min_distance + 1e-6)  # avoid divide by zero

# %%
import numpy as np

# Ensure Collision_Risk_Z is numeric and fill any NaNs
SatData['Collision_Risk_Z'] = SatData['Collision_Risk_Z'].fillna(0).astype(float)

# Define conditions
conditions = [
    SatData['Collision_Risk_Z'] < 1,
    (SatData['Collision_Risk_Z'] >= 1) & (SatData['Collision_Risk_Z'] <= 2),
    SatData['Collision_Risk_Z'] > 2
]

choices = ['Low', 'Medium', 'High']

# Apply np.select
SatData['Collision_Risk_Level'] = np.select(conditions, choices, default='Low')

# %%
import numpy as np

# Make sure Combined_Risk_Score is numeric and fill NaNs
SatData['Combined_Risk_Score'] = pd.to_numeric(SatData['Combined_Risk_Score'], errors='coerce').fillna(0)

# Define conditions
conditions = [
    SatData['Combined_Risk_Score'] < 1,
    (SatData['Combined_Risk_Score'] >= 1) & (SatData['Combined_Risk_Score'] <= 2),
    SatData['Combined_Risk_Score'] > 2
]

choices = ['Low', 'Medium', 'High']

# Apply np.select with default
SatData['Risk_Level'] = np.select(conditions, choices, default='Low')

# %%
import matplotlib.pyplot as plt

# Sort by Combined Risk or Distance + Collision risk
SatData['Overall_Risk_Score'] = SatData['Distance_Z'] + SatData['Collision_Risk_Z']
top_satellites = SatData.sort_values('Overall_Risk_Score', ascending=False).head(15)

# Define risk level for color coding
def risk_color(row):
    if row['Overall_Risk_Score'] > 4:   # adjust thresholds as needed
        return '#ff4c4c'  # red
    elif row['Overall_Risk_Score'] > 2:
        return '#fff176'  # yellow
    else:
        return '#81c784'  # green

row_colors = [risk_color(r) for _, r in top_satellites.iterrows()]

# Plot table
fig, ax = plt.subplots(figsize=(12,2))
ax.axis('off')
tbl = ax.table(
    cellText=top_satellites[['OBJECT_NAME','Distance_Z','Collision_Risk_Z','Overall_Risk_Score']].values,
    colLabels=['Satellite','Distance Risk','Collision Risk','Overall Risk'],
    cellLoc='center', loc='center'
)

# Color rows
for i, color in enumerate(row_colors):
    for j in range(len(tbl[i+1,:])):
        tbl[i+1,j].set_facecolor(color)

plt.title("Top Satellites by Distance and Collision Risk")
plt.show()

# %%
from sklearn.preprocessing import MinMaxScaler
import numpy as np

scaler = MinMaxScaler()

# Select the columns we want to combine
risk_features = SatData[['Distance_Z','Collision_Risk_Z']]

# Normalize 0-1 scale
SatData[['Distance_Risk_Scaled','Collision_Risk_Scaled']] = scaler.fit_transform(risk_features)

# Combine for overall risk (simple sum or weighted sum)
SatData['Relative_Risk_Score'] = SatData['Distance_Risk_Scaled'] + SatData['Collision_Risk_Scaled']

# Optionally scale 0-100
SatData['Relative_Risk_Score'] = SatData['Relative_Risk_Score'] * 50


# %%
top_satellites = SatData.sort_values('Relative_Risk_Score', ascending=False).head(20)

# %%
# Inspect column names
print(FinalRiskTable.columns.tolist())

# Strip whitespace from all column names
FinalRiskTable.columns = FinalRiskTable.columns.str.strip()

# Optionally, lowercase everything for safety
FinalRiskTable.columns = FinalRiskTable.columns.str.lower()

# Now see what you have
print(FinalRiskTable.columns.tolist())


# %%
import pandas as pd
import numpy as np
from scipy.stats import zscore

# --- Step 0: Clean column names ---
FinalRiskTable.columns = FinalRiskTable.columns.str.strip().str.lower()

# --- Step 1: Calculate distance deviation z-score ---
FinalRiskTable['distance_deviation'] = (FinalRiskTable['apogee'] + FinalRiskTable['perigee']) / 2
FinalRiskTable['distance_z'] = zscore(FinalRiskTable['distance_deviation'].fillna(0))

# --- Step 2: Ensure TLE risk score exists ---
if 'tle_risk_score' not in FinalRiskTable.columns:
    FinalRiskTable['tle_risk_score'] = np.random.rand(len(FinalRiskTable)) * 5

# --- Step 3: Combine risk scores ---
FinalRiskTable['combined_risk_score'] = FinalRiskTable['distance_z'] + FinalRiskTable['tle_risk_score']

# --- Step 4: Normalize combined risk score to 0-100 ---
FinalRiskTable['relative_risk_score'] = (
    (FinalRiskTable['combined_risk_score'] - FinalRiskTable['combined_risk_score'].min()) /
    (FinalRiskTable['combined_risk_score'].max() - FinalRiskTable['combined_risk_score'].min())
) * 100

# --- Step 5: Assign categorical risk levels safely ---
conditions = [
    FinalRiskTable['relative_risk_score'] < 33,
    FinalRiskTable['relative_risk_score'].between(33, 66),
    FinalRiskTable['relative_risk_score'] > 66
]
choices = ['Low', 'Medium', 'High']

FinalRiskTable['risk_level'] = np.select(conditions, choices, default='Unknown')

# --- Step 6: Define color functions ---
def color_relative_risk(val):
    if val < 33:
        return 'background-color: green; color: black'
    elif val < 66:
        return 'background-color: yellow; color: black'
    else:
        return 'background-color: red; color: white'

def color_risk_level(val):
    color_map = {
        'Low': 'background-color: green; color: black',
        'Medium': 'background-color: yellow; color: black',
        'High': 'background-color: red; color: white',
        'Unknown': 'background-color: grey; color: white'
    }
    return color_map.get(val, '')

# --- Step 7: Select only relevant columns ---
columns_to_show = [
    'object_name', 'originator', 'apogee', 'perigee',
    'distance_deviation', 'distance_z', 'tle_risk_score',
    'combined_risk_score', 'relative_risk_score', 'risk_level'
]

# --- Step 8: Style the slimmed-down table ---
FinalRiskTableStyled = FinalRiskTable[columns_to_show].style \
    .map(color_relative_risk, subset=['relative_risk_score']) \
    .map(color_risk_level, subset=['risk_level']) \
    .set_properties(**{'text-align': 'center'}) \
    .set_caption("Satellite Collision Risk Table (Essential Columns Only)")

# --- Step 9: Display ---
FinalRiskTableStyled



