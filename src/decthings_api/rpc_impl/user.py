from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from decthings_api.client import DecthingsClient
    from decthings_api.client_sync import DecthingsClientSync

class UserRpc:
    def __init__(self, client: "DecthingsClient"):
        self.__client = client

    async def find_matching_users(self, params):
        res = await self.__client._raw_method_call("User", "findMatchingUsers", params, [])
        return res[1], res[2]

    async def get_users(self, params):
        res = await self.__client._raw_method_call("User", "getUsers", params, [])
        return res[1], res[2]

    async def get_notifications(self, params):
        res = await self.__client._raw_method_call("User", "getNotifications", params, [])
        return res[1], res[2]

    async def set_notification(self, params):
        res = await self.__client._raw_method_call("User", "setNotification", params, [])
        return res[1], res[2]

    async def get_billing_stats(self, params):
        res = await self.__client._raw_method_call("User", "getBillingStats", params, [])
        return res[1], res[2]

    async def estimate_amount_due(self, params):
        res = await self.__client._raw_method_call("User", "estimateAmountDue", params, [])
        return res[1], res[2]

    async def get_quotas(self, params):
        res = await self.__client._raw_method_call("User", "getQuotas", params, [])
        return res[1], res[2]

class UserRpcSync:
    def __init__(self, client: "DecthingsClientSync"):
        self.__client = client

    def find_matching_users(self, params):
        res = self.__client._raw_method_call("User", "findMatchingUsers", params, [])
        return res[1], res[2]

    def get_users(self, params):
        res = self.__client._raw_method_call("User", "getUsers", params, [])
        return res[1], res[2]

    def get_notifications(self, params):
        res = self.__client._raw_method_call("User", "getNotifications", params, [])
        return res[1], res[2]

    def set_notification(self, params):
        res = self.__client._raw_method_call("User", "setNotification", params, [])
        return res[1], res[2]

    def get_billing_stats(self, params):
        res = self.__client._raw_method_call("User", "getBillingStats", params, [])
        return res[1], res[2]

    def estimate_amount_due(self, params):
        res = self.__client._raw_method_call("User", "estimateAmountDue", params, [])
        return res[1], res[2]

    def get_quotas(self, params):
        res = self.__client._raw_method_call("User", "getQuotas", params, [])
        return res[1], res[2]
