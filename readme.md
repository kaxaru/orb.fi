# Orbiter finance

Avalaible chains: Ethereum, Arbitrum, Optimism, Nova, Zksync Lite, Zksync Era, Matic, BSC

In order to work with the zksync you need:

1) Download sdk for Zksync -> https://github.com/zksync-sdk/zksync-python
2) You have to download zksync-crypto-library from https://github.com/zksync-sdk/zksync-crypto-c/releases for your system.
3) Set env variable ZK_SYNC_LIBRARY_PATH with a path to the downloaded library

More details are written here, if you don't understand https://docs.zksync.io/api/sdk/python/tutorial/#installation

Please check the commission for your network in config.py. If you find an error in 'withholding_fee', write me about it. Thank you. 

For ethereum network I haven't written 'withholding_fee' yet, insert it if necessary.