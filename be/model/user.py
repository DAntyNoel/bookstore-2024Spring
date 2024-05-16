import jwt
import time
import logging
import sqlite3 as sqlite

import pymongo.errors
from be.model import error
# from be.model import db_conn
from be.model.mongo_classes import UserMongo, UserStoreMongo, StoreMongo
import mongoengine.errors
from typing import Tuple


def jwt_encode(user_id: str, terminal: str) -> str:
    '''
    encode a json string like:
    {
        "user_id": [user name],
        "terminal": [terminal code],
        "timestamp": [ts]} to a JWT
    }
    '''
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded

def jwt_decode(encoded_token, user_id: str) -> str:
    '''decode a JWT to a json string like:
        {
            "user_id": [user name],
            "terminal": [terminal code],
            "timestamp": [ts]} to a JWT
        }
    '''
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded

class User:
    token_lifetime: int = 3600  # 3600 seconds

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str):
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            UserMongo(user_id=user_id, password=password, balance=0, token=token, terminal=terminal).save(force_insert=True)
        except mongoengine.errors.NotUniqueError:
            return error.error_exist_user_id(user_id)
        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> Tuple[int, str]:
        row = UserMongo.query(user_id=user_id).only('token').first()
        if row is None:
            return error.error_authorization_fail()
        db_token = row.token
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> Tuple[int, str]:
        row = UserMongo.query(user_id=user_id).only('password').first()
        if row is None:
            return error.error_authorization_fail()

        if password != row.password:
            return error.error_authorization_fail()

        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> Tuple[int, str, str]:
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            user:UserMongo = UserMongo.query(user_id=user_id).first()
            if user is None:
                return error.error_authorization_fail() + ("",)
            user.token = token
            user.terminal = terminal
            user.save()
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""
        return 200, "ok", token

    def logout(self, user_id: str, token: str) -> bool:
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)

            user:UserMongo = UserMongo.query(user_id=user_id).first()
            if user is None:
                return error.error_authorization_fail()
            user.token = dummy_token
            user.terminal = terminal
            user.save()
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def unregister(self, user_id: str, password: str) -> Tuple[int, str]:
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            result = [x for x in UserMongo.query(user_id=user_id)]
            if len(result) == 1:
                result[0].delete()
            else:
                return error.error_authorization_fail()
            user_stores = [x for x in UserStoreMongo.query(user_id=user_id)]
            for userstore in user_stores:
                StoreMongo.query(store_id=userstore.store_id).delete()
                userstore.delete()
        except mongoengine.errors.MongoEngineException as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def change_password(
        self, user_id: str, old_password: str, new_password: str
    ) -> bool:
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            user:UserMongo = UserMongo.query(user_id=user_id).first()
            if user is None:
                return error.error_authorization_fail()
            user.password = new_password
            user.token = token
            user.terminal = terminal
            user.save()
        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
