from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
accounts = w3.eth.accounts
artifact = 'Enabling_Reliable_Keyword_Search'
fn_abi = 'D:\pythonProject/{0}.abi'.format(artifact)
fn_bin = 'D:\pythonProject/{0}.bin'.format(artifact)
fn_addr = 'D:\pythonProject/{0}.addr'.format(artifact)

with open(fn_abi,'r') as f:
  abi = json.load(f)
with open(fn_bin,'r') as f:
  bin = f.read()
factory = w3.eth.contract(abi=abi,bytecode=bin)
tx_hash = factory.constructor().transact({'from':accounts[0]})
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(receipt)
with open(r'D:\pythonProject\addr.txt','w') as f:
  f.write(receipt.contractAddress)
