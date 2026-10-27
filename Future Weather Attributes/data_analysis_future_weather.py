"""Exploratory analysis of the historical LSTM-ready Japan weather dataset.

Run from anywhere: python -B data_analysis_future_weather.py
Outputs: plots/*.png and plots/future_weather_iqr_summary.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / 'dataset' / 'LSTM_processed' / 'japan_daily_lstm_processed.csv'
OUT = ROOT / 'plots'
OUT.mkdir(parents=True, exist_ok=True)
SELECT = ['temperature_2m_mean','temperature_2m_max','relative_humidity_2m_mean',
          'rain_sum','snowfall_sum','wind_speed_10m_max','pressure_msl_mean',
          'river_discharge','shortwave_radiation_sum','cloud_cover_mean',
          'dew_point_2m_mean','wind_direction_10m_dominant']

def save(name):
    plt.tight_layout(rect=(0,0,1,.96))
    plt.savefig(OUT / name, dpi=160, bbox_inches='tight')
    plt.close()
    print('Saved', OUT / name)

def main():
    if not INPUT.is_file():
        raise FileNotFoundError(f'Dataset missing: {INPUT}')
    df = pd.read_csv(INPUT, low_memory=False)
    print(f'Loaded {len(df):,} rows; {len(df.columns)} columns')
    cols = [c for c in SELECT if c in df]
    for col in cols: df[col] = pd.to_numeric(df[col],errors='coerce')
    sample = df.sample(n=min(40000,len(df)), random_state=42)
    # Full-dataset quartiles and Tukey fences (univariate outliers, not automatic errors)
    stats=[]
    for c in cols:
        x=df[c].replace([np.inf,-np.inf],np.nan).dropna()
        if x.empty: continue
        q1,q3=x.quantile([.25,.75]);iqr=q3-q1; lo=q1-1.5*iqr;hi=q3+1.5*iqr
        n=int(((x<lo)|(x>hi)).sum())
        stats.append(dict(attribute=c,count=len(x),q1=q1,median=x.median(),q3=q3,iqr=iqr,lower_fence=lo,upper_fence=hi,outlier_count=n,outlier_pct=100*n/len(x)))
    pd.DataFrame(stats).to_csv(OUT/'future_weather_iqr_summary.csv',index=False)
    # Boxplots
    fig,axes=plt.subplots(3,4,figsize=(18,11));
    for ax,c in zip(axes.flat,cols):
        x=sample[c].dropna();ax.boxplot(x,vert=True,showfliers=True,flierprops={'markersize':1,'alpha':.15})
        ax.set_title(c.replace('_',' '),fontsize=9);ax.set_xticks([])
    for ax in list(axes.flat)[len(cols):]: ax.axis('off')
    fig.suptitle('Historical weather attributes — boxplots (40k-row sample maximum)')
    save('future_weather_boxplots.png')
    # Distributions
    fig,axes=plt.subplots(3,4,figsize=(18,11))
    for ax,c in zip(axes.flat,cols):
        x=sample[c].replace([np.inf,-np.inf],np.nan).dropna();ax.hist(x,bins=50,color='#4787bd')
        ax.set_title(c.replace('_',' '),fontsize=9);ax.tick_params(labelsize=8)
    for ax in list(axes.flat)[len(cols):]: ax.axis('off')
    fig.suptitle('Historical weather attributes — distributions (40k-row sample maximum)')
    save('future_weather_distributions.png')
    # Missing
    miss=df.isna().mean().mul(100).sort_values(ascending=False)
    fig,ax=plt.subplots(figsize=(13,6));subset=miss[miss>0]
    if subset.empty:ax.text(.5,.5,'No missing values detected',ha='center',va='center',transform=ax.transAxes)
    else:ax.bar(subset.index,subset.values);ax.tick_params(axis='x',rotation=75,labelsize=8)
    ax.set_ylabel('Missing (%)');ax.set_title('Missing-value percentage by column');save('future_weather_missing_values.png')
    # correlations
    numeric=df[cols].corr();fig,ax=plt.subplots(figsize=(12,10));im=ax.imshow(numeric,vmin=-1,vmax=1,cmap='coolwarm');fig.colorbar(im,ax=ax,label='Pearson correlation')
    ax.set_xticks(range(len(cols)),cols,rotation=75,ha='right',fontsize=8);ax.set_yticks(range(len(cols)),cols,fontsize=8)
    ax.set_title('Weather attribute correlations');save('future_weather_correlations.png')
    # seasonal
    if 'month' in df:
        cols_month=[c for c in ['temperature_2m_mean','rain_sum','wind_speed_10m_max','pressure_msl_mean'] if c in df]
        aggregate=df.groupby('month')[cols_month].mean(numeric_only=True)
        fig,axes=plt.subplots(2,2,figsize=(12,8))
        for ax,c in zip(axes.flat,cols_month): ax.plot(aggregate.index,aggregate[c],marker='o');ax.set_title(c);ax.set_xlabel('Month');ax.set_xticks(range(1,13))
        fig.suptitle('Average meteorological attributes by month');save('future_weather_monthly_trends.png')
    # geographical coverage
    if 'prefecture' in df:
        coverage=df.groupby('prefecture').size().sort_values(ascending=False).head(20)
        fig,ax=plt.subplots(figsize=(12,7));coverage.sort_values().plot.barh(ax=ax,color='#4787bd');ax.set_xlabel('Historical observations');ax.set_title('Top 20 prefectures by observation count');save('future_weather_prefecture_coverage.png')
    # daily temperature and rain comparison monthly across years
    if {'year','month','temperature_2m_mean','rain_sum'}.issubset(df.columns):
        ym=df.groupby(['year','month'],as_index=False)[['temperature_2m_mean','rain_sum']].mean()
        ym['period']=pd.to_datetime(dict(year=ym.year,month=ym.month,day=1))
        fig,axes=plt.subplots(2,1,figsize=(12,7),sharex=True)
        axes[0].plot(ym.period,ym.temperature_2m_mean);axes[0].set_ylabel('Mean temperature (°C)')
        axes[1].plot(ym.period,ym.rain_sum);axes[1].set_ylabel('Average daily rain (mm)')
        fig.suptitle('Historical monthly weather patterns');save('future_weather_historical_trends.png')
    # wind direction
    if 'wind_direction_10m_dominant' in df:
        angles=df['wind_direction_10m_dominant'].dropna().mod(360)
        fig,ax=plt.subplots(figsize=(10,5));ax.hist(angles,bins=np.arange(0,361,15),color='#4787bd');ax.set_xticks(np.arange(0,361,45));ax.set_xlabel('Dominant wind direction (degrees)');ax.set_ylabel('Observations');ax.set_title('Dominant wind direction distribution');save('future_weather_wind_direction.png')
    print('Completed. Plots folder:',OUT)

if __name__=='__main__':main()
