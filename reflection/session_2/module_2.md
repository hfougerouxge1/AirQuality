# Module 2 — Build a First Pipeline

## Question 1 — Train on Nairobi, test on Kampala

| Direction | RMSE | MAE | R² |
|---|---|---|---|
| Train Kampala → test Nairobi | 24.59 | 10.03 | -0.02 |
| Train Nairobi → test Kampala | 15.17 | 11.02 | -0.16 |

**What the difference tells us:**
- The two RMSE values are different (24.59 vs. 15.17), but this is mostly because the test cities are different, not because one model is better. Nairobi has much more spread in PM2.5 (standard deviation about 24) than Kampala (about 14), so any model will make bigger errors in Nairobi.
- Both R² values are negative or close to zero. This means the model is not better than a model that always predicts the average PM2.5 of the training city. Always predicting the mean gives an RMSE of 24.68 for Nairobi and 14.69 for Kampala. This is as good as our model, or even better.
- So the linear model has learned almost nothing that transfers from one city to the other. The link between the satellite measurements and the PM2.5 on the ground is not the same in the two cities (different pollution sources, climate and altitude).
- The two directions also give different answers on MAE (10.03 vs. 11.02), so the result depends on which city we choose for training. One test is not enough to judge a model.

**Would I trust either direction to deploy it?**
No. Neither direction beats the simple "predict the average" baseline, so the model would not help anyone. A model like this could even be misleading, because it looks like a real prediction. This is only a baseline. To do better, we would need stronger models, better features, and a more careful test.

## Question 2 — CRISP-DM

**Phases already done:**
- **Business understanding:** in "Understand the Air Quality Problem", we looked at who uses the predictions and what makes them trustworthy.
- **Data understanding:** we looked at the data, the missing values and which columns are measurements and which are labels.

**This activity:**
- We did a first part of **Data preparation**: cleaning missing values by city and creating the `month` and `dayofweek` features.
- Building and evaluating the baseline pipeline itself belongs to **Modeling** (training the `LinearRegression`) and **Evaluation** (checking RMSE, MAE and R² on a city the model has never seen).
- **Deployment** is not done yet, and given the results above, it would be too early.
