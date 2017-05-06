import pandas as pd
import numpy as np
import matplotlib
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge, RidgeCV, ElasticNet, LassoCV, LassoLarsCV, LinearRegression
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt
from scipy.stats import skew


def rmse_cv(model):
    rmse= np.sqrt(-cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv = 5))
    return rmse

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

numeric_feats = cleaned_data.dtypes[cleaned_data.dtypes != "object"].index
skewed_feats = cleaned_data[numeric_feats].apply(lambda x: skew(x.dropna()))
skewed_feats = skewed_feats[skewed_feats > 0.75]
skewed_feats = skewed_feats.index
cleaned_data[skewed_feats] = np.log1p(cleaned_data[skewed_feats])
cleaned_data = pd.get_dummies(cleaned_data)

# split data set
X_train, X_test, y_train, y_test = \
    train_test_split(cleaned_data[cleaned_data.columns.drop('price')], cleaned_data['price'],test_size=0.2, random_state=0)

# ridge
# alpha - a regularization parameter that measures how flexible our model is
# the higher the regularization the less prone our model will be to overfit
alphas = [0.05, 0.1, 0.3, 1, 3, 5, 10, 15, 30, 50, 75]
cv_ridge = [rmse_cv(Ridge(alpha = alpha)).mean()
            for alpha in alphas]
cv_ridge = pd.Series(cv_ridge, index = alphas)
cv_ridge.plot()
plt.xlabel("alpha")
plt.ylabel("rmse")
cv_ridge.min()

# lasso
# the alphas in Lasso CV are really the inverse or the alphas in Ridge
model_lasso = LassoCV(alphas=[1, 0.1, 0.001, 0.0005]).fit(X_train, y_train)
rmse_cv(model_lasso).mean()
coef = pd.Series(model_lasso.coef_, index = X_train.columns)
# feature selection: setting coefficients of unimportant attributes to 0
print("Lasso picked " + str(sum(coef != 0)) + " variables and eliminated the other "
      + str(sum(coef == 0)) + " variables")

# residual plot
matplotlib.rcParams['figure.figsize'] = (6.0, 6.0)
predictions = pd.DataFrame({"preds": model_lasso.predict(X_train), "true": y_train})
predictions["residuals"] = predictions["true"] - predictions["preds"]
predictions.plot(x="preds", y="residuals", kind="scatter")

# xgboost
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test)

params = {"max_depth": 2, "eta": 0.1}
# the params were tuned using xgb.cv
model = xgb.cv(params, dtrain,  num_boost_round=500, early_stopping_rounds=100)
model.loc[30:,["test-rmse-mean", "train-rmse-mean"]].plot()
model_xgb = xgb.XGBRegressor(n_estimators=360, max_depth=2, learning_rate=0.1)
model_xgb.fit(X_train, y_train)