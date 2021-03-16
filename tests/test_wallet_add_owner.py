from brownie import reverts
from fixtures import setup_wallet, ACCOUNTS

def test_add_owner(setup_wallet):
    setup_wallet.add_owner_with_threshold(ACCOUNTS[3].address, 1)
    assert setup_wallet.owners(3) == ACCOUNTS[3].address
    assert setup_wallet.threshold() == 1

def test_add_owner_reverts(setup_wallet):
    with reverts():
        setup_wallet.add_owner_with_threshold(ACCOUNTS[1].address, 1)

    with reverts():
        setup_wallet.add_owner_with_threshold(ACCOUNTS[1].address, 0)

    with reverts():
        setup_wallet.add_owner_with_threshold(ACCOUNTS[1].address, 9)
    
    with reverts():
        setup_wallet.add_owner_with_threshold("0x0000000000000000000000000000000000000000", 1)

    with reverts():
        setup_wallet.add_owner_with_threshold(setup_wallet.address, 1)

def test_add_owner_too_many(setup_wallet):
    for i in range(3, 10):
        setup_wallet.add_owner_with_threshold(ACCOUNTS[i].address, 1)
    with reverts():
        setup_wallet.add_owner_with_threshold(ACCOUNTS[10].address, 1)
