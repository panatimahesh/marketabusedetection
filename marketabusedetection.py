
import time
import datetime
import pandas as pd
import logging
import inspect

#initiate logger
logger = logging.getLogger(__name__)


def getStockDataYahoo(stock, start_date, end_date):

    '''
        Extracts stock data from Yahoo between the dates range start_date and end_date
    :param stock: stock name ex: 'AMZN'
    :param start_date: start date for the data to be extracted ex:'2020-02-01' (YYYY-MM-DD)
    :param end_date: end date for the data to be extracted ex:'2020-03-31' (YYYY-MM-DD)
    :return: pandas dataframe with stockdata
    '''
    func_name = inspect.stack()[0][3]
    logger.info(f"Inside function {func_name}")
    period1 = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    period1 = int(time.mktime(datetime.datetime(period1.year,period1.month,period1.day,23,59).timetuple()))
    period2 = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    period2 = int(time.mktime(datetime.datetime(period2.year,period2.month,period2.day,23,59).timetuple()))
    query_str = f"https://query1.finance.yahoo.com/v7/finance/download/{stock}?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true"
    stock_df = pd.read_csv(query_str)
    logger.info(f"The function {func_name} execution has been complete")
    return stock_df





def stripTime(value):
    '''
        This function strips time part from datetime type and returns only datepart
    :param value: datetime as string
    :return: date
    '''
    date_part = datetime.datetime.strptime(value,'%Y-%m-%d %H:%M:%S').date()
    return date_part




def findAbuse(tr_stock_df, yahoo_stock_df):
    '''
     This function finds the traders who committed the market abuse
     criteria:
        The trader has submitted an order above the high price/below the low price for a given day of a stock
        The trader has submitted an order in a date when the stock was not traded

    :param tr_stock_df: traders data as panda df from trader file
    :param yahoo_stock_df: Stock from yahoo for a particular stock
    :return: data of traders who committed market abuse as dataframe
    '''

    func_name = inspect.stack()[0][3]
    logger.info(f"Inside function {func_name}")
    merged_df = tr_stock_df.merge(yahoo_stock_df, how='left', left_on='tradeDate', right_on='Date')
    merged_df['abuse_flag'] = merged_df.apply(driveAbuseFlag,axis=1)
    #Records with abuse_flag == 1 are abuse records
    abuse_df = merged_df.loc[merged_df['abuse_flag']==1]
    logger.info(f"The function {func_name} execution has been complete")
    return abuse_df






def getTradersData(traders_file):

    '''
        This function reads the traders file supplied and returns it to a Pandas dataframe
    :param traders_file: Traders file as the input data
    :return: Pandas dataframe
    '''
    func_name = inspect.stack()[0][3]
    logger.info(f"Inside function {func_name}")
    traders_df = pd.read_csv(traders_file, delimiter=',', header='infer')
    logger.info(f"The function {func_name} execution has been complete")
    return traders_df




def driveAbuseFlag(row):
    '''
    This function derives the abuse flag
    :param row: row of abuse_df
    :return: int
    '''

    if pd.isnull(row['Date']):
        val =  1
    elif (row['price'] > row['High']) or (row['price'] < row['Low']):
        val =  1
    else:
        val = 0
    return val



def cleanseYahooStockData(yahoo_stock_df):
    '''
        This function does the following tasks
        1. coverts the Date into  date(YYYY-MM-DD) format
    :param yahoo_stock_df: yahoo stock dataframe
    :return: pandas dataframe
    '''
    func_name = inspect.stack()[0][3]
    logger.info(f"Inside function {func_name}")
    yahoo_stock_df['Date'] = yahoo_stock_df['Date']\
                                .apply(pd.to_datetime)
    logger.info(f"The function {func_name} execution has been complete")

    return  yahoo_stock_df



