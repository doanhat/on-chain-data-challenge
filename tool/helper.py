from web3 import Web3


def convert_value_to_ether(w3_client: Web3, transaction):
    transaction['value'] = float(w3_client.fromWei(transaction['value'], 'ether'))
    return transaction
