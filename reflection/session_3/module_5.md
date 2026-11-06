# Module 5 — Réglage des hyperparamètres

| Modèle (mêmes 8 colonnes RFE) | RMSE moyen | MAE moyen | R² moyen |
|---|---|---|---|
| LinearRegression (Module 4) | 27,6 | — | 0,07 |
| XGBRegressor non réglé | 31,9 | 16,7 | -0,77 |
| XGBRegressor réglé (`max_depth=3`, `learning_rate=0.05`) | 27,6 | 14,2 | 0,085 |

**Pourquoi un modèle plus complexe peut être moins bon.** XGBoost sans réglage est moins bon que la régression linéaire sur les mêmes colonnes (RMSE 31,9 contre 27,6, R² de -0,77 contre 0,07). Ses valeurs par défaut sont des arbres assez profonds avec un apprentissage rapide. Sur un jeu de données petit (4 villes) et plutôt linéaire, il apprend les particularités des villes d'entraînement et généralise mal à la ville mise de côté. La flexibilité n'aide que si les hyperparamètres la dirigent dans la bonne direction.

**Lecture de la recherche.** `GridSearchCV` a testé 4 combinaisons avec `GroupKFold` (une ville par pli) :

| `learning_rate` | `max_depth` | RMSE | R² |
|---|---|---|---|
| 0,05 | 3 | **27,57** | 0,085 |
| 0,2 | 3 | 28,79 | -0,07 |
| 0,05 | 5 | 28,89 | -0,09 |
| 0,2 | 5 | 31,07 | -0,49 |

Les deux hyperparamètres vont dans le même sens : plus le modèle est simple et prudent, meilleur est le résultat. La pire combinaison (`learning_rate=0.2`, `max_depth=5`) est proche du modèle non réglé. Lire tout le tableau, et pas seulement la meilleure ligne, montre que l'erreur vient de la complexité du modèle.

**Ce que le réglage apporte vraiment.** Le RMSE passe de 31,9 à 27,6, mais le modèle réglé fait seulement aussi bien que la régression linéaire. Le réglage répare le modèle, il ne le rend pas meilleur que le modèle simple. Le R² de 0,085 reste très faible : sur une ville jamais vue, le modèle explique à peine plus que la moyenne.

**Limites.**
- La meilleure combinaison est au bord de la grille (la plus petite valeur testée pour les deux paramètres). Une grille plus large, avec `max_depth=2` ou un `learning_rate` plus petit, pourrait faire mieux.
- Les écarts entre combinaisons (27,6 à 28,9) sont petits pour seulement 4 villes. Le modèle varie beaucoup d'une ville à l'autre (Lagos : RMSE 51,8 ; Kampala : 13,7), donc il faut rester prudent.
- Les mêmes plis servent à choisir les hyperparamètres et à rapporter le score, donc le RMSE de 27,6 est un peu optimiste.
