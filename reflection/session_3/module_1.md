# Module 1 — Rigorous Correlation Analysis

## Question — Comparing `correlation_table` with the Session 2 discovery

**Did the importance of a variable change?**
A little. CO and NO2 are still the top two, but they are stronger with 4 cities (CO: 0.31 → 0.42, NO2: 0.31 → 0.40). The UV aerosol index goes from almost nothing (0.01) to 0.17, so it only appears when Lagos and Bujumbura are added. The other variables are about the same.

**Is n large enough for CO?**
For the whole sample, yes (n = 4441, p ≈ 1e-192). But I would not trust it too much:
- Most rows come from Kampala (2876) and only 44 from Bujumbura.
- The correlation is about 0.50 in Kampala but 0.02 in Nairobi, so the global r is mostly driven by one city.
- r = 0.42 means only about 18% of the variance is explained, and a small p-value does not prove causality.

**What I would investigate next:**
- the correlation city by city, to see if it is stable,
- the scatter plots and outliers, to check the shape of the relationship,
- why there are so many missing values for some variables (e.g. aerosol height),
- whether CO and NO2 are redundant, and the effect of the season,
- whether these variables really help a model on a city it has not seen.
