import traceback

from web3 import Web3
import json
import os
from loguru import logger
import functools
import time
import random

from functools import partial
from enum import Enum

USER_GAS_PRICE = 25

RPCS = {
    'ethereum' : {'chain': 'ETHEREUM', 'chain_id': 10, 'rpc': 'https://rpc.ankr.com/eth', 'scan': 'https://etherscan.io/tx', 'token': 'ETH'},

    'optimism' : {'chain': 'OPTIMISM', 'chain_id': 10, 'rpc': 'https://1rpc.io/op', 'scan': 'https://optimistic.etherscan.io/tx', 'token': 'ETH'},

    'bsc' : {'chain': 'BSC', 'chain_id': 56, 'rpc': 'https://rpc.ankr.com/bsc', 'scan': 'https://bscscan.com/tx', 'token': 'BNB'},

    'polygon' : {'chain': 'MATIC', 'chain_id': 137, 'rpc': 'https://polygon-rpc.com', 'scan': 'https://polygonscan.com/tx', 'token': 'MATIC'},

    'arbitrum' : {'chain': 'ARBITRUM', 'chain_id': 42161, 'rpc': 'https://rpc.ankr.com/arbitrum', 'scan': 'https://arbiscan.io/tx', 'token': 'ETH'},

    'avaxc' : {'chain': 'AVAXC', 'chain_id': 43114, 'rpc': 'https://rpc.ankr.com/avalanche', 'scan': 'https://snowtrace.io/tx', 'token': 'AVAX'},

    'fantom' : {'chain': 'FANTOM', 'chain_id': 250, 'rpc': 'https://rpc.ankr.com/fantom', 'scan': 'https://ftmscan.com/tx', 'token': 'FTM'},

    'celo' : {'chain': 'CELO', 'chain_id': 42220, 'rpc': 'https://rpc.ankr.com/celo', 'scan': 'https://celoscan.io/tx', 'token': 'CELO'},

    'harmony' : {'chain': 'HARMONY', 'chain_id': 1666600000, 'rpc': 'https://api.harmony.one', 'scan': 'https://explorer.harmony.one/tx', 'token': 'Harmony'},

    'xDai' : {'chain': 'xDai', 'chain_id': 100, 'rpc': 'https://rpc.ankr.com/gnosis', 'scan': 'https://blockscout.com/xdai/mainnet/tx', 'token': 'xDai'},

    'era' : {'chain': 'Era', 'chain_id': 324, 'rpc': 'https://zksync.meowrpc.com', 'scan': 'https://explorer.zksync.io/tx', 'token': 'ETH'}
}


def load_contract(web3, abi_name, address):
    address = web3.toChecksumAddress(address)
    return web3.eth.contract(address=address, abi=_load_abi(abi_name))

def _load_abi(name):
        path = f"{os.path.dirname(os.path.abspath(__file__))}/assets/"
        with open(os.path.abspath(path + f"{name}.abi")) as f:
            abi: str = json.load(f)
        return abi

class RollupChain(Enum):
    optimism = 1
    arbitrum = 2
    era = 3
    ethereum = 4

class NotEip1559(Enum):
    optimism = 1
    bsc = 2
    fantom = 3
    harmony = 4


def estimateFasPrise(w3, tx):
    errors = {}

    provider = w3.provider.endpoint_uri
    for chain in RPCS:
        if RPCS[chain]['rpc'] == provider:
            native_token = RPCS[chain]["token"]

    is_prise_cost = False
    attempts = 5
    while not is_prise_cost:
        try:
            if 'gasPrice' in tx and  type(tx["gasPrice"]).__name__ == 'float':
                tx.update({'gasPrice': int(tx["gasPrice"])})
            if 'maxFeePerGas' in tx and type(tx['maxFeePerGas']).__name__ == 'float':
                tx.update({'maxFeePerGas': int(tx["maxFeePerGas"])})
            if 'maxPriorityFeePerGas' in tx and type(tx['maxPriorityFeePerGas']).__name__ == 'float':
                tx.update({'maxPriorityFeePerGas': int(tx["maxPriorityFeePerGas"])})
            gasLimit = w3.eth.estimateGas(tx)
            tx.update({'gas': int(gasLimit * 11 / 10)})
            is_prise_cost = True
        except Exception as e:
            errors = e
            logger.info(e)
            if type(e).__name__ == 'ValueError' and 'message' in e.args[0] and e.args[0]["message"] == "insufficient funds for transfer":
                logger.info(f'not enough balance on wallet - {native_token}')
                break
            logger.info('timeout 1 sec')
            time.sleep(1)
            attempts -=1
            if attempts == 0:
                break

    return {'tx': tx, 'errors': errors}

