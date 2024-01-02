from web3 import Web3
from loguru import logger
from zksync_sdk import HttpJsonRPCTransport, ZkSyncProviderV01, network

contract_orbiter_router = {
    'usdc': '0x41d3D33156aE7c62c094AAe2995003aE63f587B3',
    'usdt': '0xd7Aa9ba6cAAC7b0436c91396f22ca5a7F31664fC',
    'eth': '0x80C67432656d59144cEFf962E8fAF8926599bCF8',
    'dai': '0x095D2918B03b2e86D68551DCF11302121fb626c9'
}

#https://github.com/Orbiter-Finance/OrbiterFE-V2/blob/main/src/config/chains-v3.json
contract_stable = {
    'ethereum': {
        'usdc' : '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
        'usdt': '0xdAC17F958D2ee523a2206206994597C13D831ec7',
        'dai': '0x6B175474E89094C44Da98b954EedeAC495271d0F'
    },
    'arbitrum': {
        'usdc': '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8',
        'usdt': '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9',
        'dai': '0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1'
    },
    'optimism': {
        'usdc': '0x7F5c764cBc14f9669B88837ca1490cCa17c31607',
        'usdt': '0x94b008aA00579c1307B0EF2c499aD98a8ce58e58',
        'dai': "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1"
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
            'dai': ''
        },
    'nova': {
            'usdc': '0x750ba8b76187092b0d1e87e28daaf484d1b5273b',
            'usdt': '',
            'dai': '',
    },
    'avaxc': {
            'usdc': '',
            'usdt': '',
            'dai': '',
    },
    'zksync_era': {
            'usdc': "0x3355df6d4c9c3035724fd0e3914de96a5a83aaf4",
            'usdt': '',
            'dai': '',
    },
    'starknet': {
            'eth': "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7",
            'usdc': "0x053c91253bc9682c04929ca02ed00b3e423f6710d2ee7e0d5ebb06f3ecf368a8",
            'usdt': "0x068f5c6a61780768455de69077e07e89787839bf8166decfbf92b645209c0fb8",
            'dai': "0x00da114221cb83fa859dbdb4c44beeaa0bb37c7537ad5ae66fe5e0efd20e6eb3"
    },
    'imx': {
        'usdc': "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    },
    'metis': {
        'eth': "0x420000000000000000000000000000000000000a",
        'usdc': "0xEA32A96608495e54156Ae48931A7c20f0dcc1a21"
    },
    'dydx': {
        'usdc': "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    },
    'zkspace': {
        'usdc': "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    },
    'boba': {

    },
    'zkevm': {
        'usdc': "0xa8ce8aee21bc2a48a5ef670afcc9274c7bbbc035",
        'usdt': "0x1e4a5963abfd975d8c9021ce480b42188849d41d"
    },
    "linea": {
        'usdc': "0x176211869ca2b568f2a7d4ee941e073a821ee1ff",
        'usdt': "0xA219439258ca9da29E9Cc4cE5596924745e12B93"
    },
    "mantle": {
        'eth': "0xdeaddeaddeaddeaddeaddeaddeaddeaddead1111"
    },
    "base": {
        "usdc": "0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA"
    },
    "zora": {

    },
    "opBnb": {
        'eth': "0xe7798f023fc62146e8aa1b36da45fb70855a77ea"
    },
    "manta": {

    },
    "scroll": {
      "usdc":  "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",
      "usdt":  "0xf55BEC9cafDbE8730f096Aa55dad6D22d44099Df"
    },
    "zkfair": {
        'usdc': '0x0000000000000000000000000000000000000000',
        'eth': '0x4b21b980d0Dc7D3C0C6175b0A412694F3A1c7c6b'
    }

}

orbiter_network_code = {
    'ethereum': 9001,
    'arbitrum': 9002,
    'zksync_lite': 9003,
    'starkNet': 9004,
    'matic': 9006,
    'optimism': 9007,
    'imx': 9008,
    'metis': 9010,
    'dydx': 9011,
    'zkspace': 9012,
    'boba': 9013,
    'zksync_era': 9014,
    'bsc': 9015,
    'nova': 9016,
    'zkevm': 9017,
    'linea': 9023,
    'mantle': 9024,
    'base': 9021,
    'zora': 9030,
    'opbnb': 9025,
    'manta': 9031,
    'scroll': 9019,
    'zkfair': 9038
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
             },
    'zksync_era': {'chainId': 324,
                "rpc": 'https://mainnet.era.zksync.io',
                "name": 'zkSync era',
                "scanner": 'https://explorer.zksync.io/',
             },
    'starknet': {'chainId': "",
                "rpc": 'https://starknet-mainnet.g.alchemy.com/v2/qeW9Qg4ew8AKLyzicQ7J7oOFI1NCtKyz',
                "name": 'starknet',
                "scanner": 'https://starkscan.co/',
             },
    'imx': {'chainId': "",
                "rpc": 'https://api.x.immutable.com/v1',
                "name": 'immutable',
                "scanner": ''
            },
    'metis': {'chainId': "1088",
                "rpc": 'https://andromeda.metis.io/?owner=1088',
                "name": 'metis',
                "scanner": 'https://andromeda-explorer.metis.io'
            },
    'dydx': {'chainId': "",
                "rpc": '',
                "name": 'dydx',
                "scanner": ''
            },
    'zkspace': {'chainId': "",
                "rpc": '',
                "name": 'zkspace',
                "scanner": 'https://zkspace.info'
            },
    'boba': {'chainId': "288",
                "rpc": 'https://mainnet.boba.network',
                "name": 'boba',
                "scanner": 'https://bobascan.com'
            },
    'zkevm': {'chainId': "1101",
                "rpc": 'https://zkevm-rpc.com',
                "name": 'zkevm',
                "scanner": 'https://zkevm.polygonscan.com/'
            },
    'linea': {'chainId': "59144",
                "rpc": 'https://rpc.linea.build',
                "name": 'linea',
                "scanner": 'https://explorer.linea.build'
            },
    'mantle': {'chainId': "5000",
                "rpc": 'https://rpc.mantle.xyz',
                "name": 'mantle',
                "scanner": 'https://explorer.mantle.xyz'
            },
    'base': {'chainId': "8453",
                "rpc": 'https://mainnet.base.org',
                "name": 'base',
                "scanner": 'https://basescan.org/'
            },
    'zora': {'chainId': "7777777",
                "rpc": 'https://rpc.zora.energy',
                "name": 'zora',
                "scanner": 'https://explorer.zora.energy'
            },
    'opbnb': {'chainId': "204",
                "rpc": 'https://opbnb-mainnet-rpc.bnbchain.org',
                "name": 'opbnb',
                "scanner": 'https://mainnet.opbnbscan.com/'
            },
    'manta': {'chainId': "169",
                "rpc": 'https://manta-pacific.calderachain.xyz/http',
                "name": 'manta',
                "scanner": 'https://manta-pacific.calderaexplorer.xyz'
            },
    'scroll': {'chainId': "534352",
                "rpc": 'https://rpc.scroll.io',
                "name": 'scroll',
                "scanner": 'https://scrollscan.com/'
            },
    'zkfair': {'chainId': "42766",
                "rpc": 'https://rpc.zkfair.io',
                "name": 'zkfair',
                "scanner": 'https://scan.zkfair.io'
    }
}

def get_default_provider():
    return {'provider': providers['ethereum']}

def get_current_provider(name) -> {}:
    return providers[name]

