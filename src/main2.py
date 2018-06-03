# -*- coding: utf-8 -*-
from src import mutiheston,reader
from scipy.optimize import minimize, fmin
import pandas as pd


#parameter calibration(kappa, theta, sigma, rho, v0)
def calibrate(init_val, market_datas):

    opt = minimize(error, init_val, args = (market_datas,),
                   bounds = ((0.1, 0.5),(0.01, 0.4), (0.1,0.99),(-0.99,-0.045),(0.01,0.5),
                             (1,5),(0.01, 0.5),(0.01,0.6), (-0.89,-0.45),(0.01,0.5)),
                   method='Nelder-Mead',options = {'maxiter': None})
    # opt = fmin(error, init_val, args=(market_datas,),maxiter= 20)
    return opt

def error(x, market_datas):
    kappa1, theta1, sigma1, rho1, v01, kappa2, theta2, sigma2, rho2, v02 = x
    print ("kappa1:{0}, theta1:{1}, sigma1:{2}, rho1:{3}, v01:{4}".format(kappa1, theta1, sigma1, rho1, v01))
    print ("kappa2:{0}, theta2:{1}, sigma2:{2}, rho2:{3}, v02:{4}".format(kappa2, theta2, sigma2, rho2, v02))

    result = 0.0
    for market_data in market_datas:
        s0, k, market_price, r, T, vega, weekNo = market_data
        # print ("s0:{0}, k:{1}, market_price:{2}, r:{3}, T:{4}".format(s0, k, market_price, r, T))

        heston_price = mutiheston.call_price(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v01, v02, r, T, s0, k)

        errorNum = (heston_price - market_price)**2/market_price**2/vega**2
        result+= errorNum

        if (kappa1 < 0.01) | (kappa1 > 3) | (kappa2 < 1.01) | (kappa2 > 5):
            result+= errorNum * 10
        if (theta1 < 0.01) | (theta1 > 1) | (theta2 < 0.01) | (theta2 > 1):
            result+= errorNum * 10
        if (sigma1 < 0.01) | (sigma1 > 2) | (sigma2 < 0.01) | (sigma2 > 0.5):
            result+= errorNum * 10
        if (rho1 < -0.88) | (rho1 > -0.45) | (rho2 < -0.98) | (rho2 > -0.35):
            result+= errorNum * 10
        if (v01 < 0.01) | (v01 > 1) | (v02 < 0.01) | (v02 > 1):
            result+= errorNum * 100
    return result

if __name__ == '__main__':
    
    for yearNumber in ["2014"]:

        market_datas = reader.getArrays(yearNumber)

        init_val = [0.2, 0.1, 0.8, -0.8, 0.2, 2, 0.1, 0.5, -0.8, 0.2]

        print (("error: {0}").format(error(init_val,market_datas)/len(market_datas)))

    market_prices = np.array([])
    heston_prices = np.array([])
    K = np.array([])
    for market_data in market_datas:
        s0, k, market_price, r, T = market_data
        heston_prices = np.append(heston_prices, heston.call_price(kappa, theta, sigma, rho, v0, r, T, s0, k))
        market_prices = np.append(market_prices, market_price)
        K = np.append(K,k)
    #plot result
    plt.plot(K, market_prices, 'g*',K, heston_prices, 'b')
    plt.xlabel('Strike (K)')
    plt.ylabel('Price')
    plt.show()
