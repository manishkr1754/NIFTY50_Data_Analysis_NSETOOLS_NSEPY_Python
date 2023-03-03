#!/usr/bin/env python
# coding: utf-8

# In[39]:


# importing required libraries

import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time
import os
import glob

from nsepy import get_history
from datetime import date, timedelta, datetime




class NIFTY50():
    
    def get_data(self, start_year, end_year):
        '''
        Gets NIFTY50 data from an API and generate separate .csv files for each year within the 
        specified start_year and end_year range passed as parameters. 
        Includes a sleep function for 10 seconds after each API call to allow sufficient time for
        processing the request.
        
        Parameters: 
        The function takes two parameters(both integers) representing the range of years 
        from which the NIFTY data is to be fetched-
            start_year(int) : Beginning Year from which NIFTY50 data is to be fetched
            end_year(int)   : End Year from which NIFTY50 data is to be fetched
        
        Returns:
        Returns a list called yearly_data_list and a dictionary called available_years
            yearly_data_list(dtype-list) : Containing the fetched NIFTY50 yearly data
            available_years(dtype-dict)  : Provides the index positions of available years 
                                           within the yearly_data_list.
        
        
        The function is intended to be used to easily retrieve and organize NIFTY 50 data.
        '''
        
        years = [year for year in range(start_year, end_year+1)]
        
        available_years = []
        yearly_data_list = []
        
        print('\nFetching NIFTY50 Data........')
        
        for year in years:
            year_start = datetime(year,1,1)
            year_end = datetime(year,12,31)
            
            data = get_history(symbol = "NIFTY50", start = year_start, end = year_end, index = True)
            data[["Open", "High", "Low", "Close"]]
            
            data = pd.DataFrame(data)
            data = data.reset_index()
            yearly_data_list.append(data)
            
            print('\nNIFTY50 Data for year ', year, 'Fetched Successfully.')
            
            nifty50_year_name = 'nifty50_'+str(year)+'.csv'
            available_years.append(nifty50_year_name)
            
            data.to_csv(nifty50_year_name)
            print('Exported', year, ' NIFTY50 data in ', nifty50_year_name)
            
            time.sleep(10)
            
        return yearly_data_list, dict(enumerate(available_years))
    
    
    
    def combine_data(self, export=False):
        '''
        Combines all available .csv files fetched/available in the same directory and returns a
        master file.
        
        Parameters:
        The function takes one parameter(bool) giving an option to export the concatenated master 
        file in the same directory.
            export : The default value for the export parameter is False.
                     True to export master concatenated file in same directory.
                     
        Returns:
        Returns a pandas DataFrame called nifty50_df.
            nifty50_df : Master DataFrame after concatenating all .csv
            
            
        This function is useful for consolidating data from multiple CSV files into a 
        single master file for analysis.
        '''
        
        csv_files = glob.glob('*.{}'.format('csv'))
        
        print('-> Available .csv files in current directory are: \n')
        print(csv_files)
        print('\n-> Combining Files......')
        
        nifty50_df = pd.concat([pd.read_csv(file) for  file in csv_files], ignore_index=True)
        nifty50_df.drop(['Unnamed: 0'], axis=1, inplace=True)
        print('\n-> Files Combined.')
        
        nifty50_df['Year'] = pd.DatetimeIndex(nifty50_df['Date']).year
        nifty50_df['Month'] = pd.DatetimeIndex(nifty50_df['Date']).month
        
        if export == True:
            nifty50_df.to_csv('master_nifty50_df.csv')
            print('\n=>Master NIFTY50 file Exported!')

        return nifty50_df
    
    
    
    def display_line_plots(self, nifty50_df, volume=False, open_close=False, high_low=False, year=False):
        '''
        Displays NIFTY50 Analysis for three categories: Volume, Open-Close & High-Low.
        
        
        Parameters:
        The function takes five parameters giving an option to display analysis 
        for the different categories.
            nifty50_df : Takes in a pandas DataFrame called nifty50_df as the master dataframe.
            volume     : True-Displays Open-Close Analysis (By Default-False)
            open_close : True-Displays High-Low Analysis (By Default-False)
            year       : Selection of a specific year for Analysis (By Default-False)
        
        
        The function is designed to display analysis for various categories using the data from 
        the master DataFrame. It is a useful tool for visualizing and interpreting NIFTY 50 data.
        '''
        
        if volume == True:
            if year == False:
                fig = px.line(nifty50_df, 
                              x='Date', 
                              y=['Volume'], 
                              title='NIFTY50 Volume Analysis')
                fig.show()
            else:
                temp_nifty50_df = nifty50_df[nifty50_df['Year']==year]
                
                fig = px.line(temp_nifty50_df, 
                              x='Date',
                              y=['Volume'],
                              title='NIFTY50 Volume Analysis'
                             )
                fig.show()
        
        if open_close == True:
            if year == False:
                fig = px.line(nifty50_df, 
                              x='Date', 
                              y=['Open', 'Close'], 
                              title='NIFTY50 Daily Open-Close Analysis'
                             )
                fig.show()
                
            else:
                temp_nifty50_df = nifty50_df[nifty50_df['Year']==year]
                
                fig = px.line(temp_nifty50_df,
                              x='Date', 
                              y=['Open','Close'], 
                              title='NIFTY50 Daily Open-Close Analysis'
                             )
                fig.show()
                
        if high_low == True:
            if year == False:
                fig = px.line(nifty50_df, 
                              x='Date', 
                              y=['High','Low'], 
                              title='NIFTY50 Daily High-Low Analysis'
                             )
                fig.show()
                
            else:
                temp_nifty50_df = temp_nifty50_df = nifty50_df[nifty50_df['Year']==year]
                    
                fig = px.line(temp_nifty50_df,
                              x='Date',
                              y=['High','Low'],
                              title='NIFTY50 Daily High-Low Analysis'
                             )
                fig.show()
                
      
    
    
    def display_candlesticks(self, nifty50_df, year=False, month=False):
        '''
        Displays NIFTY50 Analysis using candestick plot.
        
        The candlestick plot is a commonly used financial visualization tool that displays the 
        open, high, low and close prices for a given period. The plot is designed to help 
        visualize the price movement of an asset over time.
        
        Parameters:
        The function takes three parameters to display NIFTY50 Analysis using candlestick plot.
            nifty50_df : Takes in a pandas DataFrame called nifty50_df as the master dataframe.
            year       : Selection of a specific year for Analysis (By Default-False)
            month      : Selection of a specific month for Analysis (By Default-False).
                         Year necessary to be passed for month analysis.
                         
        
        This function is useful for visualizing NIFTY 50 data using a candlestick plot. It can 
        help provide insight into the price movement of the index over a specific period of time.
        
        '''
        
        if year == False:
            
            fig = go.Figure(data=[go.Candlestick(
                                                 x=nifty50_df['Date'],
                                                 open=nifty50_df['Open'],
                                                 high=nifty50_df['High'],
                                                 low=nifty50_df['Low'],
                                                 close=nifty50_df['Close'])])
            fig.update_layout(title_text='NIFTY50 Analysis',
                              xaxis_rangeslider_visible=True,
                              xaxis_title="Time", 
                              yaxis_title="Price"
                              )
            
            fig.show()
            
        else:
            def specific_candlestick(temp_nifty50_df):
                fig = go.Figure(data=[go.Candlestick(x=temp_nifty50_df['Date'],
                                                     open=temp_nifty50_df['Open'],
                                                     high=temp_nifty50_df['High'],
                                                     low=temp_nifty50_df['Low'],
                                                     close=temp_nifty50_df['Close'])])
                fig.update_layout(title_text='NIFTY50 Analysis Jan-Dec' + str(year),
                                  open=temp_nifty50_df['Open'],
                                  high=temp_nifty50_df['High'],
                                  low=temp_nifty50_df['Low'],
                                  close=temp_nifty50_df['Close'])
                
                fig.show()
                
            
            if month == False:
                temp_nifty50_df = nifty50_df[nifty50_df['Year']==year]
                specific_candlestick(temp_nifty50_df)
                
            else:
                temp_nifty50_month_df = temp_nifty50_df[temp_nifty50_df['Month']==month]
                specific_candlestick(temp_nifty50_month_df)
       
    
    
                
    def gap_analyis(self, nifty50_df, percentage=False, points=False):
        '''
        Calculates required features for gap analysis either by percentage or points.
        
        Gap analysis is a technique used by traders to identify gaps in the price of an 
        asset between two periods. 
        
        Parameters:
        The function takes three parameters.
            nifty50_df : Takes in a pandas DataFrame called nifty50_df as the master dataframe.
            percentage : True- Calculates gaps with percentage as the metric (By Default-False)
            points     : True- Calculates gaps with (deafult=200) points as the threshold (By Default-False)
            
        Returns:
        The function returns three pandas DataFrame.
            nifty50_df  : Master NIFTY50 DataFrame
            gap_ups_df  : DataFrame of only records with gap ups (percentage or points)
            gap_downs_df: DataFrame of only records with gap downs (percentage or points)
            
            
        This function is useful for calculating and analyzing gaps in the NIFTY 50 index. It can 
        help traders identify potential trading opportunities and gain insight into the price 
        movement of the index.

        '''
        
        nifty50_df['Previous Close'] = nifty50_df['Close'].shift(1)
        
        if percentage == True:
            nifty50_df['Per_Change_Prev_Close'] = round((nifty50_df['Open']-nifty50_df['Previous Close']))
            gap_ups_df = nifty50_df[nifty50_df['Per_Change_Prev_Close']>0]
            gap_downs_df = nifty50_df[nifty50_df['Per_Change_Prev_Close']<0]
            
            print('\n-> Gap Ups Open : ', gap_ups_df.shape[0])
            print('\n-> Gap Downs Open : ', gap_downs_df.shape[0])
            print('\n-> Total Market Days : ', nifty50_df.shape[0])
            
            return nifty50_df, gap_ups_df, gap_downs_df
        
        else:
            points_threshold = 200
            nifty50_df['Points_Change_Prev_Close'] = nifty50_df['Open'] -  nifty50_df['Previous Close']
            gap_ups_df = nifty50_df[nifty50_df['Points_Change_Prev_Close'] > points_threshold]
            gap_downs_df = nifty50_df[nifty50_df['Points_Change_Prev_Close'] < (-points_threshold)]
            
            print('\n-> Gap Ups Open : ', gap_ups_df.shape[0])
            print('\n-> Gap Downs Open : ', gap_downs_df.shape[0])
            print('\n->Total Market Days : ', nifty50_df.shape[0])
            
            return nifty50_df, gap_ups_df, gap_downs_df
        
       
    
    
    def movement_from_open(self, nifty50_df):
        '''
        Calculates the Price deviation from the open price of the NIFTY50 index.
        Assigns a positive value if the deviation points towards the high and a
        negative value if the deviation points towards the low.

        +ve value => Points towards High.
        -ve value => Points towards Low.
        
        
        Parameters:
        The function takes one parameter(pandas DataFrame).
            nifty50_df : Takes in a pandas DataFrame called nifty50_df as the master dataframe.
            
        Returns:
        The function returns an updated pandas DataFrame with the price movement features added.
            nifty50_df : Updated df with Movement feature
        
        
        This analysis can be useful for traders to identify the direction of price movement of 
        the NIFTY 50 index. By analyzing the price deviation from the open price, traders can 
        make informed trading decisions and gain insights into the market's price behavior.
        
        '''
        
        nifty50_df['High-Low'] = nifty50_df['High'] - nifty50_df['Low']
        
        movement_conditions = [
            (abs(nifty50_df['High'] - nifty50_df['Open'])) > (abs(nifty50_df['Low'] - nifty50_df['Open'])),
            (abs(nifty50_df['High'] - nifty50_df['Open'])) < (abs(nifty50_df['Low'] - nifty50_df['Open']))
        ]
        
        movement_result = [
            (nifty50_df['High'] - nifty50_df['Open']),
            (nifty50_df['Low'] - nifty50_df['Open'])
        ]
        
        
        nifty50_df['Movement from Open'] = np.select(movement_conditions,movement_result)
        
        return nifty50_df
      
        
        
                
    def exponential_moving_average(self, nifty50_df, plot=False, year=False):
        '''
        Calculates the Exponential Moving Average(EMA) for 7, 14, 21, 50 and 200 days of the 
        NIFTY50 data. It can also display the EMA Line plots and EMA plots for a specific year.
        
        
        Parameters:
        The function takes three parameters.
            nifty50_df : Takes in a pandas DataFrame called nifty50_df as the master dataframe.
            plot       : True-Display EMA line plots(By Default-False)
            year       : Selection of a specific year for Analysis (By Default-False)
        
        
        Returns:
        The function returns an updated pandas DataFrame with the EMA features added.
            nifty50_df : Updated df with EMA features

        '''
        
        EMA_7D = nifty50_df['Close'].rolling(window=7).mean()
        EMA_15D = nifty50_df['Close'].rolling(window=14).mean()
        EMA_21D = nifty50_df['Close'].rolling(window=21).mean()
        EMA_50D = nifty50_df['Close'].rolling(window=50).mean()
        EMA_200D = nifty50_df['Close'].rolling(window=200).mean()
        
        nifty50_df['EMA_7D'] = np.round(EMA_7D, decimal=3)
        nifty50_df['EMA_15D'] = np.round(EMA_15D, decimal=3)
        nifty50_df['EMA_21D'] = np.round(EMA_21D, decimal=3)
        nifty50_df['EMA_50D'] = np.round(EMA_50D, decimal=3)
        nifty50_df['EMA_200D'] = np.round(EMA_200D, decimal=3)
        