def load_contract(web3, abi_name, address):
    address = web3.toChecksumAddress(address)
    return web3.eth.contract(address=address, abi=_load_abi(abi_name))

def _load_abi(name):
        path = f"{os.path.dirname(os.path.abspath(__file__))}/assets/"
        with open(os.path.abspath(path + f"{name}.abi")) as f:
            abi: str = json.load(f)
        return abi

def is_gasL1_low():
    w3 = Web3(Web3.HTTPProvider(RPCS["ethereum"]["rpc"]))
    while True:
        gasPrice = Web3.fromWei(w3.eth.gasPrice, 'gwei')
        if gasPrice > USER_GAS_PRICE:
            logger.info(f'gas in ethereum to high - {gasPrice}, sleep 30s')
            time.sleep(30)
        else:
            break

def get_tx_type(c_chain, func_type, params, wallet, to, tx_data):
    notEip_chains = list(NotEip1559)
    _gasPrice = params["gasPrice"]
    function = params["function"]
    w3 = params["w3"]
    nonce = params["nonce"]
    is_not_eip = False
    for _ch in notEip_chains:
        if func_type:
            if c_chain.lower() == _ch.name.lower():
                is_not_eip = True
                break

    if is_not_eip:
        tx = {
            'chainId': w3.eth.chain_id,
            'from': Web3.toChecksumAddress(wallet.address),
            'gas': 0,
            'gasPrice': w3.eth.gasPrice,
            'nonce': nonce,
        }
    else:
        tx = {
            'chainId': w3.eth.chain_id,
            'from': Web3.toChecksumAddress(wallet.address),
            'gas': 0,
            # 'gasPrice': w3.eth.gasPrice,
            'maxFeePerGas': int(_gasPrice * 1.1),
            'maxPriorityFeePerGas': _gasPrice,
            'nonce': nonce,
        }

    if func_type:
        tx_func = function.buildTransaction(tx)
    else:
        tx_func = tx
        tx_func.update({'to': to})
        if tx_data != None:
            tx_func.update({'data': tx_data})

    return tx_func

class Transaction:
    @staticmethod
    def build_transaction(function, w3, wallet, chain, log_value, value = 0):
        to_address = None
        if function == None:
            try:
                if 'cex_address' in wallet:
                    to_address = Web3.toChecksumAddress(wallet["cex_address"])
                    tx_data = None
                else:
                    to_address = Web3.toChecksumAddress(wallet["to_address"])
                    tx_data = wallet["tx_data"]

                wallet = wallet["wallet"]

            except Exception as e:
                logger.error(e)
        else:
            to_address = Web3.toChecksumAddress(wallet.address)

        nonce = w3.eth.get_transaction_count(wallet.address)
        rollup_chain = list(RollupChain)
        if chain.lower() in [chain.name for chain in rollup_chain]:
            is_gasL1_low()

        logger.info(f'base {w3.eth.gasPrice} --fee {w3.eth.gas_price}')
        _gasPrice = int(w3.eth.gasPrice)

        func_type = False
        if function != None:
            func_type = True


        tx_params = {
            "gasPrice": _gasPrice,
            "function": function,
            "w3": w3,
            "nonce": nonce
        }

        tx = get_tx_type(chain, func_type, tx_params, wallet, to_address, tx_data)

        if value > 0:
            tx.update({'value': value})
        isValid_tx = estimateFasPrise(w3, tx)
        if bool(isValid_tx["errors"]):
            return {"transaction_status": False, 'errors': isValid_tx["errors"]}

        signed_txn = w3.eth.account.sign_transaction(tx, private_key=wallet.privateKey)
        tx_token = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        logger.info(f'{log_value[0]}{w3.toHex(tx_token)} {log_value[1]}')
        task_timeout('_task')
        try:
            tx_log = w3.eth.wait_for_transaction_receipt(tx_token, timeout=6000)
            if tx_log['status'] == 1:
                return {"transaction_status": True, 'errors': isValid_tx["errors"]}
            else:
                return {"transaction_status": False, 'errors': isValid_tx["errors"]}
        except Exception as e:
            logger.info('timeout approve')

