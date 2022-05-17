from tool.client import Client, ConnectionType
from tool.helper import convert_value_to_ether

client = Client()

mongodb_client = client.get_mongodb_client(ConnectionType.remote)
w3_client = client.get_main_net_web3_client()

db = mongodb_client.etherium
transactions_collection = db.transactions

f = open("block_number.txt", "r")
current_block_number = int(f.read())
main_net_block_number = w3_client.eth.get_block_number()
i = current_block_number

while i < main_net_block_number:
    for j in range(i, w3_client.eth.get_block_number()):
        block = w3_client.eth.get_block(i, True)
        transactions = block.get('transactions') if block else []
        if transactions:
            transactions_list = list(map(lambda x: dict(x), transactions))
            transactions_list = list(map(lambda x: convert_value_to_ether(w3_client, x), transactions_list))
            transactions_collection.insert_many(transactions_list)
