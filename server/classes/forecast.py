import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
class Forecast:
    def __init__(self,tmp_dict,prod_df):
        self.tmp_dict = tmp_dict
        self.params = getFit(prod_df)
        self.forecast= getForecast(self.params)
        
def decline_curve(q_i):
    def hyperbolic_decline(T, a_i, b):
        return q_i / np.power((1 + b * a_i * T), 1. / b)
    return hyperbolic_decline      
        
def getFit(df):
    df = df.reset_index()
    df['time'] = list(range(0,len(df)))
    outDict = {}
    fluids= ['oil','gas']
    for fluid in fluids:
        if np.mean(df[fluid]) < 5:
            d_i = 0
            b = 1
            q_i = 0
            iP = 0

            hypDict = {}
            hypDict['d_i'] = d_i
            hypDict['b'] = b
            hypDict['q_i'] = q_i


            outDict[fluid]=hypDict
        else:

        # TODO parameterize 'date';
            df.sort_values(by='time', inplace=True)
            df = df.reset_index(drop=True)
            hypDict = hypParams(df, fluid)
            
            outDict[fluid]=hypDict
    return outDict


def getNewMax(df, fluid):
    df = df.reset_index(drop=True)
    maxId = df[fluid].idxmax()
    return maxId

def hypParams(df, fluid):
    df.reset_index(drop=True, inplace=True)
    fDate = df.loc[0]['prod_date']

    df['years_old'] = df['time']

    maxId = getNewMax(df, fluid)
    df = df[maxId:]
    df = df.reset_index(drop=True)

    T = df.years_old
    Q = df[fluid]
    hyp_decline = decline_curve(Q[0])
    # create the weighting array
    y_weight = np.empty(len(df))
    # high pseudo-sd values, meaning less weighting in the fit
    y_weight.fill(10)
    # low values for point 0 and the last points, meaning more weighting during the fit procedure
    y_weight[-5:] = 0.1
    mySig = y_weight
    p0 = [.15, 1]

    popt_hyp, pcov_hyp = curve_fit(hyp_decline, T, Q, method="trf", sigma=mySig, absolute_sigma=True, p0=p0,
                                   bounds=([.1, 1], [.4, 1.2]))

    d_i = popt_hyp[0]
    b = popt_hyp[1]
    q_i = Q[0]
    iP = fDate

    hypDict = {}
    hypDict['d_i'] = d_i
    hypDict['b'] = b
    hypDict['q_i'] = q_i
    hypDict['iP'] = iP
    hypDict['q_i_init']=q_i

    return hypDict

def getForecast(params):
    outDf = pd.DataFrame()

    months = 700
    outDf['time'] = list(range(0,months))
    outDf['gas_forecast'] = 0
    outDf['oil_forecast']=0
    

    for tmpKey in params:
        if params[tmpKey]['q_i']<20:
            continue
        else:
            outDf[f'{tmpKey}_forecast']=outDf.apply(hyper_decline,axis=1,args=(params[tmpKey]['b'],params[tmpKey]['d_i'],params[tmpKey]['q_i']))
    outDf['activity_date'] = pd.date_range(start=params['oil']['iP'], periods=months, freq='MS')
    outDf['activity_date']=pd.to_datetime(outDf.activity_date).dt.date
    return outDf

def hyper_decline(row,b,d_i,q_i):

    T = row.time
    b = b
    a_i = d_i
    q_i = q_i
    return q_i / np.power((1 + b * a_i * T), 1. / b)