def is_approved(w3, address, token_spender, token, limit, type_token):
    amount = (
             load_contract(w3, type_token, token)
            .functions.allowance(address, token_spender)
            .call()
    )
    if type(limit) != None:
        max_approval_check_int = limit
    else:
        max_approval_check_hex = f"0x{15 * '0'}{49 * 'f'}"
        max_approval_check_int = int(max_approval_check_hex, 16)

    if amount >= max_approval_check_int:
        return True
    else:
        return False

def approve(w3, wallet, token, token_spender, max_approval, type, chain):
    max_approval_int = int(f"0x{64 * 'f'}", 16)
    max_approval = max_approval_int if not max_approval else max_approval

    function = load_contract(w3, type, token).functions.approve(
        token_spender, max_approval
    )
    logger.warning(f"Approving {token}...")
    nonce = w3.eth.get_transaction_count(Web3.toChecksumAddress(wallet.address))
    logger.info(f'nonce - {nonce}')
    log_value = [ f'\n>>> approve {RPCS[chain]["scan"]}/', f'amount - {max_approval}']
    Transaction.build_transaction(function, w3, wallet, chain ,log_value)

def check_approval(method):
    @functools.wraps(method)
    def approved(wallet, w3, *args, **kwargs):
        token = args[0] if args[0] != ETH else None
        token_spender = args[1] if args[1] != ETH else None
        max_approval = args[2] if type(args[2]) == int else None
        amount = args[3]
        type_token = args[4] if type(args[4]) != None else None
        chain = args[5] if args[5] != None else 'ethereum'

        _new = [_arg for idx, _arg in enumerate(args) if idx > 5]

        if token:
            _is_approved = is_approved(w3, Web3.toChecksumAddress(wallet.address) ,Web3.toChecksumAddress(token_spender), token, max_approval, type_token)
            if not _is_approved:
                approve(w3, wallet, token, token_spender, max_approval, type_token, chain)

        return method(wallet, w3, token, token_spender, max_approval, amount, type_token, chain, _new)

    return approved

def task_timeout(_t = 'gl_task'):
    if _t == 'gl_task':
        t_sl = random.randint(30, 60)
    else:
        t_sl = random.randint(15, 25)

    logger.info(f'task break - {t_sl} second')
    time.sleep(t_sl)


def logger_wrapper(func):
    @functools.wraps(func)
    def logger_func(*args, **kwargs):
        try:
            logger.info(f'launch - {func.__name__}')
            func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
    return logger_func


def logger_wrapper_record(func):
    @functools.wraps(func)
    def logger_func(*args, **kwargs):
        try:
            logger.info(f'launch - {func.__name__}')
            wallet = args[0]
            wallets_with_res = []
            if os.path.exists(f'logs/{func.__name__}.txt'):
                with open(f'logs/{func.__name__}.txt', 'r') as file:
                    wallets_with_res = [row.strip() for row in file]
            for _w in wallets_with_res:
                if _w == wallet["wallet"].address:
                    logger.info(f'current address {_w} has already done the task')
                    if func.__name__ == 'task_bridge':
                        return 0
                    else:
                        return None
            value = func(*args, **kwargs)
            with open(f'logs/{func.__name__}.txt', 'a+') as file:
                file.write(f'{wallet["wallet"].address}\n')
        except Exception as e:
            logger.error(traceback.format_exc())
            return None
        return value
    return logger_func

