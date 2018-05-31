from src import black_sholes, heston,reader
from scipy.optimize import minimize, fmin
import pandas as pd
import numpy as np

#sample market data
def sample_data():
    x = [x.split() for x in open('marketdata.txt')]
    header = x[0]
    market_datas = []
    for market_data in x[1:]:
        market_datas += [map(lambda z:float(z), market_data)]
    return (header, market_datas)

#parameter calibration(kappa, theta, sigma, rho, v0)
def calibrateParam(init_para, market_datas, vols):

    paraEs = init_para

    optParam = minimize(errorParameters, paraEs, args = (market_datas, vols), bounds = ((1.01, 5), (0.01, 1), (0.01, 1), (-0.88, -0.45), (0.01, 1)), method='Nelder-Mead', options = {'maxiter': 50})
    param = optParam.x

    return param

def calibrateVol (init_para, market_datas, vols):
    for i in range(1,52):
        v0 = vols[i-1]

        optV  = minimize(errorVol, v0, args = (market_datas,init_para, i), method='Nelder-Mead', options = {'maxiter': 50})
        v0result = optV.x[0]
        vols[i-1] = v0result
    return vols


def errorParameters(x, market_datas, vols):
    kappa, theta, sigma, rho = x
    print ("kappa:{0}, theta:{1}, sigma:{2}, rho:{3}".format(kappa, theta, sigma, rho))
    result = 0.0
    for market_data in market_datas:
        s0, k, market_price, r, T, vega, weekNo = market_data

        v0 = vols[int(weekNo)-1]

        heston_price = heston.call_price(kappa, theta, sigma, rho, v0, r, T, s0, k)

        error= (heston_price - market_price)**2/market_price**2/vega**2
        result += error

        if (kappa < 1.01) | (kappa > 5):
            result+= error * 10
        if (theta < 0.01) | (theta > 1):
            result+= error * 10
        if (sigma < 0.01) | (sigma > 1):
            result+= error * 10
        if (rho < -0.88) | (rho > -0.45):
            result+= error * 10
    return result

def errorVol(x, market_datas, parameters, i):
    v0 = x
    kappa, theta, sigma, rho = parameters
    result = 0.0
    print ("v0:{0}".format(v0))

    for market_data in market_datas:
        s0, k, market_price, r, T, vega, weekNo = market_data

        # print ("s0:{0}, k:{1}, market_price:{2}, r:{3}, T:{4}".format(s0, k, market_price, r, T))

        if (int(weekNo) == i):
            heston_price = heston.call_price(kappa, theta, sigma, rho, v0[0], r, T, s0, k)

            error = (heston_price - market_price) ** 2 / market_price ** 2 / vega ** 2
            result += error

            if (v0 < 0) | (v0 > 100):
                result += error * 10
    return result


if __name__ == '__main__':
    #load market data
    header, market_datas = sample_data()

    for yearNumber in ["2015","2016","2017"]:

        market_datas = reader.getArrays(yearNumber)
    #Initialize kappa, theta, sigma, rho, v0
        init_val = [2, 0.1, 0.4, -0.6]
        vols = np.repeat(0.1,53)
        # init_val = [1.7857335413857758, 0.09828053359611841, 0.76161049388424428, -0.8383242759610362, 0.1]
        sumNum = 10000

        while True:
            params = calibrateParam(init_val, market_datas, vols)
            init_val = params
            vols = calibrateVol(params, market_datas, vols)
            if ((sumNum - sum(vols))**2 < 100):
                break
            sumNum = sum(vols)
        #     init_val = test.x
        #
        #     if test.x[4] > 0:
        #         break;

        print (("error: {0}").format(errorParameters(params, market_datas,vols) / len(market_datas)))
        result = pd.DataFrame([params, vols])
        result.to_csv("calonefactor"+yearNumber+".csv")

    #
    # market_prices = np.array([])
    # heston_prices = np.array([])
    # K = np.array([])
    # for market_data in market_datas:
    #     s0, k, market_price, r, T = market_data
    #     heston_prices = np.append(heston_prices, heston.call_price(kappa, theta, sigma, rho, v0, r, T, s0, k))
    #     market_prices = np.append(market_prices, market_price)
    #     K = np.append(K,k)
    # #plot result
    # plt.plot(K, market_prices, 'g*',K, heston_prices, 'b')
    # plt.xlabel('Strike (K)')
    # plt.ylabel('Price')
    # plt.show()
