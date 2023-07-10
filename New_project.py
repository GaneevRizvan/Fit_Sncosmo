#!/usr/bin/env python
# coding: utf-8

# In[6]:


import sncosmo
import sfdmap
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table
from Oid_to_ref import oid_to_ref
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from Models_to_parameters import models_to_parameters


def mag_flux(data, ref):
    flux = [10 ** (-0.4 * a) - 10 ** (-0.4 * b[0]) for a, b in zip(data['mag'], ref)]
    fluxerr = [((-0.4 * np.log(10) * 10 ** (-0.4 * a) * c) ** 2 + 
                        (-0.4 * np.log(10) * 10 ** (-0.4 * b[0]) * b[1]) ** 2) ** 0.5  for a, b, c, in zip(data['mag'], ref, data['magerr'])]
    return (flux, fluxerr)


def print_params(result):
    print("Number of chi^2 function calls:", result.ncall)
    print("Number of degrees of freedom in fit:", result.ndof)
    print("chi^2 value at minimum:", result.chisq)
    print("model parameters:", result.param_names)
    print("best-fit values:", result.parameters)
    print("The result contains the following attributes:\n", result.keys())

    
def plot(data, fitted_model, result, oid, name_model):
    fig = sncosmo.plot_lc(data, model=fitted_model, errors=result.errors)
    #fig.savefig('Fits/' + str(oid) + '_' + name_model)
    plt.show()

    
def fit(data, name_model, oid):
    ebv = 0.03
    dust = sncosmo.CCM89Dust()
    model = sncosmo.Model(source=name_model, effects=[dust], effect_names=['mw'], effect_frames=['obs'])
    model.set(mwebv=ebv)
    result, fitted_model = sncosmo.fit_lc(data, model, models_to_parameters[name_model], bounds={'z':(0.01, 0.3)})
    print_params(result)
    plot(data, fitted_model, result, oid, name_model)

    
def give_chrome_option(folder_path):
    chromeOptions = webdriver.ChromeOptions() #setup chrome option
    prefs = {"download.default_directory" : folder_path,
           "download.prompt_for_download": False,
           "download.directory_upgrade": True}  #set path
    chromeOptions.add_experimental_option("prefs", prefs) #set option
    #chromeOptions.add_argument("--headless")
    return chromeOptions


def get_data(oid):
    folder_path = f'home/Downloads'
    link = str()
    while len(link) <= len('https://ztf.snad.space/dr17/csv/') + len(str(oid)):
        #print(len(link), len('https://ztf.snad.space/dr17/csv/') + len(str(oid)))
        driver = webdriver.Chrome(options = give_chrome_option(folder_path))
        url = "https://ztf.snad.space/dr17/view/" + str(oid)
        driver.get(url)
        time.sleep(3.5)
        base = driver.find_element(By.ID, "csv-link")
        link = base.get_attribute('href')
        #print(link, len(link))
    df = pd.read_csv(link)
    return df


def aproximate(oid, name_model):
    #data = pd.read_csv(str(oid) + ".csv")
    print('OID:', oid, ' ', 'MODEL:', name_model)
    data = get_data(oid)
    ref = data['oid'].map(oid_to_ref[oid])
    #data['mag_d'] = [-2.5 * np.log10(10 ** (-0.4 * a) - 10 ** (-0.4 * b[0])) for a, b in zip(data['mag'], ref)]
    data['flux'], data['fluxerr'] = mag_flux(data, ref)
    data['filter'] = data['filter'].str.replace('z', 'ztf')
    data['band'] = data['filter']
    del data['filter']
    data['zp'] = 0
    data['zpsys'] = 'ab'
    data = Table.from_pandas(data)
    dust = sncosmo.CCM89Dust()
    fit(data, name_model, oid)

[aproximate(796201400007564, i) for i in ['nugent-sn1a', 'nugent-sn91t', 'nugent-sn91bg', 
                                          'nugent-sn1bc', 'nugent-hyper', 'nugent-sn2n', 'nugent-sn2p','nugent-sn2l']]
[aproximate(633207400004730, i) for i in ['nugent-sn1a', 'nugent-sn91t', 'nugent-sn91bg', 
                                          'nugent-sn1bc', 'nugent-hyper', 'nugent-sn2n', 'nugent-sn2p','nugent-sn2l']]
[aproximate(633216300024691, i) for i in ['nugent-sn1a', 'nugent-sn91t', 'nugent-sn91bg', 
                                          'nugent-sn1bc', 'nugent-hyper', 'nugent-sn2n', 'nugent-sn2p','nugent-sn2l']]
[aproximate(633216300024691, i) for i in ['nugent-sn1a', 'nugent-sn91t', 'nugent-sn91bg', 
                                          'nugent-sn1bc', 'nugent-hyper', 'nugent-sn2n', 'nugent-sn2p','nugent-sn2l']]
[aproximate(758205400019523, i) for i in ['nugent-sn1a', 'nugent-sn91t', 'nugent-sn91bg', 
                                          'nugent-sn1bc', 'nugent-hyper', 'nugent-sn2n', 'nugent-sn2p','nugent-sn2l']]
aproximate(796201400007564, 'salt2')

aproximate(633207400004730, 'salt2')

aproximate(633216300024691, 'salt2')

aproximate(758205100001118, 'salt2')

aproximate(758205400019523, 'salt2')


# In[ ]:




