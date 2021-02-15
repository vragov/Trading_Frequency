import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as pdr
from matplotlib.ticker import FixedLocator
import math
import streamlit as st
from matplotlib.pyplot import rc
import datetime
import pandas_market_calendars as mcal
from PIL import Image
import seaborn as sns
import matplotlib.ticker as ticker

def price_diff_loaded(dataset, startDate, endDate, dayprice = 'open'):
    '''
    Function takes in the dataset for a particular asset class, start and end dates, dayprice to use and calculates the absolute price change (in $)
    '''
    price_diff = dataset.loc[endDate,dayprice] - dataset.loc[startDate,dayprice]
    return price_diff

def price_ratio_loaded(dataset, startDate, endDate, dayprice = 'open'):
    '''
    Function takes in the dataset for a particular asset class, start and end dates, dayprice to use and calculates the relative price change
    '''
    price_ratio = dataset.loc[endDate,dayprice]/dataset.loc[startDate,dayprice]        
    return price_ratio

def dollar_cost_average_loaded(dataset, startDate, endDate, initial_investment = 0, regular_invest = 1000, freq = 10, dayprice = 'open'):
    '''
    Function takes in the dataset for a particular asset class, start and end dates, dayprice to use and calculates final value of the portfolio as a result of the dollar cost averaging
    '''
 
    dict_list = []
   
    nyse = mcal.get_calendar('NYSE')
    early = nyse.schedule(start_date=startDate, end_date=endDate)
    startDate = early.index[0]
    endDate = early.index[-1]
    dca_dates = list(early[::freq].index)
    #dca_dates = investment_dates_all = pd.bdate_range(start = startDate, end = endDate, freq = str(freq)+"B") #tracks the days when regular investment is made
    
    current_value = initial_investment*price_ratio_loaded(dataset, startDate, startDate, dayprice) 
    invested = initial_investment
    previous_date = startDate
    history_dict = {'dates':startDate,'Invested':initial_investment,'Portfolio Value':current_value}
    dict_list.append(history_dict)
    
    for date in dca_dates[1:]:
        #add to the sum to track both current and at the end values of the portfolio
        current_value = current_value*price_ratio_loaded(dataset, startDate = previous_date, endDate = date, dayprice = dayprice) + regular_invest 
        invested += regular_invest
        #log invested, portfolio_value
        tmp_dict = {'dates':date,'Invested':invested,'Portfolio Value':current_value}
        dict_list.append(tmp_dict)
        previous_date = date   
    current_value = current_value*price_ratio_loaded(dataset, startDate = date, endDate = endDate, dayprice = dayprice)
    tmp_dict = {'dates':endDate,'Invested':invested,'Portfolio Value':current_value}
    dict_list.append(tmp_dict)
    return pd.DataFrame(dict_list).set_index('dates')

def hold_overnight_ratio(dataset, startDate, endDate):
    '''
    This function calculates the difference assuming
    '''
    price_ratio_list = (dataset.loc[startDate:endDate,'open'][1:] - dataset.loc[startDate:endDate,'close'][:-1])/(dataset.loc[startDate:endDate,'close'][:-1]+0.000001)
    running_price_ratio = np.cumprod(1 + price_ratio_list)
    price_ratio = np.prod(1+price_ratio_list)
    return price_ratio, price_ratio_list, running_price_ratio 

