from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from decthings_api.client import DecthingsClient
    from decthings_api.client_sync import DecthingsClientSync

class TeamRpc:
    def __init__(self, client: "DecthingsClient"):
        self.__client = client

    async def create_team(self, params):
        res = await self.__client._raw_method_call("Team", "createTeam", params, [])
        return res[1], res[2]

    async def update_team(self, params):
        res = await self.__client._raw_method_call("Team", "updateTeam", params, [])
        return res[1], res[2]

    async def get_teams(self, params):
        res = await self.__client._raw_method_call("Team", "getTeams", params, [])
        return res[1], res[2]

    async def invite_users_to_team(self, params):
        res = await self.__client._raw_method_call("Team", "inviteUsersToTeam", params, [])
        return res[1], res[2]

    async def remove_users_from_team(self, params):
        res = await self.__client._raw_method_call("Team", "removeUsersFromTeam", params, [])
        return res[1], res[2]

    async def accept_team_invitation(self, params):
        res = await self.__client._raw_method_call("Team", "acceptTeamInvitation", params, [])
        return res[1], res[2]

    async def deny_team_invitation(self, params):
        res = await self.__client._raw_method_call("Team", "denyTeamInvitation", params, [])
        return res[1], res[2]

    async def set_share_model_with_team(self, params):
        res = await self.__client._raw_method_call("Team", "setShareModelWithTeam", params, [])
        return res[1], res[2]

    async def set_share_dataset_with_team(self, params):
        res = await self.__client._raw_method_call("Team", "setShareDatasetWithTeam", params, [])
        return res[1], res[2]

    async def create_role(self, params):
        res = await self.__client._raw_method_call("Team", "createRole", params, [])
        return res[1], res[2]

    async def edit_role(self, params):
        res = await self.__client._raw_method_call("Team", "editRole", params, [])
        return res[1], res[2]

    async def remove_role(self, params):
        res = await self.__client._raw_method_call("Team", "removeRole", params, [])
        return res[1], res[2]

    async def assign_role(self, params):
        res = await self.__client._raw_method_call("Team", "assignRole", params, [])
        return res[1], res[2]

class TeamRpcSync:
    def __init__(self, client: "DecthingsClientSync"):
        self.__client = client

    def create_team(self, params):
        res = self.__client._raw_method_call("Team", "createTeam", params, [])
        return res[1], res[2]

    def update_team(self, params):
        res = self.__client._raw_method_call("Team", "updateTeam", params, [])
        return res[1], res[2]

    def get_teams(self, params):
        res = self.__client._raw_method_call("Team", "getTeams", params, [])
        return res[1], res[2]

    def invite_users_to_team(self, params):
        res = self.__client._raw_method_call("Team", "inviteUsersToTeam", params, [])
        return res[1], res[2]

    def remove_users_from_team(self, params):
        res = self.__client._raw_method_call("Team", "removeUsersFromTeam", params, [])
        return res[1], res[2]

    def accept_team_invitation(self, params):
        res = self.__client._raw_method_call("Team", "acceptTeamInvitation", params, [])
        return res[1], res[2]

    def deny_team_invitation(self, params):
        res = self.__client._raw_method_call("Team", "denyTeamInvitation", params, [])
        return res[1], res[2]

    def set_share_model_with_team(self, params):
        res = self.__client._raw_method_call("Team", "setShareModelWithTeam", params, [])
        return res[1], res[2]

    def set_share_dataset_with_team(self, params):
        res = self.__client._raw_method_call("Team", "setShareDatasetWithTeam", params, [])
        return res[1], res[2]

    def create_role(self, params):
        res = self.__client._raw_method_call("Team", "createRole", params, [])
        return res[1], res[2]

    def edit_role(self, params):
        res = self.__client._raw_method_call("Team", "editRole", params, [])
        return res[1], res[2]

    def remove_role(self, params):
        res = self.__client._raw_method_call("Team", "removeRole", params, [])
        return res[1], res[2]

    def assign_role(self, params):
        res = self.__client._raw_method_call("Team", "assignRole", params, [])
        return res[1], res[2]
