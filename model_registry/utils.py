# -*- coding: utf-8 -*-
import hashlib
import os
import pwd

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
    model_application = config["model_application"]
    model_architecture = config["model_architecture"]
    model_version = config["model_version"]
    model_name = project_name + "_" + model_application + "_" +\
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

    model_application = query['metadata.model_application']
    collection = query['metadata.model_format']
    db = client[model_application]
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
