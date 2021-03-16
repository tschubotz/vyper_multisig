from brownie import reverts
from fixtures import not_setup_wallet, owners_1, owners_2, owners_3

def test_setup_owners_1(not_setup_wallet, owners_1):
    not_setup_wallet.setup(owners_1, 1)

    for i in range(10):
        assert not_setup_wallet.owners(i) == owners_1[i]

def test_setup_owners_2(not_setup_wallet, owners_2):
    not_setup_wallet.setup(owners_2, 1)

    for i in range(10):
        assert not_setup_wallet.owners(i) == owners_2[i]

def test_setup_threshold(not_setup_wallet, owners_2):
    not_setup_wallet.setup(owners_2, 2)
    assert not_setup_wallet.threshold() == 2

def test_setup_threshold_not_higher_than_num_owners(not_setup_wallet, owners_2):
    with reverts():
        not_setup_wallet.setup(owners_2, 3)
    with reverts():
        not_setup_wallet.setup(owners_2, 10)

def test_setup_threshold_not_too_low(not_setup_wallet, owners_2):
    with reverts():
        not_setup_wallet.setup(owners_2, 0)

def test_setup_only_once(not_setup_wallet, owners_2):
    not_setup_wallet.setup(owners_2, 2)
    with reverts():
        not_setup_wallet.setup(owners_2, 2)

def test_setup_nonce(not_setup_wallet, owners_2):
    not_setup_wallet.setup(owners_2, 2)
    assert not_setup_wallet.nonce() == 0

# def test_wallet_can_receive_eth():
#     pass