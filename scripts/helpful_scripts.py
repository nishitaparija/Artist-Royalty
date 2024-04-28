from brownie import accounts, network, config

# Forks the main Ethereum blockchain using Infura to interact with it locally: brownie networks add development
# brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1
# fork="https://mainnet.infura.io/v3/$WEB3_INFURA_PROJECT_ID" accounts=10 mnemonic=brownie port=8545

# to fork using Alchemy: create app with development environment, chain Ethereum, and network mainnet run the
# following command: brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1
# fork="https://eth-mainnet.alchemyapi.io/v2/9LK......" accounts=10 mnemonic=brownie port=Port where Ganache is running

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev", "matic-fork", "matic-fork-dev"]

# Add custom ganache chain running locally:
# brownie networks add Ethereum ganache-local host=http://127.0.0.1:7545 chainid=5777
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "hardhat", "ganache"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS \
            or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        # Using local account that Brownie automatically spins in Ganache
        account = accounts[0]

    elif network.show_active() in config["networks"]:
        account = accounts.add(config["wallets"]["from_key"])

    else:
        # using account added to Brownie with: brownie accounts new name_of_account
        # it will password encrypt the key
        # to list all the accounts: brownie accounts list
        # to delete: brownie accounts delete name_of_account
        account = accounts.load("testing")

        # Another option to import private key using the .env file with the .yaml file
        # account = accounts.add(config['wallet']['from_key'])

    return account
