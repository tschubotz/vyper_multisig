from brownie import reverts
from fixtures import setup_wallet, ACCOUNTS

def test_swap_owner(setup_wallet):
    old_threshold = setup_wallet.threshold()
    setup_wallet.swap_owners(ACCOUNTS[0].address, ACCOUNTS[3].address)
    assert setup_wallet.owners(0) == ACCOUNTS[3].address
    assert setup_wallet.threshold() == old_threshold

def test_swap_owners_reverts(setup_wallet):
    with reverts():
        setup_wallet.swap_owners(ACCOUNTS[1].address, ACCOUNTS[0].address)

    with reverts():
        setup_wallet.swap_owners(ACCOUNTS[4].address, ACCOUNTS[5].address)

    with reverts():
        setup_wallet.swap_owners(ACCOUNTS[1].address, "0x0000000000000000000000000000000000000000")

    with reverts():
        setup_wallet.swap_owners(ACCOUNTS[1].address, setup_wallet)
