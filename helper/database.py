import motor.motor_asyncio
import time
import uuid
from config import Config
from .utils import send_log


class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.user_data_col = self.db.user_data

    def new_user(self, id):
        return dict(
            _id=int(id),                                   
            file_id=None,
            caption=None,
            token=None,
            time=None,
            page=0
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)
            await send_log(b, u)
            await self.user_data_col.insert_one({"user_id": u.id, "data": {}})

    async def is_user_exist(self, id):
        user = await self.col.find_one({"_id": int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({"_id": int(user_id)})
        await self.user_data_col.delete_many({"user_id": user_id})

    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({"_id": int(id)}, {"$set": {"file_id": file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({"_id": int(id)})
        return user.get("file_id", None)

    async def set_caption(self, id, caption):
        await self.col.update_one({"_id": int(id)}, {"$set": {"caption": caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({"_id": int(id)})
        return user.get("caption", None)

    async def get_user_data(self, user_id):
        user_data = await self.user_data_col.find_one({"user_id": user_id})
        if user_data is None:
            return {}
        return user_data.get("data", {})

    async def update_user_data(self, user_id, data):
        await self.user_data_col.update_one(
            {"user_id": user_id}, {"$set": {"data": data, "page": data.get("page", 0)}}, upsert=True
        )

db = Database(Config.DB_URL, Config.DB_NAME)
