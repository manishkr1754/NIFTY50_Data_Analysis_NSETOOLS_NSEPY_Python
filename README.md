# NIFTY50 Data Analysis using Python
![image](https://user-images.githubusercontent.com/114581035/216782163-eea21cbf-2560-4919-a28c-3ecf3cfbb499.png)

# Detailed Article @ Medium
- [NIFTY50 Data Analysis Series using Python](https://medium.com/@kmrmanish/nifty50-data-analysis-using-python-d9227e525894)
- [A Data Extraction Guide for NIFTY50 Historical Data [1]](https://medium.com/@kmrmanish/a-data-extraction-guide-for-nifty50-historical-data-1-220a097c7a1a)


# Structure of NIFTY50 Data Analysis Series
1. **Data Extraction :** Download NIFTY50 daily data for last 15 years using API like nsetools/nsepy
2. **Data Visualization :** Plot the interactive trends(Line, Candlesticks and Heikin Ashi Charts) for different period using Cufflinks and Plotly
3. **High-Low Analysis & Open-Close Analysis**
4. **Gap Up-Gap Down Analysis**
5. **Simple Moving Average (SMA) Analysis :** Calculate and Plot 7 days, 14 days, 21 days, 50 days and 200 days SMA
6. **Exponential Moving Average (EMA) Analysis :** Calculate and Plot 7 days, 14 days, 21 days, 50 days and 200 days EMA
7. **Monthly Return Analysis :** Calculate and Plot %Monthly Return and Positive & Negative Return Count
8. **Portfolio Analysis :** One Time Lump-sum Investment
9. **Portfolio Analysis :** Monthly SIP on 1st trading day of the month
10. **Portfolio Analysis :** Invest only on First Gap Down Day of the every month
11. **Portfolio Analysis :** Invest on All Gap Down Days
12. **Sharpe Ratio Comparison :** Compare different investment strategies and risk adjusted returns

# Problem Statement
NIFTY50 Data Analysis from scratch (Data Extraction to Data Visualization)


    Tasks to be performed: 
    1. Use nsetools/nsepy to download NSE/NIFTY50 data (daily data) for last 15 years. Use for loop and time sleep for 1 min
    2. If possible, download the 1 year 5min data for NIFTY50
    3. Data Visualization : plots to visualize the trends over the last one year and so. Go for cufflinks and plotly
    4. How many times NIFTY gave a gap-up or gap-down opening and what dates
    5. Add on column- (High-Low)
    6. Add another column- (Movement from open)
    7. "Perchange_prev_close" 
    8. Calculate 7days/14days/21 days/50 days and 200 days exponential moving averages
    9. Plot the historical data (for one month for example) using candlesticks
    10. Heikin aashi candle data( as separate df). Try to calculate using python code and create it as a function

# Approach
Extracted 15 years NIFTY50 data using **nsepy/nsetools**, performed **technical analysis**, used **Cufflinks** and **Plotly** for interactive **candlestick** and **Heikin Ashi charts**

# Outcome
Understood NIFTY50 trends through interactive data visualization, providing investment insights

# About NIFTY50
https://www.nseindia.com/products-services/indices-nifty50-index

