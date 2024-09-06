from pymongo import MongoClient

# class MongoDBConnector:
#     """
#     A class to handle MongoDB connections using pymongo.

#     Attributes:
#         username (str): The username for MongoDB authentication.
#         password (str): The password for MongoDB authentication.
#         host (str): The host address of the MongoDB server.
#         db_name (str): The name of the database to connect to.
#         replica_set (str, optional): The name of the replica set (default is None).
#         tls (bool, optional): Flag to use TLS/SSL (default is True).
#         client (MongoClient, optional): The MongoDB client instance (default is None).
#         uri (str): The constructed MongoDB URI.
#     """

#     def __init__(self, username, password, host, db_name, replica_set=None, tls=True):
#         """
#         Constructs all the necessary attributes for the MongoDBConnector object.

#         Args:
#             username (str): The username for MongoDB authentication.
#             password (str): The password for MongoDB authentication.
#             host (str): The host address of the MongoDB server.
#             db_name (str): The name of the database to connect to.
#             replica_set (str, optional): The name of the replica set (default is None).
#             tls (bool, optional): Flag to use TLS/SSL (default is True).
#         """
#         self.username = username
#         self.password = password
#         self.host = host
#         self.db_name = db_name
#         self.replica_set = replica_set
#         self.tls = tls
#         self.client = None
#         self.uri = self._construct_uri()

#     def _construct_uri(self):
#         """
#         Constructs the MongoDB URI from the given attributes.

#         Returns:
#             str: The constructed MongoDB URI.
#         """
#         uri = f"mongodb+srv://{self.username}:{self.password}@{self.host}/{self.db_name}?"
#         if self.replica_set:
#             uri += f"replicaSet={self.replica_set}&"
#         if self.tls:
#             uri += "tls=true"
#         else:
#             uri = uri.rstrip('&')
#         print(uri)
#         return uri

#     def connect(self):
#         """
#         Establishes a connection to the MongoDB server.

#         Returns:
#             MongoClient: The MongoDB client instance if the connection is successful.

#         Raises:
#             Exception: If an error occurs while connecting to MongoDB.
#         """
#         try:
#             self.client = MongoClient(self.uri)
#             print("Connected to MongoDB")
#             return self.client
#         except Exception as e:
#             print(f"An error occurred while connecting to MongoDB: {e}")
#             raise

class MongoDBConnector:
    """
    A class to handle MongoDB connections using pymongo.

    Attributes:
        username (str): The username for MongoDB authentication.
        password (str): The password for MongoDB authentication.
        host (str): The host address of the MongoDB server.
        db_name (str): The name of the database to connect to.
        replica_set (str, optional): The name of the replica set (default is None).
        tls (bool, optional): Flag to use TLS/SSL (default is True).
        client (MongoClient, optional): The MongoDB client instance (default is None).
        uri (str): The constructed MongoDB URI.
    """

    def __init__(self, username, password, host, db_name, replica_set=None, tls=False):
        """
        Constructs all the necessary attributes for the MongoDBConnector object.

        Args:
            username (str): The username for MongoDB authentication.
            password (str): The password for MongoDB authentication.
            host (str): The host address of the MongoDB server.
            db_name (str): The name of the database to connect to.
            replica_set (str, optional): The name of the replica set (default is None).
            tls (bool, optional): Flag to use TLS/SSL (default is True).
        """
        self.username = username
        self.password = password
        self.host = host
        self.db_name = db_name
        self.replica_set = replica_set
        self.tls = tls
        self.client = None
        self.uri = self._construct_uri()

    def _construct_uri(self):
        """
        Constructs the MongoDB URI from the given attributes.

        Returns:
            str: The constructed MongoDB URI.
        """
        uri = f"mongodb://{self.username}:{self.password}@{self.host}/?authSource={self.db_name}"
        if self.replica_set:
            uri += f"replicaSet={self.replica_set}&"
        if self.tls:
            uri += "tls=true"
        else:
            uri = uri.rstrip('&')
        print(uri)
        return uri

    def connect(self):
        """
        Establishes a connection to the MongoDB server.

        Returns:
            MongoClient: The MongoDB client instance if the connection is successful.

        Raises:
            Exception: If an error occurs while connecting to MongoDB.
        """
        try:
            self.client = MongoClient(self.uri)
            print("Connected to MongoDB")
            return self.client
        except Exception as e:
            print(f"An error occurred while connecting to MongoDB: {e}")
            raise