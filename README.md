ECE 143 Group 4: Adverse Food Events Analysis
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
- Natural Language Tool Kit
```
pip install nltk
```

Details can be found in requirements.txt


## Project Organization

    ├── LICENSE
    ├── README.md                      <- The top-level README for developers using this project.
	├── requirements.txt               <- Required 3rd party modules. 
    ├── data
    │   ├── processed      		       <- The final, canonical data sets for modeling.
    │   └── raw            		       <- The original, immutable raw data.
    │
    ├── references         		       <- News clippings related to adverse food events. 
    │
    ├── reports            		       <- Generated analysis as HTML, PDF, LaTeX, etc.
	│   └── figures					   <- Figures used in presentation. 
    │   └── ECE 143 Final Project.pdf  <- pdf of presentation.
    │
    └── src                		       <- Source code for use in this project.
        ├── __init__.py    		       <- Makes src a Python module.
        │
        ├── data           		       <- Scripts to generate data.
        │   └── make_dataset.py
        │
        └── visualization  		       <- Create exploratory and results oriented visualizations.
            └── visualizations.ipynb   <- Visualization notebook. 
			└── visualize.py    	   <- File containing functions used in visualizations.ipynb.
 

## Visualization

The notebook for visualization of data is found in [<code>src/visualization</code>](https://github.com/Rajasvi/adverse_food_events_analysis/tree/master/src/visualization).

```
visualizations.ipynb
```

## Note

The code has been run using:

- Python 3.8.11
- MacOS/Windows
