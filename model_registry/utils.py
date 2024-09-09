# -*- coding: utf-8 -*-
import hashlib
import os
import pwd
import secrets
import string

import gridfs
from loguru import logger


def generate_model_name(config: dict) -> dict:
    """
    Generate a unique model name based on provided
    configuration parameters.

    Parameters:
    - config (dict): A dictionary containing configuration
    parameters for model naming.


    Returns:
    - dict: The input 'config' dictionary updated with
    the generated 'model_name' key-value pair.

    """

    project_name = config["project_name"]
    model_architecture = config["model_architecture"]
    model_version = config["model_version"]
    model_name = project_name + "_" + "_" +\
        model_architecture + "_" + "V" + str(model_version)
    config['model_name'] = model_name
    return config


def create_query(query_file):

    """
    Args:
        query_file (dict): query file

    Returns:
        query: query dict to in order to query the a given model

    """
    query = {}
    for key, value in query_file.items():

        query[f"metadata.{key}"] = value
    return query


def model_search(client, query):
    """
    Args:
        query (dict): query to search for a model

    Returns:
        object_id: id of the model to query

    """

    db = query['metadata.database']
    collection = query['metadata.model_format']
    db = client[db]
    fs = gridfs.GridFS(database=db, collection=collection)
    # Query for specific documents
    collection = db[collection+".files"]
    result = collection.find_one(query)
    if result:
        logger.warning('Model already is in the database')
        return fs, result
    else:
        return None, None


def calculate_checksum(data: bytes)-> float:
    """
    Calculate the checksum value for the given data.

    Args:
        data (bytes): Data to calculate the checksum for.

    Returns:
        str: Checksum value.
    """
    checksum = hashlib.md5(data).hexdigest()
    return checksum


def get_username() -> str:
    return pwd.getpwuid(os.getuid())[0]


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