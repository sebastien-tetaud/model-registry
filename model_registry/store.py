# -*- coding: utf-8 -*-
import gridfs
from loguru import logger

from utils import calculate_checksum, create_query, get_username, model_search
from utils import generate_model_name


def store(client, metadata: dict, model_path: str, collection: str) -> bool:
    """
    Store a model file in MongoDB GridFS.

    Parameters:
    - client (MongoClient): The MongoClient instance for
    the MongoDB connection.
    - metadata (dict): A dictionary containing metadata
    about the model to be stored.
    - collection (str): collection name of the database

    Returns:
    - bool: True if the model is successfully stored, False otherwise.

    Workflow:
    - Adds the 'author' key to the metadata by fetching the username.
    - Creates a query based on the provided metadata for model search.
    - Searches for an existing model based on the query.
    - If an existing model is not found, stores the model file
    in GridFS under the specified application and format.
    - Logs the success or failure of storing the model
    along with its ID and application.
    """
    metadata = generate_model_name(config=metadata)
    metadata['author'] = get_username()
    metadata['model_path'] = model_path
    metadata['model_format'] = collection
    query = create_query(query_file=metadata)
    logger.info("Search for existing model...")
    fs_local, result_local = model_search(client=client, query=query)
    if not result_local:
        logger.info("Model storing...")
        model_name = metadata['model_name']
        model_path = metadata['model_path']
        db = client[metadata['model_application']]
        # Create a new GridFS bucket
        fs = gridfs.GridFS(db, collection=metadata['model_format'])
        with open(model_path, 'rb') as f:
            # Calculate and store the checksum value
            model_data = f.read()
            checksum = calculate_checksum(model_data)
            metadata['checksum'] = checksum
            model_id = fs.put(data=model_data,
                              filename=model_name,
                              metadata=metadata)

        logger.info(f"Model with ID: {model_id} successfully stored in \
                    {metadata['model_application']}")
        return True
    else:
        return False
