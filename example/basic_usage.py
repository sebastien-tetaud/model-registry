from model_registry.connector import MongoDBConnector
from model_registry.db_manager import DbManager

def main():
    # Database connection details
    username = "username"
    password = "password"
    host = "ip_address"
    db_name = "db_name"
    collection = "your_collection"
    model_path = "/home/ubuntu/project/model.onnx"

    # Metadata for the model
    metadata = {
        "project_name": "llm",
        "model_application": "model_registry",
        "model_architecture": "AutoencoderCNN3D",
        "model_version": "0",
    }
    # Connect to MongoDB
    connector = MongoDBConnector(username, password, host, db_name)
    client = connector.connect()

    dm = DbManager(client=client)
    # Store the model in MongoDB GridFS
    dm.store_model(database=db_name,
                   collection=collection, metadata=metadata,
                   model_path=model_path)

if __name__ == "__main__":
    main()
