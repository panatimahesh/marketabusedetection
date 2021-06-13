import unittest
from marketabusedetection import  marketAbuseDetectionApp
from genericfunctions import get_config
import logging

logger = logging.getLogger(__name__)

class MyTestCase(unittest.TestCase):
    def test_mktabuse(self):
        config = get_config(r'C:\Users\panati\PycharmProjects\MarketAbuseDetection\config\test_configuration.ini')
        rank_orders_df,abuse_tendency_df=marketAbuseDetectionApp(config)
        total_orders_rank = sum(list(rank_orders_df['num_of_orders']))
        total_traders_tendency = sum(list(abuse_tendency_df['num_traders']))
        self.assertEqual(total_orders_rank, 30)
        self.assertEqual(total_traders_tendency, 1)


if __name__ == '__main__':
    unittest.main()
