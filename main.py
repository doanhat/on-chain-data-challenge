import json
from abc import ABC
from typing import Optional

from dotenv import *
from web3 import Web3


class Currency(ABC):
    pass


class FiatCurrency(Currency):
    USD = 'USD'


class Asset:
    def __init__(self, symbol: Currency, quantity):
        self.symbol = symbol
        self.quantity = quantity


class Transaction:
    def __init__(self, out_address, in_address, amount: Asset):
        self.out_address = out_address
        self.in_address = in_address
        self.amount = amount


def get_pair(symbol, currency):
    return 1


class Wallet:
    def __init__(self, address, token_balance: Optional[list[Asset]] = None,
                 transactions: Optional[list[Transaction]] = None):
        self.address = address
        self.token_balance = token_balance
        self.transactions = transactions

    def get_balance(self, currency: Currency):
        return sum([a.quantity * get_pair(a.symbol, currency) for a in self.token_balance])

    def get_token_balance(self, currency: Currency):
        portfolio = {}
        balance = self.get_balance(currency)
        for a in self.token_balance:
            value = a.quantity * get_pair(a.symbol, currency)
            portfolio[a.symbol] = {
                'value': value,
                'allocation': value / balance * 100
            }
        return portfolio

    def update_token_balance(self):
        for t in self.transactions:
            pass


def convert_value_to_ether(w3_client: Web3, transaction):
    transaction['value'] = float(w3_client.fromWei(transaction['value'], 'ether'))
    return transaction


def get_wallet_balance(w3_client: Web3, wallet_address: str) -> object:
    return w3_client.fromWei(w3_client.eth.get_balance(wallet_address), 'ether')


def get_wallet_token_balance(w3_client: Web3, wallet_address: str, contract_address: str, abi: str):
    try:
        contract = w3_client.eth.contract(address=contract_address, abi=abi)
        symbol = contract.functions.symbol().call()
        balance = contract.functions.balanceOf(wallet_address).call()
        return {
            symbol: balance
        }
    except Exception:
        raise


if __name__ == '__main__':
    # Load config
    config = dotenv_values(".env")

    # HTTPProvider:
    w3 = Web3(Web3.HTTPProvider(config.get("INFURA_URL")))

    wallet_adr = '0x2C0bAdC1679FB7666E4705Ef3c0084654bc81673'
    contract_adr = '0xC13eac3B4F9EED480045113B7af00F7B5655Ece8'
    abi = json.loads(
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{'
        '"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,'
        '"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256",'
        '"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{'
        '"indexed":true,"internalType":"address","name":"delegator","type":"address"},{"indexed":true,'
        '"internalType":"address","name":"delegatee","type":"address"},{"indexed":false,"internalType":"enum '
        'IGovernancePowerDelegationToken.DelegationType","name":"delegationType","type":"uint8"}],'
        '"name":"DelegateChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,'
        '"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256",'
        '"name":"amount","type":"uint256"},{"indexed":false,"internalType":"enum '
        'IGovernancePowerDelegationToken.DelegationType","name":"delegationType","type":"uint8"}],'
        '"name":"DelegatedPowerChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,'
        '"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address",'
        '"name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],'
        '"name":"Transfer","type":"event"},{"inputs":[],"name":"DELEGATE_BY_TYPE_TYPEHASH","outputs":[{'
        '"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"DELEGATE_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{'
        '"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"EIP712_REVISION","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{'
        '"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"REVISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"_aaveGovernance","outputs":[{'
        '"internalType":"contract ITransferHook","name":"","type":"address"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"_nonces",'
        '"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},'
        '{"internalType":"uint256","name":"","type":"uint256"}],"name":"_votingSnapshots","outputs":[{'
        '"internalType":"uint128","name":"blockNumber","type":"uint128"},{"internalType":"uint128","name":"value",'
        '"type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"","type":"address"}],"name":"_votingSnapshotsCounts","outputs":[{"internalType":"uint256","name":"",'
        '"type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],'
        '"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender",'
        '"type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender",'
        '"type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],'
        '"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatee",'
        '"type":"address"}],"name":"delegate","outputs":[],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"delegatee","type":"address"},{"internalType":"uint256",'
        '"name":"nonce","type":"uint256"},{"internalType":"uint256","name":"expiry","type":"uint256"},'
        '{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},'
        '{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"delegateBySig","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatee",'
        '"type":"address"},{"internalType":"enum IGovernancePowerDelegationToken.DelegationType",'
        '"name":"delegationType","type":"uint8"}],"name":"delegateByType","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatee",'
        '"type":"address"},{"internalType":"enum IGovernancePowerDelegationToken.DelegationType",'
        '"name":"delegationType","type":"uint8"},{"internalType":"uint256","name":"nonce","type":"uint256"},'
        '{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v",'
        '"type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s",'
        '"type":"bytes32"}],"name":"delegateByTypeBySig","outputs":[],"stateMutability":"nonpayable",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"delegator","type":"address"},'
        '{"internalType":"enum IGovernancePowerDelegationToken.DelegationType","name":"delegationType",'
        '"type":"uint8"}],"name":"getDelegateeByType","outputs":[{"internalType":"address","name":"",'
        '"type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address",'
        '"name":"user","type":"address"},{"internalType":"uint256","name":"blockNumber","type":"uint256"},'
        '{"internalType":"enum IGovernancePowerDelegationToken.DelegationType","name":"delegationType",'
        '"type":"uint8"}],"name":"getPowerAtBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user",'
        '"type":"address"},{"internalType":"enum IGovernancePowerDelegationToken.DelegationType",'
        '"name":"delegationType","type":"uint8"}],"name":"getPowerCurrent","outputs":[{"internalType":"uint256",'
        '"name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue",'
        '"type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"initialize","outputs":[],'
        '"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{'
        '"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{'
        '"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender",'
        '"type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256",'
        '"name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},'
        '{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s",'
        '"type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],'
        '"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{'
        '"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},'
        '{"inputs":[{"internalType":"uint256","name":"blockNumber","type":"uint256"}],"name":"totalSupplyAt",'
        '"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view",'
        '"type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},'
        '{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{'
        '"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},'
        '{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address",'
        '"name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],'
        '"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],'
        '"stateMutability":"nonpayable","type":"function"}]'
    )
    b = get_wallet_balance(w3, wallet_adr)
    tb = get_wallet_token_balance(w3, wallet_adr, contract_adr, abi)
    print("--")
