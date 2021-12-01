Adverse Food Events Analysis
==============================

Detailed EDA of adverse food events reported to FDA.


## Team Members

- Mohit Shah 
- Aditya Rustagi
- Jianghong Wan
- Rajasvi Vinayak Sharma
- Sydney Larson

## Motivation and Objective 

- Everyone gets sick due to bad food products. 
- Study and analyse the [FDA data of reported adverse food events from 2004-2020.](https://www.fda.gov/food/compliance-enforcement/cfsan-adverse-event-reporting-system-caers)
- Help users be aware of potential health risks before purchasing a product.

## Required Packages
- pandas
```
pip install pandas
```
- plotly
```
pip install plotly
```
- Natural Tool Kit
```
pip install nltk
```


## Project Organization

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks for visualization. 
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Script to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


## Running the Code 

### Data Cleaning

Script for cleaning the raw data is found in <code>scr/data</code>.

### Visualization

Script for visualization of data is found in <code>src/visualization</code>.

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
