from web3 import Web3
from loguru import logger
import json

#ERC
ERC20_ABI = json.loads('''[{"inputs":[{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"uint256","name":"_initialSupply","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"name":"setupDecimals","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]''')

usdc_orbiter = '0x41d3D33156aE7c62c094AAe2995003aE63f587B3'
usdt_orbiter = '0xd7Aa9ba6cAAC7b0436c91396f22ca5a7F31664fC'
eth_orbiter = '0x80C67432656d59144cEFf962E8fAF8926599bCF8'
dai_orbiter = '0x095D2918B03b2e86D68551DCF11302121fb626c9'

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
}

sourthmap_currency = {
    'usdc': {
        'matic': {
            'withholding_fee': 1.5,
            'restricted': False,
        },
        'optimism': {
            'withholding_fee': 1.8,
            'restricted': False
        },
        'arbitrum': {
            'withholding_fee': 1.8,
            'restricted': False
        },
        'bsc': {
            'withholding_fee': None,
            'restricted': True
        },
    },
    'usdt': {
        'matic': {
            'withholding_fee': 1.5,
            'restricted': False
        },
        'optimism': {
            'withholding_fee': 2,
            'restricted': False
        },
        'arbitrum': {
            'withholding_fee': 1.8,
            'restricted': False
        },
        'bsc': {
            'withholding_fee': None,
            'restricted': True
        },
    },
    'dai': {
        'matic': {
            'withholding_fee': 1.3,
            'restricted': False
        },
        'optimism': {
            'withholding_fee': 1.3,
            'restricted': False
        },
        'arbitrum': {
            'withholding_fee': 1.8,
            'restricted': False
        },
        'bsc': {
            'withholding_fee': None,
            'restricted': True
        },
    },
    'eth': {
        'matic': {
            'withholding_fee': 0.0006,
            'restricted': False
        },
        'optimism': {
            'withholding_fee': None,
            'restricted': False
        },
        'arbitrum': {
            'withholding_fee': None,
            'restricted': False
        },
        'bsc': {
            'withholding_fee': 0.0003,
            'restricted': False
        },
    },
}


network_code = {
    'ethereum': 9001,
    'arbitrum': 9002,
    'zkSync': 9003,
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
              "name": 'matic'},
    'bsc': {'chainId': 56,
            "rpc": 'https://bsc-dataseed.binance.org/',
            "name": 'bsc'},
    'ethereum': {'chainId': 1,
            "rpc": 'https://mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161',
            "name": 'ethereum'},
    'fuji': {'chainId': 43113,
             "rpc": 'https://api.avax-test.network/ext/bc/C/rpc',
             "name": 'fuji'},
    'mumbai': {'chainId': 80001,
               "rpc": 'https://matic-mumbai.chainstacklabs.com',
               "name": 'mumbai'},
    'rinkeby': {'chainId': 4,
                   "rpc": 'https://rinkeby.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161',
                   "name": 'rinkeby'},
    'optimism': {'chainId': 10,
            "rpc": 'https://mainnet.optimism.io',
            "name": 'optimism'},
    'arbitrum': {'chainId': 42161,
                "rpc": 'https://arb1.arbitrum.io/rpc',
                "name": 'arbitrum'},
    'nova': {'chainId': 42170,
                    "rpc": 'https://nova.arbitrum.io/rpc',
                    "name": 'nova'},
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
    else:
        logger.info(f'not found chain')

    return provider


default_gasPrice = {
    'arbitrum': {
        'gasPrice':  Web3.toWei(0.0000000001, 'ether'),
        'gasLimit': 3000000
    },
    'optimism': {
        'gasPrice':  Web3.toWei(0.0000000001, 'ether'),
        'gasLimit': 3000000
    },
    'matic': {
        'gasPrice':  Web3.toWei('190', 'gwei'),
        'gasLimit': 120000
    },
    'ethereum': {
        'gasPrice':  Web3.toWei(20, 'gwei'),
        'gasLimit': 3000000
    },
    'bsc': {
        'gasPrice':  Web3.toWei('5', 'gwei'),
        'gasLimit': 70000
    }
}

