import pprint

import grpc
import pytest
from google.protobuf.json_format import MessageToDict
from grpclib.client import Channel

from apis.dm_api_account_grpc.account_pb2 import RegisterAccountRequest
#from apis.dm_api_account_grpc.account_pb2_grpc import AccountServiceStub
from apis.dm_api_account_grpc_async import AccountServiceStub


def test_account_no_fixture():
    channel = grpc.insecure_channel(target='5.63.153.31:5055')
    client = AccountServiceStub(channel=channel)
    response = client.RegisterAccount(
        request=RegisterAccountRequest(
            login='user_64',
            email='user_64@user_64',
            password='user_62!%'
        )
    )

    pprint.pprint(MessageToDict(response))
    channel.close()


def test_account_with_sync_client(grpc_account):
    response = grpc_account.register_account(
            login='user_67',
            email='user_67@user_67',
            password='user_67!%'
        )


@pytest.mark.asyncio
async def test_account_async(grpc_account_async):
    response = await grpc_account_async.register_account(
        register_account_request=RegisterAccountRequest(
            login='user_74',
            email='user_74@user_74',
            password='user_74!%'
        )
    )
    print(response)


@pytest.mark.asyncio
async def test_account_async_no_fixture():
    channel = Channel(host='5.63.153.31', port=5055)
    client = AccountServiceStub(channel=channel)
    response = await client.register_account(
        register_account_request=RegisterAccountRequest(
            login='user_70',
            email='user_70@user_70',
            password='user_70!%'
        )
    )
    print(response)
