# Module 6 — Experiment Tracking

| Run (`max_depth`, `learning_rate`) | RMSE | MAE | R² |
|---|---|---|---|
| 3, 0,05 | **27,57** | 14,24 | 0,085 |
| 3, 0,2 | 28,79 | 15,89 | -0,074 |
| 5, 0,05 | 28,89 | 14,77 | -0,092 |
| 5, 0,2 | 31,07 | 17,28 | -0,492 |

**Quelle combinaison gagne.** En triant par `rmse`, `max_depth=3` et `learning_rate=0.05` arrive en tête, avec un RMSE de 27,57. C'est exactement la combinaison que le Module 5 avait déjà trouvée, avec les mêmes valeurs : MLflow relit les résultats de `tune_xgboost`, il ne refait pas de calcul différent. Cette combinaison est aussi première sur le MAE et le R², donc le classement ne dépend pas de la métrique choisie.

**Aurais-je trouvé la réponse aussi vite dans le terminal ?** Pour 4 combinaisons, oui : le tableau de `cv_results` tient à l'écran et le meilleur RMSE se lit d'un coup d'œil. MLflow n'apporte pas de gain de temps à cette taille. Il apporte autre chose : les résultats restent enregistrés avec leurs paramètres, on peut trier, filtrer (`metrics.rmse < 28`) et comparer des runs sans relancer la recherche.

**À partir de combien de runs le terminal ne suffit plus.** Je dirais autour d'une dizaine de runs. Au-delà, le tableau ne tient plus à l'écran, il faut relancer le script pour retrouver un résultat, et les sorties des anciennes exécutions sont perdues dès que le terminal est fermé. Ça arrive vite : une grille de 4 valeurs par paramètre sur 3 paramètres donne déjà 64 combinaisons, et chaque nouveau jeu de features (RFE, SelectKBest) multiplie encore ce nombre.

**Limite observée.** Relancer le script ajoute 4 runs identiques à chaque exécution, car MLflow ne remplace jamais un run (j'en ai eu 12 au lieu de 4 après 3 exécutions). Il faut relancer seulement quand le code ou la grille change.
