# Module 9 — Model Registry

**1. Quel modèle est champion dans mon run, et est-ce cohérent avec le Module 7 ?** Ridge est champion. J'ai lancé le script deux fois, donc le registre contient 4 versions : les versions 1 et 3 sont des LinearRegression, les versions 2 et 4 des Ridge, et l'alias `champion` pointe sur la version 4 (Ridge). Les deux lancements donnent les mêmes résultats :

| Modèle | Versions | RMSE moyen | Champion |
|---|---|---|---|
| LinearRegression | 1 et 3 | 1321,24 | |
| Ridge | 2 et 4 | **29,26** | oui (version 4) |

C'est cohérent avec le Module 7 : ce sont exactement les deux moyennes de mon tableau, donc le pipeline est bien reconstruit à l'identique. La cause est la même qu'au Module 7 : la régression linéaire simple explose sur le pli Kampala (RMSE de 5 190), à cause de poids énormes sur des colonnes quasi identiques, et Ridge évite cela grâce à sa pénalité sur la taille des coefficients. Ridge gagne ici surtout parce que l'autre candidat est très mauvais : il reste moins bon que XGBoost (27,8 au Module 7), qui ne faisait pas partie de cette comparaison.

**2. Que casserait un `models:/air_quality_model/2` écrit en dur ?** Rien ne casse tout de suite : la version 2 existe toujours et se charge normalement. Le problème apparaît quand on enregistre un meilleur modèle. Le code qui fait les prédictions continue de charger la version 2, sans erreur et sans prévenir, donc il n'utilise jamais le nouveau modèle tant que je ne change pas le numéro à la main. Si ce numéro est écrit à plusieurs endroits, un oubli laisse une partie du code sur l'ancien modèle. Ce cas est réel dans mon propre run : après le deuxième lancement du script, le meilleur Ridge est la version 4, et un code figé sur la version 2 serait resté sur l'ancienne.

L'alias `@champion` est un nom qu'on peut déplacer. Pour changer de modèle, il suffit d'un seul `set_registered_model_alias(...)`, et tous les `load_model("models:/air_quality_model@champion")` chargent la nouvelle version sans qu'aucune ligne de code change. On peut aussi revenir à l'ancienne version en une commande si la nouvelle est moins bonne. Un numéro de version dit seulement « celle-ci », alors que l'alias dit « celle que j'ai choisie d'utiliser », et ce choix peut évoluer.
