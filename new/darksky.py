import forecastio

api_key = "77eb864c8ec94685a5834e714c840e03"
lat = -6.978887
lng = 107.630328

forecast = forecastio.load_forecast(api_key, lat, lng)
print(forecast)