# -*- coding: utf-8 -*-
from scipy import *
from scipy.integrate import quad


# public
def call_price(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, K: object) -> object:
    p1 = __p1(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, K)
    p2 = __p2(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, K)
    return (s0 * p1 - K * exp(-r * T) * p2)


# private
def __p(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, K, status):
    if status == 1:
        integrand = lambda phi: (exp(-1j * phi * log(K)) *
                                 __f(phi + 1, kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, status) / (1j * phi * s0 * exp(r * T))).real
    else:
        integrand = lambda phi: (exp(-1j * phi * log(K)) *
                                 __f(phi, kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, status) / (1j * phi)).real

    return (0.5 + (1 / pi) * quad(integrand, 0, 100)[0])


def __p1(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, K):
    return __p(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, K, 1 )


def __p2(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, K):
    return __p(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, K, 2)


def __f(phi, kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, status):
    if status == 1:
        u = 0.5
        b = kappa1 - rho1 * sigma1
    else:
        u = -0.5
        b = kappa1

    a = kappa1 * theta1
    x = log(s0)
    d = sqrt((rho1 * sigma1 * phi * 1j - b) ** 2 - sigma1 ** 2 * (2 * u * phi * 1j - phi ** 2))
    g = (b - rho1 * sigma1 * phi * 1j + d) / (b - rho1 * sigma1 * phi * 1j - d)
    A = r * phi * 1j * T + (a / sigma1 ** 2) * (
                (b - rho1 * sigma1 * phi * 1j + d) * T - 2 * log((1 - g * exp(d * T)) / (1 - g)))
    B1 = (b - rho1 * sigma1 * phi * 1j + d) / sigma1 ** 2 * ((1 - exp(d * T)) / (1 - g * exp(d * T)))
    return exp(A + B1 * v0 + 1j * phi * x)


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from src import black_sholes

    # maturity
    T = 5.0
    # risk free rate
    r = 0.05
    # long term volatility(equiribrium level)
    theta1 = 0.1
    theta2 = 0.1
    # Mean reversion speed of volatility
    kappa1 = 1.1
    kappa2 = 1.1
    # sigma(volatility of Volatility)
    sigma1 = 0.4
    sigma2 = 0.4
    # rho
    rho1 = -0.6
    rho2 = -0.6
    # Initial stock price
    s0 = 1.0
    # Initial volatility
    v0 = 0.1
    # 0.634
    print("call_price: {0}".format(call_price(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, 0.5)))
    # 0.384
    print("call_price: {0}".format(call_price(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, 1.0)))
    # 0.176
    print("call_price: {0}".format(call_price(kappa1, theta1, sigma1, rho1, kappa2, theta2, sigma2, rho2, v0, r, T, s0, 1.5)))
    # Strikes
    K = np.arange(0.1, 5.0, 0.25)
    # simulation
    imp_vol = np.array([])
    for k in K:
        # calc option price
        price = call_price(kappa1, theta1, sigma1, rho1, v0, r, T, s0, k)
        # calc implied volatility
        imp_vol = np.append(imp_vol, black_sholes.implied_vol(price, s0, k, T, r, 'C'))
        print("k: {0} , price: {1}, imp_vol: {2}".format(k, price, imp_vol[-1]))

    # plot result
    plt.plot(K, imp_vol)
    plt.xlabel('Strike (K)')
    plt.ylabel('Implied volatility')
    plt.title('Volatility skew by Heston model')
    plt.show()
