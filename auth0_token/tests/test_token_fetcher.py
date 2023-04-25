from unittest import mock
from auth0_token import Auth0AccessTokenFetcher
from time import sleep


@mock.patch("auth0_token.Auth0AccessTokenFetcher.fetch_auth0_credentials")
def test_get_access_token(mock_fetch_auth0_credentials):
    mock_fetch_auth0_credentials.return_value = {
        "access_token": "some_token",
        "expires_in": 1
    }
    fetcher = Auth0AccessTokenFetcher("client_a", "secret_a", "aud_a")
    assert fetcher.get_access_token("domain_a") == "some_token"


def test_add_token_to_cache():
    cache_key = "client_aud"
    token = "some_token"
    fetcher = Auth0AccessTokenFetcher("client_a", "secret_a", "aud_a")
    fetcher.add_token_to_cache(cache_key, token)
    assert fetcher.cache[cache_key]["token"] == token


def test_remove_token_from_cache():
    cache_key = "client_aud"
    token = "some_token"
    fetcher = Auth0AccessTokenFetcher("client_a", "secret_a", "aud_a")
    fetcher.add_token_to_cache(cache_key, token)
    fetcher.remove_token_from_cache(cache_key)
    assert fetcher.token_in_cache(cache_key) == False


@mock.patch("auth0_token.Auth0AccessTokenFetcher.fetch_auth0_credentials")
def test_cache_expire_in_skew(mock_fetch_auth0_credentials, skew=1):
    mock_fetch_auth0_credentials.return_value = {
        "access_token": "some_token",
        "expires_in": 5
    }
    fetcher = Auth0AccessTokenFetcher(
        "client_a", "secret_a", "aud_a", expires_in_skew=3)
    fetcher.get_access_token("domain_a")
    assert fetcher.get_token_from_cache("secret_a_domain_a") == "some_token"
    sleep(2)
    assert fetcher.get_token_from_cache("secret_a_domain_a") == None
