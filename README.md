Ideal Trading Frequency
==============================

What is an ideal trading frequency to trade stocks as a retail investor? In this project I explore a few basic trading/investing strategies to identify the most effective trading frequency. This app allows user to evaluate buy-and-hold with dollar cost averaging strategy against daily hold overnight and don't hold overnight strategies. To run an app online: https://trading-frequency.herokuapp.com/

Through this app you select start and end dates, initial investment, regular investment and it's frequency for buy & hold portfolio and the app returns % profile return for the strategy. After you can compare performance of buy-and-hold method to the daily daily hold overnight and don't hold overnight strategies.

You can choose 3 different asset classes (presented by their respected ETFs):
 - An ETF that tracks the S&P500 index (SPY)
 - An ETF that tracks the US T-bonds (VGLT) 
 - An ETF on Gold (GLD)

Requirements
Python 3.8 version or superior

How to run this demo

 - cd to the directory where requirements.txt is located
 - activate your virualenv
 - run: pip install -r requirements.txt in your shell
 - git clone https://github.com/vragov/Trading_Frequency.git
 - cd into the project folder
 - 'path'>cd Trading_Frequency
 - streamlit run src/app.py