def dollar_cost_average_hold_overnight(dataset, startDate, endDate, initial_investment = 0, regular_invest = 1000, freq = 10):
    '''
    Function takes in the dataset for a particular asset class, start and end dates, dayprice to use and calculates final value of the portfolio as a result of the dollar cost averaging
    ''' 
 
    dict_list = []

    nyse = mcal.get_calendar('NYSE')
    early = nyse.schedule(start_date=startDate, end_date=endDate)
    startDate = early.index[0]
    endDate = early.index[-1]
    dca_dates = list(early[::freq].index)
    #dca_dates = investment_dates_all = pd.bdate_range(start = startDate, end = endDate, freq = str(freq)+"B") #tracks the days when regular investment is made
    
    current_value = initial_investment*hold_overnight_ratio(dataset, startDate, startDate)[0] 
    
    value_at_the_end = initial_investment*hold_overnight_ratio(dataset, startDate, endDate)[0]
    invested = initial_investment
    previous_date = startDate
    
    history_dict = {'dates':startDate,'Invested':initial_investment,'Portfolio Value':current_value}
    dict_list.append(history_dict)
    
    for date in dca_dates[1:]:
        #add to the sum to track both current and at the end values of the portfolio
        current_value = current_value*hold_overnight_ratio(dataset, startDate = previous_date, endDate = date)[0] + regular_invest 
        invested += regular_invest
        #log invested, portfolio_value
        tmp_dict = {'dates':date,'Invested':invested,'Portfolio Value':current_value}
        dict_list.append(tmp_dict)
        previous_date = date   
    current_value = current_value*hold_overnight_ratio(dataset, startDate = date, endDate = endDate)[0]
    tmp_dict = {'dates':endDate,'Invested':invested,'Portfolio Value':current_value}
    dict_list.append(tmp_dict)
    return pd.DataFrame(dict_list).set_index('dates')


   
def dont_hold_overnight_ratio(dataset, startDate, endDate):
    '''
    This function calculates the difference assuming
    '''
    price_ratio_list = (dataset.loc[startDate:endDate,'close'] - dataset.loc[startDate:endDate,'open'])/(dataset.loc[startDate:endDate,'open']+0.000001)
    running_price_ratio = np.cumprod(1 + price_ratio_list)
    price_ratio = np.prod(1+price_ratio_list)
    return price_ratio, price_ratio_list, running_price_ratio 

def dollar_cost_average_dont_hold_overnight(dataset, startDate, endDate, initial_investment = 0, regular_invest = 1000, freq = 10):
    '''
    Function takes in the dataset for a particular asset class, start and end dates, dayprice to use and calculates final value of the portfolio as a result of the dollar cost averaging
    ''' 
 
    dict_list = []

    nyse = mcal.get_calendar('NYSE')
    early = nyse.schedule(start_date=startDate, end_date=endDate)
    startDate = early.index[0]
    endDate = early.index[-1]
    dca_dates = list(early[::freq].index)
    #dca_dates = investment_dates_all = pd.bdate_range(start = startDate, end = endDate, freq = str(freq)+"B") #tracks the days when regular investment is made
    
    current_value = initial_investment*dont_hold_overnight_ratio(dataset, startDate, startDate)[0] 
    
    value_at_the_end = initial_investment*dont_hold_overnight_ratio(dataset, startDate, endDate)[0]
    invested = initial_investment
    previous_date = startDate
    
    history_dict = {'dates':startDate,'Invested':initial_investment,'Portfolio Value':current_value}
    dict_list.append(history_dict)
    
    for date in dca_dates[1:]:
        #add to the sum to track both current and at the end values of the portfolio
        current_value = current_value*dont_hold_overnight_ratio(dataset, startDate = previous_date, endDate = date)[0] + regular_invest 
        invested += regular_invest
        #log invested, portfolio_value
        tmp_dict = {'dates':date,'Invested':invested,'Portfolio Value':current_value}
        dict_list.append(tmp_dict)
        previous_date = date   
    current_value = current_value*dont_hold_overnight_ratio(dataset, startDate = date, endDate = endDate)[0]
    tmp_dict = {'dates':endDate,'Invested':invested,'Portfolio Value':current_value}
    dict_list.append(tmp_dict)
    return pd.DataFrame(dict_list).set_index('dates')

@st.cache 
def read_data(file):
    data = pd.read_csv(file,parse_dates=['date'])
    data['date'] = data['date'].dt.tz_convert(None)
    data = data.set_index('date')
    return data



st.title('Day Trading vs Buy-and-Hold')
'''
### What kind of return could you get by following traditional dollar cost averaging strategy? Typical mom-and-pop investor starts with certain amount of money and are allocating certain amount of their salary bi-weekly or monthly to their investment account. 
'''
'''
You can choose among 3 asset classes (data pulled using tiingo API):
    
1. An ETF that tracks the S&P500 index
2. An ETF that tracks the US 10-year T-bonds
3. An ETF that tracks physical Gold


Choose the asset class, initial invesment, frequency (bi-weekly or monthly) and size of regular contribution, start and end date of the investigation period.   
'''

