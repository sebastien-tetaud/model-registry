# -*- coding: utf-8 -*-
import os
import json
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


    def store_model(self, database: str, collection: str, metadata: dict, model_path: str) -> bool:
        """
        Store a model file in MongoDB GridFS.

        Parameters:
        - client (MongoClient): The MongoClient instance for the MongoDB connection.
        - collection (str): The name of the collection in the MongoDB database.
        - database (str): The name of the database where the model will be stored.
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
        metadata['database'] = database
        query = create_query(query_file=metadata)
        logger.info("Searching for existing model...")
        fs_local, result_local = model_search(client=self.client, query=query)

        if not result_local:
            logger.info("Storing new model...")
            model_name = metadata['model_name']
            model_path = metadata['model_path']
            db = self.client[database]
            # Create a new GridFS bucket
            fs = gridfs.GridFS(db, collection=metadata['model_format'])
            with open(model_path, 'rb') as f:
                # Calculate and store the checksum value
                model_data = f.read()
                checksum = calculate_checksum(model_data)
                metadata['checksum'] = checksum
                model_id = fs.put(data=model_data, filename=model_name, metadata=metadata)

            logger.info(f"Model with ID: {model_id} successfully stored in {metadata['database']}")
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

    def search_model(self, database: str, collection: str, model_id: str):
        """
        Search for a model in the MongoDB GridFS by its model_id.

        Args:
            database (str): The name of the database to search within.
            collection (str): The name of the collection to search within.
            model_id (str): The ID of the model (in string format) to search for.

        Returns:
            dict: The document corresponding to the model, or None if not found.
        """
        db = self.client[database]
        collection_files = f"{collection}.files"
        collection = db[collection_files]

        # Convert model_id to ObjectId
        model_object_id = ObjectId(model_id)

        # Search for the model in the collection
        result = collection.find_one({"_id": model_object_id})

        return result

    def get_model(self, database: str, collection: str, model_id: str):
        """
        Retrieve a model file and its metadata from MongoDB GridFS and save them locally.

        Args:
            database (str): The name of the database.
            collection (str): The name of the collection containing the model.
            model_id (str): The ID of the model (in string format).

        Returns:
            dict: The document corresponding to the model, or None if not found.
        """
        db = self.client[database]
        fs = gridfs.GridFS(db, collection=collection)
        collection_files = f"{collection}.files"
        collection = db[collection_files]

        # Convert model_id to ObjectId
        model_object_id = ObjectId(model_id)

        # Find the model in the collection
        result = collection.find_one({"_id": model_object_id})

        if result:
            # Retrieve the model data and metadata
            model_id = result['_id']
            model_data = fs.get(model_id).read()
            metadata = result['metadata']

            # Prepare the local directory for saving the model and metadata
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_dir = os.path.join(current_dir, "model")

            if not os.path.exists(model_dir):
                os.makedirs(model_dir)

            # Save the model file
            model_filename = os.path.join(model_dir, f"{metadata['model_name']}.pt")
            with open(model_filename, 'wb') as model_file:
                model_file.write(model_data)

            # Save the metadata as a JSON file
            metadata_filename = os.path.join(model_dir, f"{metadata['model_name']}.json")
            with open(metadata_filename, "w") as metadata_file:
                json.dump(metadata, metadata_file)

        return result
