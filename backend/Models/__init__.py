import os
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None
	
    def connect(self):
        self.client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
        self.engine = AIOEngine(client=self.client, database=os.getenv("Mongo_DB_Name"))
        print("몽고디비와 성공적으러 연결")
    
    def close(self):
        self.client.close()
        print("몽고디비 연결 종료")

mongodb = MongoDB()