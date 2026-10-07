# Module 1 — Understand the Air Quality Problem

## Question 1 — What the problem statement tells us, and what it leaves open

**Known:**
- Target: `pm2_5`, ground-measured PM2.5 concentration (µg/m³).
- Predictors: Sentinel-5P satellite column measurements (SO2, CO, NO2, HCHO, UV aerosol index, O3, aerosol layer height, cloud fraction), plus site coordinates, date and hour.
- Cities in scope: Kampala and Nairobi. Each row is one reading at one site at one time.

**Unclear (to check in the data or with the data provider):**
- Number of ground stations per city and how they were chosen (Kampala looks much better covered than Nairobi, so the sample may not represent each city).
- Time span and sampling frequency: is it a continuous series or scattered days? Is there enough history to see a seasonal cycle?
- How the ground PM2.5 was measured (reference instrument or low-cost sensor), its calibration, and its error.
- How satellite pixels were matched to sites (pixel size vs. a point sensor, overpass time vs. hourly measurement, handling of cloudy scenes).
- Why values are missing (cloud cover, retrieval failures, sensor outages) and whether this is random.
- Whether the test set comes from the same sites and period as the training set, or from new sites/dates.

## Question 2 — Who would use the predictions, and what makes them trustworthy

**Users:** city and national environmental agencies, public-health authorities (alerts, asthma and cardiovascular risk), urban planners, researchers, and residents in places with few ground sensors.

**Criteria for trust:**
- Error in µg/m³ that is small relative to health thresholds (e.g. WHO limits), not only a good average score.
- Good performance on high-pollution episodes, since those drive decisions. A model that is accurate only around the mean is not useful.
- Evaluation on unseen **sites** and **periods**, not a random row split, so it reflects real deployment.
- Uncertainty estimates and a clear statement of where the model should not be used (e.g. cloudy days, cities not in training).
- Transparency about inputs and limits, so users can judge a given prediction.

## Question 3 — Physical predictors vs. identifiers

**Physical predictors (satellite columns):** SO2, CO, NO2, HCHO, UV aerosol index, O3, aerosol layer height and cloud fraction. They relate to combustion, traffic, industry, aerosols and observation conditions. Cloud fraction describes retrieval quality more than pollution itself.

**Identifiers / non-physical variables:** `id`, `site_id`, `city`, and to a large extent the coordinates `site_latitude` and `site_longitude`. They label a place but do not measure anything in the atmosphere. A model can use them to memorize site-specific averages, which looks good on a random split but does not generalize to new sites or cities. `date` and `hour` are context rather than physical measurements. They can stand in for seasonal and daily cycles, but must be handled with care.

## Question 4 — Risks of applying a Kampala-trained model to Nairobi without retraining

1. **Different pollution sources and mix.** Traffic, biomass and waste burning, and industry differ between the two cities, so the relationship between satellite columns and ground PM2.5 differs too (distribution shift).
2. **Different climate and geography.** Nairobi is higher in altitude and has its own rainy/dry seasons, boundary-layer height and cloud patterns. The same column density can correspond to a different ground concentration, and the satellite's cloud-related gaps and biases differ.
3. **Different sensor network and PM2.5 level.** Nairobi has fewer sites (about 12 vs. 29 in the training data) and a different PM2.5 range. A model tuned to Kampala's range will be biased in Nairobi and may extrapolate poorly.
4. **Location features do not transfer.** Coordinates and site-specific effects learned in Kampala are meaningless in Nairobi.

## Question 5 — Variables: type, scale and role

| Variable | Type / scale | Role |
|---|---|---|
| `id`, `site_id` | Categorical, nominal (identifier) | Identifier; not a predictor, used for grouping and splits |
| `city` | Categorical, nominal | Grouping / stratification; not a physical predictor |
| `date` | Datetime | Time context (trend, seasonality); used for temporal splits |
| `hour` | Discrete, cyclic (0–23) | Daily-cycle context (traffic, boundary layer) |
| `site_latitude`, `site_longitude` | Continuous, degrees | Location; spatial grouping, risky as a feature |
| `pm2_5` | Continuous, ratio scale, ≥ 0, right-skewed (µg/m³) | **Target** |
| `sulphurdioxide_so2_column_number_density` | Continuous (mol/m²), can be noisy/negative | Predictor: industry, combustion |
| `carbonmonoxide_co_column_number_density` | Continuous (mol/m²) | Predictor: incomplete combustion, biomass burning, traffic |
| `nitrogendioxide_no2_column_number_density` | Continuous (mol/m²) | Predictor: traffic, combustion |
| `formaldehyde_tropospheric_hcho_column_number_density` | Continuous (mol/m²) | Predictor: VOC emissions, biomass burning |
| `uvaerosolindex_absorbing_aerosol_index` | Continuous, dimensionless index | Predictor: absorbing aerosols (smoke, dust) |
| `ozone_o3_column_number_density` | Continuous (mol/m²) | Predictor: weak, mostly stratospheric ozone |
| `uvaerosollayerheight_aerosol_height` | Continuous (m or Pa) | Predictor: height of the aerosol layer |
| `cloud_cloud_fraction` | Continuous, bounded [0, 1] | Observation quality / meteorology; related to missing values |
