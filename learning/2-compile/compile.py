from solc import compile_files


def separate_main_n_link(sols, contracts):
    # separate out main file and link files
    # assuming first file is main file.
    main = {}
    link = {}

    all_keys = list(contracts.keys())
    for key in all_keys:
        if sols[0] in key:
            main = contracts[key]
        else:
            link[key] = contracts[key]
    return main, link


sols = ['sols/shipment.sol', 'sols/stringUtils.sol']

contracts = compile_files(sols)

contract_interface, links = separate_main_n_link(sols, contracts)

print("MAIN CONTRACT")
print(contract_interface)
print("==============================END====================================")
print("LINK CONTRACTS")
print(links)
print("==============================END====================================")
