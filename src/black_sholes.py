# -*- coding: utf-8 -*-
from math import * 
from scipy.stats import norm
from scipy.optimize import fmin_bfgs

# Black Sholes Function
def BSPrice(S, K, T, r, vol, callPutFlag ='c'):
    d1 = (log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * sqrt(T))
    d2 = d1 - vol * sqrt(T)
    if (callPutFlag == 'c') or (callPutFlag == 'C'):
        return S * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
    else:
        return K * exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

#Calc Implied volatility        
def implied_vol(marketPrice, S, K, T, r, callPutFlag ='c'):
    Objective = lambda x: (marketPrice - BSPrice(S, K, T, r, x, callPutFlag)) ** 2
    return fmin_bfgs(Objective, 1, disp = False)[0]

if __name__ == '__main__':
    #correct : call 3.68
    print ("BlackS Print: {0}".format(BSPrice(49.0, 50.0, 1.0, 0.01, 0.2, 'C')))
    #correct : put 4.18
    print ("BlackS Print: {0}".format(BSPrice(49.0, 50.0, 1.0, 0.01, 0.2, 'P')))
    #correct : 0.2
    print ("BlackS Print: {0}".format(implied_vol(3.68, 49.0, 50.0, 1.0, 0.01, 'C')))
    #correct : 0.2
    print ("BlackS Print: {0}".format(implied_vol(4.18, 49.0, 50.0, 1.0, 0.01, 'P')))