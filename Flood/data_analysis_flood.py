"""Flood dataset exploratory analysis. Run: python -B data_analysis_flood.py

Expected project layout:
Flood/
  data_analysis_flood.py
  dataset/processed/flood_preprocessed.csv
  plots/                     # created automatically

You can override input with --input path/to/flood_preprocessed.csv.
"""
from pathlib import Path
import argparse
import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DEFAULT_INPUTS = [
    ROOT / 'dataset' / 'processed' / 'flood_preprocessed.csv',
    ROOT / 'dataset' / 'flood_preprocessed.csv',
    ROOT / 'flood_preprocessed.csv',
]
FEATURES = [
    'rain_sum', 'precipitation_hours', 'elevation', 'river_discharge',
    'rain_sum_past_3day', 'rain_sum_past_7day', 'max_daily_rain_past_7day',
    'precipitation_hours_past_7day', 'river_discharge_previous_day',
    'river_discharge_mean_7day', 'river_discharge_median_7day',
    'river_discharge_max_7day', 'discharge_ratio',
]
CLASS_ORDER = ['Low', 'Medium', 'High']


def save(fig, outdir, name):
    fig.savefig(outdir / name, dpi=160, bbox_inches='tight')
    plt.close(fig)
    print('Saved:', outdir / name)


