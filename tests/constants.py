""" SKALE test constants """

import os
from decimal import Decimal

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

DEFAULT_NODE_NAME = 'test_node'
SECOND_NODE_NAME = 'test_node_2'
DEFAULT_NODE_HASH = '23bdf46c41fa300e431425baff124dc31625b34ec09b829f61aa16ab0102ca8d'
DEFAULT_NODE_PORT = 3000

TEST_CONTRACT_NAME = 'NodesFunctionality'
TEST_CONTRACT_NAME_HASH = 'f88bdb637038c4be9f72381c0db0b0d7b7f369cfdd49619ee7e48aa7940482b9'
ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

TOKEN_TRANSFER_VALUE = 100
ETH_TRANSFER_VALUE = Decimal('0.05')

DEFAULT_SCHAIN_NAME = 'test_schain'
DEFAULT_SCHAIN_INDEX = 0
DEFAULT_SCHAIN_ID = '9ca5dee9297f25a2d182b4a437c9b57b15430750391861ca3ddf1a763ba285e0'

LIFETIME_YEARS = 1
LIFETIME_SECONDS = LIFETIME_YEARS * 366 * 86400

EMPTY_SCHAIN_ARR = ['', '0x0000000000000000000000000000000000000000', 0, 0, 0, 0, 0, 0]
EMPTY_ETH_ACCOUNT = '0x0000000000000000000000000000000000000001'

MIN_NODES_IN_SCHAIN = 2

N_TEST_WALLETS = 2

ENDPOINT = os.environ['ENDPOINT']
TEST_ABI_FILEPATH = os.path.join(DIR_PATH, os.pardir, 'test_abi.json')
ETH_PRIVATE_KEY = os.environ['ETH_PRIVATE_KEY']

# constants contract
NEW_REWARD_PERIOD = 500
NEW_DELTA_PERIOD = 400

TEST_URL = 'http://localhost:3030'
TEST_RPC_WALLET_URL = 'http://localhost:3000'
NOT_EXISTING_RPC_WALLET_URL = 'http://abc:9999'
EMPTY_HEX_STR = '0x0'

# validator

D_VALIDATOR_ID = 1
D_VALIDATOR_NAME = 'test'
D_VALIDATOR_DESC = 'test'
D_VALIDATOR_FEE = 10
D_VALIDATOR_MIN_DEL = 1000

D_DELEGATION_ID = 0
D_DELEGATION_AMOUNT = 55000000
D_DELEGATION_PERIOD = 3
D_DELEGATION_INFO = 'test'

NOT_EXISTING_ID = 123123
