# Module 3 — Transfer to Python

## Question — Why move the pipeline to `src/air_quality/`?

### Why a notebook alone is not enough

1. **Reuse:** in a notebook, we copy and paste code to reuse it, and the copies can become different. In `src/air_quality/`, we write a function once and import it everywhere.
2. **Tests:** functions in a package can be tested automatically with `pytest`. A notebook cannot, so we only see a bug by reading the output.
3. **Reproducibility:** a notebook depends on the order in which the cells were run. `run_baseline(config)` gives the same result every time and can run from the terminal with `scripts/run_pipeline.py`.
4. **Git:** a `.ipynb` file has a messy diff (outputs, metadata), while `.py` files are easy to review.

### What is a dataclass?

A dataclass is a class that mainly stores data. The `@dataclass` decorator writes the usual methods for us from the annotated fields. For `PipelineConfig`, it saves us from writing by hand:
- `__init__` with all the parameters and their default values (`train_city="Kampala"`, etc.),
- `__repr__` to print the config clearly,
- `__eq__` to compare two configs.

So all the settings are in one place, and we can change an experiment with `PipelineConfig(train_city="Nairobi", test_city="Kampala")`.

### Why split into `data.py`, `features.py` and `evaluation.py`?

Each file has one responsibility:
- `data.py`: loading and cleaning the data,
- `features.py`: creating and choosing the features,
- `evaluation.py`: computing the metrics (RMSE, MAE, R²).

Compared with one long script, it is easier to read and to find a bug, a change in one part does not break the others, each function can be tested alone, and the code can be reused (for example `regression_metrics` for any future model). `workflows.py` then just chains the steps.
