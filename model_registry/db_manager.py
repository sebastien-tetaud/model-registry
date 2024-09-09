# -*- coding: utf-8 -*-
import gridfs
from bson import ObjectId
from loguru import logger

from model_registry.utils import (calculate_checksum, create_query,
                                  generate_model_name, get_username,
                                  model_search)


class DbManager:
    def __init__(self, client: str):
        """
        Initialize the MongoUserManager with connection details.

        Parameters:
        - client (MongoClient): The MongoClient instance for the MongoDB connection.
        """
        self.client = client


    def store_model(self, db: str, collection: str, metadata: dict, model_path: str) -> bool:
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
        fs_local, result_local = model_search(client=self.client, query=query)

        if not result_local:
            logger.info("Storing new model...")
            model_name = metadata['model_name']
            model_path = metadata['model_path']
            db = self.client[db]
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

    def delete_model(self, database: str, collection:str, model_id: str):
        """
        Deletes a model from the MongoDB database using its ID.

        Args:
            client (pymongo.MongoClient): MongoDB client object.
            database (str): Name of the database.
            collection (str): Name of the collection within the database.
            model_id (str): ID of the model to be deleted.


        Returns:
            None
        """
        fs = gridfs.GridFSBucket(db=self.client[database], bucket_name=collection)
        model_object_id = ObjectId(model_id)
        try:
            result = fs.delete(model_object_id)
            if result is None:

                logger.info(f"model id {model_id}\
                            successfully deleted from db: \
                            {database} and collection: {collection}")

            else:

                logger.error(f"model id {model_id}\
                            not successfully deleted from db: \
                            {database} and collection: {collection}")
        except Exception as e:
            logger.error(e)
