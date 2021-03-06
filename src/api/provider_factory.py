from rpc.rpc_block_api import RpcBlockApiImpl
from rpc.rpc_reward_api import RpcRewardApiImpl
from tzstats.tzstats_block_api import TzStatsBlockApiImpl
from tzstats.tzstats_reward_api import TzStatsRewardApiImpl

class ProviderFactory:
    URL = "https://{}.tezrpc.me"
    url_prefixes = {"MAINNET": "mainnet", "ALPHANET": "alphanet", "ZERONET": "zeronet"}

    def __init__(self, provider, verbose=False):
        self.provider = provider
        self.verbose = verbose

    def newRewardApi(self, network_config, baking_address, node_url, node_url_public=''):
        if self.provider == 'rpc':
            if node_url.find("http") == -1:
                node_url = 'http://' + node_url
            return RpcRewardApiImpl(network_config, baking_address, node_url, verbose=self.verbose)
        elif self.provider == 'prpc':
            if node_url_public == '':
                url_prefix = self.url_prefixes[network_config['NAME']]
                node_url_public = self.URL.format(url_prefix)
            return RpcRewardApiImpl(network_config,  baking_address, node_url_public, verbose=self.verbose)
        elif self.provider == 'tzstats':
            return TzStatsRewardApiImpl(network_config, baking_address, verbose=self.verbose)

        raise Exception("No supported reward data provider : {}".format(self.provider))

    def newBlockApi(self, network_config, wllt_clnt_mngr, node_url):
        if self.provider == 'rpc' or self.provider == 'prpc':
            return RpcBlockApiImpl(network_config, wllt_clnt_mngr, node_url)
        elif self.provider == 'tzstats':
            return TzStatsBlockApiImpl(network_config)
        raise Exception("No supported reward data provider : {}".format(self.provider))
