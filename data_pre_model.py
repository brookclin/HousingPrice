import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, RidgeCV, ElasticNet, LassoCV, LassoLarsCV, LinearRegression
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from scipy.stats import skew

# read in data, transform data types, clean nulls
raw_data = pd.read_json("result.json")
raw_data = raw_data.transpose()
raw_data = raw_data.drop("neighborhood", axis=1)
raw_data['price'] = pd.to_numeric(raw_data['price'])
raw_data['flooring'] = pd.to_numeric(raw_data['flooring'])
raw_data['score'] = pd.to_numeric(raw_data['score'])
raw_data['lot'] = pd.to_numeric(raw_data['lot'])
raw_data = raw_data[pd.notnull(raw_data['price'])]
raw_data = raw_data.loc[raw_data.dropna().index]

# deleting for cleaned data
bedrooms = raw_data.groupby("bedrooms").size()
bedrooms = bedrooms[bedrooms > 5].index
cleaned_data = raw_data[raw_data["bedrooms"].isin(bedrooms)]
postcode = cleaned_data.groupby("postcode").size()
postcode = postcode[postcode > 20].index
cleaned_data = cleaned_data[cleaned_data["postcode"].isin(postcode)]
cleaned_data = cleaned_data[cleaned_data["flooring"] < 10000]
cleaned_data = cleaned_data[cleaned_data["flooring"] > 200]
cleaned_data = cleaned_data[cleaned_data["lot"] < 100000]
cleaned_data = cleaned_data[cleaned_data["price"] < 8000000]
cleaned_data = cleaned_data[cleaned_data["price"] > 20000]