image = Image.open('./TradingvsInvesting.jpg')
st.sidebar.image(image, caption='', use_column_width=True)
#frequency = st.selectbox(label = "")

st.sidebar.header('Explore different trading strategies')
st.sidebar.subheader('Choose the option to visualize')

dca = st.sidebar.checkbox('Dollar Cost Averaging Calculator', value = True)

daily_trading = st.sidebar.checkbox('Daily Trading', value = False)



asset_class_selection = st.selectbox(label = 'Select Asset Class', 
						   options = ['S&P500 ETF (SPY)',
						    		  'Vanguard Long-Term Treasury Index Fund ETF (VGLT)',
						    		  'Physical Gold ETF (GLD)'])

if asset_class_selection == 'S&P500 ETF (SPY)':
	asset_class = 'SPY'
elif asset_class_selection == 'Vanguard Long-Term Treasury Index Fund ETF (VGLT)':
	asset_class = 'VGLT'
else:
	asset_class = 'GLD'	


initial_investment = st.slider('Select the size of the initial_investment', min_value = 1000, max_value = 100000, value = 10000)

contribution_selection = st.selectbox(label = 'Frequency of Contributions', 
						   options = ['Weekly','Bi-weekly',
						    		  'Monthly'])

if contribution_selection == 'Weekly':
	invest_freq = 5
elif contribution_selection == 'Bi-weekly':
	invest_freq = 10
else:
	invest_freq = 25

freq_investment = st.slider('Select the size of the regular contribution', min_value = 10, max_value = 5000, value = 1000)


startDate = st.date_input(label = "Investing Start Date", 
	min_value = datetime.datetime(2000,1,1), 
	max_value = datetime.datetime(2021,2,10),
	value = datetime.datetime(2014,7,10))

endDate = st.date_input(label = "Investment End Date", 
	min_value = datetime.datetime(2000,1,1), 
	max_value = datetime.datetime(2021,2,10),
	value = datetime.datetime(2020,12,10))



df_data = read_data(f'./data/raw/{asset_class}_flattened.csv')
df = dollar_cost_average_loaded(df_data, startDate=startDate, endDate=endDate, 
								initial_investment = initial_investment, regular_invest = freq_investment, 
								freq = invest_freq, dayprice = 'open')

df['Percent Return'] = 100*(df['Portfolio Value'] - df['Invested'])/(df['Invested'] + 0.001)

fig, (ax1, ax2) = plt.subplots(2)
#ax = df.plot(subplots = True, grid = True)
sns.set_style("whitegrid")
fig.set_size_inches(20,18)

ax1.plot(df['Percent Return'], color ='black')
#tick = ticker.StrMethodFormatter('${x:,.0f}')
#ax1.yaxis.set_major_formatter(tick) 
# Labels
ax1.set_title('Dollar Cost Averaging Return', size=18)
ax1.set_ylabel('Percent Return (%)', size=14)
ax1.set_xlabel('Date', size=14)

ax2.plot(df['Portfolio Value'], color ='orange')
ax2.plot(df['Invested'], color ='green')
tick = ticker.StrMethodFormatter('${x:,.0f}')
ax2.yaxis.set_major_formatter(tick) 
# Labels
ax2.set_title('Amount Invested vs Portfolio Value', size=18)
ax2.set_ylabel('Amount ($)', size=14)
ax2.set_xlabel('Date', size=14)
ax2.legend(['Portfolio Value',"Amount Invested"], fontsize=18)

st.pyplot(plt)
#$st.write("Annulaized Rate of Return =", (1 + df['Percent Return'][-1]/100, 365/(df.index[-1] - df.index[0]).days)
st.write("Annualized Rate of Return =", ((1+df['Percent Return'][-1]/100)**(365/(df.index[-1] - df.index[0]).days) - 1)*100,'%')
'''
### Now once we familirized ourselves with the returns provided by the traditional buy-and-hold investment accross multiple asset classes let's move on to the "Daily Trading" to evaluate a few simple day trading strategies. 
'''


