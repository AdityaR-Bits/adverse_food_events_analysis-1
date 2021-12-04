Adverse Food Events Analysis
==============================

Detailed EDA of adverse food events reported to FDA.


## Team Members

- Mohit Shah             (@razor139)
- Aditya Rustagi         (@AdityaR-Bits)
- Jianghong Wan          (@JWRickyWan)
- Rajasvi Vinayak Sharma (@Rajasvi)
- Sydney Larson          (@phoenix-flames)

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
    ├── README.md                      <- The top-level README for developers using this project.
    ├── data
    │   ├── processed      		       <- The final, canonical data sets for modeling.
    │   └── raw            		       <- The original, immutable data dump.
    │
    ├── notebooks          		       <- Jupyter notebooks for visualization and data cleaning. 
    │
    ├── references         		       <- News clippings related to adverse food events. 
    │
    ├── reports            		       <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── ECE 143 Final Project.pdf  <- pdf of presentation.
    │
    └── src                		       <- Source code for use in this project.
        ├── __init__.py    		       <- Makes src a Python module.
        │
        ├── data           		       <- Scripts to generate data.
        │   └── make_dataset.py
        │
        └── visualization  		       <- Script to create exploratory and results oriented visualizations.
            └── visualizations.ipynb   <- Visualization notebook. 
 

## Visualization

The notebook for visualization of data is found in <code>src/visualization</code>.

```
visualizations.ipynb
```

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