# USe of ewm(span=7). Needto check

        if plot == True:
            if year == False:
                fig = px.line(nifty50_df,
                              x='Date',
                              y= ['Close','EMA_7D', 'EMA_14D', 'EMA_21D', 'EMA_50D', 'EMA_200D'],
                              title='Exponential Moving Average Analysis'
                              )
                fig.show()
                
            else:
                temp_nifty50_df = nifty50_df[nifty50_df['Year']==year]
                
                fig = px.line(temp_nifty50_df,
                              x='Date',
                              y=['Close', 'EMA_7','EMA_14D', 'EMA_21D', 'EMA_50D', 'EMA_200D'],
                              title='Exponential Moving Average Analysis'
                              )
                fig.show()
                
        return nifty50_df
    
    
    
    
    def display_heikin_ashi(self, nifty50_df, year=False, month=False):
        '''
        Displays Heikin-Ashi Plot for NIFTY50.
        
        Heikin-Ashi charts are a type of candlestick chart that uses a modified calculation 
        to display the price movements of an asset. The chart is calculated using averages 
        of the open, high, low and close prices to produce a smoother and less volatile chart 
        compared to traditional candlestick charts. 
        
        
        Parameters:
        The function takes three parameters.
            nifty50_df : Takes in a pandas DataFrame called nifty50_df as the master dataframe.
            year       : Selection of a specific year for Analysis (By Default-False)
            month      : Selection of a specific month for Analysis (By Default-False).
                         Year necessary to be passed for month analysis.
                         

        '''
        
        def heikin_ashi():
            '''
            Calculates the Heikin Ashi candelstick values for the given NIFTY50 Data.
            
            The Heikin Ashi candlestick chart is a variant of the traditional candlestick chart
            that filters out some of the noise in price action by taking the average of the
            current and previous day's open and close prices to determine the new open price
            and using this value to calculate the high, low and close prices.
             
             
            Parameters:
            The function takes one parameter.
                nifty50_df : Takes in a pandas DataFrame called nifty50_df as the master dataframe.
                
                
            Returns:
            The function returns a pandas DataFrame.
                ha_df : A new DataFrame containing Heikin Ashi candlestick values computed from
                        nifty50_df DataFrame.
            
            '''
 
            ha_date = nifty50_df['Date']
            ha_open = (nifty50_df['Open']+nifty50_df['Close'])/2
            ha_high = nifty50_df[['High', 'Open', 'Close']].max(axis=1)
            ha_low = nifty50_df[['Low', 'Open', 'Close']].min(axis=1)
            ha_close = (nifty50_df['Open'] + nifty50_df['High'] + nifty50_df['Low'] + nifty50_df['Close'])/4
            ha_df = pd.DataFrame({'Date': ha_date, 'Open':ha_open, 'High':ha_high, 
                                  'Low':ha_low, 'Close':ha_close})
            return ha_df
        
        if year == False:
            ha_nifty50_df = heikin_ashi()
            
            fig = go.Figure(data=[go.Candlestick(x=ha_nifty50_df['Date'],
                                                 open=ha_nifty50_df['Open'],
                                                 high=ha_nifty50_df['High'],
                                                 low=ha_nifty50_df['Low'],
                                                 close=ha_nifty50_df['Close'])])
            
            fig.update_layout(title_text='Heikin Ashi Chart',
                              xaxis_rangeslider_visible=True,
                              xaxis_title='Time',
                              yaxis_title='Price')
            
            fig.show()
            
        else:
            
            if month == False:
                ha_nifty50_df = heikin_ashi()
                
                temp_ha_nifty50_df = ha_nifty50_df[ha_nifty50_df['Year']==year]
                
                fig =go.Figure(data=[go.Candlestick(x=temp_ha_nifty50_df['Date'],
                                                    open=temp_ha_nifty50_df['Open'],
                                                    high=temp_ha_nifty50_df['High'],
                                                    low=temp_ha_nifty50_df['Low'],
                                                    close=temp_ha_nifty50_df['Close'])])
                
                fig.update_layout(title_text='Heikin Ashi Chart Jan-Dec'+ str(year),
                                  xaxis_rangeslider_visible=True,
                                  xaxis_title='Time',
                                  yaxis_title='Price')
                
                fig.show()
                
            else:
                
                ha_nifty50_df = heikin_ashi()
                
                temp_ha_nifty50_df = ha_nifty50_df[ha_nifty50_df['Year']==year]
                temp_ha_nifty50_month_df = temp_ha_nifty50_df[temp_ha_nifty50_df['Month']==month]
                
                fig = go.Figure(data=[go.Candlestick(x=temp_ha_nifty50_month_df['Date'],
                                                     open=temp_ha_nifty50_month_df['Open'],
                                                     high=temp_ha_nifty50_month_df['High'],
                                                     low=temp_ha_nifty50_month_df['Low'],
                                                     close=temp_ha_nifty50_month_df['Close'])])
                
                fig.update_layout(title_text='Heikin Ashi Chart' + str(year)+ " " + str(month),
                                  xaxis_rangeslider_visible=True,
                                  xaxis_title='Time',
                                  yaxis_title='Price')
                
                fig.show()
                  


