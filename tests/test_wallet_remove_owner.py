from brownie import reverts
from fixtures import setup_wallet, ACCOUNTS

def test_remove_owner(setup_wallet):
    setup_wallet.remove_owner_with_threshold(ACCOUNTS[1].address, 1)
    assert setup_wallet.owners(1) == "0x0000000000000000000000000000000000000000"
    assert setup_wallet.threshold() == 1

def test_remove_owner_reverts(setup_wallet):
    with reverts():
        setup_wallet.remove_owner_with_threshold(ACCOUNTS[5].address, 1)

    with reverts():
        setup_wallet.remove_owner_with_threshold(ACCOUNTS[1].address, 0)

    with reverts():
        setup_wallet.remove_owner_with_threshold(ACCOUNTS[1].address, 9)
    
    with reverts():
        setup_wallet.remove_owner_with_threshold("0x0000000000000000000000000000000000000000", 1)
