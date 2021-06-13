Market Abuse Detection application identifies suspicious orders for a stock based on criteria mentioned below.
traders file to be supplied and the actual history stock data be downloaded from Yahoo finance.

Criteria to identify the suspicion orders:


- The trader has submitted an order above the high price/below the low price for a given day of a stock
- The trader has submitted an order in a date when the stock was not traded

If any suspicious orders are found, we want to do the following analysis:

- If more than one trader is found, rank by number of suspicious orders per trader.

- Try to find if there is a correlation between the nationality of the trader and the 
tendency to make suspicious orders 

Note: Since the currency for the price in traders_file supplied is not given I assumed it to be US dollar.



Run Guide :

1. Setup the configuration file according to the configuration.ini example is already given the project dir /MarketAbuseDetection/config/configuration.ini

2. Run the application with the below command
	
	Python  <<application_dir>>/MarketAbuseDetection/main.py'  --configuration  <<application_dir>>/MarketAbuseDetection/config/configuration.ini