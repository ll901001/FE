# -*- coding: utf-8 -*-
from src import mutiheston,reader
from scipy.optimize import minimize, fmin
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

    opt = minimize(error, init_val, args = (market_datas,),
                   bounds = ((0.1, 0.5),(0.01, 0.4), (0.1,0.99),(-0.99,-0.045),
                             (1,5),(0.01, 0.5),(0.01,0.6), (-0.89,-0.45),(0.01,0.5),(0.01,0.5)),
                   method='BFGS',options = {'maxiter': 20})
    # opt = fmin(error, init_val, args=(market_datas,),maxiter= 20)
    return opt

def error(x, market_datas):
    kappa1, theta1, sigma1, rho1, v01, kappa2, theta2, sigma2, rho2, v02 = x
    print ("kappa1:{0}, theta1:{1}, sigma1:{2}, rho1:{3}, v01:{4}".format(kappa1, theta1, sigma1, rho1, v01))
    print ("kappa2:{0}, theta2:{1}, sigma2:{2}, rho2:{3}, v02:{4}".format(kappa2, theta2, sigma2, rho2, v02))

    result = 0.0
    for market_data in market_datas:
        s0, k, market_price, r, T, vega = market_data
        # print ("s0:{0}, k:{1}, market_price:{2}, r:{3}, T:{4}".format(s0, k, market_price, r, T))

        heston_price = mutiheston.call_price(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v01, v02, r, T, s0, k)

        result += (heston_price - market_price)**2/market_price**2/vega**2
    return result

if __name__ == '__main__':
    #load market data
    header, market_datas = sample_data()

    for yearNumber in ["2010"]:

        market_datas = reader.getArrays(yearNumber)
    #Initialize kappa, theta, sigma, rho, v0
        # init_val = [1.1, 0.1, 0.4, -0.6, 0.1]
        init_val = [0.2, 0.1, 0.8, -0.8, 0.1, 2, 0.1, 0.5, -0.8, 0.1]
        #calibration of parameters
        # [kappa, theta, sigma, rho, v0] = calibrate(init_val, market_datas).x
        # print ("kappa:{0}, theta:{1}, sigma:{2}, rho:{3}, v0:{4}".format(kappa, theta, sigma, rho, v0))
        # result = pd.DataFrame([kappa, theta, sigma, rho, v0] )

        test = calibrate(init_val, market_datas)


        print (("error: {0}").format(error(test.x,market_datas)/len(market_datas)))
        result = pd.DataFrame([test])
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
