# @version ^0.2.10

from contracts import WalletImplementation

walletImplementation: public(address)

@external
def __init__(_walletImplementation: address):
    assert _walletImplementation != ZERO_ADDRESS
    self.walletImplementation = _walletImplementation

@external
def createWallet(_owners: address[10], _threshold: uint256) -> address:
    wallet: address = create_forwarder_to(self.walletImplementation)
    WalletImplementation(wallet).setup(_owners, _threshold)
    return wallet