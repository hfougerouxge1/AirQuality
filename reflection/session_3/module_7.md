# Module 7 — A Scikit-learn Transformer

**1. `fit` qui lit des données extérieures : `clone()` protège-t-il encore ?** Non. `clone()` ne protège que d'une fuite entre plis : il fabrique une copie neuve à partir des paramètres de `__init__`, sans les attributs appris (`means_`), donc ce qui a été appris sur un pli ne passe pas au suivant. Il ne contrôle pas d'où `fit` tire ses données. Si `fit` lit une variable globale ou un fichier qui contient toutes les villes, chaque copie neuve relit la même source et apprend des moyennes qui incluent la ville de validation. Le contrat `fit`/`transform` n'est une garantie que si `fit` n'utilise que le `X` qu'il reçoit.

**2. Pourquoi le seuil du Module 2 et le RFE du Module 4 sont le même problème.** Ces deux étapes apprennent une décision à partir des données (quelles colonnes supprimer, lesquelles garder). Calculées une fois sur les 4 villes avant le découpage, elles ont vu la ville qui sera ensuite mise de côté : c'est exactement un `fit` qui lit des données extérieures à son pli d'entraînement. Mon run le montre : le nombre de colonnes supprimées vaut 19 quand Kampala ou Nairobi est retenue, et 28 quand c'est Lagos ou Bujumbura, et le RFE choisit d'autres colonnes (SO2 pour Kampala, albédo et fraction nuageuse pour Lagos). La décision dépend donc des villes d'entraînement, et un calcul unique sur tout le jeu de données ne correspond à aucun pli. L'effet sur le score reste petit : le RMSE moyen passe de 27,57 (Module 5) à 27,81. Cet écart n'est pas une mesure pure de la fuite, car le seuil est passé de 0,7 à 0,6 entre les deux.

**3. Un pli ressort : Lagos.**

| Ville retenue | RMSE | PM2,5 moyen | Écart-type | Max |
|---|---|---|---|---|
| Kampala | 14,5 | 22,8 | 14,3 | 142,5 |
| Nairobi | 25,1 | 18,9 | 25,0 | 456,2 |
| Lagos | **53,3** | **46,2** | **52,8** | 419,5 |
| Bujumbura | 18,4 | 30,7 | 22,4 | 122,6 |

Quand Lagos est retenue, le modèle s'entraîne sur Kampala, Nairobi et Bujumbura, trois villes bien moins polluées (moyennes de 19 à 31 µg/m³ contre 46 pour Lagos). Il n'a jamais vu ces niveaux et prédit trop bas. La mise à l'écart de Lagos modifie aussi l'entraînement : Kampala fournit 5 596 lignes sur 8 071, et les colonnes retenues par le RFE changent. Je ne peux pas dire laquelle des deux causes pèse le plus.

**4. Remplacer par `Ridge` (RFE et modèle final).**

| Configuration | RMSE par pli (Kampala, Nairobi, Lagos, Bujumbura) | RMSE moyen |
|---|---|---|
| XGBoost final, RFE sur LinearRegression (mon run) | 14,5 / 25,1 / 53,3 / 18,4 | 27,81 |
| LinearRegression final | **5189,8** / 25,7 / 51,5 / 17,9 | 1321,2 |
| Ridge final, RFE sur Ridge | 15,6 / 26,0 / 55,1 / 20,4 | 29,26 |
| XGBoost final, RFE sur Ridge | 13,9 / 25,0 / 52,8 / 18,4 | 27,53 |

Ridge fait tout de même changer le résultat. La régression linéaire simple explose sur le pli Kampala (RMSE de 5 190), comme au Module 4 avec les poids énormes sur des colonnes quasi identiques. Ridge ajoute une pénalité sur la taille des coefficients, ce qui empêche ces poids énormes qui se compensent entre colonnes corrélées. Il ramène la moyenne à 29,3, mais il n'est pas meilleur que XGBoost (27,8). Le RFE sur Ridge à la place de LinearRegression donne un résultat un peu meilleur (27,53). Je n'ai pas testé de `StandardScaler` avant Ridge : sa pénalité dépend de l'échelle des colonnes, et celles des satellites sont très petites.
