from flask_login import UserMixin
from pymongo import MongoClient
from bson.objectid import ObjectId

from app import login_manager

class User():
    client = MongoClient()
    db = client.hc_database
    users_db = db.users

    def __init__(self, dic):
        self.first_name = dic["first_name"]
        self.last_name = dic['last_name']
        self.username = dic['username']
        self.is_admin = dic['is_admin']
        self.password = dic['password']
        self._id = dic['_id']

    @staticmethod
    def create_admin():
        """
        Inserts admin user into database if one is not present
        """
        client = MongoClient()
        db = client.hc_database
        users_db = db.users
        new_admin = User({ "first_name": "Test",
                    "last_name": "Admin",
                    "username": "testadmin2",
                    "password": "test123",
                    "is_admin": True
        })
        users_db.insert_one(new_admin)
        print "success"

    def is_active(self):
        """
        Needed for flask_login to verify current_user
        """
        return True

    def is_authenticated(self):
        """
        Needed for flask_login to verify current_user
        """
        return True

    def is_anonymous(self):
        """
        Needed for flask_login to verify current_user
        """
        return False

    def get_id(self):
        """
        Needed for flask_login to verify current_user
        """
        return unicode(str(self._id))

    @staticmethod
    def get_user(user):
        client = MongoClient()
        db = client.hc_database
        users_db = db.users
        found_user = users_db.find_one({"username": user})
        return found_user

    @staticmethod
    def check_pass(user, password):
        client = MongoClient()
        db = client.hc_database
        users_db = db.users
        if users_db.find_one({"username": user})["password"] == password:
            return True
        else:
            return False


@login_manager.user_loader
def load_user(user_id):
    client = MongoClient()
    db = client.hc_database
    users_db = db.users
    return User(users_db.find_one({"_id": ObjectId(user_id)}))

class Table():
    """
    Class to represent dining tables to display
    """
    client = MongoClient()
    db = client.hc_database
    tables_db = db.tables

    def __init__(self, formDic):
        self.height = formDic["height"]
        self.length = formDic["length"]
        self.width = formDic["width"]
        self.color = formDic["color"]
        self.chair_count = formDic["chair_count"]
        self.chair_color = formDic["chair_color"]


    @staticmethod
    def insert_table(table):
        client = MongoClient()
        db = client.hc_database
        tables_db = db.tables
        tables_db.insert_one(table)

    @staticmethod
    def get_tables():
        client = MongoClient()
        db = client.hc_database
        tables_db = db.tables
        return tables_db.find()

    @staticmethod
    def search_tables(searchObj):
        client = MongoClient()
        db = client.hc_database
        tables_db = db.tables
        search_filter = {}

        if "catalog_no" in searchObj:
            search_filter["catalog_no"] = searchObj["catalog_no"]

        if "color" in searchObj:
            search_filter["color"] = searchObj["color"]

        if "price" in searchObj:
            if searchObj["priceRange"] == 'less':
                search_filter["price"] = { '$lt': searchObj["price"] }
            else:
                search_filter["price"] = { '$gt': searchObj["price"] }

        if "chair_count" in searchObj:
            search_filter["chair_count"] = searchObj["chair_count"]

        if "length" in searchObj:
            if searchObj["dimensionRange"] == 'less':
                search_filter["length"] = { '$lt': searchObj["length"] }
            elif searchObj["dimensionRange"] == 'greater':
                search_filter["length"] = { '$gt': searchObj["length"] }
            else:
                search_filter["length"] = searchObj["length"]

        if "width" in searchObj:
            if searchObj["dimensionRange"] == 'less':
                search_filter["width"] = { '$lt': searchObj["width"] }
            elif searchObj["dimensionRange"] == 'greater':
                search_filter["width"] = { '$gt': searchObj["width"] }
            else:
                search_filter["width"] = searchObj["width"]

        if "height" in searchObj:
            if searchObj["dimensionRange"] == 'less':
                search_filter["height"] = { '$lt': searchObj["height"] }
            elif searchObj["dimensionRange"] == 'greater':
                search_filter["height"] = { '$gt': searchObj["height"] }
            else:
                search_filter["height"] = searchObj["height"]

        print "search filter"
        print search_filter
        found_tables = tables_db.find(search_filter)
        tables_list = {}
        tables_list["results"] = []
        for i in found_tables:
            i["_id"] = str(i["_id"])
            tables_list["results"].append(i)
        return tables_list

    @staticmethod
    def update_table(table_id, table_obj):
        client = MongoClient()
        db = client.hc_database
        tables_db = db.tables

        update = tables_db.update_one({"_id": ObjectId(table_id)}, {"$set": table_obj}, upsert=False)
        print update
        return update

    @staticmethod
    def delete_table(table_obj):
        client = MongoClient()
        db = client.hc_database
        tables_db = db.tables

        found_tables = tables_db.find(table_obj)
        photo = found_tables[0]['photo']
        tables_db.delete_one(found_tables[0])
        return photo[19:]
