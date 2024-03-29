import matplotlib.pyplot as plt
import numpy as np
import random
import math
import time
import os
import argparse
import logging
from scipy.optimize import curve_fit                                                     
logging.basicConfig(level=logging.INFO)    


_description = 'analize gamma ray spectrum ' 


def sottrazione_fondo(file_path,source_path):
   data=np.loadtxt(file_path,skiprows=26, usecols=[1,2,3,4,5], unpack=True)
   data=data.transpose().flatten()
   logging.info('Done. {} data found in background file'.format(len(data))) 

   data_source=np.loadtxt(source_path,skiprows=26, usecols=[1,2,3,4,5], unpack=True)
   data_source=data_source.transpose().flatten()
   logging.info('Done. {} data found in source file'.format(len(data_source))) 




   '''with open(file_path) as imput_file:                                              
        data_time_fondo=imput_file.read()
        print (data_time_fondo)
        print(type(data_time_fondo))'''


   t_source = 621.739986         #tempo exp. sorgente
   t_fondo = 1581.579965         #tempo exp. fondo         
   #data=(621.739986/1581.579965)*data
   data=(t_source/t_fondo)*data

   data_fin=data_source-data
   data_zero=np.zeros(len(data_fin))
   data_fin=np.where(data>=0 , data_fin, data_zero )

   

   x=np.linspace(0,2050,2050)
   plt.figure('data_finale')
   plt.plot(x,data_source,label='sorgente', alpha=0.6, color='purple')
   plt.plot(x,data, label='fondo', alpha=0.6, color='red')
   plt.plot(x,data_fin, label='sorgente - fondo', color='blue')
   plt.grid()
   plt.legend()


   









   #fitting...
   ydata = data_fin[763:1063]
   xdata = x[763:1063]
   def gaussian(x, a, mu, sigma):
      return a/(sigma*np.sqrt(2*np.pi))*(np.exp(-np.power(x - mu, 2.) / (2 * np.power(sigma, 2.))))

   popt, pcov = curve_fit(gaussian, xdata, ydata, p0=[4000,930,30])
   print(' i parametri stimati sono (a, mu, sigma)',popt)
   print(' le relative incertezze sono di ',np.sqrt(pcov.diagonal()))


   _x = np.linspace(763, 1063, 300)
   _y = gaussian(_x, *popt)
   plt.figure('fit')
   plt.plot(x,data_fin, label='sorgente-fondo', alpha=1)
   plt.plot(_x, _y, label='fit')
   #plt.text(1270,450,'mu = {}'.format(popt[1]))
   plt.legend()
   plt.grid()

   #mask = ydata > 0
   #chi2 = sum(((ydata- gaussian(xdata, *popt)) / np.sqrt(ydata))**2.)
   chi2 = sum(((ydata-gaussian(xdata, *popt))**2)/(ydata))
   nu = len(xdata) - 3
   sigma = np.sqrt(2 * nu)
   print('chi2_norm = {} , dof = {}, incetezza chi2 = {}'.format(chi2/nu, nu, sigma/nu))






if __name__ == '__main__':
    parser=argparse.ArgumentParser(description =_description)
    parser.add_argument('infile', help= 'nome del file del fondo')
    parser.add_argument('sorgente', help= 'nome del file della sorgente')
    args = parser.parse_args()
    sottrazione_fondo(args.infile, args.sorgente)


    plt.show()