def cleanseTradersData(traders_df, stock_name, start_date, end_date):

    '''
        Cleans the traders dataframe
        1. Filter data for a range of dates Ex : February '2020-02-01' (YYYY-MM-DD) March and '2020-03-31' (YYYY-MM-DD)
        2. Filter data for the stock that needs to be analysed  Ex: 'AMZN'
        3. Strip the time part in the tradeDateTime column
        4.Coverts the tradeDateTime column from object to Date
        5. Sorts the date on tradeDateTime in ascending Order
    :param traders_df: dataframe created from traders file
    :return: cleaned data as panads dataframe

    '''
    func_name = inspect.stack()[0][3]
    logger.info(f"Inside function {func_name}")
    tr_stock_df = traders_df.loc[traders_df['stockSymbol'].isin([ stock_name])]
    tr_stock_df = tr_stock_df.loc[(tr_stock_df['tradeDatetime'] >= start_date) & (tr_stock_df['tradeDatetime'] <= end_date)]\
                     .sort_values(['tradeDatetime'], ascending=[1])\
                     .reset_index()
    tr_stock_df['tradeDate'] = tr_stock_df['tradeDatetime']\
                                    .apply(stripTime)\
                                    .apply(pd.to_datetime)
    logger.info(f"The function {func_name} execution has been complete")
    return tr_stock_df




def rankByOrders(abuse_df):
    '''
        Sum the volume for each trader and sort the values by descending order
        Rank the values on num of order by trader , Highest number of orders to be 1
    :param abuse_df: Dataframe with abuse data
    :return: pandas dataframe
    '''
    func_name = inspect.stack()[0][3]
    logger.info(f"Inside function {func_name}")
    num_orders_df = abuse_df.groupby(['traderId'], as_index=False) \
            .agg({'countryCode': 'first', 'firstName': 'first', 'lastName': 'first', 'volume': 'sum'}) \
            .rename(columns={'volume': 'num_of_orders'})
    num_orders_df = num_orders_df.sort_values(['num_of_orders'], ascending=[0])\
                        .reset_index(drop=True)
    num_orders_df['rank_by_orders'] = num_orders_df['num_of_orders'].rank(ascending=False)
    num_orders_df = num_orders_df.astype({'num_of_orders':'int','rank_by_orders':'int'})
    logger.info(f"The function {func_name} execution has been complete")
    return num_orders_df



def findCountByCountry(abuse_df):
    '''
        Find the number of traders per country and return as dataframe
    :param abuse_df: Dataframe with abuse data
    :return:
    '''
    func_name = inspect.stack()[0][3]
    logger.info(f"Inside function {func_name}")
    count_by_country_df = abuse_df.groupby(['countryCode'], as_index=False) \
        .agg({'traderId': 'count', 'volume': 'sum'}) \
        .rename(columns={'traderId': 'num_traders', 'volume': 'num_orders'}) \
        .astype({'num_orders': 'int'}) \
        .sort_values(['num_orders'], ascending=[0]).reset_index(drop=True)
    logger.info(f"The function {func_name} execution has been complete")
    return count_by_country_df.set_index('countryCode')


def marketAbuseDetectionApp(config):
    '''
        This function stitches the Market Abuse Detection application together.
            Once the suspicion order are detected they are written into two csv files
            with different data.
            1. Sum the volume for each trader and sort the values by descending order and rank in that order
            2. Correlation data of the traders and country they belong to
    :param config: Configuration details
    :return: df
    '''
    func_name = inspect.stack()[0][3]
    logger.info(f"Inside function {func_name}")
    stock_name = config['stock_extract_values']['stock_name']
    start_date = config['stock_extract_values']['start_date']
    end_date = config['stock_extract_values']['end_date']
    traders_file = config['traders_values']['traders_file']
    output_dir = config['output_values']['output_dir']
    yahoo_stock_df = getStockDataYahoo(stock_name, start_date, end_date)
    tr_stock_df = getTradersData(traders_file)
    cleansed_yahoo_stock_df= cleanseYahooStockData(yahoo_stock_df)
    cleansed_tr_stock_df = cleanseTradersData(tr_stock_df, stock_name, start_date, end_date)
    abuse_df = findAbuse(cleansed_tr_stock_df,cleansed_yahoo_stock_df)
    rank_num_orders_df = rankByOrders(abuse_df)
    count_by_country_df = findCountByCountry(abuse_df)
    rank_num_orders_df.to_csv(f"{output_dir}rank_num_orders_df.csv",header=True, index=False)
    count_by_country_df.to_csv(f"{output_dir}country_suspicion_tendency.csv",header=True, index=True)
    logger.info(f"The function {func_name} execution has been complete")
    return rank_num_orders_df, count_by_country_df





