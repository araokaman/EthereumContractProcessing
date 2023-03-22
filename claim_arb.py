import time
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

# 事前準備
eth_url = 'YOUR_ETHEREUM_NODE_URL'  # 例: InfuraのEthereumノードURL
private_key = 'YOUR_PRIVATE_KEY'
public_key = 'YOUR_PUBLIC_KEY'

w3 = Web3(HTTPProvider(eth_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # POAチェーンの場合は必要

# スマートコントラクトのABI (Application Binary Interface)
contract_abi = [{"inputs":[{"internalType":"contract IERC20VotesUpgradeable","name":"_token","type":"address"},{"internalType":"address payable","name":"_sweepReceiver","type":"address"},{"internalType":"address","name":"_owner","type":"address"},{"internalType":"uint256","name":"_claimPeriodStart","type":"uint256"},{"internalType":"uint256","name":"_claimPeriodEnd","type":"uint256"},{"internalType":"address","name":"delegateTo","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"CanClaim","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"HasClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"newSweepReceiver","type":"address"}],"name":"SweepReceiverSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Swept","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"recipient","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdrawal","type":"event"},{"inputs":[],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"delegatee","type":"address"},{"internalType":"uint256","name":"expiry","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"claimAndDelegate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimPeriodEnd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"claimPeriodStart","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"claimableTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_recipients","type":"address[]"},{"internalType":"uint256[]","name":"_claimableAmount","type":"uint256[]"}],"name":"setRecipients","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address payable","name":"_sweepReceiver","type":"address"}],"name":"setSweepReciever","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sweep","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"sweepReceiver","outputs":[{"internalType":"address payable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"token","outputs":[{"internalType":"contract IERC20VotesUpgradeable","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalClaimable","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]  # スマートコントラクトのABIをここに入れてください

# コントラクトアドレスとABIを設定する
contract_address = '0x67a24ce4321ab3af51c2d0a4801c3e111d88c9d9'
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# トランザクションのガス価格とガスリミットを設定する
gas_price = w3.eth.gasPrice
gas_limit = 210000

# イーサリアムのブロック生成を監視する
target_block_number = 16890400
while True:
    current_block_number = w3.eth.blockNumber
    print(f'Current block number: {current_block_number}')
    if current_block_number >= target_block_number:
        break
    time.sleep(10)

# Claimスマートコントラクトを実行する
nonce = w3.eth.getTransactionCount(public_key)

transaction = {
    'to': contract_address,
    'from': public_key,
    'gas': gas_limit,
    'gasPrice': gas_price,
    'nonce': nonce,
}

claim_function = contract.functions.claim()
transaction.update(claim_function.as_dict())
transaction['data'] = claim_function.buildTransaction({'gas': gas_limit, 'gasPrice': gas_price, 'nonce': nonce})['data']

signed_transaction = w3.eth.account.signTransaction(transaction, private_key)
transaction_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

# トランザクションの完了を待つ
w3.eth.waitForTransactionReceipt(transaction_hash)

# 完了メッセージを表示する
print('Claim process has completed.')
