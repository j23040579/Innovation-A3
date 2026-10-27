"""Exploratory data analysis for the Wind regression dataset.

Run from any working directory: python -B data_analysis_wind.py
Reads dataset/wind_preprocessed.csv and writes figures and summary to plots/.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'dataset' / 'wind_preprocessed.csv'
OUT = ROOT / 'plots'
FEATURES = ['surface_pressure_mean', 'surface_pressure_max', 'surface_pressure_min',
            'pressure_change', 'wind_direction_10m_dominant', 'wind_speed_10m_max']
TARGET = 'wind_speed_10m_max'
SAMPLE_SIZE = 30000


def save(fig, filename):
    fig.savefig(OUT / filename, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print(f'Saved {OUT / filename}')


def main():
    if not DATA.is_file():
        raise FileNotFoundError(f'Missing processed dataset: {DATA}')
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA, parse_dates=['date'], low_memory=False)
    for col in FEATURES:
        if col not in df:
            raise ValueError(f'Missing expected column: {col}')
        df[col] = pd.to_numeric(df[col], errors='coerce')
    subset = df[FEATURES].replace([np.inf, -np.inf], np.nan)
    sample = subset.sample(min(SAMPLE_SIZE, len(subset)), random_state=42)
    print(f'Rows: {len(df):,}; columns: {len(df.columns)}; dates: {df.date.min().date()}–{df.date.max().date()}')

    # Full-data IQR fences and counts (the charts sample to remain readable).
    rows = []
    for col in FEATURES:
        vals = subset[col].dropna()
        q1, q3 = vals.quantile([0.25, 0.75]); iqr = q3 - q1
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        count = int(((vals < low) | (vals > high)).sum())
        rows.append({'feature': col, 'count': len(vals), 'q1': q1, 'median': vals.median(),
                     'q3': q3, 'iqr': iqr, 'lower_fence': low, 'upper_fence': high,
                     'outlier_count': count, 'outlier_pct': 100 * count / len(vals) if len(vals) else np.nan})
    pd.DataFrame(rows).to_csv(OUT / 'wind_iqr_summary.csv', index=False)

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for ax, col in zip(axes.flat, FEATURES):
        vals = sample[col].dropna()
        ax.boxplot(vals, vert=True, showfliers=True, flierprops={'markersize': 1.6})
        ax.set_title(col.replace('_', ' '), fontsize=10)
        ax.set_xticks([]); ax.grid(axis='y', alpha=0.2)
    fig.suptitle('Wind — Feature Boxplots (sampled; Tukey 1.5 × IQR)', fontsize=14)
    fig.tight_layout(); save(fig, 'wind_boxplots.png')

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    for ax, col in zip(axes.flat, FEATURES):
        ax.hist(sample[col].dropna(), bins=55, edgecolor='none')
        ax.set_title(col.replace('_', ' '), fontsize=10)
        ax.set_ylabel('Observations'); ax.grid(axis='y', alpha=0.2)
    fig.suptitle('Wind — Feature Distributions (sampled)', fontsize=14)
    fig.tight_layout(); save(fig, 'wind_distributions.png')

    missing = df.isna().mean().mul(100).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar(missing.index, missing.values)
    ax.set_ylabel('Missing observations (%)'); ax.set_title('Wind — Missing Values by Column')
    ax.tick_params(axis='x', rotation=45); fig.tight_layout(); save(fig, 'wind_missing_values.png')

    correlations = subset.corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(correlations, vmin=-1, vmax=1, cmap='coolwarm')
    ax.set_xticks(range(len(FEATURES)), [x.replace('_', '\n') for x in FEATURES], fontsize=8)
    ax.set_yticks(range(len(FEATURES)), [x.replace('_', ' ') for x in FEATURES], fontsize=9)
    for i in range(len(FEATURES)):
        for j in range(len(FEATURES)):
            ax.text(j, i, f'{correlations.iloc[i,j]:.2f}', ha='center', va='center', fontsize=8)
    fig.colorbar(im, ax=ax, label='Pearson correlation')
    ax.set_title('Wind — Numeric Feature Correlations')
    fig.tight_layout(); save(fig, 'wind_correlations.png')

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df[TARGET].dropna(), bins=80)
    ax.axvline(df[TARGET].median(), linestyle='--', color='black', label=f'Median: {df[TARGET].median():.1f} km/h')
    ax.set_title('Wind — Maximum Daily Wind Speed Distribution')
    ax.set_xlabel('Wind speed at 10 m (km/h)'); ax.set_ylabel('Observations'); ax.legend()
    fig.tight_layout(); save(fig, 'wind_target_distribution.png')

    working = df[['date', TARGET]].dropna().copy()
    working['month'] = working['date'].dt.month
    monthly = working.groupby('month')[TARGET].agg(['mean', 'median'])
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly.index, monthly['mean'], marker='o', label='Mean')
    ax.plot(monthly.index, monthly['median'], marker='s', label='Median')
    ax.set_xticks(range(1,13)); ax.set_xlabel('Month'); ax.set_ylabel('Daily maximum wind speed (km/h)')
    ax.set_title('Wind — Seasonal Wind Speed Patterns (all available years)'); ax.legend(); ax.grid(alpha=0.25)
    fig.tight_layout(); save(fig, 'wind_monthly_trends.png')

    counts = df['prefecture'].value_counts().head(20).sort_values()
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.barh(counts.index.astype(str), counts.values)
    ax.set_xlabel('Number of records'); ax.set_title('Wind — Top 20 Prefectures by Observation Count')
    fig.tight_layout(); save(fig, 'wind_prefecture_coverage.png')

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    directions = (df['wind_direction_10m_dominant'].dropna() % 360)
    axes[0].hist(directions, bins=np.arange(0, 361, 15))
    axes[0].set_xlabel('Dominant wind direction (degrees)')
    axes[0].set_ylabel('Observations'); axes[0].set_title('Direction distribution')
    scatter = df[['wind_direction_10m_dominant', TARGET]].dropna().sample(min(12000, len(df)), random_state=42)
    axes[1].scatter(scatter['wind_direction_10m_dominant'] % 360, scatter[TARGET], s=2, alpha=0.18)
    axes[1].set_xlabel('Dominant wind direction (degrees)'); axes[1].set_ylabel('Daily maximum wind speed (km/h)')
    axes[1].set_title('Direction vs wind speed (sampled)')
    fig.suptitle('Wind — Dominant Direction Analysis'); fig.tight_layout(); save(fig, 'wind_direction_analysis.png')
    print('All figures and the IQR summary have been saved.')


if __name__ == '__main__':
    main()