if daily_trading:
    '''# Evaluating two daily trading strategies against DCA (Buy-and-Hold Dollar Cost Averaging)'''

    st.markdown('''Based on the price data availabily (Open, Close, Low, High daily prices) I came up with two daily strategies that will be evaluated and compared to buy-and-hold stretegy above: 
* The first strategy is called "only hold overnight", where investor buys stock at the close and sells at the open of next day. This way investor only makes money during the period when the stock market is closed. 
* The second strategy is called "don't hold overnight", where investor buys at the open and sells at the close, holding security only while NYSE is open. 

Now let's take a look at the returns we can expect from the first daily trading streategy using the same amounts as selected for the Dollar Cost Averaging:
	''')

    df_hold_overnight = dollar_cost_average_hold_overnight(df_data, startDate=startDate, endDate=endDate, 
								initial_investment = initial_investment, regular_invest = freq_investment, 
								freq = invest_freq)
    df_hold_overnight['Percent Return'] = 100*(df_hold_overnight['Portfolio Value'] - df_hold_overnight['Invested'])/(df_hold_overnight['Invested'] + 0.001)
    fig, (ax1, ax2, ax3) = plt.subplots(3)
	#ax = df.plot(subplots = True, grid = True)
    fig.set_size_inches(20,18)
    ax1.plot(df_hold_overnight['Percent Return'], color ='black')
	
    ax1.set_title('Only Hold Overnight', size=18)
    ax1.set_ylabel('Percent Return (%)', size=14)
    ax1.set_xlabel('Date', size=14)

    ax2.plot(df_hold_overnight['Portfolio Value'], color ='orange')
    ax2.plot(df_hold_overnight['Invested'], color ='green')
    tick = ticker.StrMethodFormatter('${x:,.0f}')
    ax2.yaxis.set_major_formatter(tick) 
	# Labels
    ax2.set_title('Amount Invested vs Portfolio Value', size=18)
    ax2.set_ylabel('Amount ($)', size=14)
    ax2.set_xlabel('Date', size=14)
    ax2.legend(['Portfolio Value',"Amount Invested"], fontsize=18)

    # Get difference with array operations
    difference = np.array(df_hold_overnight['Portfolio Value']) - np.array(df['Portfolio Value'])
    ax3.fill_between(df_hold_overnight.index, y1=difference, y2=0, color='green', where=difference > 0, edgecolor='black')
    ax3.fill_between(df_hold_overnight.index, y1=difference, y2=0, color='red', where=difference < 0, edgecolor='black') 
    ax3.plot(df_hold_overnight.index, difference, color='black', linewidth=.4)

    ax3.set_title('Only Hold Overnight - DCA', size=18)
    ax3.set_ylabel('Current Value Difference($)', size=14)
    ax3.set_xlabel('Date of Investment', size=14)

    plt.legend(['Amount','Only Hold Overnight > DCA','Only Hold Overnight < DCA'])

    st.pyplot(plt)
	#$st.write("Annulaized Rate of Return =", (1 + df['Percent Return'][-1]/100, 365/(df.index[-1] - df.index[0]).days)
    st.write("Annualized Rate of Return for Only Hold Overnight =", ((1+df_hold_overnight['Percent Return'][-1]/100)**(365/(df_hold_overnight.index[-1] - df_hold_overnight.index[0]).days) - 1)*100,'%')
    st.write("Only Hold Overnight beats Dollar Cost Averaging exactly:",(100*sum(difference>0)/len(difference)),'%')

    df_dont_hold_overnight = dollar_cost_average_dont_hold_overnight(df_data, startDate=startDate, endDate=endDate, 
								initial_investment = initial_investment, regular_invest = freq_investment, 
								freq = invest_freq)
    df_dont_hold_overnight['Percent Return'] = 100*(df_dont_hold_overnight['Portfolio Value'] - df_dont_hold_overnight['Invested'])/(df_dont_hold_overnight['Invested'] + 0.001)
    fig, (ax1, ax2, ax3) = plt.subplots(3)
	#ax = df.plot(subplots = True, grid = True)
    fig.set_size_inches(20,18)
    ax1.plot(df_dont_hold_overnight['Percent Return'], color ='black')
	
    ax1.set_title("Don't Hold Overnight", size=18)
    ax1.set_ylabel('Percent Return (%)', size=14)
    ax1.set_xlabel('Date', size=14)

    ax2.plot(df_dont_hold_overnight['Portfolio Value'], color ='orange')
    ax2.plot(df_dont_hold_overnight['Invested'], color ='green')
    tick = ticker.StrMethodFormatter('${x:,.0f}')
    ax2.yaxis.set_major_formatter(tick) 
	# Labels
    ax2.set_title('Amount Invested vs Portfolio Value', size=18)
    ax2.set_ylabel('Amount ($)', size=14)
    ax2.set_xlabel('Date', size=14)
    ax2.legend(['Portfolio Value',"Amount Invested"], fontsize=18)

    # Get difference with array operations
    difference = np.array(df_dont_hold_overnight['Portfolio Value']) - np.array(df['Portfolio Value'])
    ax3.fill_between(df_dont_hold_overnight.index, y1=difference, y2=0, color='green', where=difference > 0, edgecolor='black')
    ax3.fill_between(df_dont_hold_overnight.index, y1=difference, y2=0, color='red', where=difference < 0, edgecolor='black') 
    ax3.plot(df_dont_hold_overnight.index, difference, color='black', linewidth=.4)

    ax3.set_title("Don't Hold Overnight - DCA", size=18)
    ax3.set_ylabel('Current Value Difference($)', size=14)
    ax3.set_xlabel('Date of Investment', size=14)

    plt.legend(['Amount',"Don't Hold Overnight > DCA"," Don't Only Hold Overnight < DCA"])

    st.pyplot(plt)
	#$st.write("Annulaized Rate of Return =", (1 + df['Percent Return'][-1]/100, 365/(df.index[-1] - df.index[0]).days)
    st.write("Annualized Rate of Return for Only Hold Overnight =", ((1+df_hold_overnight['Percent Return'][-1]/100)**(365/(df_hold_overnight.index[-1] - df_hold_overnight.index[0]).days) - 1)*100,'%')
    st.write("Only Hold Overnight beats Dollar Cost Averaging exactly:",(100*sum(difference>0)/len(difference)),'%')


