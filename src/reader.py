import pandas as pd

def getArrays ():
    option2008 = pd.read_csv('result/2017.csv');

    result = pd.DataFrame({'S':option2008["close"], 'K':option2008["strike_price"], 'price':option2008["price"], 'rf':option2008["rf"],'dtm':option2008["day_diff"]}, columns=['S', 'K', 'price', 'rf', 'dtm'])
    result = result.reset_index(drop=True)
    result["dtm"]= result['dtm'].divide(360)
    arrays = result.as_matrix()

    print(len(arrays))
    return arrays

getArrays()