from loguru import logger


class UserManager:
    def __init__(self, client: str):
        """
        Initialize the MongoUserManager with connection details.

        Parameters:
        - client (MongoClient): The MongoClient instance for the MongoDB connection.
        """
        self.client = client


    def create_user(self, database: str, user: str, password: str, role: str) -> None:
        """
        Create a user in the specified MongoDB database with the given role and password.

        Parameters:
        - database (str): The name of the database where the user will be created.
        - user (str): The username of the user to be created.
        - password (str): The password for the new user.
        - role (str): The role assigned to the user in the database.

        Returns:
        - None
        """
        db = self.client[database]
        try:
            db.command("createUser", user,
                    pwd=password,
                    roles=[{"role": role,
                            "db": database}])
            logger.info(f"User '{user}' created successfully with role '{role}'.")
        except Exception as e:
            logger.error(f"Error creating user '{user}': {e}")


    def delete_user(self, database: str, user: str) -> None:
            """
            Delete a user from the specified MongoDB database.

            Parameters:
            - database (str): The name of the database from which the user will be deleted.
            - user (str): The username of the user to be deleted.

            Returns:
            - None
            """
            db = self.client[database]
            try:
                # Use the 'dropUser' command to delete the user
                db.command("dropUser", user)
                logger.info(f"User '{user}' deleted successfully from database '{database}'.")
            except Exception as e:
                logger.error(f"Error deleting user '{user}' from database '{database}': {e}")
