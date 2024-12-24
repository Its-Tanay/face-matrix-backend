# Face Recognition System

A facial recognition system that can detect faces, extract features, and match faces against a database of users.

## Features

- Face detection using MTCNN (Multi-Task Cascaded Convolutional Networks).
- Feature extraction using InceptionResnetV1 pre-trained on VGGFace2.
- Similarity search using cosine distance.
- PostgreSQL with pgvector for similarity search.
- REST API endpoints for user recognition and addition.
- Docker support.

## Prerequisites

- Python 3.9 or higher
- PostgreSQL with pgvector extension
- CUDA-capable GPU (optional, for good performance)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd face-recognition-system
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (config.py):
```bash
export DB_CONNECTION_STRING="postgresql://user:password@localhost:5432/dbname"
```

## Running with Docker

1. Build the Docker image:
```bash
docker build -t face-recognition-system .
```

2. Run the container:
```bash
docker run -p 8000:8000 \
  -e DB_CONNECTION_STRING="postgresql://user:password@db:5432/dbname" \
  face-recognition-system
```

## API Endpoints

### 1. Recognize User
- **URL**: `/api/recogniseUser`
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Request Body**: 
  - `image`: Image file containing a face
- **Response**:
  ```json
  {
    "status": "success",
    "message": "User recognised",
    "user": {
      "userId": "uuid",
      "name": "Hritik Roshan"
    }
  }
  ```
  or
  ```json
  {
    "status": "no_match",
    "message": "No matching user found.",
    "reqId": "cache-key"
  }
  ```

### 2. Add User
- **URL**: `/api/addUser`
- **Method**: POST
- **Content-Type**: application/json
- **Request Body**:
  ```json
  {
    "name": "Hritik Roshan",
    "birthdate": "1990-01-01",
    "reqId": "cache-key"
  }
  ```
- **Response**:
  ```json
  {
    "message": "Hritik Roshan was added",
    "userId": "uuid"
  }
  ```

## Project Structure

```
face-recognition-system/
├── app/
│   ├── services/
│   │   ├── faceDetectionService.py
│   │   ├── featureExtractionService.py
│   │   ├── similaritySearchService.py
│   │   └── userManagementService.py
│   ├── routes/
│   │   ├── recogniseUser.py
│   │   └── addUser.py
│   ├── models/
│   │   └── user.py
│   ├── database/
│   │   ├── db.py
│   │   └── userSchema.py
│   └── exception/
│       └── exceptions.py
├── main.py
├── requirements.txt
└── Dockerfile
```

## Error Handling

- 400: Bad Request
- 404: Resource Not Found
- 409: Duplicate Entry
- 500: Internal Server Error
- 503: Service Unavailable
- 400: Face Not Detected
- 400: Low Similarity Score

## Development

To run the application in development mode:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b username/feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin username/feature`)
5. Open a Merge Request

## Acknowledgments

- [FaceNet PyTorch](https://github.com/timesler/facenet-pytorch) for MTCNN and InceptionResnetV1 implementations
- [pgvector](https://github.com/pgvector/pgvector) for vector similarity search in PostgreSQL