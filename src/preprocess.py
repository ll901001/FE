import pandas as pd

index = pd.read_csv('Data/index.csv');

file_list = ['2008', "2009", "2010", "2011","2012","2013","2014","2015","2016","2017"];

for file in file_list:

    option = pd.read_csv("Data/"+file+".csv")

    option["strike_price"] =option["strike_price"]/1000

    option["price"] = (option["best_bid"] + option["best_offer"])/2

    result = pd.merge(option, index, how='inner', on=['date'])

    result["S/K"] = result["close"]/result["strike_price"]

    date_format = "%Y%m%d"
    result["date"] = pd.to_datetime(result["date"], format=date_format)
    result["weekNo"] = pd.to_datetime(result["date"], format=date_format).dt.week
    result["exdate"] = pd.to_datetime(result["exdate"], format=date_format)
    result["day_diff"] = result["exdate"] - result["date"]
    result["day_diff"] = result["day_diff"].astype('timedelta64[D]')

    result = result[result["vega"] > 0]
    result = result[result["day_diff"] < 360]
    result = result[result["day_diff"] > 14]
    result = result[(result["day_diff"] == 30).iloc[::50] | (result["day_diff"] == 60).iloc[::10] | (result["day_diff"] == 90).iloc[::5] | (
                result["day_diff"] == 120) | (result["day_diff"] == 150).iloc[::3] | (result["day_diff"] == 180) | (
                                result["day_diff"] == 210).iloc[::2] | (result["day_diff"] == 240).iloc[::2] | (result["day_diff"] == 270).iloc[::2]| (result["day_diff"] == 300)]
    result = result[result["S/K"] > 0.9]
    result = result[result["S/K"] < 1.1]

    result = result[["close","strike_price", "price", "rf", "S/K","day_diff","weekNo","date","exdate","impl_volatility","vega"]]
    result.to_csv("result/result"+file+".csv")



