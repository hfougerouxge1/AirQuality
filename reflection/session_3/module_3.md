# Module 3 — Robust Evaluation

## Question — Highest RMSE, comparison with Session 2, and the std across folds

**Which city has the highest RMSE when held out?**
Lagos, with an RMSE of 53.1 (MAE 22.5). It is four times the RMSE of Kampala (13.2). Lagos has very variable PM2.5 (mean 46, std 53, max 420), so a linear model trained on the other three cities cannot predict its peaks.

| Held-out city | RMSE | MAE | R² |
|---|---|---|---|
| Kampala | 13.2 | 9.2 | 0.15 |
| Nairobi | 25.3 | 10.1 | -0.02 |
| Lagos | 53.1 | 22.5 | -0.01 |
| Bujumbura | 23.7 | 20.9 | -0.14 |

**Does the mean RMSE match one of Session 2's numbers?**
No. The mean RMSE is 28.8, while Session 2 gave 24.6 (Kampala → Nairobi) and 15.2 (Nairobi → Kampala). It is higher than both, mostly because of Lagos (53.1), which Session 2 never tested. The numbers are also not computed in the same way: here the model is trained on three cities, not one. Only Nairobi is close (25.3 vs 24.6), and Kampala is lower (13.2 vs 15.2) with a higher R² (0.15 vs -0.16). The mean R² is about 0 (-0.004), so on a new city the model is no better than predicting the average.

**What does a large std tell us about a single train/test pair?**
The std of the RMSE is 14.8 for a mean of 28.8, so the result changes a lot depending on the city that is held out: it goes from 13 to 53. A single pair like Session 2's only gives one of these values, so it is a fragile estimate that depends on the pair chosen. It says nothing about Lagos or Bujumbura, and the two directions of Session 2 already gave different numbers. I should not trust one RMSE as "the performance of the model". It is better to report the mean and the std over all cities, and to look at the per-city results, because the worst case (Lagos) is the one that matters if we want to use the model on a new city.
