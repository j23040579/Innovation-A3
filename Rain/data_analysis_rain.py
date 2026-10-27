"""Rain dataset exploratory analysis; exports PNG figures and an IQR CSV to plots/."""
from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "dataset" / "rain_preprocessed.csv"
OUT = ROOT / "plots"
OUT.mkdir(parents=True, exist_ok=True)
FEATURES = ["temperature_2m_max", "temperature_2m_min", "relative_humidity_2m_mean",
            "dew_point_2m_mean", "cloud_cover_mean", "pressure_msl_mean",
            "wind_speed_10m_max", "shortwave_radiation_sum", "rain_sum"]
CLASSES = ["No/Minimal Rain", "Low", "Moderate", "High"]
SAMPLE_SIZE = 40000  # Limit plotted points only; statistics use all available records

def save(fig, filename):
    fig.savefig(OUT / filename, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {OUT / filename}")

def main():
    if not DATA.is_file():
        raise FileNotFoundError(f"Expected processed Rain dataset at {DATA}")
    df = pd.read_csv(DATA, low_memory=False)
    print(f"Loaded {len(df):,} rows and {len(df.columns)} columns")
    metrics = [c for c in FEATURES if c in df.columns]
    for c in metrics:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    if not metrics:
        raise ValueError("No expected numeric features were found")
    sample = df[metrics].sample(n=min(len(df), SAMPLE_SIZE), random_state=42)

    # 1. Feature-wise IQR summaries (full dataset) and boxplots (sample)
    records=[]
    for col in metrics:
        s=df[col].dropna()
        if s.empty: continue
        q1,q3=s.quantile([.25,.75]); iqr=q3-q1
        lower,upper=q1-1.5*iqr,q3+1.5*iqr
        count=int(((s<lower)|(s>upper)).sum())
        records.append(dict(feature=col, count=int(len(s)), q1=q1, median=s.median(), q3=q3,
                            iqr=iqr, lower_fence=lower, upper_fence=upper,
                            outlier_count=count, outlier_percent=100*count/len(s)))
    result=pd.DataFrame(records)
    result.to_csv(OUT/'rain_iqr_summary.csv', index=False)
    print(f"Saved {OUT / 'rain_iqr_summary.csv'}")

    fig,axes=plt.subplots(math.ceil(len(metrics)/3),3,figsize=(16,4*math.ceil(len(metrics)/3)))
    for ax,col in zip(np.ravel(axes),metrics):
        x=sample[col].dropna()
        if len(x): ax.boxplot(x,vert=True,showfliers=True,flierprops={'markersize':1.5})
        ax.set_title(col.replace('_',' '), fontsize=10);ax.set_xticks([])
    for ax in np.ravel(axes)[len(metrics):]:ax.axis('off')
    fig.suptitle('Rain: Feature Distributions and IQR Outliers (sample)', fontsize=15)
    fig.tight_layout();save(fig,'rain_boxplots.png')

    # 2. Distributions; rainfall uses log1p view separately to retain zero days
    fig,axes=plt.subplots(math.ceil(len(metrics)/3),3,figsize=(16,4*math.ceil(len(metrics)/3)))
    for ax,col in zip(np.ravel(axes),metrics):
        x=sample[col].dropna()
        if col=='rain_sum':
            x=np.log1p(x.clip(lower=0));ax.set_xlabel('log1p(rain_sum)')
        if len(x):ax.hist(x,bins=45,edgecolor='none')
        ax.set_title(col.replace('_',' '),fontsize=10);ax.set_ylabel('Sample count')
    for ax in np.ravel(axes)[len(metrics):]:ax.axis('off')
    fig.suptitle('Rain: Numeric Feature Histograms (sample)', fontsize=15)
    fig.tight_layout();save(fig,'rain_distributions.png')

    # 3. Raw vs log1p rain distribution
    if 'rain_sum' in df:
        s=sample['rain_sum'].dropna().clip(lower=0)
        fig,axes=plt.subplots(1,2,figsize=(12,4))
        axes[0].hist(s,bins=60); axes[0].set_title('Daily Rainfall — Original (mm)')
        axes[1].hist(np.log1p(s),bins=60);axes[1].set_title('Daily Rainfall — log1p (illustrative)')
        axes[1].set_xlabel('log(1 + rain_sum)')
        for a in axes:a.set_ylabel('Sample count')
        fig.tight_layout();save(fig,'rain_log_transform_comparison.png')

    # 4. Missing values
    missing=(df.isna().mean()*100).sort_values(ascending=False)
    fig,ax=plt.subplots(figsize=(12, max(4,len(missing)*.32)))
    ax.barh(missing.index[::-1],missing.values[::-1]);ax.set_xlabel('Missing records (%)')
    ax.set_title('Rain: Missing Values by Column');fig.tight_layout();save(fig,'rain_missing_values.png')

    # 5. Correlation heatmap (full dataset)
    corr=df[metrics].corr()
    fig,ax=plt.subplots(figsize=(11,9))
    im=ax.imshow(corr.to_numpy(),cmap='coolwarm',vmin=-1,vmax=1)
    ax.set_xticks(range(len(metrics)),metrics,rotation=65,ha='right',fontsize=9)
    ax.set_yticks(range(len(metrics)),metrics,fontsize=9)
    for i in range(len(metrics)):
        for j in range(len(metrics)):
            v=corr.iloc[i,j]
            if np.isfinite(v):ax.text(j,i,f'{v:.2f}',ha='center',va='center',fontsize=7)
    ax.set_title('Rain: Pearson Correlations');fig.colorbar(im,ax=ax,shrink=.8)
    fig.tight_layout();save(fig,'rain_correlations.png')

    # 6. Rain class distribution
    if 'rain_class' in df:
        counts=df['rain_class'].value_counts().reindex(CLASSES,fill_value=0)
        fig,ax=plt.subplots(figsize=(10,5))
        bars=ax.bar(counts.index,counts.values)
        for bar,val in zip(bars,counts):ax.text(bar.get_x()+bar.get_width()/2,val,f'{val:,}',ha='center',va='bottom',fontsize=9)
        ax.set_title('Rain: Classification Target Distribution');ax.set_ylabel('Records')
        fig.tight_layout();save(fig,'rain_class_distribution.png')

        if 'month' in df:
            month=pd.to_numeric(df['month'],errors='coerce')
        elif 'date' in df:
            month=pd.to_datetime(df['date'],errors='coerce').dt.month
        else:month=None
        if month is not None:
            proportions=pd.crosstab(month,df['rain_class'],normalize='index').reindex(index=range(1,13),columns=CLASSES,fill_value=0)*100
            fig,ax=plt.subplots(figsize=(12,5));bottom=np.zeros(len(proportions))
            for cls in CLASSES:
                vals=proportions[cls].to_numpy();ax.bar(proportions.index,vals,bottom=bottom,label=cls);bottom+=vals
            ax.set_title('Rain: Monthly Distribution of Rain Classes');ax.set_xlabel('Month')
            ax.set_ylabel('Percentage of records (%)');ax.set_xticks(range(1,13));ax.legend(loc='upper left',bbox_to_anchor=(1,1))
            fig.tight_layout();save(fig,'rain_monthly_classes.png')

    if 'prefecture' in df:
        counts=df['prefecture'].value_counts().head(20).iloc[::-1]
        fig,ax=plt.subplots(figsize=(11,8));ax.barh(counts.index,counts.values)
        ax.set_title('Rain: Top 20 Prefectures by Observation Count')
        ax.set_xlabel('Record count');fig.tight_layout();save(fig,'rain_prefecture_coverage.png')
    print('Finished. Summary statistics use all records; histograms and boxplots use a reproducible sample.')
if __name__=='__main__':main()
