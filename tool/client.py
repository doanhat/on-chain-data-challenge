from pymongo import MongoClient
from web3 import Web3

from tool.config import CONFIG


class ConnectionType:
    remote = "REMOTE"
    local = "LOCAL"


class Client:
    def __init__(self):
        self.config = CONFIG

    def get_mongodb_client(self, connect_type: ConnectionType):
        if connect_type == ConnectionType.remote:
            return MongoClient(
                f"mongodb+srv://{self.config.get('USERNAME')}:{self.config.get('PASSWORD')}@{self.config.get('DOMAIN')}/"
                f"{self.config.get('DATABASE_NAME')}?retryWrites=true&w=majority")
        else:
            return MongoClient(port=self.config.get('PORT'))

    def get_main_net_web3_client(self):
        return Web3(Web3.HTTPProvider(self.config.get("INFURA_URL")))
