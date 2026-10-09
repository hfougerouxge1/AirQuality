# Module 1 — Understand the Air Quality Problem

## Question 1 — What the problem statement tells us, and what it leaves open

**What we know:**
- What we want to predict (`pm2_5`): the amount of fine particles (PM2.5) measured on the ground, in µg/m³.
- What we use to predict it: measurements from the Sentinel-5P satellite (gases such as SO2, CO, NO2, HCHO and ozone, smoke or dust in the air, the height of these particles, and how cloudy it is), plus the location of the sensors, the date and the hour.
- Two cities: Kampala and Nairobi. Each row in the table is one measurement, at one place, at one time.

**What is still unclear (to check in the data or ask the people who provide it):**
- How many ground stations there are in each city, and how they were chosen. Kampala seems much better covered than Nairobi, so the data may not represent each city equally well.
- What period the data covers: is it a continuous record or just a few scattered days? Is there enough history to see the seasons?
- What device measured the PM2.5 (a high-quality reference instrument or a cheap sensor), and how reliable it is.
- How a satellite image (which covers a large area) was matched to one specific sensor on the ground, and how the time gap is handled between the satellite passing over and the hourly ground measurement.
- Why some values are missing (clouds, sensor breakdowns, satellite problems), and whether these gaps are random or not.
- Whether the test data comes from the same sites and dates as the training data, or from new sites and new dates.

## Question 2 — Who would use the predictions, and what makes them trustworthy

**Users:** environmental agencies, public health authorities (alerts, asthma and heart disease risk), city planners, researchers, and people living in places with few sensors.

**What makes people trust the model:**
- A small error in µg/m³ compared with health limits (for example the WHO ones), not just a good average score.
- Good results on very polluted days, because these are the ones that matter for decisions. A model that is only right near the average is not useful.
- Testing on **sites** and **periods** the model has never seen, instead of randomly picked rows, so that the test looks like real use.
- An idea of how uncertain each prediction is, and clear limits on where the model should not be used (for example cloudy days, or cities that were not in the training data).
- Transparency about which data is used, so that anyone can judge a prediction.

## Question 3 — Physical measurements vs. simple labels

**Physical measurements (satellite):** SO2, CO, NO2, HCHO, ozone, UV aerosol index, aerosol layer height and cloud fraction. They tell us about traffic, burning, industry and particles in the air. Cloud fraction mostly tells us how good the satellite measurement is, rather than how polluted the air is.

**Labels (identifiers):** `id`, `site_id`, `city`, and to a large extent the coordinates `site_latitude` and `site_longitude`. They tell us *where* a measurement was taken but measure nothing in the air. A model can use them to simply memorize the average of each site. This works well when rows are split randomly, but fails on a new site or a new city. `date` and `hour` give context (seasons, time of day) without being physical measurements; they are useful but need to be used with care.

## Question 4 — Risks of using a Kampala-trained model in Nairobi

1. **The sources of pollution are different.** Traffic, waste and wood burning, and industry are not the same in both cities, so the link between what the satellite sees and the pollution on the ground is not the same either (this is called a distribution shift).
2. **The climate and the terrain are different.** Nairobi is at a higher altitude, with its own rainy seasons, weather and clouds. The same amount of gas seen from space can mean a different amount of pollution on the ground.
3. **The sensor network and the PM2.5 levels are different.** Nairobi has fewer sites (about 12 vs. 29 in the training data) and different pollution levels. A model tuned on Kampala will be shifted in Nairobi and may make big errors.
4. **Location information does not transfer.** The coordinates and site-specific habits learned in Kampala mean nothing in Nairobi.

## Question 5 — Variables: type, scale and role

| Variable | Type / scale | Role |
|---|---|---|
| `id`, `site_id` | Categorical (just a label) | Identifier; not a predictor, used to group data and build splits |
| `city` | Categorical (just a label) | Grouping; not a physical measurement |
| `date` | Date and time | Time context (trend, seasons); used to split data over time |
| `hour` | Whole number from 0 to 23, which loops back (after 23 comes 0) | Daily rhythm (traffic, weather) |
| `site_latitude`, `site_longitude` | Continuous number (degrees) | Position; useful for grouping, risky as a predictor |
| `pm2_5` | Continuous number, never negative, with a few very high values (µg/m³) | **What we want to predict (target)** |
| `sulphurdioxide_so2_column_number_density` | Continuous number (mol/m²), can be noisy or negative | Predictor: industry, burning |
| `carbonmonoxide_co_column_number_density` | Continuous number (mol/m²) | Predictor: incomplete burning, fires, traffic |
| `nitrogendioxide_no2_column_number_density` | Continuous number (mol/m²) | Predictor: traffic, burning |
| `formaldehyde_tropospheric_hcho_column_number_density` | Continuous number (mol/m²) | Predictor: compounds released by fires and vegetation |
| `uvaerosolindex_absorbing_aerosol_index` | Continuous number, no unit | Predictor: smoke and dust in the air |
| `ozone_o3_column_number_density` | Continuous number (mol/m²) | Weak predictor: mostly ozone high in the atmosphere |
| `uvaerosollayerheight_aerosol_height` | Continuous number (m or Pa) | Predictor: altitude of the particle layer |
| `cloud_cloud_fraction` | Continuous number between 0 and 1 | Measurement quality and weather; linked to missing values |
