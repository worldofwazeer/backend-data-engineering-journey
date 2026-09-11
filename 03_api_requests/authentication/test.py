# from api_client import APIClient
#
# with APIClient() as client:
#     print(client.session.adapters)

from api_client import APIClient

with APIClient() as client:
    adapter = client.session.get_adapter("https://")

    print(adapter.max_retries)