transfer_limit = {
    'ethereum': {
        'arbitrum': {
            'eth': {
                'min': 0.005,
                'max': 10
            },
            'usdc': {
                            'min': 0.005,
                            'max': 10000
                        },
            'usdt': {
                            'min': 0.005,
                            'max': 10000
                        },
            'dai': {
                            'min': 0.01,
                            'max': 3000
            },
        },
        'optimism': {
                    'eth': {
                        'min': 0.005,
                        'max': 10
                    },
                    'usdc': {
                                    'min': 0.005,
                                    'max': 10000
                                },
                    'usdt': {
                                    'min': 0.005,
                                    'max': 10000
                                },
                    'dai': {
                                    'min': 0.01,
                                    'max': 3000
                    },
        },
        'matic': {
                    'eth': {
                        'min': 0.005,
                        'max': 10
                    },
                    'usdc': {
                                    'min': 0.005,
                                    'max': 10000
                                },
                    'usdt': {
                                    'min': 0.005,
                                    'max': 10000
                                },
                    'dai': {
                                    'min': 0.01,
                                    'max': 3000
                    },
        },
        'bsc': {
                    'eth': {
                        'min': 0.005,
                        'max': 10
                    },
                },
    },
    'arbitrum': {
            'matic': {
                'eth': {
                    'min': 0.005,
                    'max': 10
                },
                'usdc': {
                                'min': 0.005,
                                'max': 10000
                            },
                'usdt': {
                                'min': 0.005,
                                'max': 10000
                            },
                'dai': {
                                'min': 0.01,
                                'max': 3000
                },
            },
            'optimism': {
                            'eth': {
                                'min': 0.005,
                                'max': 10
                            },
                            'usdc': {
                                            'min': 0.005,
                                            'max': 10000
                                        },
                            'usdt': {
                                            'min': 0.005,
                                            'max': 10000
                                        },
                            'dai': {
                                            'min': 0.01,
                                            'max': 3000
                            },
                        },
            'ethereum': {
                            'eth': {
                                'min': 0.005,
                                'max': 10
                            },
                            'usdc': {
                                            'min': 0.005,
                                            'max': 10000
                                        },
                            'usdt': {
                                            'min': 0.005,
                                            'max': 10000
                                        },
                            'dai': {
                                            'min': 0.01,
                                            'max': 3000
                            },
                        },
            'bsc': {
                            'eth': {
                                'min': 0.005,
                                'max': 10
                            },
                   },
    },
    'optimism': {
                'matic': {
                    'eth': {
                        'min': 0.005,
                        'max': 10
                    },
                    'usdc': {
                                    'min': 0.005,
                                    'max': 10000
                                },
                    'usdt': {
                                    'min': 0.005,
                                    'max': 10000
                                },
                    'dai': {
                                    'min': 0.01,
                                    'max': 3000
                    },
                },
                'arbitrum': {
                                'eth': {
                                    'min': 0.005,
                                    'max': 10
                                },
                                'usdc': {
                                                'min': 0.005,
                                                'max': 10000
                                            },
                                'usdt': {
                                                'min': 0.005,
                                                'max': 10000
                                            },
                                'dai': {
                                                'min': 0.01,
                                                'max': 3000
                                },
                            },
                'ethereum': {
                                'eth': {
                                    'min': 0.005,
                                    'max': 10
                                },
                                'usdc': {
                                                'min': 0.005,
                                                'max': 10000
                                            },
                                'usdt': {
                                                'min': 0.005,
                                                'max': 10000
                                            },
                                'dai': {
                                                'min': 0.01,
                                                'max': 3000
                                },
                            },
                'bsc': {
                                'eth': {
                                    'min': 0.005,
                                    'max': 10
                                },
                       },
        },
    'matic': {
                    'optimism': {
                        'eth': {
                            'min': 0.005,
                            'max': 10
                        },
                        'usdc': {
                                        'min': 0.005,
                                        'max': 10000
                                    },
                        'usdt': {
                                        'min': 0.005,
                                        'max': 10000
                                    },
                        'dai': {
                                        'min': 0.01,
                                        'max': 3000
                        },
                    },
                    'arbitrum': {
                                    'eth': {
                                        'min': 0.005,
                                        'max': 10
                                    },
                                    'usdc': {
                                                    'min': 0.005,
                                                    'max': 10000
                                                },
                                    'usdt': {
                                                    'min': 0.005,
                                                    'max': 10000
                                                },
                                    'dai': {
                                                    'min': 0.01,
                                                    'max': 3000
                                    },
                                },
                    'ethereum': {
                                    'eth': {
                                        'min': 0.005,
                                        'max': 10
                                    },
                                    'usdc': {
                                                    'min': 0.005,
                                                    'max': 10000
                                                },
                                    'usdt': {
                                                    'min': 0.005,
                                                    'max': 10000
                                                },
                                    'dai': {
                                                    'min': 0.01,
                                                    'max': 3000
                                    },
                                },
                    'bsc': {
                                    'eth': {
                                        'min': 0.005,
                                        'max': 10
                                    },
                           },
            },
    'bsc': {
                        'optimism': {
                            'eth': {
                                'min': 0.005,
                                'max': 10
                            },
                        },
                        'arbitrum': {
                                        'eth': {
                                            'min': 0.005,
                                            'max': 10
                                        }
                                    },
                        'ethereum': {
                                        'eth': {
                                            'min': 0.005,
                                            'max': 10
                                        }
                                    },
                        'matic': {
                                        'eth': {
                                            'min': 0.005,
                                            'max': 10
                                        },
                               },
                },
}