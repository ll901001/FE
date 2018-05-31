import pandas as pd

def getArrays (year):
    option2008 = pd.read_csv('result/result'+year+'.csv');

    result = pd.DataFrame({'S':option2008["close"], 'K':option2008["strike_price"], 'price':option2008["price"], 'rf':option2008["rf"],'dtm':option2008["day_diff"], 'vega':option2008["vega"],'weekNo':option2008["weekNo"]}, columns=['S', 'K', 'price', 'rf', 'dtm','vega','weekNo'])
    result = result.reset_index(drop=True)
    result["dtm"]= result['dtm'].divide(360)
    result["vega"] = result['vega'].divide(100)
    arrays = result.as_matrix()

    print(len(arrays))
    print(result.head(2))
    return arrays

if __name__ == '__main__':
    getArrays("2017")