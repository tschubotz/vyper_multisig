import pytest 
from brownie import ZERO_ADDRESS
from eth_account import Account


    # '0x7E5F4552091A69125d5DfCb7b8C2659029395Bdf', 
    # '0x2B5AD5c4795c026514f8317c7a215E218DcCD6cF', 
    # '0x6813Eb9362372EEF6200f3b1dbC3f819671cBA69'

ACCOUNTS = [
    Account.from_key('0000000000000000000000000000000000000000000000000000000000000001'),
    Account.from_key('0000000000000000000000000000000000000000000000000000000000000002'),
    Account.from_key('0000000000000000000000000000000000000000000000000000000000000003'),
    Account.from_key('0000000000000000000000000000000000000000000000000000000000000004'),
    Account.from_key('0000000000000000000000000000000000000000000000000000000000000005'),
    Account.from_key('0000000000000000000000000000000000000000000000000000000000000006'),
    Account.from_key('0000000000000000000000000000000000000000000000000000000000000007'),
    Account.from_key('0000000000000000000000000000000000000000000000000000000000000008'),
    Account.from_key('0000000000000000000000000000000000000000000000000000000000000009'),
    Account.from_key('000000000000000000000000000000000000000000000000000000000000000A'),
    Account.from_key('000000000000000000000000000000000000000000000000000000000000000B'),
    ]


@pytest.fixture(scope="function", autouse=True)
def not_setup_wallet(WalletImplementation, accounts):
    wallet = accounts[0].deploy(WalletImplementation)
    yield wallet

@pytest.fixture(scope="function", autouse=True)
def setup_wallet(WalletImplementation, accounts):
    wallet = accounts[0].deploy(WalletImplementation)

    owners = [ACCOUNTS[0].address, ACCOUNTS[1].address, ACCOUNTS[2].address]
    for i in range(7):
        owners.append(ZERO_ADDRESS)
    
    wallet.setup(owners, 2)
    yield wallet

@pytest.fixture(scope="function", autouse=True)
def owners_1():
    owners = [ACCOUNTS[0].address]
    for i in range(9):
        owners.append(ZERO_ADDRESS)
    yield owners

@pytest.fixture(scope="function", autouse=True)
def owners_2():
    owners = [ACCOUNTS[0].address, ACCOUNTS[1].address]
    for i in range(8):
        owners.append(ZERO_ADDRESS)
    yield owners

@pytest.fixture(scope="function", autouse=True)
def owners_3():
    owners = [ACCOUNTS[0].address, ACCOUNTS[1].address, ACCOUNTS[2].address]
    for i in range(7):
        owners.append(ZERO_ADDRESS)
    yield owners

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass