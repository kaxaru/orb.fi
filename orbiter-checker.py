import json
import time
from requests import Session
from get_wallet import get_addresses
from multiprocessing.dummy import Pool
from loguru import logger

def task(wallet):
    repeat = 100
    while repeat > 0:
        try:
            session = Session()
            session.headers.update({
                'host': 'openapi.orbiter.finance',
                'origin': 'https://www.orbiter.finance',
                'referer': 'https://www.orbiter.finance/',
                'accept': 'application/json, text/plain, */*'
            })
            req = session.get(f"https://openapi.orbiter.finance/points_system/v2/user/points?address={wallet.lower()}")
            if req.status_code == 200:
                data = json.loads(req.content)

                total = data["data"]["total"]
                logger.info(f"total points on wallet {wallet} -> {total}")
            req = session.get(f"https://openapi.orbiter.finance/points_system/user/nfts?address={wallet.lower()}")
            if req.status_code == 200:
                data = json.loads(req.content)
                nfts = data["data"]["nfts"]
                logger.info(f"total nfts  {nfts}")
            break
        except Exception as e:
            #logger.error(e)
            repeat -= 1
            time.sleep(5)



if __name__ == '__main__':

    wallets_adresses = get_addresses()
    multith = str(input("multithreading? - y/n \n"))
    if multith == 'Y' or multith == 'y':
        threads = int(input("number of threads? \n"))
    else:
        threads = 1
    pool = Pool(threads)
    pool.map(task, wallets_adresses)