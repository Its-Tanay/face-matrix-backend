# Model Repository

This directory contains the FaceNet model in ONNX format for Triton Inference Server.

## Structure

```
model_repository/
└── facenet/
    ├── config.pbtxt          # Triton model configuration
    └── 1/
        └── model.onnx        # FaceNet model (~90MB)
```

The model is pre-trained InceptionResNetV1 on VGGFace2, converted to ONNX. It generates 512-dimensional face embeddings from 160x160 face images.

## Configuration

By default, the model runs on CPU (`KIND_CPU` in config.pbtxt). To use GPU, change to `KIND_GPU` and ensure GPU runtime is enabled in docker-compose.yml.
