import os
import uuid

from usso.session import AsyncUssoSession, UssoSession

from ..base_app import App, AsyncApp, AsyncResource, Resource
from .schemas import EnrollmentSchema, QuotaSchema, UsageSchema


class SaaS(App):
    def __init__(
        self,
        *,
        ufaas_base_url: str = os.getenv("UFAAS_URL"),
        usso_base_url: str | None = os.getenv("USSO_URL"),
        api_key: str | None = os.getenv("UFAAS_API_KEY"),
        usso_refresh_url: str | None = os.getenv("USSO_REFRESH_URL"),
        refresh_token: str | None = os.getenv("USSO_REFRESH_TOKEN"),
        client: UssoSession | None = None,
    ):
        super().__init__(
            app_name="saas",
            ufaas_base_url=ufaas_base_url,
            usso_base_url=usso_base_url,
            api_key=api_key,
            usso_refresh_url=usso_refresh_url,
            refresh_token=refresh_token,
            client=client,
        )

    def initiate_resources(self, **kwargs):
        self.usages = Usage(client=self)
        self.enrollments = Enrollment(client=self)


class AsyncSaaS(AsyncApp):

    def __init__(
        self,
        *,
        ufaas_base_url: str = os.getenv("UFAAS_URL"),
        usso_base_url: str | None = os.getenv("USSO_URL"),
        api_key: str | None = os.getenv("UFAAS_API_KEY"),
        usso_refresh_url: str | None = os.getenv("USSO_REFRESH_URL"),
        refresh_token: str | None = os.getenv("USSO_REFRESH_TOKEN"),
        client: AsyncUssoSession | None = None,
    ):
        super().__init__(
            app_name="saas",
            ufaas_base_url=ufaas_base_url,
            usso_base_url=usso_base_url,
            api_key=api_key,
            usso_refresh_url=usso_refresh_url,
            refresh_token=refresh_token,
            client=client,
        )

    def initiate_resources(self, **kwargs):
        self.usages = AsyncUsage(client=self)
        self.enrollments = AsyncEnrollment(client=self)


class Usage(Resource):

    def __init__(
        self,
        *,
        ufaas_base_url: str = os.getenv("UFAAS_URL"),
        usso_base_url: str | None = os.getenv("USSO_URL"),
        api_key: str | None = os.getenv("UFAAS_API_KEY"),
        usso_refresh_url: str | None = os.getenv("USSO_REFRESH_URL"),
        refresh_token: str | None = os.getenv("USSO_REFRESH_TOKEN"),
        client: UssoSession | None = None,
    ):
        super().__init__(
            app_name="saas",
            resource_name="usages",
            schema=UsageSchema,
            ufaas_base_url=ufaas_base_url,
            usso_base_url=usso_base_url,
            api_key=api_key,
            usso_refresh_url=usso_refresh_url,
            refresh_token=refresh_token,
            client=client,
        )

    def cancel_item(self, uid: str, **kwargs):
        resp = self.post(f"{self.resource_url}{uid}/cancel", params=kwargs)
        resp.raise_for_status()
        return self.retrieve_response_schema(**resp.json())


class AsyncUsage(AsyncResource):

    def __init__(
        self,
        *,
        ufaas_base_url: str = os.getenv("UFAAS_URL"),
        usso_base_url: str | None = os.getenv("USSO_URL"),
        api_key: str | None = os.getenv("UFAAS_API_KEY"),
        usso_refresh_url: str | None = os.getenv("USSO_REFRESH_URL"),
        refresh_token: str | None = os.getenv("USSO_REFRESH_TOKEN"),
        client: AsyncUssoSession | None = None,
    ):
        super().__init__(
            app_name="saas",
            resource_name="usages",
            schema=UsageSchema,
            ufaas_base_url=ufaas_base_url,
            usso_base_url=usso_base_url,
            api_key=api_key,
            usso_refresh_url=usso_refresh_url,
            refresh_token=refresh_token,
            client=client,
        )

    async def cancel_item(self, uid: str, **kwargs):
        resp = await self.post(f"{self.resource_url}{uid}/cancel", params=kwargs)
        resp.raise_for_status()
        return self.retrieve_response_schema(**resp.json())


class Enrollment(Resource):
    def __init__(
        self,
        *,
        ufaas_base_url: str = os.getenv("UFAAS_URL"),
        usso_base_url: str | None = os.getenv("USSO_URL"),
        api_key: str | None = os.getenv("UFAAS_API_KEY"),
        usso_refresh_url: str | None = os.getenv("USSO_REFRESH_URL"),
        refresh_token: str | None = os.getenv("USSO_REFRESH_TOKEN"),
        client: UssoSession | None = None,
    ):
        super().__init__(
            app_name="saas",
            resource_name="enrollments",
            schema=EnrollmentSchema,
            ufaas_base_url=ufaas_base_url,
            usso_base_url=usso_base_url,
            api_key=api_key,
            usso_refresh_url=usso_refresh_url,
            refresh_token=refresh_token,
            client=client,
        )

    def get_quotas(
        self,
        asset: str,
        user_id: uuid.UUID | None = None,
        variant: str | None = None,
        **kwargs,
    ):
        if isinstance(user_id, uuid.UUID):
            user_id = str(user_id)
        params = {"asset": asset, "user_id": user_id, "variant": variant, **kwargs}
        resp = self.get(f"{self.resource_url}quotas", params=params)
        resp.raise_for_status()
        return QuotaSchema(**resp.json())


class AsyncEnrollment(AsyncResource):
    def __init__(
        self,
        *,
        ufaas_base_url: str = os.getenv("UFAAS_URL"),
        usso_base_url: str | None = os.getenv("USSO_URL"),
        api_key: str | None = os.getenv("UFAAS_API_KEY"),
        usso_refresh_url: str | None = os.getenv("USSO_REFRESH_URL"),
        refresh_token: str | None = os.getenv("USSO_REFRESH_TOKEN"),
        client: AsyncUssoSession | None = None,
    ):
        super().__init__(
            app_name="saas",
            resource_name="enrollments",
            schema=EnrollmentSchema,
            ufaas_base_url=ufaas_base_url,
            usso_base_url=usso_base_url,
            api_key=api_key,
            usso_refresh_url=usso_refresh_url,
            refresh_token=refresh_token,
            client=client,
        )

    async def get_quotas(
        self,
        asset: str,
        user_id: uuid.UUID | None = None,
        variant: str | None = None,
        **kwargs,
    ):
        if isinstance(user_id, uuid.UUID):
            user_id = str(user_id)
        params = {"asset": asset, "user_id": user_id, "variant": variant, **kwargs}
        resp = await self.get(f"{self.resource_url}quotas", params=params)
        resp.raise_for_status()
        return QuotaSchema(**resp.json())
