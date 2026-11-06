# Module 4 — Sélection de features

| Ensemble de features | Colonnes | RMSE moyen | R² moyen |
|---|---|---|---|
| Toutes les features | 66 | 3995,0 | -306 447 |
| SelectKBest | 8 | 32,8 | -1,19 |
| Choisies à la main (Module 3) | 8 | 28,8 | -0,004 |
| RFE | 8 | 27,6 | 0,07 |

**RFE face aux colonnes choisies à la main.** RFE est aussi bon que les 8 colonnes choisies à la main (27,6 contre 28,8). Il a gardé des colonnes de SO2, CO, NO2 et HCHO : l'algorithme a donc retrouvé presque le même choix qu'un humain.

**Pourquoi SelectKBest est moins bon.** Il note chaque colonne séparément, donc il ne voit pas les copies. Quatre de ses 8 colonnes sont des colonnes `solar_azimuth_angle` avec une corrélation de 1,00 : la même information quatre fois. RFE réentraîne le modèle après chaque suppression, donc il élimine les copies.

**Quand la méthode univariée suffit.** Elle suffit quand les colonnes sont assez différentes les unes des autres. Elle ne suffit pas quand beaucoup de colonnes sont des copies, comme ici, car elle ne voit pas la redondance.

**Il ne faut pas faire confiance au modèle avec toutes les features.** Le RMSE moyen est de 3995 alors que le PM2.5 va seulement de 1,2 à 456. Le modèle donne des poids énormes à des colonnes presque identiques, par exemple -358 825 pour `nitrogendioxide_stratospheric_no2_column_number_density`. Sur une nouvelle ville, les poids ne se compensent plus et l'erreur explose (multicolinéarité).
