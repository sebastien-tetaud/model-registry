from loguru import logger


def create_user(client, database: str, user: str, password: str, role: str) -> None:
    """
    Create a user in the specified MongoDB database with the given role and password.

    Parameters:
    - client (MongoClient): The MongoClient instance for the MongoDB connection.
    - database (str): The name of the database where the user will be created.
    - user (str): The username of the user to be created.
    - password (str): The password for the new user.
    - role (str): The role assigned to the user in the database.

    Returns:
    - None
    """
    db = client[database]
    try:
        db.command("createUser", user,
                   pwd=password,
                   roles=[{"role": role,
                           "db": database}])
        logger.info(f"User '{user}' created successfully with role '{role}'.")
    except Exception as e:
        logger.error(f"Error creating user '{user}': {e}")