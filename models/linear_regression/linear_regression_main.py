import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error

from shared.utils import fetch_api_data, plot_predictions
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def linear_regression_prediction(company_code, period):
    data, metadata = fetch_api_data(company_code, period)

    x_train_open, x_test_open, y_train_open, y_test_open = prepare_data(data, 'open')
    x_train_close, x_test_close, y_train_close, y_test_close = prepare_data(data, 'close')
    x_train_high, x_test_high, y_train_high, y_test_high = prepare_data(data, 'high')
    x_train_low, x_test_low, y_train_low, y_test_low = prepare_data(data, 'low')
    x_train_volume, x_test_volume, y_train_volume, y_test_volume = prepare_data(data, 'volume')

    y_pred_open, mse_open = predict(x_train_open, x_test_open, y_train_open, y_test_open)
    y_pred_close, mse_close = predict(x_train_close, x_test_close, y_train_close, y_test_close)
    y_pred_high, mse_high = predict(x_train_high, x_test_high, y_train_high, y_test_high)
    y_pred_low, mse_low = predict(x_train_low, x_test_low, y_train_low, y_test_low)
    y_pred_volume, mse_volume = predict(x_train_volume, x_test_volume, y_train_volume, y_test_volume)

    response = {
        "companyCode": company_code,
        "period": period,
        "open": {
            "dates": x_test_open.tolist(),
            "predictedCustom": y_pred_open.tolist(),
            "predictedLibrary": y_pred_open.tolist(),
            "errorCustom": mse_open,
            "errorLibrary": mse_open,
            "actual": y_test_open.tolist()
        },
        "close": {
            "dates": x_test_close.tolist(),
            "predictedCustom": y_pred_close.tolist(),
            "predictedLibrary": y_pred_close.tolist(),
            "errorCustom": mse_close,
            "errorLibrary": mse_close,
            "actual": y_test_close.tolist()
        },
        "high": {
            "dates": x_test_high.tolist(),
            "predictedCustom": y_pred_high.tolist(),
            "predictedLibrary": y_pred_high.tolist(),
            "errorCustom": mse_high,
            "errorLibrary": mse_high,
            "actual": y_test_high.tolist()
        },
        "low": {
            "dates": x_test_low.tolist(),
            "predictedCustom": y_pred_low.tolist(),
            "predictedLibrary": y_pred_low.tolist(),
            "errorCustom": mse_low,
            "errorLibrary": mse_low,
            "actual": y_test_low.tolist()
        },
        "volume": {
            "dates": x_test_volume.tolist(),
            "predictedCustom": y_pred_volume.tolist(),
            "predictedLibrary": y_pred_volume.tolist(),
            "errorCustom": mse_volume,
            "errorLibrary": mse_volume,
            "actual": y_test_volume.tolist()
        },
    }

    return response


def predict(x_train, x_test, y_train, y_test):
    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)

    return y_pred, mse


def prepare_data(data, factor):
    y = data[factor].values
    x = data['Date'].values.reshape(-1,1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    return x_train, x_test, y_train, y_test

#
# if __name__ == '__main__':
#     x_test_1, y_test_1, y_pred_1 = linear_regression_prediction("IBM", "weekly")
#     plot_predictions(x_test_1, y_test_1, y_pred_1, "Plot title")
