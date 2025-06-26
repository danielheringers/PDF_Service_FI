import json
from abc import ABC, abstractmethod

class AuthValidator(ABC):
    def __init__(self, query):
        self.query = query
        self.request_data = None

    async def validate(self):
        if not self.is_authorized():
            return await self.handle_unauthorized()
        return await self.handle_authorized()

    def is_authorized(self):
        not_receipt_authorizations = (
            self.request_data is None or
            self.request_data.get('authorizations') is None
        )
        has_authorizations = self.auth_matcher(self.query, self.request_data.get('authorizations', []))
        return not_receipt_authorizations or has_authorizations

    async def setup(self, request_headers):
        self.request_data = {
            'authorizations': await self.get_authorizations(request_headers)
        }
        return self

    def auth_matcher(self, query, authorizations):
        and_conditions = query.get("$and", [])
    
        auth_set = set(authorizations)
    
        for condition in and_conditions:
            if condition in auth_set:
                return True
    
        return False


class Authorization(AuthValidator):
    @classmethod
    async def create(cls, query, request_headers):
        instance = cls(query)
        await instance.setup(request_headers)
        return instance

    async def handle_unauthorized(self):
        return {"status": 401, "body": "Unauthorized"}

    async def handle_authorized(self):
        return {"status": 200, "body": "Authorized"}

    async def get_authorizations(self, request_headers):
        authorizations = request_headers.get('authorizations') or request_headers.get('auths')
        if isinstance(authorizations, str):
            return json.loads(authorizations)
        return authorizations
