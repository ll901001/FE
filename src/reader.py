import pandas as pd

def getArrays ():
    option2008 = pd.read_csv('result/result2017.csv');

    option2008 = option2008[(option2008["S/K"]<1.2) & (option2008["S/K"]> 0.8)]
    option2008 = option2008[option2008["day_diff"]==180]

    result = pd.DataFrame({'S':option2008["close"], 'K':option2008["strike_price"], 'price':option2008["price"], 'rf':option2008["rf"],'dtm':option2008["day_diff"]}, columns=['S', 'K', 'price', 'rf', 'dtm'])
    result = result.reset_index(drop=True)
    result["dtm"]= result['dtm'].divide(360)
    arrays = result.as_matrix()

    print(arrays)
    return arrays

getArrays()