import random
import time
from decimal import Decimal
from web3 import Web3
from loguru import logger
from get_wallet import get_main_wallet, get_all_wallets
from config import ERC20_ABI, contract_stable, default_gasPrice
from config import usdc_orbiter, usdt_orbiter, eth_orbiter, dai_orbiter, network_code
from config import sourthmap_currency, get_current_provider
from config import transfer_limit

from multiprocessing.dummy import Pool

def get_balance(chain, type_currency, contract_stable_instance = None, web3 = None):
    if type_currency != 'eth':
        balance = contract_stable_instance.functions.balanceOf(wallet['wallet'].address).call()
        logger.info(f'wallet balance - {Web3.fromWei(balance, "mwei")}')
    else:
        if chain == 'bsc' or chain == 'matic':
            balance = contract_stable_instance.functions.balanceOf(wallet['wallet'].address).call()
        else:
            balance = web3.eth.get_balance(wallet['wallet'].address)
        logger.info(f'wallet balance - {Web3.fromWei(balance, "ether")}')
    return balance


def bridge(user_info):
    wallet = user_info['wallet']
    provider_info = get_current_provider(user_info['chain_current'])
    web3 = Web3(Web3.HTTPProvider(provider_info['rpc']))
    code = network_code[user_info['code']]
    if type_currency != 'eth':
        contract_stable_address = contract_stable[user_info['chain_current']][user_info['type_currency']]
        contract_stable_instance = web3.eth.contract(Web3.toChecksumAddress(contract_stable_address), abi=ERC20_ABI)
        if type_currency == 'usdc' or type_currency == 'usdt':
            amount = web3.toWei(Decimal(user_info['amount']), 'mwei') // 10000 * 10000 + code
        else:
            amount = web3.toWei(Decimal(user_info['amount']), 'ether') // 10000 * 10000 + code

        if type_currency == 'usdc':
            address_to = usdc_orbiter
        elif type_currency == 'usdt':
            address_to = usdt_orbiter
        elif type_currency == 'dai':
            address_to = dai_orbiter

    else:
        if user_info['chain_current'] == 'bsc' or user_info['chain_current'] == 'matic':
            contract_stable_address = contract_stable[user_info['chain_current']][user_info['type_currency']]
            contract_stable_instance = web3.eth.contract(Web3.toChecksumAddress(contract_stable_address), abi=ERC20_ABI)
        else:
            contract_stable_instance = None
        address_to = eth_orbiter
        amount =web3.toWei(Decimal(user_info['amount']), 'ether') // 10000 * 10000 + code

    nonce = web3.eth.get_transaction_count(wallet['wallet'].address)
    for tx in enumerate(range(user_info['trx_count'])):
        balance = get_balance(user_info['chain_current'], user_info['type_currency'], contract_stable_instance, web3)
        logger.info(f'transaction number - {nonce}')
        if balance > amount:
            contract_txn = contract_stable_instance.functions.transfer(Web3.toChecksumAddress(address_to), amount).buildTransaction({
                    'chainId': web3.eth.chain_id,
                    'gas': default_gasPrice[user_info['chain_current']]['gasLimit'],
                    'gasPrice': default_gasPrice[user_info['chain_current']]['gasPrice'],
                    'nonce': nonce,
                })
            signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=wallet['wallet'].privateKey)
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            if user_info['chain_current'] == 'arbitrum':
                logger.info(f'\n>>> bridge | https://arbiscan.io/tx/{web3.toHex(tx_token)}')
            elif user_info['chain_current'] == 'optimism':
                logger.info(f'\n>>> bridge | https://optimistic.etherscan.io/tx/{web3.toHex(tx_token)}')
            elif user_info['chain_current'] == 'matic':
                logger.info(f'\n>>> bridge | https://polygonscan.com/tx/{web3.toHex(tx_token)}')
            elif user_info['chain_current'] == 'bsc':
                logger.info(f'\n>>> bridge | https://bscscan.com/tx/{web3.toHex(tx_token)}')
            else:
                logger.info(f'\n>>> bridge | https://etherscan.io//tx/{web3.toHex(tx_token)}')

            time.sleep(random.randint(5, 10))
        else:
            logger.info(f'wallet balance less than amount, cur balance - {balance}')
            break
        nonce = nonce + 1



if __name__ == '__main__':
    wallets = get_main_wallet()
    wallets = get_all_wallets(wallets)
    chain_from = str(input('Specify the network with which you want to bridge: Ethereum, Arbitrum, Optimism, Matic, BSC \n')).lower()
    chain_to = str(input('Specify the network where we are going to bridge: Ethereum, Arbitrum, Optimism, Matic, BSC \n')).lower()
    trx_count = int(input('Number of transaction'))
    type_currency = str(input('eth, usdt , usdc, dai')).lower()
    is_possible_transfer = False
    while not is_possible_transfer:
        try:
            cur_info = sourthmap_currency[type_currency][chain_to]
        except Exception as e:
            with open(f'helper.txt', 'r', encoding='utf-8') as file:
                helper = [row.strip() for row in file]
            logger.info(helper)
            type_currency = str(input('eth, usdt , usdc, dai')).lower()
            cur_info = sourthmap_currency[type_currency][chain_to]


        if chain_from == chain_to:
            logger.info('Selected the same network')
            chain_from = str(input(
                'Specify the network with which you want to bridge: Ethereum, Arbitrum, Optimism, Matic, BSC \n')).lower()
            chain_to = str(input(
                'Specify the network where we are going to bridge: Ethereum, Arbitrum, Optimism, Matic, BSC \n')).lower()
        if not cur_info['restricted'] and chain_from != chain_to:
            is_possible_transfer = True

    amount = float(input('how much amount transfer to bridge?'))
    amount_check = False
    while not amount_check:
        cur_limit = transfer_limit[chain_from][chain_to][type_currency]
        if amount > cur_limit['max'] or amount < cur_limit['min']:
            logger.info(f'transfer limit out of range, minimum - {cur_limit["min"]} and max - {cur_limit["max"]}')
            amount = float(input('how much amount transfer to bridge?'))
        else:
            amount_check = True

    if type_currency == 'eth':
        total_txs_cost = (amount + amount * 0.03 + sourthmap_currency[type_currency][chain_to]['withholding_fee']) * trx_count
    else:
        total_txs_cost = (amount + amount * 0.003 + sourthmap_currency[type_currency][chain_to]['withholding_fee']) * trx_count

    multith = str(input("multithreading? - y/n \n"))
    if multith == 'Y' or multith == 'y':
        threads = int(input("number of threads? \n"))
    else:
        threads = 1

    logger.info(f'total cost for transaction with fee {total_txs_cost}')

    pool = Pool(threads)
    collections_user_info = []

    for wallet in wallets:
        user_info = {
            'amount': amount,
            'type_currency': type_currency,
            'trx_count': trx_count,
            'chain_current': chain_from,
            'code': chain_to,
            'wallet': wallet,
            'total_tx_cost': total_txs_cost
        }
        collections_user_info.append(user_info)

    pool.map(bridge, collections_user_info)

    #for wallet in wallets:
    #        bridge(amount, type_currency, trx_count, chain_from, chain_to, wallet, total_txs_cost)
