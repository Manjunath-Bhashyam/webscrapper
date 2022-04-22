# Necessary Imports

import pymongo


class MongoDBconnect:

    def __init__(self, username, password):
        """Function collects username, password and prepares url for MongoDB Atlas"""
        try:
            self.username = username
            self.password = password
            self.url = "mongodb+srv://{}:{}@cluster0.dnuul.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(self.username, self.password)

        except Exception as e:
            raise Exception("(__init__) error/issue occurred\n" + str(e))

    def mongodbclient(self):
        """Function to connect mongo DB"""
        try:
            mongo_client = pymongo.MongoClient(self.url)
            return mongo_client

        except Exception as e:
            raise Exception("(mongodbclient) error/issue with db connection\n" + str(e))

    def isdatabasepresent(self, db_name):
        """Function checks if database exists"""
        try:
            mongo_client = self.mongodbclient()
            if db_name in mongo_client.list_database_names():
                return True
            else:
                mongo_client.close()
                return False

        except Exception as e:
            raise Exception(f"(isdatabasepresent) error/issue with database {db_name} availablility check\n" + str(e))

    def getdatabase(self, db_name):
        """Function returns database"""
        try:
            mongo_client = self.mongodbclient()
            return mongo_client[db_name]

        except Exception as e:
            raise Exception(f"(getdatabase) error/issue to get database {db_name}\n" + str(e))

    def iscollectionpresent(self, db_name, collection_name):
        """Function checks if collection exists in the respective database"""
        try:
            database_check = self.isdatabasepresent(db_name=db_name)
            if database_check:
                database = self.getdatabase(db_name=db_name)
                if collection_name in database.list_collection_names():
                    return True
                else:
                    return False
            else:
                return False

        except Exception as e:
            raise Exception(f"(iscollectionpresent) error/issue to check {collection_name} in {db_name}" + str(e))

    def getcollection(self, db_name, collection_name):
        """Function returns collection"""
        try:
            database = self.getdatabase(db_name=db_name)
            return database[collection_name]

        except Exception as e:
            raise Exception("(getcollection) error/issue in fetching collection" + str(e))

    def createdatabase(self, db_name):
        """Function creates a database"""
        try:
            database_check = self.isdatabasepresent(db_name=db_name)
            if not database_check:
                mongo_client = self.mongodbclient()
                database = mongo_client[db_name]
                return database

        except Exception as e:
            raise Exception(f"(createdatabase) issue creating database {db_name}" + str(e))

    def createcollection(self, db_name, collection_name):
        """Function creates a collection under respective database"""
        try:
            collection_check = self.iscollectionpresent(db_name=db_name, collection_name=collection_name)
            if not collection_check:
                database = self.getdatabase(db_name=db_name)
                collection = database[collection_name]
                return collection

        except Exception as e:
            raise Exception(f"(createcollection) issue creating collection {collection_name}" + str(e))

    def insertrecords(self, db_name, collection_name, records):
        """Function inserts one record into respective collection"""
        try:
            collection = self.getcollection(db_name=db_name, collection_name=collection_name)
            collection.insert_many(records)

        except Exception as e:
            raise Exception("(insertrecords) issue in inserting records to collection" + str(e))

    def findallrecords(self, db_name, collection_name):
        """Function finds all records"""
        try:
            collection_check = self.iscollectionpresent(db_name=db_name, collection_name=collection_name)
            if collection_check:
                collection = self.getcollection(db_name=db_name, collection_name=collection_name)
                findallrecords = collection.find()
                return findallrecords

        except Exception as e:
            raise Exception("(findallrecords) issue in finding records" + str(e))

    def findrecordsonquery(self, db_name, collection_name, query):
        """Function finds all records"""
        try:
            collection_check = self.iscollectionpresent(db_name=db_name, collection_name=collection_name)
            if collection_check:
                collection = self.getcollection(db_name=db_name, collection_name=collection_name)
                findrecords = collection.find(query)
                return findrecords

        except Exception as e:
            raise Exception("(findrecordsonquery) issue in finding records as per input query" + str(e))
