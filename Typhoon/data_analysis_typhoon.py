"""Exploratory analysis of JMA typhoon landfall sequences and Open-Meteo weather.

Run from the Typhoon project (or any working directory):
    python -B data_analysis_typhoon.py
Plots and the IQR table are written to Typhoon/plots/.
"""
from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'processed' / 'jma_day3_to_landfall_with_weather_prefecture.csv'
OUT = ROOT / 'plots'
OUT.mkdir(exist_ok=True)
if not DATA.exists():
    raise FileNotFoundError(f'Processed dataset missing: {DATA}')
df = pd.read_csv(DATA, low_memory=False)
print(f'Loaded {len(df):,} rows, {len(df.columns)} columns from {DATA}')

# Select interpretable weather measurements, excluding administrative/JMA metadata.
features = [x for x in [
    'temperature_2m_mean', 'relative_humidity_2m_mean', 'dew_point_2m_mean',
    'rain_sum','precipitation_sum','cloud_cover_mean', 'pressure_msl_mean',
    'wind_speed_10m_mean','wind_gusts_10m_mean','shortwave_radiation_sum',
    'openmeteo_elevation'
] if x in df]
for col in features:
    df[col] = pd.to_numeric(df[col], errors='coerce')
plt.rcParams.update({'figure.dpi':110,'savefig.dpi':160,'font.size':9})

def save(name):
    plt.tight_layout()
    plt.savefig(OUT / name, bbox_inches='tight')
    plt.close()
    print('Saved', name)

# 1. Tukey 1.5-IQR boxplots (untrimmed data)
cols = 3
rows = math.ceil(len(features)/cols)
fig, axes = plt.subplots(rows, cols, figsize=(15, rows*3.2))
for ax, feat in zip(np.array(axes).flatten(), features):
    vals = df[feat].dropna()
    if not vals.empty: ax.boxplot(vals, vert=True, showfliers=True)
    ax.set_title(feat);ax.set_xticks([]);ax.grid(axis='y', alpha=.2)
for ax in np.array(axes).flatten()[len(features):]: ax.axis('off')
fig.suptitle('Typhoon: Weather Attributes and IQR Outliers', fontsize=15, y=1.01)
save('typhoon_boxplots.png')

# 2. Numeric distributions
fig, axes = plt.subplots(rows, cols, figsize=(15, rows*3.2))
for ax, feat in zip(np.array(axes).flatten(), features):
    v=df[feat].dropna()
    if len(v):ax.hist(v, bins=min(35,max(8,int(np.sqrt(len(v))))),edgecolor='white')
    ax.set_title(feat);ax.set_ylabel('Count')
for ax in np.array(axes).flatten()[len(features):]: ax.axis('off')
fig.suptitle('Typhoon: Weather Feature Distributions',fontsize=15,y=1.01)
save('typhoon_distributions.png')

# 3. Missing percent of weather features plus prefecture/risk metadata
cols_check=features+[x for x in ['nearest_prefecture','risk','landfall_event_id'] if x in df]
missing=df[cols_check].isna().mean().sort_values(ascending=False)*100
fig,ax=plt.subplots(figsize=(11,max(4,len(missing)*.35)))
ax.barh(missing.index[::-1],missing.values[::-1]);ax.set_xlabel('Missing values (%)')
ax.set_title('Typhoon: Missing Data by Attribute');ax.set_xlim(0,max(5,float(missing.max())*1.15))
save('typhoon_missing_values.png')

# 4. Correlation heatmap
corr=df[features].corr()
fig,ax=plt.subplots(figsize=(11,9)); im=ax.imshow(corr, vmin=-1,vmax=1,cmap='coolwarm')
ax.set_xticks(range(len(features)),features,rotation=60,ha='right')
ax.set_yticks(range(len(features)),features)
for i in range(len(features)):
 for j in range(len(features)):
  val=corr.iloc[i,j]
  if pd.notna(val):ax.text(j,i,f'{val:.2f}',ha='center',va='center',fontsize=7)
fig.colorbar(im,ax=ax,label='Pearson r'); ax.set_title('Typhoon: Numerical Weather Correlations')
save('typhoon_correlations.png')

# 5. Risk distribution (classes are assigned by days before *confirmed* landfall)
if 'risk' in df:
 count=df['risk'].value_counts().reindex(['Low','Moderate','Medium','High']).dropna()
 fig,ax=plt.subplots(figsize=(8,5));bars=ax.bar(count.index,count.values)
 for b,n in zip(bars,count.values):ax.text(b.get_x()+b.get_width()/2,n,str(int(n)),ha='center',va='bottom')
 ax.set_title('Typhoon: Label Distribution (Confirmed Landfall Sequences)');ax.set_ylabel('Records')
 save('typhoon_risk_distribution.png')

# 6. Daily progression of measured features before landfall; not a causal effect
if 'days_before_landfall' in df:
 selected=[x for x in ['pressure_msl_mean','wind_speed_10m_mean','rain_sum','precipitation_sum'] if x in features]
 fig,axes=plt.subplots(2,2,figsize=(12,8))
 for ax,feat in zip(axes.flat,selected):
  group=df.groupby('days_before_landfall')[feat].agg(['mean','count']).sort_index(ascending=False)
  ax.plot(group.index,group['mean'],marker='o');ax.invert_xaxis();ax.set_title(feat)
  ax.set_xlabel('Days before landfall');ax.set_ylabel('Mean');ax.grid(alpha=.25)
 for ax in list(axes.flat)[len(selected):]:ax.axis('off')
 fig.suptitle('Typhoon: Weather Means Across Day -3 to Landfall',fontsize=14,y=1.01)
 save('typhoon_landfall_progression.png')

# 7. Seasonality (event counts using unique landfall events, not 4 daily rows)
if {'landfall_event_id','month'}.issubset(df):
 d=df[['landfall_event_id','month']].drop_duplicates('landfall_event_id').copy()
 d['month']=pd.to_numeric(d['month'],errors='coerce')
 cnt=d.groupby('month').size().reindex(range(1,13),fill_value=0)
 fig,ax=plt.subplots(figsize=(10,4));ax.bar(cnt.index,cnt.values)
 ax.set_xticks(range(1,13));ax.set_xlabel('Month of sampled sequence record')
 ax.set_ylabel('Unique confirmed landfall events');ax.set_title('Typhoon: Event Coverage by Month')
 save('typhoon_monthly_events.png')

# 8. Prefecture coverage
if 'nearest_prefecture' in df:
 coverage=df['nearest_prefecture'].fillna('Missing').value_counts().head(20).sort_values()
 fig,ax=plt.subplots(figsize=(11,7));ax.barh(coverage.index.astype(str),coverage.values)
 ax.set_xlabel('Rows');ax.set_title('Typhoon: Top 20 Nearest Prefecture Labels')
 save('typhoon_prefecture_coverage.png')

# 9. IQR audit (do not remove outliers automatically)
rows=[]
for feat in features:
 s=df[feat].dropna();q1=s.quantile(.25);q3=s.quantile(.75);iqr=q3-q1
 lo=q1-1.5*iqr;hi=q3+1.5*iqr;n=int(((s<lo)|(s>hi)).sum())
 rows.append(dict(feature=feat,n_valid=len(s),missing=int(df[feat].isna().sum()),q1=q1,q3=q3,iqr=iqr,lower_fence=lo,upper_fence=hi,n_outliers=n,outlier_pct=100*n/len(s) if len(s) else np.nan))
pd.DataFrame(rows).to_csv(OUT/'typhoon_iqr_summary.csv',index=False)
print('Saved typhoon_iqr_summary.csv')
