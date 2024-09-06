from model_registry.store import store
from model_registry.connector import MongoDBConnector

def main():
    # Database connection details
    username = "username"
    password = "password"
    host = "ip_address"
    db_name = "db_name"
    collection = "your_collection"

    # Path to the model file
    model_path = "path/to/model.onnx"

    # Metadata for the model
    metadata = {
        "project_name": "ssh_mapping",
        "model_architecture": "AutoencoderCNN3D",
        "model_version": "0",
    }

    # Connect to MongoDB
    connector = MongoDBConnector(username, password, host, db_name)
    client = connector.connect()

    # Store the model in MongoDB GridFS
    success = store(client=client, db=db_name, collection=collection, metadata=metadata, model_path=model_path)

    if success:
        print("Model successfully stored.")
    else:
        print("Failed to store the model.")

if __name__ == "__main__":
    main()
