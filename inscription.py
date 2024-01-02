import random

from web3 import Web3
from enum import Enum
from help import Transaction, RPCS
from loguru import logger
from get_wallet import get_main_wallet, get_all_wallets
from multiprocessing.dummy import Pool

class chains(Enum):
    linea = 9023
    arbitrum = 9002
    optimism = 9007
    base = 9021
    era = 9014
    zkEvm = 9017
    scroll = 9019


class ch_contract(Enum):
    linea = ''
    arbitrum = ''
    optimism = ''
    base = ''
    era = '0x0a88BC5c32b684D467b43C06D9e0899EfEAF59Df'
    zkEvm = ''
    scroll = ''


class OrbiterInscription:
    def __init__(self, web3, wallet, chain):
        self.web3 = web3
        self.wallet = wallet
        self.address = Web3.toChecksumAddress(wallet["wallet"].address)
        self.contract = Web3.toChecksumAddress(ch_contract[chain].value)

    def get_chain(self, chain_id):
        chain = None
        for _ch in RPCS:
            if RPCS[_ch]['chain_id'] == chain_id:
                chain = RPCS[_ch]['chain']
                break
        return chain

    def mint(self, amount_tx):
        mint_func = None
        try:
            while amount_tx > 0:
                data = '0x646174613a2c7b2270223a226c61796572322d3230222c226f70223a22636c61696d222c227469636b223a22244c32222c22616d74223a2231303030227d'
                chain_from = self.get_chain(int(self.web3.eth.chain_id))

                value = Web3.toWei(0.00023, 'ether')

                random_chain = random.choice(list(chains))
                value_to_chain = random_chain.value

                log_value = [f'\n>>> tx {RPCS[chain_from.lower()]["scan"]}/',
                             f'mint inscription from chain ->{chain_from}; to chain -> {random_chain.name} ']

                value = value + value_to_chain

                self.wallet['to_address'] = self.contract
                self.wallet['tx_data'] = data

                tx = Transaction.build_transaction(mint_func, self.web3, self.wallet, chain_from.lower(), log_value, value)
                amount_tx -=1
        except Exception as e:
            logger.error(e)

def task(wallet):

    web3_from = Web3(Web3.HTTPProvider(RPCS[chain_from]['rpc']))

    orb = OrbiterInscription(web3_from, wallet, chain_from)
    orb.mint(amount)


if __name__ == '__main__':
    wallets = get_all_wallets(get_main_wallet())
    avalaible_ch = []
    for ch in chains:
        avalaible_ch.append(ch.name)
    logger.info(f'avalaible chains -> {avalaible_ch}')
    chain_from = str(input('Specify the network with which you want mint:  \n')).lower()

    amount = int(input('Amount mint insription on account:  \n'))

    multith = str(input("multithreading? - y/n \n"))
    if multith == 'Y' or multith == 'y':
        threads = int(input("number of threads? \n"))
    else:
        threads = 1

    pool = Pool(threads)
    pool.map(task, wallets)
    pool.close()

