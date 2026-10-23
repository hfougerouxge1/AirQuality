# Module 2 — Advanced Cleaning

## Question — Drop before fill, and why 0.7?

**Why drop before the per-city fill?**
The fill hides the missing values that the threshold uses to decide. `uvaerosollayerheight_aerosol_height` is 94.7% missing at first (Bujumbura 100%, Nairobi 97%). After `fill_missing_by_city`, Kampala, Nairobi and Lagos are filled from their few real values, and only the 123 Bujumbura rows are still NaN (about 1.5%). The column then looks almost clean, even though it is mostly a few real values copied over thousands of rows. It still crashes the model when we train on Kampala and test on Bujumbura (`Input X contains NaN`).

So the order matters: first measure the missingness on the raw data and drop the columns that are too empty, then fill what remains. In my notebook this gave 0 missing values left, and the Kampala → Bujumbura evaluation ran (RMSE 19.2, MAE 12.0, R² 0.26).

**What would `columns_above_missing_threshold` report on filled data?**
An empty list `[]` with 0.7, because the worst column is at about 1.5% and all the others are at 0%. Nothing is dropped, so I keep a column with fake information and the NaN for Bujumbura at the same time. The check passes but the problem is still there. It is a silent failure, which is the worst kind.

**Why 0.7, and what changes with 0.5?**
Missing ratios on the 4 cities (8071 rows):

| column | missing |
|---|---|
| aerosol height | 94.7% |
| NO2 | 61.5% |
| SO2 | 60.9% |
| HCHO | 48.5% |
| CO | 45.0% |
| cloud fraction | 38.1% |
| O3, aerosol index | ~1%, ~0% |

- **0.7:** only the aerosol height is dropped. There is a big gap before the next column (61.5%), so the threshold is easy to justify. The other columns are kept and filled per city.
- **0.5:** NO2 and SO2 are dropped too. NO2 was one of the two best correlated variables in Module 1 (0.40), so I would lose useful signal just to avoid filling a column that is 60% missing.
- **0.3:** six columns are dropped, including CO, the best predictor. Almost nothing would be left for the model.

There is a trade-off. A higher threshold keeps more information but relies more on the fill (ffill/bfill invents more values). A lower threshold is safer but throws away real signal. 0.7 works here because of the clear gap, but it is not a magic number: it was chosen by looking at this dataset. Before changing it, I would compare the model score (for example the Kampala → Bujumbura R² of 0.26) with each threshold.
