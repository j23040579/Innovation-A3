"""Generate exploratory temperature dataset figures and IQR summary in plots/.
Run: python -B data_analysis_temperature.py
"""
from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'dataset' / 'temperature_preprocessed.csv'
OUT = ROOT / 'plots'
OUT.mkdir(parents=True, exist_ok=True)
FEATURES = ['shortwave_radiation_sum','sunshine_duration','daylight_duration','cloud_cover_mean','dew_point_2m_mean','month']
TARGETS = ['temperature_2m_max','temperature_2m_min']
METRICS = [x for x in FEATURES + TARGETS if x != 'month']
LABEL = {x: x.replace('_',' ').title() for x in FEATURES + TARGETS}

def save(filename):
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=160, bbox_inches='tight')
    plt.close()
    print('Saved', OUT / filename)

def main():
    if not DATA.exists():
        raise FileNotFoundError(f'Dataset missing: {DATA}')
    df = pd.read_csv(DATA, low_memory=False)
    print(f'Loaded {len(df):,} records, {len(df.columns)} columns')
    df['date'] = pd.to_datetime(df['date'], errors='coerce') if 'date' in df else pd.NaT
    for c in METRICS + ['month']:
        if c in df: df[c] = pd.to_numeric(df[c], errors='coerce')
    metrics = [c for c in METRICS if c in df]
    rng = np.random.default_rng(42)
    sample = df.iloc[rng.choice(len(df), size=min(40000,len(df)), replace=False)] if len(df) else df
    # 1 IQR boxplots; use full data per column so fences match summary.
    ncol = 3; nrow = math.ceil(len(metrics)/ncol)
    fig, axes = plt.subplots(nrow,ncol,figsize=(16,4*nrow)); axes=np.ravel(axes)
    summary=[]
    for idx,c in enumerate(metrics):
        s=df[c].dropna(); q1=s.quantile(.25); q3=s.quantile(.75); iqr=q3-q1; lo=q1-1.5*iqr; hi=q3+1.5*iqr
        outlier=((s<lo)|(s>hi)).sum()
        summary.append(dict(attribute=c,count=int(len(s)),q1=q1,median=s.median(),q3=q3,iqr=iqr,lower_fence=lo,upper_fence=hi,outlier_count=int(outlier),outlier_percent=100*outlier/len(s) if len(s) else np.nan))
        axes[idx].boxplot(s.to_numpy(), vert=True, showfliers=False)
        axes[idx].set_title(f'{LABEL[c]} (outliers: {outlier:,})',fontsize=10)
        axes[idx].grid(axis='y', alpha=.3)
    for a in axes[len(metrics):]: a.axis('off')
    fig.suptitle('Temperature Dataset — IQR Boxplots (outlier markers hidden)',fontsize=15,y=1.01)
    save('temperature_boxplots.png')
    pd.DataFrame(summary).to_csv(OUT/'temperature_iqr_summary.csv',index=False)
    print('Saved', OUT/'temperature_iqr_summary.csv')
    # 2 distributions
    fig,axes=plt.subplots(nrow,ncol,figsize=(16,4*nrow)); axes=np.ravel(axes)
    for idx,c in enumerate(metrics):
        s=sample[c].dropna(); axes[idx].hist(s,bins=45,alpha=.85);axes[idx].set_title(LABEL[c]);axes[idx].set_ylabel('Frequency');axes[idx].grid(alpha=.2)
    for a in axes[len(metrics):]:a.axis('off')
    fig.suptitle('Temperature Dataset — Attribute Distributions',fontsize=15,y=1.01)
    save('temperature_distributions.png')
    # 3 missing value percentages
    missing=df.isna().mean().mul(100).sort_values(ascending=False)
    plt.figure(figsize=(12,5)); plt.bar(range(len(missing)),missing.values);plt.xticks(range(len(missing)),missing.index,rotation=50,ha='right');plt.ylabel('Missing (%)');plt.title('Missing Values by Column');plt.grid(axis='y',alpha=.2)
    save('temperature_missing_values.png')
    # 4 numeric correlation heatmap
    num=df[[c for c in FEATURES+TARGETS if c in df]].corr()
    fig,ax=plt.subplots(figsize=(11,9));im=ax.imshow(num,cmap='coolwarm',vmin=-1,vmax=1)
    ax.set_xticks(range(len(num)),[LABEL[c] for c in num.columns],rotation=45,ha='right');ax.set_yticks(range(len(num)),[LABEL[c] for c in num.index]);
    for i in range(len(num)):
        for j in range(len(num)):ax.text(j,i,f'{num.iat[i,j]:.2f}',ha='center',va='center',fontsize=8,color='black')
    fig.colorbar(im,ax=ax,label='Pearson correlation');ax.set_title('Temperature Attributes — Correlation Matrix')
    save('temperature_correlations.png')
    # 5 target maximum and minimum comparison
    fig,axes=plt.subplots(1,2,figsize=(14,5))
    for a,c in zip(axes,[c for c in TARGETS if c in df]):
        a.hist(sample[c].dropna(),bins=50);a.set_title(LABEL[c]);a.set_xlabel('Temperature (°C)');a.set_ylabel('Frequency');a.grid(alpha=.2)
    save('temperature_target_distributions.png')
    # 6 monthly mean temperatures
    if 'month' in df and all(c in df for c in TARGETS):
        monthly=df.groupby('month')[TARGETS].mean().sort_index();fig,ax=plt.subplots(figsize=(11,5))
        for c in TARGETS:ax.plot(monthly.index,monthly[c],marker='o',label=LABEL[c])
        ax.set_xticks(range(1,13));ax.set_xlabel('Month');ax.set_ylabel('Mean temperature (°C)');ax.set_title('Monthly Mean Daily Temperatures');ax.legend();ax.grid(alpha=.3)
        save('temperature_monthly_trends.png')
    # 7 coverage by prefecture
    if 'prefecture' in df:
        counts=df['prefecture'].value_counts().head(20).sort_values()
        plt.figure(figsize=(11,8));plt.barh(counts.index.astype(str),counts.values);plt.xlabel('Number of observations');plt.title('20 Prefectures with the Most Records');plt.grid(axis='x',alpha=.2)
        save('temperature_prefecture_coverage.png')
    # 8 dew point vs max temperature
    if 'dew_point_2m_mean' in sample and 'temperature_2m_max' in sample:
        plt.figure(figsize=(9,6));plt.scatter(sample['dew_point_2m_mean'],sample['temperature_2m_max'],alpha=.1,s=4,rasterized=True)
        plt.xlabel('Mean dew point (°C)');plt.ylabel('Daily maximum temperature (°C)');plt.title('Dew Point vs Daily Maximum Temperature');plt.grid(alpha=.2)
        save('temperature_dewpoint_vs_max.png')
    print('Done. Plots:', OUT)

if __name__=='__main__':main()
