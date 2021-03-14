# @version ^0.2.10

owners: public(address[10])
threshold: public(uint256)
nonce: public(uint256)

@external
def setup(_owners: address[10], _threshold: uint256):
    assert self.threshold == 0, "setup can only be called once"

    _num_owners: uint256 = 0
    for i in range(10):
        if _owners[i] != ZERO_ADDRESS:
            self.owners[i] = _owners[i]
            _num_owners += 1
    assert _num_owners > 0, "at least 1 owner needs to be provided"
    assert _num_owners >= _threshold, "threshold can't be greater than number of owners"

    self.nonce = empty(uint256)
    self.threshold = _threshold

@external
@payable
def __default__():
    pass

@external
@view
def calculate_transaction_hash(_nonce: uint256, _to: address, _value: uint256, _data: Bytes[4096]) -> bytes32:
    return keccak256(concat(convert(_nonce, bytes32), convert(_to, bytes32), convert(_value, bytes32), _data))

@external
@payable
def execute(_to: address, _value: uint256, _data: Bytes[4096], sigdata: uint256[3][10]) -> Bytes[4096]:
    
    assert msg.value >= _value, "you are trying to send more ETH than you provided"
    assert self.threshold > 0, "threshold needs to be defined - did you setup your Safe?"
    approvals: uint256 = 0

    transaction_hash: bytes32 = keccak256(concat(convert(self.nonce, bytes32), convert(_to, bytes32), convert(_value, bytes32), _data))

    # Then we combine the Ethereum Signed message with our previous hash
    # Owners will have to sign the below message
    message_to_be_signed: bytes32 = keccak256(concat(b"\x19Ethereum Signed Message:\n32", transaction_hash))
    
    # # Iterates through all the owners and verifies that there signatures,
    # # given as the signatures argument are correct
    for i in range(10):
        if sigdata[i][0] != 0:
            # If an invalid signature is given for an owner then the contract throws
            assert ecrecover(message_to_be_signed, sigdata[i][0], sigdata[i][1], sigdata[i][2]) == self.owners[i], 'signature invalid'
            # For every valid signature increase the number of approvals by 1
            approvals += 1
    # Throw if the number of approvals is less then the number of approvals required (the threshold)
    assert approvals >= self.threshold
    # The transaction has been approved
    # Increase the number of approved transactions by 1
    self.nonce += 1
    # Use raw_call to send the transaction
    return raw_call(_to, _data, max_outsize=4096, value=_value)
