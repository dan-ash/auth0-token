from auth0.v3.authentication import GetToken
from cachetools import TTLCache
import logging.config


class Auth0AccessTokenFetcher:

    def __init__(self, domain, client_id, client_secret, expires_in_skew=30):
        self.cache = {}
        self.logger = logging.getLogger(__name__)
        self.domain = domain
        self.client_id = client_id
        self.client_secret = client_secret
        self.expires_in_skew = expires_in_skew

    def get_token_from_cache(self, cache_key):
        if self.token_in_cache(cache_key):
            self.logger.info(f"Hit cached token for key {cache_key}")
            return self.cache[cache_key]["token"]
        return None

    def remove_token_from_cache(self, cache_key):
        if self.cache.__contains__(cache_key):
            self.cache.__delitem__(cache_key)

    def token_in_cache(self, cache_key):
        if self.cache.__contains__(cache_key):
            if self.cache[cache_key].__contains__("token"):
                self.logger.info(f"found token in cache for {cache_key}")
                return True
            else:
                # cache pointer exist but no cache is stored for token
                # hence removing self.chache["cache_key"]
                self.cache.__delitem__(cache_key)
        return False

    def add_token_to_cache(self, cache_key, token, ttl=300, maxsize=1):
        if not self.token_in_cache(cache_key):
            self.cache[cache_key] = TTLCache(maxsize=maxsize, ttl=ttl)
            self.cache[cache_key].__setitem__("token", token)
            self.logger.info(f"Added token to cache {cache_key}")

    def fetch_auth0_credentials(self, audience):
        token_getter = GetToken(self.domain)
        self.logger.info("Fetching token from auth0")
        credentials = token_getter.client_credentials(
            self.client_id,
            self.client_secret,
            audience)
        return credentials

    def get_access_token(self, audience):
        '''
        Fetch token from Auth0 (returns the token from cache if exist)
        :return: Auth0 access token
        '''
        try:
            cache_key = f"{self.client_id}_{audience}"
            token = self.get_token_from_cache(cache_key)
            if not token:
                aut0_credentials = self.fetch_auth0_credentials(audience)
                token = aut0_credentials["access_token"]
                ttl = aut0_credentials["expires_in"] - self.expires_in_skew
                self.add_token_to_cache(cache_key, token, ttl=ttl)
            return token
        except Exception as e:
            raise e
