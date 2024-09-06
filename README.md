# Model Registry Library

A Python library for storing and managing machine learning models in MongoDB using GridFS.

## Features
- Store machine learning models in MongoDB's GridFS.
- Easily connect to MongoDB using `MongoDBConnector`.

## Installation

To install the library locally, follow these steps:

0. Create your python environment and activate it.

1. Clone the repository:
   ```bash
   git clone https://github.com/tetaud-sebastien/model-registry
   cd model-registry

   ```
2. Install the library:
   ```Bash
   pip install -e .
   ```
## Usage

### Connect to the Model Registry

```Python
username = "username"
password = "password"
host = "ip_address"
db_name = "db_name"

# Connect to MongoDB
connector = MongoDBConnector(username, password, host, db_name)
client = connector.connect()
```

### Store a Model in the Model Registry

```Python
collection = "your_collection"
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

```

## Information

Feel free to open an issues whether you want for reporting issues, improving documentation, or contributing code, your input is valuable.

## Contact

sebastien.tetaud@esa.int
