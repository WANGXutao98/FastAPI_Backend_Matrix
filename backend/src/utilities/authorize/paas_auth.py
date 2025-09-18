from fastapi import Request
from src.config.manager import business_settings
from src.utilities.common import async_timing_decorator
from src.utilities.requests.ailab_auth import AilabAuth, Interface


class PaasAuth:
    def __init__(self):
        auth_conf = business_settings["adaptor"]["api"]["ailab_auth"]
        self.ailab_auth = AilabAuth(auth_conf["url"], auth_conf["paas_uid"], auth_conf["paas_token"])


    async def commit_delete_app(self, app_group_id: int):
        params = {"app_id": str(app_group_id)}
        return await self.ailab_auth.request_by_signature(Interface.delete_project, data=params)

    @async_timing_decorator
    async def get_login_user(self, request: Request):
        """
        获取访问用户的信息

        Args:
            request (Request): 请求对象

        Returns:
            dict: 用户信息
            eg:
            {
                "company": "腾讯集团本部",
                "department": "腾讯公司/TEG技术工程事业群/AI Lab/AI技术研发中心/AI应用开发组",
                "headimgurl": "https://dayu.woa.com/avatars/lynnlchen/profile.jpg",
                "update_time": "2022-11-03 12:08:05",
                "user_fullname": "lynnlchen(陈凌)",
                "user_id": 1,
                "user_name": "lynnlchen",
                "user_type": "tof4",
                "user_uuid": "tof4_60567"
            }
        """
        return await self.ailab_auth.request_by_cookie(request, Interface.auth_who, method="get")

    @async_timing_decorator
    async def get_login_profile(self, request: Request):
        """
        获取访问用户的信息

        Args:
            request (Request): 请求对象

        Returns:
            dict: 用户信息
            eg:
            {
                "company": "腾讯集团本部",
                "department": "腾讯公司/TEG技术工程事业群/AI Lab/AI技术研发中心/AI应用开发组",
                "headimgurl": "https://dayu.woa.com/avatars/lynnlchen/profile.jpg",
                "is_login": true,
                "paas_admin": false,
                "project_admin": true,
                "user_fullname": "lynnlchen(陈凌)",
                "user_id": 1,
                "user_uuid": "tof4_60567",
                "username": "lynnlchen"
            }
        """
        return await self.ailab_auth.request_by_cookie(request, Interface.auth_profile)

    @async_timing_decorator
    async def login_user_role_list(self, request: Request):
        params = {"need_project_info": True}
        return await self.ailab_auth.request_by_cookie(request, Interface.my_roles, data=params)

    @async_timing_decorator
    async def login_user_project_list(self, request: Request, permission_list: list = []):
        params = {"permission_list": permission_list}
        return await self.ailab_auth.request_by_cookie(request, Interface.my_project_list, data=params)

    @async_timing_decorator
    async def login_user_permission_list(self, request: Request, app_id: str, show_false: bool):
        params = {"app_id": app_id, "show_false": show_false}
        return await self.ailab_auth.request_by_cookie(request, Interface.my_permission_list, data=params)

    @async_timing_decorator
    async def login_user_check_permissions(self, request: Request, app_id: str, permission_dict: dict) -> bool:
        params = {"app_id": app_id}
        if permission_dict:
            params["permission_list"] = [
                {"function_key": function_key, "permission_list": permission_dict[function_key]}
                for function_key in permission_dict
            ]

            response = await self.ailab_auth.request_by_cookie(request, Interface.check_my_permission, data=params)
        else:
            response = await self.ailab_auth.request_by_cookie(request, Interface.auth_in_project, data=params)

        if "result" in response and (not response["result"]):  # type: ignore
            return False
        return len(response) >= 1


g_paas_auth = PaasAuth()


def authorize(request: Request):
    paas_auth = PaasAuth()
    return paas_auth.get_login_user(request)