def main():
    parser = argparse.ArgumentParser(description='Analyze preprocessed flood data and export PNG figures')
    parser.add_argument('--input', type=Path, help='Path to flood_preprocessed.csv')
    parser.add_argument('--output', type=Path, default=ROOT / 'plots', help='PNG output directory (default: plots/)')
    args = parser.parse_args()
    candidates = [args.input] if args.input else DEFAULT_INPUTS
    source = next((p for p in candidates if p is not None and p.is_file()), None)
    if source is None:
        parser.error('Dataset not found. Place flood_preprocessed.csv in dataset/processed/ or pass --input.')
    outdir = args.output.resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(source, low_memory=False)
    df.columns = df.columns.str.strip()
    numeric_cols = [c for c in FEATURES if c in df.columns]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce').replace([np.inf, -np.inf], np.nan)
    if not numeric_cols:
        parser.error('No expected numeric attributes were found.')
    print(f'Loaded {len(df):,} rows and {len(df.columns)} columns from {source}')

    # 1. Feature boxplots (IQR-based outliers show as points).
    ncols = 4
    nrows = math.ceil(len(numeric_cols) / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(19, 4 * nrows))
    for ax, c in zip(np.ravel(axes), numeric_cols):
        series = df[c].dropna()
        if len(series):
            ax.boxplot(series.to_numpy(), showfliers=True, flierprops={'markersize': 1, 'alpha': .15})
        ax.set_title(c.replace('_', ' '), fontsize=10)
        ax.tick_params(axis='x', bottom=False, labelbottom=False)
    for ax in np.ravel(axes)[len(numeric_cols):]:
        ax.set_visible(False)
    fig.suptitle('Flood dataset — numeric feature boxplots (1.5 × IQR)', fontsize=15)
    fig.tight_layout()
    save(fig, outdir, 'flood_boxplots.png')

    # 2. Raw distributions; finite data and zero counts retained.
    fig, axes = plt.subplots(nrows, ncols, figsize=(19, 3.6 * nrows))
    for ax, c in zip(np.ravel(axes), numeric_cols):
        vals = df[c].dropna().to_numpy()
        if len(vals):
            ax.hist(vals, bins=45, edgecolor='none')
        ax.set_title(c.replace('_', ' '), fontsize=10)
        ax.set_ylabel('Frequency')
    for ax in np.ravel(axes)[len(numeric_cols):]:
        ax.set_visible(False)
    fig.suptitle('Flood dataset — feature distributions', fontsize=15)
    fig.tight_layout()
    save(fig, outdir, 'flood_distributions.png')

    # 3. Percent missing (all columns, including non-numeric ones).
    missing = (df.isna().mean() * 100).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(12, max(5, len(missing) * .30)))
    ax.barh(missing.index[::-1], missing.values[::-1])
    ax.set_xlabel('Missing rows (%)')
    ax.set_title('Missing-value percentage by column')
    ax.set_xlim(0, max(1, float(missing.max()) * 1.12))
    fig.tight_layout()
    save(fig, outdir, 'flood_missing_values.png')

    # 4. Pearson correlations for measured numeric predictors, not label-derived condition scores.
    corr = df[numeric_cols].corr()
    fig, ax = plt.subplots(figsize=(11, 9))
    im = ax.imshow(corr.to_numpy(), vmin=-1, vmax=1, cmap='coolwarm')
    ax.set_xticks(range(len(numeric_cols)), numeric_cols, rotation=75, ha='right', fontsize=8)
    ax.set_yticks(range(len(numeric_cols)), numeric_cols, fontsize=8)
    fig.colorbar(im, ax=ax, label='Pearson correlation')
    ax.set_title('Flood feature correlations')
    fig.tight_layout()
    save(fig, outdir, 'flood_correlations.png')

    # 5. Label distribution (these labels are generated from rule-based scores).
    if 'flood_class' in df:
        classes = df['flood_class'].astype('string').str.strip().str.title()
        order = CLASS_ORDER + sorted(set(classes.dropna()) - set(CLASS_ORDER))
        counts = classes.value_counts().reindex(order, fill_value=0)
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.bar(counts.index, counts.values)
        ax.bar_label(bars, padding=3, fmt='%d')
        ax.set_title('Flood risk class distribution (derived labels)')
        ax.set_ylabel('Number of observations')
        fig.tight_layout()
        save(fig, outdir, 'flood_class_distribution.png')

        if 'month' in df:
            months = pd.to_numeric(df['month'], errors='coerce')
        elif 'date' in df:
            months = pd.to_datetime(df['date'], errors='coerce').dt.month
        else:
            months = None
        if months is not None:
            table = pd.crosstab(months, classes, normalize='index').reindex(columns=order, fill_value=0)
            table = table.reindex(range(1, 13), fill_value=0)
            fig, ax = plt.subplots(figsize=(11, 5))
            bottom = np.zeros(12)
            for c in table.columns:
                vals = table[c].to_numpy(dtype=float) * 100
                ax.bar(table.index, vals, bottom=bottom, label=c)
                bottom += vals
            ax.set_xticks(range(1, 13))
            ax.set_xlabel('Month')
            ax.set_ylabel('Within-month share (%)')
            ax.set_title('Flood risk class proportions by month')
            ax.legend()
            fig.tight_layout()
            save(fig, outdir, 'flood_monthly_risk.png')

    if 'town' in df:
        top = df['town'].astype('string').value_counts().head(20).iloc[::-1]
        fig, ax = plt.subplots(figsize=(11, max(5, len(top) * .37)))
        ax.barh(top.index, top.values)
        ax.set_title('Top 20 towns by observation count')
        ax.set_xlabel('Number of observations')
        fig.tight_layout()
        save(fig, outdir, 'flood_town_coverage.png')

    # IQR report: an extreme-value flag is not automatically a data error.
    report = []
    for c in numeric_cols:
        s = df[c].dropna()
        if len(s) == 0:
            continue
        q1, q3 = s.quantile([.25, .75]); iqr = q3 - q1
        lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_out = int(((s < lo) | (s > hi)).sum())
        report.append({'feature': c, 'count': len(s), 'missing': int(df[c].isna().sum()),
                       'q1': q1, 'q3': q3, 'iqr': iqr, 'lower_fence': lo, 'upper_fence': hi,
                       'outlier_count': n_out, 'outlier_pct': n_out / len(s) * 100})
    pd.DataFrame(report).to_csv(outdir / 'flood_iqr_summary.csv', index=False)
    print('Saved:', outdir / 'flood_iqr_summary.csv')
    print('Analysis complete. IQR outliers are descriptive flags, not automatically invalid data.')

if __name__ == '__main__':
    main()
