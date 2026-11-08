# Data card

## Origin and attribution

The repository includes the user's supplied `heart_disease_uci.csv`, a transformed, pooled version of the UCI Heart Disease data. Its exact download URL and transformation history were not recorded; it is not presented as an untouched official UCI export.

Original source: [UCI Heart Disease](https://archive.ics.uci.edu/dataset/45/heart+disease), DOI [10.24432/C52P4X](https://doi.org/10.24432/C52P4X). UCI credits Andras Janosi, William Steinbrunn, Matthias Pfisterer, and Robert Detrano and distributes its dataset under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribute the original creators and retain this notice when reusing the data. This attribution does not establish the undocumented transformation history of the local CSV.

The original study is Detrano et al. (1989), *International application of a new probability algorithm for the diagnosis of coronary artery disease*, American Journal of Cardiology. See UCI for bibliographic details.

Local CSV SHA-256:

```text
acc0c823fe8a105fffda476b2d3e5e45f0642ca75afd8285879384a7d6d130f8
```

## Local data and transformations

- 922 rows, 16 columns. Four site labels: Cleveland, Hungary, Switzerland, VA Long Beach.
- Remove two exact duplicate rows, then two additional repeated clinical profiles ignoring `id` (including site and original diagnosis in the comparison): 918 analysis rows. Different IDs can represent different people; this is a conservative anti-overlap policy, not a claim that patient identity has been confirmed.
- Convert zero `trestbps` and zero `chol` to missing. These are fixed measurement-validity rules, not learned cutoffs.
- Keep negative `oldpeak`, clinically extreme measurements, and sparsely observed columns. Do not globally clip outliers or discard rows by a missingness threshold.
- Derive binary `target = (num > 0)`. Exclude `num`, `id`, and `dataset` from predictors.
- Fit numeric imputation, missingness indicators, scaling, categorical imputation, and encoding within each training fold. The raw CSV is never overwritten.

## Dictionary

| Column | Meaning | Role / handling |
|---|---|---|
| `id` | Local record identifier | Audit only; excluded |
| `age` | Age in years | Numeric |
| `sex` | Recorded sex | Categorical; limited representation |
| `dataset` | Collection site | Audit and site validation only |
| `cp` | Chest pain category | Categorical |
| `trestbps` | Resting blood pressure, mm Hg | Numeric; zero becomes missing |
| `chol` | Serum cholesterol, mg/dL | Numeric; zero becomes missing |
| `fbs` | Fasting blood sugar above 120 mg/dL | Categorical boolean |
| `restecg` | Resting electrocardiographic category | Categorical |
| `thalch` | Maximum heart rate achieved | Numeric; local alias of UCI `thalach` |
| `exang` | Exercise-induced angina | Categorical boolean |
| `oldpeak` | Exercise-related ST depression relative to rest | Numeric; negatives retained |
| `slope` | Peak exercise ST-segment slope | Categorical |
| `ca` | Number of major vessels coloured by fluoroscopy | Numeric count; substantial missingness |
| `thal` | Thallium test category: normal, fixed defect, reversible defect | Categorical; local spelling retained |
| `num` | Original diagnosis grade, 0–4 | Source label; never a predictor |

## Intended use and limits

Educational, retrospective analysis only. The binary label collapses diagnosis grades and does not encode future events. Diagnostic measurements may not be available at a proposed screening time. Site-specific case mix, sex imbalance, historic collection practices, and missingness limit external validity. The dataset is not a representative prevalence sample. Patient-level identity beyond the supplied ID is unavailable.

The notebook's random holdout tests discrimination in this pooled sample. Its training-only leave-one-site-out diagnostic tests a different, more demanding transfer setting. Neither is independent contemporary clinical validation.
