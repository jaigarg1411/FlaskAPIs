import sqlite3
from db.dbConn import Database
from exceptions import ObjectAlreadyExist, ObjectNotFound
import hashlib
from flask_jwt_extended import create_access_token


class UsersDatabase(Database):
    def __init__(self):
        super().__init__()

    def getUsers(self):
        query = "SELECT id, username FROM users"
        self.cursor.execute(query)
        user_list = [{"id": row[0], "username": row[1]} for row in self.cursor.fetchall()]
        return user_list

    def getUser(self, id):
        query = "SELECT id, username FROM users WHERE id = ?"
        self.cursor.execute(query, (id,))
        row = self.cursor.fetchone()
        if row is None:
            return {}
        return {"id": row[0], "username": row[1]}

    def addUser(self, bodyObj):
        try:
            # Check if user already exists
            select_query = "SELECT * FROM users WHERE username = ?"
            self.cursor.execute(select_query, (bodyObj["username"],))
            user = self.cursor.fetchone()

            if user is None:
                # Hash password
                hashed_password = hashlib.sha256(bodyObj["password"].encode("utf-8")).hexdigest()

                # Insert new user
                insert_query = "INSERT INTO users (username, password) VALUES (?, ?)"
                self.cursor.execute(insert_query, (bodyObj["username"], hashed_password))
                self.conn.commit()

                print(f"User '{bodyObj['username']}' added successfully.")
            else:
                raise ObjectAlreadyExist("User already exists")

        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"SQLite error: {e}")
            raise Exception(f"SQLite error: {e}")

        except ObjectAlreadyExist as e:
            self.conn.rollback()
            raise ObjectAlreadyExist("User already exists")

        except Exception as e:
            self.conn.rollback()
            print(f"Unexpected error: {e}")
            raise Exception(f"Unexpected error: {e}")

    def updateUser(self, id, bodyObj):
        updatedUsername = bodyObj.get("username")
        updatedPassword = bodyObj.get("password")
        
        if updatedUsername is not None and updatedPassword is not None:
            query = "UPDATE users SET username = ?, password = ? WHERE id = ?"
            self.cursor.execute(query, (updatedUsername, hashlib.sha256(updatedPassword.encode("utf-8")).hexdigest(), id))
        elif updatedUsername is not None:
            query = "UPDATE users SET username = ? WHERE id = ?"
            self.cursor.execute(query, (updatedUsername, id))
        elif updatedPassword is not None:
            query = "UPDATE users SET password = ? WHERE id = ?"
            self.cursor.execute(query, (hashlib.sha256(updatedPassword.encode("utf-8")).hexdigest(), id))

        self.conn.commit()
        if self.cursor.rowcount == 0:
            raise ObjectNotFound("User not found")

    def deleteUser(self, id):
        query = "DELETE FROM users WHERE id = ?"
        self.cursor.execute(query, (id,))
        self.conn.commit()
        if self.cursor.rowcount == 0:
            raise ObjectNotFound("User not found")

    def loginUser(self, bodyObj):
        query = "SELECT id, username FROM users WHERE username = ? AND password = ? LIMIT 1"
        try:
            self.cursor.execute(query, (bodyObj["username"], hashlib.sha256(bodyObj["password"].encode("utf-8")).hexdigest()))
            row = self.cursor.fetchone()
            if row is None:
                raise ObjectNotFound("Invalid credentials")
            else:
                return create_access_token(identity={"id": row[0], "username": row[1]})
        
        except ObjectNotFound as e:
            raise ObjectNotFound("Invalid credentials")
        
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    def getBlockedTokenList(self):
        query = "SELECT jwt_id FROM blockedTokens"
        self.cursor.execute(query)
        blockedTokenList = [row[0] for row in self.cursor.fetchall()]
        return blockedTokenList

    def invalidateToken(self, jti):
        query = "INSERT INTO blockedTokens (jwt_id) VALUES (?)"
        try:
            self.cursor.execute(query, (jti,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise Exception(f"Error invalidating token: {e}")