# if considerations:
#     '''# Hypothesis and results'''
#     st.markdown('''Before we reach conclusions let's clarify which are the hypothesis.
# Too often the hypothesis of a model are overlooked, but if hypothesis aren't realistic, results won't be realistic neither.
# ### Hypothesis of the model:
# 1. Buy & hold strategy for the whole holding period
# 2. The empirical future annual returns distribution of the 3 assets won't be dramatically different compared to that of the past 69 years.
# This means that in the future the stock market can loose even 50% one year, but the model doesn't take into account the fact
# that the stock market can loose 100% or that both stocks and bonds loose 30% in one year.
# 3. Historical stock and bonds data only concern the US market. Hence the bootstrap portfolio of our model is only a benchmark portfolio.
# It is useful to compare different weights among the 3 principal assets (except cash) but it doesn't represent a fully diversified portfolio.
# Having said that, let's proceed to some considerations:
# * Gold is an insurance asset: its average CAGR is only slightly positive with high annual return volatility (indeed geometric sharpe ratio is almost null: that means
# that it is NOT an insurance asset if held individually).
# But you can try by yourself that a portfolio without a certain per cent
# of gold (I guess at least 8-10%) is not pareto efficient.
# * If you increase stocks weight the average CAGR increases (and also the average Omega ratio at 8%), but also volatility CAGR, VaR and CVaR increase.
# * Above a certain stock weight threshold (I estimate about 50%), the risk increases more than the increase of the expected return: geometric sharpe ratio begins to drop.
# Moreover max drawdown metrics begin to increase (in absolute value) in a clear manner.
# * If you increase stock weight beyond a certain threshold (I estimate 85-90%), the portfolio is not anymore pareto efficient (i.e. you can build another
# portfolio with the same expected CAGR but less risky).
# * Based on my simulations, robust portfolios are weigth sets like these: (35% - 50% - 15%), (40% - 40%- 20%), (45% - 30% - 25%).
#  Aggressive and pareto efficient portfolios are sets like these: (70% - 15% - 15%), (60% - 30% - 10%).
#   ''')