# -*- coding: utf-8 -*-
import gridfs
from loguru import logger

from model_registry.utils import calculate_checksum, create_query, get_username, model_search
from model_registry.utils import generate_model_name


def store(client,db: str, collection: str, metadata: dict, model_path: str) -> bool:
    """
    Store a model file in MongoDB GridFS.

    Parameters:
    - client (MongoClient): The MongoClient instance for the MongoDB connection.
    - collection (str): The name of the collection in the MongoDB database.
    - db (str): The name of the database where the model will be stored.
    - metadata (dict): A dictionary containing metadata about the model to be stored.
    - model_path (str): The file path to the model that needs to be stored.

    Returns:
    - bool: True if the model is successfully stored, False otherwise.

    Workflow:
    - Adds the 'author' key to the metadata by fetching the username.
    - Creates a query based on the provided metadata to search for an existing model.
    - Searches for an existing model using the generated query.
    - If no existing model is found, stores the model file in GridFS under the specified collection.
    - Logs the success or failure of storing the model, including its ID and application details.
    """
    metadata = generate_model_name(config=metadata)
    metadata['author'] = get_username()
    metadata['model_path'] = model_path
    metadata['model_format'] = collection
    metadata['db'] = db
    query = create_query(query_file=metadata)
    logger.info("Searching for existing model...")
    fs_local, result_local = model_search(client=client, query=query)

    if not result_local:
        logger.info("Storing new model...")
        model_name = metadata['model_name']
        model_path = metadata['model_path']
        db = client[db]
        # Create a new GridFS bucket
        fs = gridfs.GridFS(db, collection=metadata['model_format'])
        with open(model_path, 'rb') as f:
            # Calculate and store the checksum value
            model_data = f.read()
            checksum = calculate_checksum(model_data)
            metadata['checksum'] = checksum
            model_id = fs.put(data=model_data, filename=model_name, metadata=metadata)

        logger.info(f"Model with ID: {model_id} successfully stored in {metadata['db']}")
        return True
    else:
        return False