# ### Iniatiating an object of NIFTY50 class

# In[40]:


nifty50 =NIFTY50()


# ### Downloading NIFTY50 Data(Daily Data) for last 15 years

# In[15]:


yearly_data_list, available_years = nifty50.get_data(start_year= 2008, end_year= 2022)


# ### Combining & Exporting all files into a single master DataFrame

# In[19]:


nifty50_df = nifty50.combine_data(export=True)


# In[20]:


nifty50_df


# ## Data Visualization

# #### Overall NIFTY50 Volume Analysis (2008 - 2022)

# In[21]:


nifty50.display_line_plots(nifty50_df, volume=True)


# #### NIFTY50 Volume Analysis for Specific Year (year = 2022)

# In[22]:


nifty50.display_line_plots(nifty50_df, volume=True, year=2022)


# #### Overall NIFTY50 Open_Close Analysis (2008 - 2022)

# In[30]:


nifty50.display_line_plots(nifty50_df, open_close=True)


# #### NIFTY50 Open_Close Analysis for Specific Year (year = 2022)

# In[31]:


nifty50.display_line_plots(nifty50_df, open_close=True, year=2022)


# #### Overall NIFTY50 High_Low Analysis (2008 - 2022)

# In[32]:


nifty50.display_line_plots(nifty50_df, high_low=True)


# #### NIFTY50 High_Low Analysis for Specific Year (year = 2022)

# In[33]:


nifty50.display_line_plots(nifty50_df,high_low=True, year=2022)


# #### Overall NIFTY50 Candle Stick Analysis

# In[34]:


nifty50.display_candlesticks(nifty50_df)


# #### NIFTY50 Candle Stick Analysis for specific year (2022)

# In[41]:


nifty50.display_candlesticks(nifty50_df,year=2022)


# #### NIFTY50 Candle Stick Analysis for specific year (2022) and specific month (October => 10)

# In[42]:


nifty50.display_candlesticks(nifty50_df, year=2022, month=10)


# #### Gap Analysis => How many times NIFTY gave a gap-up or gap-down opening and what dates

# Gap Analysis could be performed by 2 ways : 1. By Percentage Change 2. By Points Change

# ##### Gap Analysis => by % Change

# In[44]:


gap_nifty50_df, gap_ups_df, gap_downs_df = nifty50.gap_analyis(nifty50_df,percentage=True)


# In[45]:


gap_nifty50_df


# In[46]:


gap_ups_df


# In[47]:


gap_downs_df


# #### Gap Analysis => by points Change (Default 200 Points as Threshold)

# In[48]:


gap_nifty50_df, gap_ups_df, gap_downs_df = nifty50.gap_analyis(nifty50_df, points=True)


# In[50]:


gap_nifty50_df


# In[54]:


gap_ups_df.head()


# In[52]:


gap_downs_df


# #### Movement from Open Analysis & Percentage Change from Previous Close
# 
# 
# 
#     +ve movement => Movement towards High
# 
#     -ve movement => Movement towards Low
# 

# In[55]:


nifty50_movement_df = nifty50.movement_from_open(nifty50_df)


# In[56]:


nifty50_movement_df.head()


# #### Exponential Moving Averages -> 7days/14days/21 days/50 days and 200 days

# In[57]:


ema_nifty50_df = nifty50.exponential_moving_average(nifty50_df)


# #### EMA Analysis by Line Plot for specific year (2022)

# In[58]:


ema_nifty50_df1 = nifty50.exponential_moving_average(nifty50_df, plot=True, year=2022)


# In[59]:


nifty50.display_heikin_ashi(nifty50_df, year=2022)


# #### Heikin aashi Plot for specific year (2022) & Specific month (October -> 10

# In[60]:


nifty50.display_heikin_ashi(nifty50_df, year=2022, month=10)


# In[61]:


nifty50_df


# In[62]:


#nifty_df.to_csv('Complete_Master_Nifty_df.csv')


# In[ ]:




