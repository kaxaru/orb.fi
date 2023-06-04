import random
import time
from enum import Enum
from web3 import Web3, Account
from loguru import logger
from get_wallet import get_main_wallet, get_all_wallets
from config import contract_stable
from config import orbiter_network_code
from config import contract_orbiter_router
from config import get_current_provider, providers
from config import transfer_limit
from helper import load_contract
from multiprocessing.dummy import Pool
import asyncio
from decimal import Decimal

from zksync_sdk import network, ZkSync, EthereumProvider, Wallet, ZkSyncSigner, EthereumSignerWeb3, ZkSyncLibrary
from zksync_sdk.types import ChangePubKeyEcdsa
import os

logger.info(os.environ["ZK_SYNC_LIBRARY_PATH"])
lib = ZkSyncLibrary()

class Chain(Enum):
    ethereum = 'Ethereum',
    arbitrum = 'Arbitrum',
    optimism = 'Optimism',
    matic = 'Matic',
    bsc = 'Bsc',
    nova = 'Nova',
    starknet = 'Starknet',
    zksync_lite = 'Zksync lite',
    zksync_era = 'Zksync era',
    fantom = 'fantom'

chain_with_native_eth = [Chain.ethereum.name, Chain.arbitrum.name, Chain.optimism.name, Chain.zksync_lite.name, Chain.nova.name, Chain.zksync_era.name]
chain_without_eipstandart = [Chain.bsc.name, Chain.optimism.name, Chain.fantom.name]

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

async def get_wallet_zk(web3_zksync, code, currency):
    zk_contracts = await web3_zksync.get_contract_address()
    signer_eth = EthereumSignerWeb3(wallet["wallet"])
    web3 = Web3(Web3.HTTPProvider(get_current_provider('ethereum')['rpc']))

    if currency == 'USDT' or currency == 'USDC':
        amount = user_info['amount'] * 1000000 + code
    else:
        amount = (web3.toWei(user_info['amount'], 'ether') // 1000000 + code) * 1000000

    zksync = ZkSync(account=wallet["wallet"], web3=web3,
                    zksync_contract_address=zk_contracts.main_contract)
    ethereum_provider = EthereumProvider(web3, zksync)
    zk_sigher = ZkSyncSigner.from_account(wallet["wallet"], lib, network.mainnet)
    _wallet = Wallet(ethereum_provider=ethereum_provider, zk_signer=zk_sigher,
                     eth_signer=signer_eth, provider=web3_zksync)
    return _wallet, amount

async def unlock_zk_wallet(wallet):
    if not await wallet.is_signing_key_set():
        tx = await wallet.set_signing_key("ETH", eth_auth_data=ChangePubKeyEcdsa())
        status = await tx.await_committed()
        return status
    else: return True

async def zk_transfer(wallet, to,  amount, token):
    logger.info(to)
    tx = await wallet.transfer(to, amount=Decimal(amount), token=token)
    status = await tx.await_committed()
    return status, tx

async def zk_wal(web3_zksync, code):
    _wallet, amount_to = await get_wallet_zk(web3_zksync, code, type_currency.upper())
    _status_unlock = await unlock_zk_wallet(_wallet)
    logger.info(f'Status unlock {_status_unlock} for wallet {wallet["wallet"].address}')

    # check balance
    account_state = await _wallet.get_account_state()
    committed_balance = account_state.committed.balances.get(user_info['type_currency'].upper())
    logger.info(f'commited balance - {committed_balance}')

    if type_currency.upper() == 'USDT' or type_currency.upper() == 'USDC':
        _amount = Web3.fromWei(amount_to, 'mwei')
    else:
        _amount = Web3.fromWei(amount_to, 'ether')

    _status, _tx = await zk_transfer(_wallet, Web3.toChecksumAddress(contract_orbiter_router[type_currency]), _amount,
                    type_currency.upper())
    logger.info(f'transfer tx - {_status}')
    logger.info(f'https://zkscan.io/explorer/transactions/0x{_tx.transaction_hash.split(":")[1]}')

def bridge(user_info):
    wallet = user_info['wallet']
    provider_info = get_current_provider(user_info['chain_current'])
    code = orbiter_network_code[user_info['code']]
    if user_info['chain_current'] == 'zksync_lite':
        web3_zksync = provider_info['rpc']
        asyncio.run(zk_wal(web3_zksync, code))
        return
    else:
        web3 = Web3(Web3.HTTPProvider(provider_info['rpc']))

    if type_currency != 'eth':
        contract_stable_address = contract_stable[user_info['chain_current']][user_info['type_currency']]
        contract_stable_instance = load_contract(web3, 'erc20', Web3.toChecksumAddress(contract_stable_address))
        #contract_stable_instance = web3.eth.contract(Web3.toChecksumAddress(contract_stable_address), abi=ERC20_ABI)
        if type_currency == 'usdc' or type_currency == 'usdt':
            amount = web3.toWei(user_info['amount'], 'mwei') // 10000 * 10000 + code
        else:
            amount = web3.toWei(user_info['amount'], 'ether') // 10000 * 10000 + code

        address_to = Web3.toChecksumAddress(contract_orbiter_router[type_currency])
    else:
        if user_info['chain_current'] == 'bsc' or user_info['chain_current'] == 'matic':
            contract_stable_address = contract_stable[user_info['chain_current']][user_info['type_currency']]
            contract_stable_instance = load_contract(web3, 'erc20', Web3.toChecksumAddress(contract_stable_address))
        else:
            contract_stable_instance = None
        address_to = Web3.toChecksumAddress(contract_orbiter_router[type_currency])
        amount = web3.toWei(user_info['amount'], 'ether') // 10000 * 10000 + code

    nonce = web3.eth.get_transaction_count(wallet['wallet'].address)
    for tx in enumerate(range(user_info['trx_count'])):
        balance = get_balance(user_info['chain_current'], user_info['type_currency'], contract_stable_instance, web3)
        logger.info(f'transaction number - {nonce}')
        if balance > amount:
            if user_info['chain_current'] in chain_with_native_eth:
                if type_currency == 'eth':
                    contract_txn = {
                        "chainId": web3.eth.chain_id,
                        'to': address_to,
                        'value': amount,
                        'nonce': nonce,
                    }
                    if not (user_info['chain_current'] in chain_without_eipstandart):
                        contract_txn.update({'maxFeePerGas': web3.eth.gasPrice})
                        contract_txn.update({'maxPriorityFeePerGas': web3.eth.gasPrice})
                    else:
                        contract_txn.update({'gasPrice': web3.eth.gasPrice})

                    if web3.eth.chain_id == providers['zksync_era']['chainId']:
                        contract_txn.update({'from': wallet["wallet"].address})

                else:
                    contract_txn = contract_stable_instance.functions.transfer(Web3.toChecksumAddress(address_to),
                                                                               amount).buildTransaction({
                        'chainId': web3.eth.chain_id,
                        'from': wallet['wallet'].address,
                        'nonce': nonce,
                    })
                    if not (user_info['chain_current'] in chain_without_eipstandart):
                        contract_txn.update({'maxFeePerGas': web3.eth.gasPrice})
                        contract_txn.update({'maxPriorityFeePerGas': web3.eth.gasPrice})
                    else:
                        contract_txn.update({'gasPrice': web3.eth.gasPrice})

                try:
                    gasLimit = web3.eth.estimateGas(contract_txn)
                    contract_txn.update({'gas': gasLimit})
                except Exception as e:
                    logger.info('impossible calculate to chain')
            else:
                contract_txn = contract_stable_instance.functions.transfer(Web3.toChecksumAddress(address_to), amount).buildTransaction({
                        'chainId': web3.eth.chain_id,
                        'from': wallet['wallet'].address,
                        'nonce': nonce,
                    })
                if not (user_info['chain_current'] in chain_without_eipstandart):
                    contract_txn.update({'maxFeePerGas': web3.eth.gasPrice})
                    contract_txn.update({'maxPriorityFeePerGas': web3.eth.gasPrice})
                else:
                    contract_txn.update({'gasPrice': web3.eth.gasPrice})

                gasLimit = web3.eth.estimateGas(contract_txn)
                contract_txn.update({'gas': gasLimit})

            signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=wallet['wallet'].privateKey)
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            logger.info(f'\n>>> bridge | {provider_info["scanner"]}/tx/{web3.toHex(tx_token)}')

            time.sleep(random.randint(5, 10))
        else:
            logger.info(f'wallet balance less than amount - {amount}, cur balance - {balance}')
            break
        nonce = nonce + 1

if __name__ == '__main__':
    wallets = get_all_wallets(get_main_wallet())
    chain_from = str(input('Specify the network with which you want to bridge: Ethereum, Arbitrum, Optimism, Matic, BSC, Nova, Zksync lite, Zksync era \n')).lower()
    chain_to = str(input('Specify the network where we are going to bridge: Ethereum, Arbitrum, Optimism, Matic, BSC, Nova, Zksync lite, Zksync era \n')).lower()
    chain_from = '_'.join(chain_from.split(' '))
    chain_to = '_'.join(chain_to.split(' '))
    trx_count = int(input('Number of transaction'))
    type_currency = str(input('eth, usdt , usdc, dai')).lower()
    is_correct_chain = False
    while not is_correct_chain:
       try:
           if Chain[chain_from] == Chain[chain_to]:
               raise Exception(f'the origin and destination network are the same')
           if Chain[chain_from] or Chain[chain_to]:
               is_correct_chain = True
       except Exception as e:
           logger.info(e)
           chain_from = str(input(
               'Specify the network with which you want to bridge: Ethereum, Arbitrum, Optimism, Matic, BSC, Nova, Zksync lite, Zksync era \n')).lower()
           chain_to = str(input(
               'Specify the network where we are going to bridge: Ethereum, Arbitrum, Optimism, Matic, BSC, Nova, Zksync lite, Zksync era \n')).lower()

    is_possible_transfer = False
    while not is_possible_transfer:
        try:
            fee = transfer_limit[chain_from][chain_to][type_currency]['withholding_fee']
            is_possible_transfer = True
        except Exception as e:
            logger.info('currency not avalaible in destination chain')
            logger.info(e)
            with open(f'helper.txt', 'r', encoding='utf-8') as file:
                for row in file:
                    logger.info(row)
            chain_to = str(input('Specify the network where we are going to bridge: Ethereum, Arbitrum, Optimism, Matic, BSC, Nova \n')).lower()
            type_currency = str(input('eth, usdt , usdc, dai')).lower()

    amount = float(input('how much amount transfer to bridge?'))
    amount_check = False
    while not amount_check:
        cur_limit = transfer_limit[chain_from][chain_to][type_currency]
        if amount <= cur_limit['max'] and amount >= cur_limit['min']:
            if amount >= cur_limit['min'] and amount <= cur_limit['min'] + transfer_limit[chain_from][chain_to][type_currency]['withholding_fee']:
                amount = amount + transfer_limit[chain_from][chain_to][type_currency]['withholding_fee']
                amount = round(amount, 4)
            if (amount + transfer_limit[chain_from][chain_to][type_currency]['withholding_fee']) >= cur_limit['max']:
                amount = amount - transfer_limit[chain_from][chain_to][type_currency]['withholding_fee']
            amount_check = True
        else:
            logger.info(f'transfer limit out of range, minimum - {cur_limit["min"]} and max - {cur_limit["max"]}')
            amount = float(input('how much amount transfer to bridge?'))
    logger.info(f'c - min amount {amount} for tx in {type_currency}')

    multith = str(input("multithreading? - y/n \n"))
    if multith == 'Y' or multith == 'y':
        threads = int(input("number of threads? \n"))
    else:
        threads = 1

    pool = Pool(threads)
    collections_user_info = []

    for wallet in wallets:
        user_info = {
            'amount': amount + round(random.uniform(0.0001, 0.0002), 5),
            'type_currency': type_currency,
            'trx_count': trx_count,
            'chain_current': chain_from,
            'code': chain_to,
            'wallet': wallet,
        }

        collections_user_info.append(user_info)

    pool.map(bridge, collections_user_info)
    pool.close()
    logger.info('task complete')

