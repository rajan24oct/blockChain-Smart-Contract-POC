import pickle
from web3 import Web3
from solc import compile_files, link_code
import settings

# web3.py instance
w3 = Web3(Web3.HTTPProvider(settings.ETH_URL))


class BCProcessor:

    file_path = ""

    def __init__(self, file_path):
        self.file_path = file_path


    def separate_main_n_link(self, contracts):
        # separate out main file and link files
        # assuming first file is main file.
        main = {}
        link = {}

        all_keys = list(contracts.keys())
        for key in all_keys:
            if self.file_path[0] in key:
                main = contracts[key]
            else:
                link[key] = contracts[key]
        return main, link


    def deploy_contract(self, contract_interface):
        # Instantiate and deploy contract
        contract = w3.eth.contract(
            abi=contract_interface['abi'], bytecode=contract_interface['bin'])

        # Get transaction hash from deployed contract
        tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[1]})

        # Get tx receipt to get contract address
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)

        return tx_receipt['contractAddress']


    def deploy_n_transact(self, mappings=[]):
        # compile all files
        contracts = compile_files(self.file_path, import_remappings=mappings)
        link_add = {}
        contract_interface, links = self.separate_main_n_link(contracts)
        # first deploy all link libraries
        for link in links:
            link_add[link] = self.deploy_contract(links[link])
            # now link dependent library code to main contract binary
        # https://solidity.readthedocs.io/en/v0.4.24/using-the-compiler.html?highlight=library
        if link_add:
            contract_interface['bin'] = link_code(contract_interface['bin'], link_add)
            # return contract receipt and abi(application binary interface)
        return self.deploy_contract(contract_interface), contract_interface['abi']