# Auth0 Access Token Python Module

## Description:
Python module used to fetch application access token.

## How to use that module:
### Example with Environment variables

**THIS IS AN EXAMPLE NOT A FULL OR RECOMMENDED IMPLEMENTATION**

```python
import os
import json
import requests
from auth0_token import Auth0AccessTokenFetcher

token_fetcher=Auth0AccessTokenFetcher(domain=os.getenv("AUTH0_DOMAIN"),
                                     client_id=os.getenv("AUTH0_CLIENT_ID"),
                                     client_secret=os.getenv("AUTH0_CLIENT_SECRET"))

def send_request(service_name, endpoint, token_fetcher):
    AUTH0_AUDIENCE = f"https://{service_name}.example.com"  # The API audience
    url = f"https://{service_name}.example.com"  # The actual server the api is served
    token=token_fetcher.get_access_token(audience=AUTH0_AUDIENCE)

    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    openapi_res = requests.get(f"{url}/{endpoint}", headers=headers)

    if openapi_res.status_code != 200:
        return {}

    if openapi_res.status_code == 200:
        return openapi_res.json()


print(json.dumps(send_request("synonyms", "openapi.json", token_fetcher), indent=2))
```
