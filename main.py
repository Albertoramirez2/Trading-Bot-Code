import logging

# Configure logging
logging.basicConfig(filename='../logs/trading_algorithm.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# Example log entry
logging.info('Starting the trading algorithm')
