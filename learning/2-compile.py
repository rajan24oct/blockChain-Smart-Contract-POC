from solc import compile_files

sols = ['1-shipment.sol']

compliled_contract = compile_files(sols)

print("CONTRACT")
print(compliled_contract)
print("==============================END====================================")
