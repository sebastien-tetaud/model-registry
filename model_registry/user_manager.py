import secrets
import string
from loguru import logger


class PasswordGenerator:
    def __init__(self, length: int = 12, include_special_chars: bool = False):
        """
        Initialize the PasswordGenerator with the desired length and special character inclusion.

        Parameters:
        - length (int): The length of the generated password. Default is 12.
        - include_special_chars (bool): Whether to include special characters in the password. Default is True.
        """
        self.length = length
        self.include_special_chars = include_special_chars

    def generate(self) -> str:
        """
        Generate a secure password based on the specified length and character set.

        Returns:
        - str: A securely generated password.
        """
        # Define the character sets
        letters = string.ascii_letters
        digits = string.digits
        special_chars = string.punctuation

        # Combine character sets based on the inclusion of special characters
        if self.include_special_chars:
            characters = letters + digits + special_chars
        else:
            characters = letters + digits

        # Generate a secure password
        password = ''.join(secrets.choice(characters) for _ in range(self.length))
        return password


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
