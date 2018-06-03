import pandas as pd
from src import main, reader

if __name__ == '__main__':
    result = pd.read_csv("calonefactor2014.csv")

    vol = result.iloc[[1]]
    vol = vol.as_matrix()
    vol = vol[0]
    vol = vol[1:]

    para = result.iloc[[0]]
    para = para.as_matrix()
    para = para[0]
    para = para[1:5]

    md = reader.getArrays("2014")


    err = main.errorParameters(x=para,market_datas=md,vols=vol)
    print (err)

    # 2013:
    # 2014: 1.6679716081939802