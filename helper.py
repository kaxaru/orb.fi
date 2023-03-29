import os
import json

def load_contract(web3, abi_name, address):
    address = web3.toChecksumAddress(address)
    return web3.eth.contract(address=address, abi=_load_abi(abi_name))

def _load_abi(name):
        path = f"{os.path.dirname(os.path.abspath(__file__))}/assets/"
        with open(os.path.abspath(path + f"{name}.abi")) as f:
            abi: str = json.load(f)
        return abi