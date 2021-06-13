
from argparse import ArgumentParser
import logging
import datetime
from genericfunctions import get_config
from marketabusedetection import marketAbuseDetectionApp
import traceback

def getArguments():
    '''
        Reads arguments from the command line for market abuse detection application
    :return: parsed arguments
    '''
    parser = ArgumentParser(description='MarketAbuseDetection')
    parser.add_argument('--configuration', '-c', dest='configuration_path', required=True,
                        help='Path of configuration file [Required]')
    parser.add_argument('--log-level', '-l', dest='log_level', required=False, default="INFO",
                        help='Log Level [Optional, Default: WARN]')
    return parser.parse_args()


def main():
    '''
        Entry point for the application Market Abuse Detection
    '''
    args = getArguments()
    config = get_config(args.configuration_path)
    log_dir = config['log_values']['log_dir']
    log_name = config['log_values']['log_name'].format(current_dt=str(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
    log_name = f"{log_dir}{log_name}"
    print(log_name)
    logging.basicConfig(filename=log_name, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=args.log_level)
    logger = logging.getLogger(__name__)
    logger.info("The Market Abuse detection application has been started")

    try:
        marketAbuseDetectionApp(config)
        logger.info("The Market Abuse detection application has been completed")
    except Exception as e:
        logger.error(f"There's an issue while running the application :\n{traceback.format_exc()}")



if __name__ == '__main__':

    '''
        find traders which made suspicious orders. To be a suspicious orders we consider the 
        following rules:
            - The trader has submitted an order above the high price/below the low price for a given day of a stock
            - The trader has submitted an order in a date when the stock was not traded

    '''

    main()
