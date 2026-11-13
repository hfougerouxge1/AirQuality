"""Register two versions of Module 7's pipeline and promote the better one to champion."""

from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import GroupKFold, cross_val_score
from sklearn.pipeline import Pipeline

from air_quality import data, features, registry
from air_quality.transformers import AirQualityCleaner

ALL_CITIES = ["Kampala", "Nairobi", "Lagos", "Bujumbura"]
EXCLUDED_RAW_COLUMNS = {"id", "site_id", "country", "month"}
MODEL_NAME = "air_quality_model"


def main() -> None:
    """
    Rebuild Module 7's chained Pipeline (AirQualityCleaner + RFE + a model)
    twice, once with LinearRegression and once with Ridge, register each as
    a new version of MODEL_NAME, and promote whichever one scores better on
    cross_val_score to the "champion" alias.
    """
    train_df, _ = data.load_datasets()
    columns = [c for c in train_df.columns if c not in EXCLUDED_RAW_COLUMNS]

    scoped = data.restrict_to_scope(train_df, ALL_CITIES, columns)
    scoped = scoped.sort_values(["city", "date"]).reset_index(drop=True)
    enriched = features.add_temporal_features(scoped)

    X = enriched.drop(columns="pm2_5")
    y = enriched["pm2_5"]

    candidates = {
        "LinearRegression": LinearRegression,
        "Ridge": Ridge,
    }

    results = {}
    for name, model_class in candidates.items():
        # Two separate instances of the same class: one for RFE, one for the final model
        pipeline = Pipeline([
            ("cleaner", AirQualityCleaner(missing_threshold=0.6)),
            ("selector", RFE(estimator=model_class(), n_features_to_select=8)),
            ("model", model_class()),
        ])

        scores = cross_val_score(
            pipeline, X, y,
            groups=X["city"],
            cv=GroupKFold(n_splits=len(ALL_CITIES)),
            scoring="neg_root_mean_squared_error",
        )
        rmse_mean = float(-scores.mean())

        # cross_val_score only estimates performance; the registered version is trained on everything
        pipeline.fit(X, y)
        version = registry.register_pipeline(pipeline, MODEL_NAME)
        results[name] = {"version": version, "rmse_mean": rmse_mean}

    best = min(results, key=lambda n: results[n]["rmse_mean"])
    registry.promote_to_champion(MODEL_NAME, results[best]["version"])

    for name, r in results.items():
        marker = "  <- champion" if name == best else ""
        print(f"{name:<17} version {r['version']}  rmse_mean = {r['rmse_mean']:.2f}{marker}")



if __name__ == "__main__":
    main()
