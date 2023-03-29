from web3 import Web3
from loguru import logger
from zksync_sdk import HttpJsonRPCTransport, ZkSyncProviderV01, network


contract_orbiter_router = {
    'usdc': '0x41d3D33156aE7c62c094AAe2995003aE63f587B3',
    'usdt': '0xd7Aa9ba6cAAC7b0436c91396f22ca5a7F31664fC',
    'eth': '0x80C67432656d59144cEFf962E8fAF8926599bCF8',
    'dai': '0x095D2918B03b2e86D68551DCF11302121fb626c9'
}

contract_stable = {
    'ethereum': {
        'usdc' : '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
        'usdt': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
        'dai': ''
    },
    'arbitrum': {
        'usdc': '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        'usdt': '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
        'dai': ''
    },
    'optimism': {
        'usdc': '0x7F5c764cBc14f9669B88837ca1490cCa17c31607',
        'usdt': '0x94b008aA00579c1307B0EF2c499aD98a8ce58e58',
        'dai': ''
    },
    'matic': {
        'eth': '0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619',
        'usdc': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
        'usdt': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
        'dai': '0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063'
    },
    'bsc': {
            'eth': '0x2170ed0880ac9a755fd29b2688956bd959f933f8',
            'usdc': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',
            'usdt': '0xc2132D05D31c914a87C6611C10748AEb04B58e8F',
            'dai': '0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3'
        },
    'nova': {
            'usdc': '0x750ba8b76187092b0d1e87e28daaf484d1b5273b',
            'usdt': '',
            'dai': '',
    }
}

orbiter_network_code = {
    'ethereum': 9001,
    'arbitrum': 9002,
    'zkSync lite': 9003,
    'starkNet': 9004,
    'matic': 9006,
    'optimism': 9007,
    'IMX': 9008,
    'bsc': 9015,
    'nova': 9016
}

providers = {
    'matic': {'chainId': 137,
              "rpc": 'https://rpc-mainnet.matic.quiknode.pro',
              "name": 'matic',
              "scanner": 'https://polygonscan.com/',
              },
    'bsc': {'chainId': 56,
                "rpc": 'https://bsc-dataseed.binance.org/',
                "name": 'bsc',
                "scanner": 'https://bscscan.com',
            },
    'ethereum': {'chainId': 1,
                "rpc": 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161',
                "name": 'ethereum',
                "scanner": 'https://etherscan.io/',
                 },
    'optimism': {'chainId': 10,
                "rpc": 'https://mainnet.optimism.io',
                "name": 'optimism',
                "scanner": 'https://optimistic.etherscan.io/',
                 },
    'arbitrum': {'chainId': 42161,
                "rpc": 'https://arb1.arbitrum.io/rpc',
                "name": 'arbitrum',
                "scanner": 'https://arbiscan.io/',

                 },
    'nova': {'chainId': 42170,
                "rpc": 'https://nova.arbitrum.io/rpc',
                "name": 'nova',
                "scanner": 'https://nova.arbiscan.io/',
             },
    'zksync_lite': {'chainId': '',
                "rpc": ZkSyncProviderV01(provider=HttpJsonRPCTransport(network=network.mainnet)),
                "name": 'zkSync lite',
                "scanner": 'https://zkscan.io/',
             }
}


def get_default_provider():
    return {'provider': providers['ethereum']}

def get_current_provider(name) -> {}:
    return providers[name]


def get_provider(chain):
    if chain == 'Ethereum':
        provider = {'provider': providers['eth']}
    elif chain == 'BSC':
        provider = {'provider': providers['bsc']}
    elif chain == 'Arbitrum':
        provider = {'provider': providers['arbitrum']}
    elif chain == 'Optimism':
        provider = {'provider': providers['optimism']}
    elif chain == 'Matic':
        provider = {'provider': providers['matic']}
    elif chain == 'Nova':
        provider = {'provider': providers['nova']}
    elif chain == 'ZkSync lite':
        provider = ZkSyncProviderV01(provider=HttpJsonRPCTransport(network=network.mainnet))
    else:
        logger.info(f'not found chain')

    return provider

MIN_VALUE_ASSETS = 0.1

transfer_limit = {
    'ethereum': {
        'arbitrum': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0012
            },
            'usdc': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 10000,

                        },
            'usdt': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 10000
                        },
            'dai': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 3000
            },
        },
        'optimism': {
                    'eth': {
                        'min': 0.005,
                        'max': 10,
                        'withholding_fee': 0.0012,
                    },
                    'usdc': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 10000
                                },
                    'usdt': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 10000
                                },
                    'dai': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 3000
                    },
        },
        'matic': {
                    'eth': {
                        'min': 0.005,
                        'max': 10,
                        'withholding_fee': 0.0005
                    },
                    'usdc': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 10000
                                },
                    'usdt': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 10000
                                },
                    'dai': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 3000
                    },
        },
        'bsc': {
                    'eth': {
                        'min': 0.005,
                        'max': 10,
                        'withholding_fee': 0.0005
                    },
                },
        'nova': {
                'eth': {
                    'min': 0.005,
                    'max': 5,
                    'withholding_fee': 0.0005
                },
                'usdc': {
                                'min': MIN_VALUE_ASSETS,
                                'max': 10000
                        },
        },
        'zksync lite': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0013
            },
            'usdc': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 10000,

                        },
            'usdt': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 10000
                        },
            'dai': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 3000
            },
        },
    },
    'arbitrum': {
            'matic': {
                'eth': {
                    'min': 0.005,
                    'max': 10,
                    'withholding_fee': 0.0006
                },
                'usdc': {
                                'min': MIN_VALUE_ASSETS,
                                'max': 10000,
                                'withholding_fee': 1.5
                            },
                'usdt': {
                                'min': MIN_VALUE_ASSETS,
                                'max': 10000,
                                'withholding_fee': 1.5
                            },
                'dai': {
                                'min': MIN_VALUE_ASSETS,
                                'max': 3000,
                                'withholding_fee': 1.5
                },
            },
            'optimism': {
                            'eth': {
                                'min': 0.005,
                                'max': 10,
                                'withholding_fee': 0.0007
                            },
                            'usdc': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 10000,
                                            'withholding_fee': 2
                                        },
                            'usdt': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 10000,
                                            'withholding_fee': 2
                                        },
                            'dai': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 3000,
                                            'withholding_fee': 2
                            },
                        },
            'ethereum': {
                            'eth': {
                                'min': 0.005,
                                'max': 10,
                                'withholding_fee': 0.0062
                            },
                            'usdc': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 10000,
                                            'withholding_fee': 12.8
                                        },
                            'usdt': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 10000,
                                            'withholding_fee': 12.8
                                        },
                            'dai': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 3000,
                                            'withholding_fee': 12.8
                            },
                        },
            'bsc': {
                            'eth': {
                                'min': 0.005,
                                'max': 10,
                                'withholding_fee': 0.0003
                            },
                   },
            'nova': {
                    'eth': {
                        'min': 0.005,
                        'max': 5,
                        'withholding_fee': 0.0005
                    },
                    'usdc': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 5000,
                                    'withholding_fee': 1.5
                    },

            },
            'zksync lite': {
                        'eth': {
                            'min': 0.005,
                            'max': 10,
                            'withholding_fee': 0.0013
                        },
                        'usdc': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 10000,
                                        'withholding_fee': 2
                                    },
                        'usdt': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 10000,
                                        'withholding_fee': 2
                                    },
                        'dai': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 3000,
                                        'withholding_fee': 2
                        },
            },
    },
    'optimism': {
                'matic': {
                    'eth': {
                        'min': 0.005,
                        'max': 10,
                        'withholding_fee': 0.0005
                    },
                    'usdc': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 10000,
                                    'withholding_fee': 1.5
                                },
                    'usdt': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 10000,
                                    'withholding_fee': 1.5
                                },
                    'dai': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 3000,
                                    'withholding_fee': 1.5
                    },
                },
                'arbitrum': {
                                'eth': {
                                    'min': 0.005,
                                    'max': 10,
                                    'withholding_fee': 0.0011
                                },
                                'usdc': {
                                                'min': MIN_VALUE_ASSETS,
                                                'max': 10000,
                                                'withholding_fee': 1.8
                                            },
                                'usdt': {
                                                'min': MIN_VALUE_ASSETS,
                                                'max': 10000,
                                                'withholding_fee': 1.8
                                            },
                                'dai': {
                                                'min': MIN_VALUE_ASSETS,
                                                'max': 3000,
                                                'withholding_fee': 1.8
                                },
                            },
                'ethereum': {
                                'eth': {
                                    'min': 0.005,
                                    'max': 10,
                                    'withholding_fee': 0.0062
                                },
                                'usdc': {
                                                'min': MIN_VALUE_ASSETS,
                                                'max': 10000,
                                                'withholding_fee': 12.8
                                            },
                                'usdt': {
                                                'min': MIN_VALUE_ASSETS,
                                                'max': 10000,
                                                'withholding_fee': 12.8
                                            },
                                'dai': {
                                                'min': MIN_VALUE_ASSETS,
                                                'max': 3000,
                                                'withholding_fee': 12.8
                                },
                            },
                'bsc': {
                                'eth': {
                                    'min': 0.005,
                                    'max': 10,
                                    'withholding_fee': 0.0003
                                },
                       },
                'nova': {
                                    'eth': {
                                        'min': 0.005,
                                        'max': 5,
                                        'withholding_fee': 0.0005
                                    },
                                    'usdc': {
                                                    'min': MIN_VALUE_ASSETS,
                                                    'max': 5000,
                                                    'withholding_fee': 1
                                            },

                 },
                'zksync lite': {
                            'eth': {
                                'min': 0.005,
                                'max': 10,
                                'withholding_fee': 0.0013
                            },
                            'usdc': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 10000,
                                            'withholding_fee': 1.5
                                        },
                            'usdt': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 10000,
                                            'withholding_fee': 1.5
                                        },
                            'dai': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 3000,
                                            'withholding_fee': 1.5
                            },
                },
    },
    'matic': {
                    'optimism': {
                        'eth': {
                            'min': 0.005,
                            'max': 10,
                            'withholding_fee': 0.0008
                        },
                        'usdc': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 10000,
                                        'withholding_fee': 2
                                    },
                        'usdt': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 10000,
                                        'withholding_fee': 2
                                    },
                        'dai': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 3000,
                                        'withholding_fee': 2
                        },
                    },
                    'arbitrum': {
                                    'eth': {
                                        'min': 0.005,
                                        'max': 10,
                                        'withholding_fee': 0.0011
                                    },
                                    'usdc': {
                                                    'min': MIN_VALUE_ASSETS,
                                                    'max': 10000,
                                                    'withholding_fee': 2.5
                                                },
                                    'usdt': {
                                                    'min': MIN_VALUE_ASSETS,
                                                    'max': 10000,
                                                    'withholding_fee': 2.5
                                                },
                                    'dai': {
                                                    'min': MIN_VALUE_ASSETS,
                                                    'max': 3000,
                                                    'withholding_fee': 2.5
                                    },
                                },
                    'ethereum': {
                                    'eth': {
                                        'min': 0.005,
                                        'max': 10,
                                        'withholding_fee': 0.0062
                                    },
                                    'usdc': {
                                                    'min': MIN_VALUE_ASSETS,
                                                    'max': 10000,
                                                    'withholding_fee': 12.8
                                                },
                                    'usdt': {
                                                    'min': MIN_VALUE_ASSETS,
                                                    'max': 10000,
                                                    'withholding_fee': 12.8
                                                },
                                    'dai': {
                                                    'min': MIN_VALUE_ASSETS,
                                                    'max': 3000,
                                                    'withholding_fee': 12.8
                                    },
                                },
                    'bsc': {
                                    'eth': {
                                        'min': 0.005,
                                        'max': 10,
                                        'withholding_fee': 0.0003
                                    },
                           },
                    'nova': {
                                        'eth': {
                                            'min': 0.005,
                                            'max': 5,
                                            'withholding_fee': 0.0005
                                        },
                                        'usdc': {
                                                        'min': MIN_VALUE_ASSETS,
                                                        'max': 10000,
                                                        'withholding_fee': 2
                                                },

                            },
                    'zksync lite': {
                                'eth': {
                                    'min': 0.005,
                                    'max': 10,
                                    'withholding_fee': 0.0013
                                },
                                'usdc': {
                                                'min': MIN_VALUE_ASSETS,
                                                'max': 10000,
                                                'withholding_fee': 2

                                            },
                                'usdt': {
                                                'min': MIN_VALUE_ASSETS,
                                                'max': 10000,
                                                'withholding_fee': 2
                                            },
                                'dai': {
                                                'min': MIN_VALUE_ASSETS,
                                                'max': 3000,
                                                'withholding_fee': 2
                                },
            },
    },
    'bsc': {
                        'optimism': {
                            'eth': {
                                'min': 0.005,
                                'max': 10,
                                'withholding_fee': 0.0008
                            },
                        },
                        'arbitrum': {
                                        'eth': {
                                            'min': 0.005,
                                            'max': 10,
                                            'withholding_fee': 0.0008
                                        }
                                    },
                        'ethereum': {
                                        'eth': {
                                            'min': 0.005,
                                            'max': 10,
                                            'withholding_fee': 0.0062
                                        }
                                    },
                        'matic': {
                                        'eth': {
                                            'min': 0.005,
                                            'max': 10,
                                            'withholding_fee': 0.0003
                                        },
                               },
                        'nova': {
                                            'eth': {
                                                'min': 0.005,
                                                'max': 5,
                                                'withholding_fee': 0.0005
                                            },
                                },
                        'zksync lite': {
                                            'eth': {
                                                'min': 0.005,
                                                'max': 5,
                                                'withholding_fee': 0.0013
                                            },
                                },

    },
    'nova': {
            'optimism': {
                        'eth': {
                            'min': 0.005,
                            'max': 10,
                            'withholding_fee': 0.0005
                        },
                        'usdc': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 10000,
                                        'withholding_fee': 1
                                    },
                        'usdt': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 10000,
                                        'withholding_fee': 1
                                    },
                        'dai': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 3000,
                                        'withholding_fee': 1
                        },
            },
            'arbitrum': {
                            'eth': {
                                'min': 0.005,
                                'max': 10,
                                'withholding_fee': 0.0006
                            },
                            'usdc': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 10000,
                                            'withholding_fee': 1
                                        },
                            'usdt': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 10000,
                                            'withholding_fee': 1
                                        },
                            'dai': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 3000,
                                            'withholding_fee': 1
                            },
                        },
            'polygon': {
                        'eth': {
                            'min': 0.005,
                            'max': 10,
                            'withholding_fee': 0.0005
                        },
                        'usdc': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 10000,
                                        'withholding_fee': 1
                                    },
                        'usdt': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 10000,
                                        'withholding_fee': 1
                                    },
                        'dai': {
                                        'min': MIN_VALUE_ASSETS,
                                        'max': 3000,
                                        'withholding_fee': 1
                        },
            },
            'ethereum': {
                            'eth': {
                                'min': 0.005,
                                'max': 10,
                                'withholding_fee': 0.0062
                            },
                            'usdc': {
                                            'min': MIN_VALUE_ASSETS,
                                            'max': 10000,
                                            'withholding_fee': 12.8
                                        },

                        },
            'bsc': {
                            'eth': {
                                'min': 0.005,
                                'max': 10,
                                'withholding_fee': 0.0005
                            },
                   },
            'zksync lite': {
                            'eth': {
                                'min': 0.005,
                                'max': 10,
                                'withholding_fee': 0.0005
                            },
                            'usdc': {
                                'min': MIN_VALUE_ASSETS,
                                'max': 10,
                                'withholding_fee': 1
                            },
            }
    },
    'zksync_lite': {
        'arbitrum': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0011
            },
            'usdc': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 10000,
                            'withholding_fee': 3
                        },
            'usdt': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 10000,
                            'withholding_fee': 3
                        },
            'dai': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 3000,
                            'withholding_fee': 3
            },
        },
        'optimism': {
                    'eth': {
                        'min': 0.005,
                        'max': 10,
                        'withholding_fee': 0.0008,
                    },
                    'usdc': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 10000,
                                    'withholding_fee': 1.8,
                                },
                    'usdt': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 10000,
                                    'withholding_fee': 1.8,
                                },
                    'dai': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 3000,
                                    'withholding_fee': 1.8,
                    },
        },
        'matic': {
                    'eth': {
                        'min': 0.007,
                        'max': 10,
                        'withholding_fee': 0.0005
                    },
                    'usdc': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 10000,
                                    'withholding_fee': 1.5
                                },
                    'usdt': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 10000,
                                    'withholding_fee': 1.5
                                },
                    'dai': {
                                    'min': MIN_VALUE_ASSETS,
                                    'max': 3000,
                                    'withholding_fee': 1.5
                    },
        },
        'bsc': {
                    'eth': {
                        'min': 0.005,
                        'max': 10,
                        'withholding_fee': 0.0005
                    },
                },
        'nova': {
                'eth': {
                    'min': 0.005,
                    'max': 5,
                    'withholding_fee': 0.0005
                },
                'usdc': {
                                'min': MIN_VALUE_ASSETS,
                                'max': 10000,
                                'withholding_fee': 1
                        },
        },
        'ethereum': {
            'eth': {
                'min': 0.005,
                'max': 10,
                'withholding_fee': 0.0062
            },
            'usdc': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 10000,
                            'withholding_fee': 12.8

                        },
            'usdt': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 10000,
                            'withholding_fee': 12.8
                        },
            'dai': {
                            'min': MIN_VALUE_ASSETS,
                            'max': 3000,
                            'withholding_fee': 12.8
            },
        },
    }
}