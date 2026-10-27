# Future Weather Attributes: LSTM and GRU Comparison

## Model training

Models requested: LSTM, GRU. Every run retains all 37 physical weather attributes (38 encoded channels because wind direction uses sine and cosine), historical calendar and static station metadata. The target-day calendar is supplied separately.

Training: 2021-01-01 to 2025-09-30; validation: 2025-10-01 to 2025-12-31; test: 2026-01-01 to 2026-01-31. Shared sampled training windows: 160,000; maximum epochs: 30; batch size: 128; seeds: [42].

Training settings are varied without removing attributes. Both cell types receive identical shared scaler fits, window samples and per-seed shuffle streams. Equal layer widths give different parameter counts in LSTM and GRU; those counts are recorded. Checkpoints minimize one-step scaled validation MSE, with early stopping and learning-rate reduction.

```json
[
  {
    "name": "longer_history",
    "lookback": 60,
    "recurrent_units": [
      96,
      64
    ],
    "dense_units": 96,
    "learning_rate": 0.001,
    "dropout": 0.0
  }
]
```

## Model evaluation

MAE, RMSE and bias are reported in each attribute's original units. Wind-direction errors use the shortest angular distance. Persistence is scored on paired observed rows. Missing inputs use training-derived repairs; missing observed targets are never substituted with repaired values for scoring. Incomplete targets are excluded from training and checkpoint validation.

One-step evaluation refreshes observed history each day. Recursive evaluation starts once at the beginning of the period and then feeds predictions back. Horizon tables are cumulative through day h. The ranking uses the mean of per-attribute recursive RMSE divided by observed training standard deviation (180 degrees for direction; one physical unit for a constant training feature), then averages across the listed seeds. This is regression, so classification accuracy percentages are not used.

### Validation comparison

| rank | model_type | setting_name | validation_mean_normalized_RMSE | validation_seed_std | seed_count | mean_parameter_count | mean_training_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | LSTM | longer_history | 0.900284 | N/A | 1 | 105094.000000 | 3180.815305 |
| 2 | GRU | longer_history | 1.076358 | N/A | 1 | 81830.000000 | 2909.609834 |

## Selected model

Selected architecture: **LSTM**; setting: **longer_history**. Validation mean normalized RMSE: 0.900284. Future forecast seed: 42 (the first configured seed). Selection was frozen before this notebook computed test results.

### Heldout test comparison

| run_id | one_step_mean_normalized_RMSE | recursive_mean_normalized_RMSE |
| --- | --- | --- |
| lstm/longer_history/seed_42 | 0.525812 | 0.795105 |
| gru/longer_history/seed_42 | 0.529542 | 0.840224 |

Per-attribute errors for every run and both evaluation modes are exported in `test_all_attribute_metrics.csv`. The heldout test is for final comparison and does not change the validation selection.

## Interpretation and limits

Single-seed results do not establish a statistically reliable model difference.
Validation uses one continuous recursive period, not repeated independent backtests. Test dates are already known from the earlier project work and are not a newly blind benchmark. Historical errors over these periods do not verify an unobserved annual forecast. Training durations are observations from this machine, not controlled speed benchmarks.

## Retained weather attributes

temperature_2m_max, temperature_2m_min, wind_speed_10m_max, wind_gusts_10m_max, snowfall_sum, rain_sum, precipitation_hours, precipitation_sum, shortwave_radiation_sum, sunshine_duration, daylight_duration, dew_point_2m_mean, dew_point_2m_max, surface_pressure_mean, surface_pressure_max, surface_pressure_min, temperature_2m_mean, relative_humidity_2m_mean, relative_humidity_2m_max, relative_humidity_2m_min, dew_point_2m_min, cloud_cover_mean, cloud_cover_max, cloud_cover_min, pressure_msl_mean, pressure_msl_max, pressure_msl_min, wind_speed_10m_mean, wind_speed_10m_min, wind_gusts_10m_mean, wind_gusts_10m_min, river_discharge, river_discharge_p75, river_discharge_mean, river_discharge_median, river_discharge_max, wind_direction_10m_dominant
