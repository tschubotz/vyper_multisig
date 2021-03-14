from brownie import reverts
from fixtures import setup_wallet, owners_2
from eth_abi import encode_abi
from web3 import Web3

from fixtures import ACCOUNTS
from eth_account.messages import encode_defunct

def calculate_transaction_hash(nonce: int, to: str, value: int, data: str='00'):
    encoded: bytes = nonce.to_bytes(32, 'big') + bytes.fromhex(to).rjust(32,b'\0') + value.to_bytes(32, 'big') + bytes.fromhex(data)
    # '0x66aB6D9362d4F35596279692F0251Db635165871'
    return Web3.keccak(encoded)


def get_sigdata(nonce: int, to: str, value: int, data: str='00', accounts=[]):
    message_to_be_signed = encode_defunct(calculate_transaction_hash(nonce, to, value, data))

    sigdata = [[0,0,0]] * 10
    
    for i, account in enumerate(accounts):
        signature = account.sign_message(message_to_be_signed)
        sigdata[i] = [signature['v'], signature['r'], signature['s']]
    
    return sigdata

def test_execute(setup_wallet):
    nonce: int = 0
    to: str = '77aB6D9362d4F35596279692F0251Db635165871'
    value: int = 1

    sigdata = get_sigdata(nonce, to, value, accounts=[ACCOUNTS[0], ACCOUNTS[1]])

    assert setup_wallet.execute(to, value, '', sigdata, {'value': value})
    assert setup_wallet.nonce() == 1

def test_execute_non_owner(setup_wallet):
    nonce: int = 0
    to: str = '77aB6D9362d4F35596279692F0251Db635165871'
    value: int = 1

    sigdata = get_sigdata(nonce, to, value, accounts=[ACCOUNTS[2]])

    with reverts():
        setup_wallet.execute(to, value, '', sigdata, {'value': value})

def test_execute_threshold_not_reached(setup_wallet):
    nonce: int = 0
    to: str = '77aB6D9362d4F35596279692F0251Db635165871'
    value: int = 1

    sigdata = get_sigdata(nonce, to, value, accounts=[ACCOUNTS[0]])

    with reverts():
        setup_wallet.execute(to, value, '', sigdata, {'value': value})