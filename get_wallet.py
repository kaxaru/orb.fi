import os
from web3 import Web3
from config import get_default_provider

def get_main_wallet():
    with open(f'{os.path.dirname(__file__)}/wallets/wallet.txt', 'r') as file:
        _main_wallet = [row.strip() for row in file]
    return _main_wallet

def get_addresses():
    with open(f'{os.path.dirname(__file__)}/wallets/addresses.txt', 'r') as file:
        _addresses = [row.strip() for row in file]
    return _addresses

def get_all_wallets(list):
    default_provider = get_default_provider()
    web3 = Web3(Web3.HTTPProvider(default_provider['provider']['rpc']))
    web3.eth.account.enable_unaudited_hdwallet_features()
    _wallets = []
    for wallet in list:
        if len(wallet) == 0:
            continue
        if len(wallet) == 64:
            cWallet = web3.eth.account.from_key(wallet)

            _wallets.append({'wallet': cWallet})
        else:
            wallet_format = wallet.split(';')
            if len(wallet_format) == 2:
                num_of_wallet = wallet_format[1]
            elif len(wallet_format) == 3:
                _indexes = wallet_format[2].split(',')
                indexes = []
                for _ind in _indexes:
                    if _ind == '':
                        continue
                    if len(_ind) > 1 and len(_ind.split('-')) == 2:
                        els = _ind.split('-')
                        _start = int(els[0])
                        _finish = int(els[1]) + 1
                        for i in range(_start, _finish):
                            indexes.append(i)
                    else:
                        indexes.append(int(_ind))
            else:
                num_of_wallet = 100
            cWallet = wallet_format[0]
            if len(wallet_format) == 3:
                num_of_wallet = indexes[len(indexes) - 1]
                _all_wallets = []
                for i in range(int(num_of_wallet)):
                    wallet_address = web3.eth.account.from_mnemonic(cWallet, account_path=f"m/44'/60'/0'/0/{i}")

                    _all_wallets.append({'wallet': wallet_address})
                _new_wallets = []
                for el in indexes:
                    _new_wallets.append(_all_wallets[el - 1])
                [_wallets.append(_new) for _new in _new_wallets]
            else:
                for i in range(int(num_of_wallet)):
                    wallet_address = web3.eth.account.from_mnemonic(cWallet, account_path=f"m/44'/60'/0'/0/{i}")

                    _wallets.append({'wallet': wallet_address})

    return _wallets
