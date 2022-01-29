#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pickle
import streamlit as st
import pandas as pd 
from plotly import graph_objs as go


# loading the trained model
### BCA
pickle_bca_open = open('BBCA/model_bca_open.pkl', 'rb') 
pickle_bca_high = open('BBCA/model_bca_high.pkl', 'rb') 
pickle_bca_low = open('BBCA/model_bca_low.pkl', 'rb') 
pickle_bca_volume = open('BBCA/model_bca_volume.pkl', 'rb') 
pickle_bca_adjclose = open('BBCA/model_bca_adjclose.pkl', 'rb') 
pickle_bca_close = open('BBCA/model_bca_close.pkl', 'rb') 
model_bca_open = pickle.load(pickle_bca_open)
model_bca_high = pickle.load(pickle_bca_high)
model_bca_low = pickle.load(pickle_bca_low)
model_bca_volume = pickle.load(pickle_bca_volume)
model_bca_adjclose = pickle.load(pickle_bca_adjclose)
model_bca_close = pickle.load(pickle_bca_close)

### BNI
pickle_bni_open = open('BBNI/model_bni_open.pkl', 'rb') 
pickle_bni_high = open('BBNI/model_bni_high.pkl', 'rb') 
pickle_bni_low = open('BBNI/model_bni_low.pkl', 'rb') 
pickle_bni_volume = open('BBNI/model_bni_volume.pkl', 'rb') 
pickle_bni_adjclose = open('BBNI/model_bni_adjclose.pkl', 'rb') 
pickle_bni_close = open('BBNI/model_bni_close.pkl', 'rb') 
model_bni_open = pickle.load(pickle_bni_open)
model_bni_high = pickle.load(pickle_bni_high)
model_bni_low = pickle.load(pickle_bni_low)
model_bni_volume = pickle.load(pickle_bni_volume)
model_bni_adjclose = pickle.load(pickle_bni_adjclose)
model_bni_close = pickle.load(pickle_bni_close)

### BRI
pickle_bri_open = open('BBRI/model_bri_open.pkl', 'rb') 
pickle_bri_high = open('BBRI/model_bri_high.pkl', 'rb') 
pickle_bri_low = open('BBRI/model_bri_low.pkl', 'rb') 
pickle_bri_volume = open('BBRI/model_bri_volume.pkl', 'rb') 
pickle_bri_adjclose = open('BBRI/model_bri_adjclose.pkl', 'rb') 
pickle_bri_close = open('BBRI/model_bri_close.pkl', 'rb') 
model_bri_open = pickle.load(pickle_bri_open)
model_bri_high = pickle.load(pickle_bri_high)
model_bri_low = pickle.load(pickle_bri_low)
model_bri_volume = pickle.load(pickle_bri_volume)
model_bri_adjclose = pickle.load(pickle_bri_adjclose)
model_bri_close = pickle.load(pickle_bri_close)

@st.cache()

# Defining the function which will make the prediction using the data which the user inputs 
def prediction(bank_type, model_type, months):   
    # Pre-processing user input    
    if bank_type == 'BBCA':
        data = pd.read_csv("BBCA/BCA_Preprocessed_Data", index_col='Date', parse_dates=True)
        data.index.freq = 'D'
        if model_type == "Open":
            model_arima = model_bca_open
        elif model_type == "High":
            model_arima = model_bca_high
        elif model_type == "Low":
            model_arima = model_bca_low
        elif model_type == "Volume":
            model_arima = model_bca_volume
        elif model_type == "Adj Close":
            model_arima = model_bca_adjclose
        elif model_type == "Close":
            model_arima = model_bca_close
    elif bank_type == 'BBNI':
        data = pd.read_csv("BBNI/BNI_Preprocessed_Data", index_col='Date', parse_dates=True)
        data.index.freq = 'D'
        if model_type == "Open":
            model_arima = model_bni_open
        elif model_type == "High":
            model_arima = model_bni_high
        elif model_type == "Low":
            model_arima = model_bni_low
        elif model_type == "Volume":
            model_arima = model_bni_volume
        elif model_type == "Adj Close":
            model_arima = model_bni_adjclose
        elif model_type == "Close":
            model_arima = model_bni_close
    elif bank_type == 'BBRI':
        data = pd.read_csv("BBRI/BRI_Preprocessed_Data", index_col='Date', parse_dates=True)
        data.index.freq = 'D'
        if model_type == "Open":
            model_arima = model_bri_open
        elif model_type == "High":
            model_arima = model_bri_high
        elif model_type == "Low":
            model_arima = model_bri_low
        elif model_type == "Volume":
            model_arima = model_bri_volume
        elif model_type == "Adj Close":
            model_arima = model_bri_adjclose
        elif model_type == "Close":
            model_arima = model_bri_close
    
    # Making predictions 
    start = 2004
    end = 2004 + round(months*30.4167)-1
    forecast = model_arima.predict(start=start, end=end, dynamic=False, typ='levels')
    df_forecast = pd.DataFrame(forecast)
    df_forecast.index.freq = 'D'
    
    return df_forecast, data

# Main function in which we define our webpage  
def main():       
    # Front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Streamlit Forecasting Bank Stock Price App</h1> 
    </div> 
    """
      
    # Display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # Following lines create boxes in which user can enter data required to make prediction 
    bank_type = st.selectbox('Type Stock Price',("BBCA", "BBNI", "BBRI")) 
    input_type = st.selectbox('Type Stock Price',("Open","High","Low","Volume","Adj Close","Close")) 
    input_months = st.number_input('Number of months that will be predicted')
    result =""
    data2 =""
      
    # When 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result, data = prediction(bank_type, input_type, input_months) 
        st.success(f'Forecasting results for the next {input_months} months :\n')
        st.write(result)

        data2 = data[[input_type]]
        data2 = pd.concat([data2,result])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data2.iloc[0:2004].index, y=data2[input_type].iloc[0:2004]))
        fig.add_trace(go.Scatter(x=data2.iloc[2004:].index, y=data2["predicted_mean"].iloc[2004:]))
        fig.layout.update(title_text=input_type, xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
        
if __name__=='__main__': 
    main()

