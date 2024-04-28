from brownie import MCOContract, NFToken, network, config
from scripts.helpful_scripts import get_account
import json
import os


def main():
    with open('./metadata/bindings.json') as f:
        accounts = json.load(f)

    # Convert accounts to tuple
    accounts = tuple(accounts.values())

    owner = get_account()
    # owner = "0x6CE64fd11f85EFaA4c02993412e62fe7641603D0"

    print("Owner:", owner)

    # Interact with latest deployed contracts
    MCO_Contract = MCOContract[-1]
    tokens = NFToken[-1]

    # Get the owner of the token
    owner_token = tokens.ownerOf(1)
    print("The owner of the token is:", owner_token)

    # Get the income percentages of a party
    percentage = MCO_Contract.getIncomePercentage(accounts[5], {'from': owner})
    print("Income percentages of party:", percentage)

    # Get the income owned to a party
    income = MCO_Contract.getIncomeOwned(accounts[5], {'from': owner})
    print("Income owned to party:", income)

    # # Update the amount to be paid to the parties
    # MCO_Contract.updateIncomeOwned(100, {'from': owner, "gasLimit": 2588199})
    # print("Income received from PerformingRighthsOrganisation for 100 XRP")

    # # Get the income owned to a party
    # income = MCO_Contract.getIncomeOwned(accounts[5], {'from': owner})
    # print("Income owned to party:", income)

    # Reduce the income owned to a party
    MCO_Contract.reduceIncomeOwned(accounts[5], 50, {'from': owner, "gasLimit": 2588199})

    # Get the income owned to a party
    income = MCO_Contract.getIncomeOwned(accounts[5], {'from': owner})
    print("Income owned to party:", income)

    # # Get the income owned to a party
    # income = MCO_Contract.getIncomeOwned(accounts[3], {'from': owner})
    # print("Income owned to party:", income)

    # # Get all the parties of the contract
    # parties = MCO_Contract.getParties({'from': owner})
    # print("Parties of the contract:", parties)

    # # Get the Contract Relations
    # relations = MCO_Contract.getContractRelations()
    # print("Relations of the contract:", relations)
    #
    # # Get the deontics of the token
    # deontics = MCO_Contract.getDeonticExpressions()
    # print("Deontics of the token:", deontics)

    # # Determine the percentage to pay to a party based on the income percentages
    # amount_to_pay = MCO_Contract.payTo(accounts[3], 100)
    # print("Amount to pay to party:", amount_to_pay)

