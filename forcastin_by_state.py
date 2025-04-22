import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error
import warnings


from backend import *


warnings.filterwarnings('ignore')


daily_data = get_salesdaily()
weekly_data = get_salesweekly()
monthly_data = get_salesmonthly()

daily_by_state_data = get_salesdaily_by_state()
weekly_by_state_data = get_salesweekly_by_state()
monthly_by_state_data = get_salesmonthly_by_state()



daily_df = pd.DataFrame(daily_data)
daily_df['datum'] = pd.to_datetime(daily_df['datum'], format="%d-%m-%Y")
daily_df = daily_df.set_index('datum').sort_index()

daily_by_state_df = pd.DataFrame(daily_by_state_data)
daily_by_state_df['datum'] = pd.to_datetime(daily_by_state_df['datum'], format="%d-%m-%Y")
daily_by_state_df = daily_by_state_df.set_index('datum').sort_index()

weekly_df = pd.DataFrame(weekly_data)
weekly_df['datum'] = pd.to_datetime(weekly_df['datum'], format="%d-%m-%Y")
weekly_df = weekly_df.set_index('datum').sort_index()

weekly_by_state_df = pd.DataFrame(weekly_by_state_data)
weekly_by_state_df['datum'] = pd.to_datetime(weekly_by_state_df['datum'], format="%d-%m-%Y")
weekly_by_state_df = weekly_by_state_df.set_index('datum').sort_index()

monthly_df = pd.DataFrame(monthly_data)
monthly_df['datum'] = pd.to_datetime(monthly_df['datum'], format="%d-%m-%Y")
monthly_df = monthly_df.set_index('datum').sort_index()

monthly_by_state_df = pd.DataFrame(monthly_by_state_data)
monthly_by_state_df['datum'] = pd.to_datetime(monthly_by_state_df['datum'], format="%d-%m-%Y")
monthly_by_state_df = monthly_by_state_df.set_index('datum').sort_index()


medication_list = list(weekly_df.columns)
state_list = list(weekly_by_state_df['state'].unique())




def forecast_medicine_daily(medicine_code, train_end='2019-10-08', forecast_periods=14):

    df = daily_df
    series = df[medicine_code].astype(float)
    

    train_end = pd.to_datetime(train_end)
    
    train = series[series.index <= train_end]
    test = series[series.index > train_end]
    

    has_weekly_pattern = len(train) >= 14  
    
    if has_weekly_pattern:
        
        model = SARIMAX(train, 
                        order=(1,1,1),           
                        seasonal_order=(1,1,1,7),  
                        enforce_stationarity=False)
    else:
        
        model = SARIMAX(train, order=(1,1,1))
    
    
    results = model.fit(disp=False)
    
    
    in_sample_pred = results.predict()
    
    
    if len(test) > 0:
        forecast = results.forecast(steps=len(test))
        mae = mean_absolute_error(test, forecast)
        rmse = np.sqrt(np.mean((test - forecast)**2))
 
    else:
        forecast = None
        mae = None
        rmse = None
 
    
   
    last_date = train.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), 
                               periods=forecast_periods, 
                               freq='D')
    
    future_forecast = results.forecast(steps=forecast_periods)
    future_forecast.index = future_dates
    
    return future_forecast

def forecast_medicine_daily_by_state(medicine_code, state, train_end='2019-10-08', forecast_periods=14):

    df = daily_by_state_df
    mask = df['state'] == state
    state_df = df[mask]
    series = state_df[medicine_code].astype(float)
    
    

    train_end = pd.to_datetime(train_end)
    
    train = series[series.index <= train_end]
    test = series[series.index > train_end]
    

    has_weekly_pattern = len(train) >= 14  
    
    if has_weekly_pattern:
        
        model = SARIMAX(train, 
                        order=(1,1,1),           
                        seasonal_order=(1,1,1,7),  
                        enforce_stationarity=False)
    else:
        
        model = SARIMAX(train, order=(1,1,1))
    
    
    results = model.fit(disp=False)
    
    
    in_sample_pred = results.predict()
    
    
    if len(test) > 0:
        forecast = results.forecast(steps=len(test))
        mae = mean_absolute_error(test, forecast)
        rmse = np.sqrt(np.mean((test - forecast)**2))
        
    else:
        forecast = None
        mae = None
        rmse = None
        
    
   
    last_date = train.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), 
                               periods=forecast_periods, 
                               freq='D')
    
    future_forecast = results.forecast(steps=forecast_periods)
    future_forecast.index = future_dates
    
    return future_forecast


