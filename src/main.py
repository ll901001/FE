# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from src import black_sholes, heston,reader
from scipy.optimize import fmin
import pandas as pd

#sample market data
def sample_data():
    x = [x.split() for x in open('marketdata.txt')]
    header = x[0]
    market_datas = []
    for market_data in x[1:]:
        market_datas += [map(lambda z:float(z), market_data)]
    return (header, market_datas)

#parameter calibration(kappa, theta, sigma, rho, v0)
def calibrate(init_val, market_datas):
    def error(x, market_datas):
        kappa, theta, sigma, rho, v0 = x
        print ("kappa:{0}, theta:{1}, sigma:{2}, rho:{3}, v0:{4}".format(kappa, theta, sigma, rho, v0))
        if v0 < 0:
            v0 = 0.08
        result = 0.0
        for market_data in market_datas:
            s0, k, market_price, r, T = market_data
            # print (s0, k, market_price, r, T)

            heston_price = heston.call_price(kappa, theta, sigma, rho, v0, r, T, s0, k)
            result += (heston_price - market_price)**2
        return result
    opt = fmin(error, init_val, args = (market_datas,), maxiter = 20)
    return opt


if __name__ == '__main__':
    #load market data
    header, market_datas = sample_data()

    for yearNumber in ["2008","2009","2010"]:

        market_datas = reader.getArrays(yearNumber)
    #Initialize kappa, theta, sigma, rho, v0
        init_val = [1.1, 0.1, 0.4, -0.6, 0.1]
        #calibration of parameters
        test = calibrate(init_val, market_datas)
        [kappa, theta, sigma, rho, v0] = calibrate(init_val, market_datas)
        print ("kappa:{0}, theta:{1}, sigma:{2}, rho:{3}, v0:{4}".format(kappa, theta, sigma, rho, v0))
        result = pd.DataFrame([kappa, theta, sigma, rho, v0])
        result.to_csv("cal"+yearNumber+".csv")

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
