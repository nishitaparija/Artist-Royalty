from brownie import IPEntity, MCOContract, NFToken, network, config
from scripts.helpful_scripts import get_account
from web3 import Web3
import time
import json

with open('./metadata/mco_example.json') as f:
    mcoCont = json.load(f)

with open('./metadata/bindings.json') as f:
    accounts = json.load(f)

# Convert accounts to tuple
accounts = tuple(accounts.values())


def mint(token, alice, deontics):
    owner = get_account()

    print(f"Minting token with deontics: {deontics} to {alice}")

    resTok = token.newToken(alice, deontics, {"from": owner})

    time.sleep(1)

    print("Waiting for transaction to be mined...")
    resTok.wait(1)

    print("Minting complete")

    return resTok


def deploy(mcoCont):
    owner = get_account()

    # owner = accounts[0]
    # Set the owner of the NFT contract on Ripple EVM sidechain
    alice = "0x6CE64fd11f85EFaA4c02993412e62fe7641603D0"

    partiesAcc = list(accounts[2:2 + len(mcoCont['parties'])])

    # Deploy the token contract
    token = NFToken.deploy("MultiMediaContract", "MCO", {'from': owner})

    print("Deployed NFT Contract address:", token.address)

    # Mint the token
    print("Minting token...")
    deontics = [{item[0]:item[1]} for item in mcoCont['deontics'].items()]
    resTok = mint(token, alice, deontics[0])

    # Get the token id
    print("Transaction logs: ", resTok.logs)
    TokenIdHex = resTok.logs[0].topics[-1]

    print("TokenIdHex:", TokenIdHex)

    # Convert the token id hex to int
    tokenId = int.from_bytes(TokenIdHex, byteorder='big', signed=False)

    print("TokenId:", tokenId)

    dlist = [tokenId]

    # Get the object id
    olist = [Web3.toBytes(2)]

    # Get the performing rights organization wallet address:
    # PROs are responsible for collecting income on behalf of
    # songwriters and music publishers when a song is publicly broadcast or performed
    relatContList = [accounts[0]]

    #
    relationsList = [Web3.toBytes(1)]

    incomeBeneficiariesList = [
        accounts[2],
        accounts[4],
        accounts[5],
        accounts[3],
        accounts[6],
    ]

    # Not accounted for in the incomeBeneficiariesList:
    # StreamingService = 10%
    # incomePercentagesList = [
    #     Web3.toBytes(2),  # 2%
    #     Web3.toBytes(1),  # 1%
    #     Web3.toBytes(50),  # 50%
    #     Web3.toBytes(1),  # 1%
    #     Web3.toBytes(20),  # 20%
    # ]

    incomePercentagesList = [
        30,  # 30%
        5,  # 5%
        50,  # 50%
        5,  # 5%
        10,  # 10%
    ]

    # The content URI is a string of the contract metadata
    contentUri = json.dumps(mcoCont)

    # The content hash is the hash of the content URI or in this case, the contract metadata
    contentHash = Web3.toBytes(text=contentUri)

    contract_deployed = MCOContract.deploy(Web3.toBytes(text='identifier'),  # identifier
                                           partiesAcc,
                                           token.address,
                                           dlist,
                                           olist,
                                           relatContList,
                                           relationsList,
                                           incomeBeneficiariesList,
                                           incomePercentagesList,
                                           contentUri,
                                           contentHash,
                                           {'from': owner})

    # RPC is sometimes killed too quick, resulting in brownie.exceptions.RPCRequestError: Web3 is not connected
    # This is a known issue, and is fixed by waiting a few seconds
    # https://github.com/smartcontractkit/full-blockchain-solidity-course-py/issues/173
    time.sleep(1)
    contract_address = contract_deployed.address
    print("Contract address:", contract_address)

    # a = cont.getDeonticExpressions()
    # b = contract_deployed.getIncomePercentagesBy(accounts[2])
    # print(b)

    return contract_deployed


def main(deploy_contract=False):
    # account = get_account()

    # price feed address of Chain link
    print("Deploying in the network:", network.show_active())

    # To use the latest version of the deployed contract
    if deploy_contract:
        contract_deployed = deploy(mcoCont)