def forecast_medicine_weekly(medicine_code, train_end='2019-10-13', forecast_periods=5):
    df = weekly_df
    series = df[medicine_code].astype(float)
    
    train_end = pd.to_datetime(train_end)
    
    train = series[series.index <= train_end]
    test = series[series.index > train_end]
    
    seasonal_period = 52
    
    has_seasonality = len(train) >= 2 * seasonal_period
    
    if has_seasonality:
        model = SARIMAX(train, 
                        order=(2,1,1),         
                        seasonal_order=(1,1,1,seasonal_period),  
                        enforce_stationarity=False)
    else:
        model = SARIMAX(train, order=(2,1,1))
    
    results = model.fit(disp=False)
    
    in_sample_pred = results.predict()

    if len(test) > 0:
        forecast = results.forecast(steps=len(test))
        mae = mean_absolute_error(test, forecast)
        rmse = np.sqrt(np.mean((test - forecast)**2))
    else:
        forecast = None
        mae = None
        rmse = None
  
    
    last_date = train.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=7), 
                               periods=forecast_periods, 
                               freq='W-SUN')
    
    future_forecast = results.forecast(steps=forecast_periods)
    future_forecast.index = future_dates  
    
    return future_forecast





def forecast_medicine_weekly_by_state(medicine_code, state, train_end='2019-10-07', forecast_periods=5):
    df = weekly_by_state_df
    mask = df['state'] == state
    state_df = df[mask]
    series = state_df[medicine_code].astype(float)
    
    
    train_end = pd.to_datetime(train_end)
   
    train = series[series.index <= train_end]
    test = series[series.index > train_end]
    
    seasonal_period = 52
    
    has_seasonality = len(train) >= 2 * seasonal_period
    
    if has_seasonality:
        model = SARIMAX(train, 
                        order=(2,1,1),         
                        seasonal_order=(1,1,1,seasonal_period),  
                        enforce_stationarity=False)
    else:
        model = SARIMAX(train, order=(2,1,1))
    
    results = model.fit(disp=False)
    
    in_sample_pred = results.predict()

    if len(test) > 0:
        forecast = results.forecast(steps=len(test))
        mae = mean_absolute_error(test, forecast)
        rmse = np.sqrt(np.mean((test - forecast)**2))
    else:
        forecast = None
        mae = None
        rmse = None
  
    
    last_date = train.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=7), 
                               periods=forecast_periods, 
                               freq='W-SUN')
    
    future_forecast = results.forecast(steps=forecast_periods)
    future_forecast.index = future_dates  
    
    return future_forecast


def forecast_medicine_monthly(medicine_code, train_end='2019-10-31', forecast_periods=5):

    df = monthly_df
    series = df[medicine_code].astype(float)
    

    train_end = pd.to_datetime(train_end)
    
    train = series[series.index <= train_end]
    test = series[series.index > train_end]
    

    has_seasonality = len(train) >= 24  
    
    if has_seasonality:
        
        model = SARIMAX(train, 
                        order=(1,1,1),           
                        seasonal_order=(1,1,1,12),  
                        enforce_stationarity=False)
    else:
        
        model = SARIMAX(train, order=(1,1,1))
    
    
    results = model.fit(disp=False)
    
    
    in_sample_pred = results.predict()
    
    
    if len(test) > 0:
        forecast = results.forecast(steps=len(test))
        mae = mean_absolute_error(test, forecast)
        rmse = np.sqrt(np.mean((test - forecast)**2))
        
    else:
        forecast = None
        mae = None
        rmse = None
        
    
   
    future_forecast = results.forecast(steps=forecast_periods)
    
    return future_forecast


def forecast_medicine_monthly_by_state(medicine_code, state, train_end='2019-10-31', forecast_periods=5):
    df = monthly_by_state_df
    mask = df['state'] == state
    state_df = df[mask]
    series = state_df[medicine_code].astype(float)
            
    train_end = pd.to_datetime(train_end)
    
    train = series[series.index <= train_end]
    test = series[series.index > train_end]
            
        
    has_seasonality = len(train) >= 24  
            
    if has_seasonality:
                
        model = SARIMAX(train, 
                                order=(1,1,1),           
                                seasonal_order=(1,1,1,12),  
                                enforce_stationarity=False)
    else:
                
        model = SARIMAX(train, order=(1,1,1))
            
            
    results = model.fit(disp=False)
            
            
    in_sample_pred = results.predict()
            
            
    if len(test) > 0:
        forecast = results.forecast(steps=len(test))
        mae = mean_absolute_error(test, forecast)
        rmse = np.sqrt(np.mean((test - forecast)**2))
                
    else:
        forecast = None
        mae = None
        rmse = None
                       
    future_forecast = results.forecast(steps=forecast_periods)
     
    return future_forecast


def forecast_medicine(time_period, medicine_code, state):

    all_forecasts_df = pd.DataFrame()
    if time_period == 'monthly':
        if state == None:
            future_forecast = forecast_medicine_monthly(medicine_code)
        else:
            future_forecast = forecast_medicine_monthly_by_state(medicine_code, state)
    if time_period == 'weekly':
        if state == None:
            future_forecast = forecast_medicine_weekly(medicine_code)

        else:
            future_forecast = forecast_medicine_weekly_by_state(medicine_code, state)

    if time_period == 'daily':
        if state == None:
            future_forecast = forecast_medicine_daily(medicine_code)
        else:
            future_forecast = forecast_medicine_daily_by_state(medicine_code, state)

    return future_forecast
    






