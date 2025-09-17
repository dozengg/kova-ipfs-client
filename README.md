# Kova IPFS Client

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/kova-ipfs-client.svg)](https://pypi.org/project/kova-ipfs-client/)
[![Build Status](https://github.com/kovasystems/kova-ipfs-client/workflows/CI/badge.svg)](https://github.com/kovasystems/kova-ipfs-client/actions)

**Python client for IPFS integration in the Kova ecosystem**

Kova IPFS Client is a high-performance Python library designed for seamless integration with the InterPlanetary File System (IPFS) within the Kova decentralized robotics network. It provides easy-to-use interfaces for storing and retrieving sensor data, managing content addressing, and handling distributed storage operations.

## Features

- **IPFS Node Management**: Easy connection and management of IPFS nodes
- **Data Storage & Retrieval**: Simple APIs for storing and retrieving data
- **Content Addressing**: Automatic content addressing and hash generation
- **Pinning Management**: Content pinning and unpinning operations
- **Metadata Handling**: Rich metadata support for stored content
- **Batch Operations**: Efficient batch processing for large datasets
- **Error Handling**: Comprehensive error handling and retry mechanisms
- **Async Support**: Full async/await support for high-performance applications
- **Progress Tracking**: Real-time progress tracking for long-running operations

## Installation

### From PyPI

```bash
pip install kova-ipfs-client
```

### From Source

```bash
git clone https://github.com/kovasystems/kova-ipfs-client.git
cd kova-ipfs-client
pip install -e .
```

### With Optional Dependencies

```bash
# Install with async support
pip install kova-ipfs-client[async]

# Install with CLI tools
pip install kova-ipfs-client[cli]

# Install with all features
pip install kova-ipfs-client[all]
```

## Quick Start

### Basic Usage

```python
from kova_ipfs_client import IPFSClient, IPFSConfig
import asyncio

# Create IPFS client
config = IPFSConfig(
    api_url="http://localhost:5001",
    gateway_url="http://localhost:8080",
    timeout=30
)

client = IPFSClient(config)

# Store data
data = b"Hello, Kova IPFS!"
hash_result = client.add_data(data)
print(f"Data stored with hash: {hash_result.hash}")

# Retrieve data
retrieved_data = client.get_data(hash_result.hash)
print(f"Retrieved data: {retrieved_data}")

# Pin content
client.pin(hash_result.hash)

# Unpin content
client.unpin(hash_result.hash)
```

### Async Usage

```python
import asyncio
from kova_ipfs_client import AsyncIPFSClient, IPFSConfig

async def main():
    config = IPFSConfig(
        api_url="http://localhost:5001",
        gateway_url="http://localhost:8080"
    )
    
    async with AsyncIPFSClient(config) as client:
        # Store data asynchronously
        data = b"Sensor data from Kova robot"
        hash_result = await client.add_data(data)
        
        # Retrieve data asynchronously
        retrieved_data = await client.get_data(hash_result.hash)
        
        # Batch operations
        hashes = await client.add_batch([b"data1", b"data2", b"data3"])
        
        print(f"Stored {len(hashes)} items")

asyncio.run(main())
```

### File Operations

```python
from kova_ipfs_client import IPFSClient, IPFSConfig
from pathlib import Path

# Create client
client = IPFSClient(IPFSConfig())

# Add file
file_path = Path("sensor_data.json")
hash_result = client.add_file(file_path)
print(f"File added with hash: {hash_result.hash}")

# Add directory
dir_path = Path("sensor_data/")
hash_result = client.add_directory(dir_path)
print(f"Directory added with hash: {hash_result.hash}")

# Get file
client.get_file(hash_result.hash, "downloaded_data.json")

# Get directory
client.get_directory(hash_result.hash, "downloaded_data/")
```

## API Reference

### IPFSClient Class

```python
from kova_ipfs_client import IPFSClient, IPFSConfig

# Configuration
config = IPFSConfig(
    api_url="http://localhost:5001",
    gateway_url="http://localhost:8080",
    timeout=30,
    retry_attempts=3,
    pin_on_add=True
)

# Create client
client = IPFSClient(config)

# Basic operations
hash_result = client.add_data(b"data")
data = client.get_data("QmHash...")
client.pin("QmHash...")
client.unpin("QmHash...")

# File operations
hash_result = client.add_file("path/to/file.txt")
client.get_file("QmHash...", "output.txt")

# Directory operations
hash_result = client.add_directory("path/to/directory/")
client.get_directory("QmHash...", "output_directory/")

# Metadata operations
metadata = client.get_metadata("QmHash...")
client.set_metadata("QmHash...", {"sensor_id": "camera_001"})
```

### AsyncIPFSClient Class

```python
import asyncio
from kova_ipfs_client import AsyncIPFSClient, IPFSConfig

async def main():
    config = IPFSConfig()
    
    async with AsyncIPFSClient(config) as client:
        # Async operations
        hash_result = await client.add_data(b"data")
        data = await client.get_data(hash_result.hash)
        
        # Batch operations
        hashes = await client.add_batch([b"data1", b"data2"])
        data_batch = await client.get_batch(hashes)
        
        # Progress tracking
        async for progress in client.add_large_file("large_file.bin"):
            print(f"Progress: {progress.percentage:.1f}%")

asyncio.run(main())
```

### Configuration Options

```python
from kova_ipfs_client import IPFSConfig

config = IPFSConfig(
    # API endpoint
    api_url="http://localhost:5001",
    
    # Gateway endpoint
    gateway_url="http://localhost:8080",
    
    # Timeout settings
    timeout=30,
    connect_timeout=10,
    
    # Retry settings
    retry_attempts=3,
    retry_delay=1.0,
    
    # Pin settings
    pin_on_add=True,
    pin_timeout=60,
    
    # Chunk settings
    chunk_size=1024 * 1024,  # 1MB
    max_chunk_size=10 * 1024 * 1024,  # 10MB
    
    # Progress settings
    enable_progress=True,
    progress_interval=0.1,
    
    # Logging
    log_level="INFO",
    enable_logging=True
)
```

## Advanced Features

### Content Addressing

```python
from kova_ipfs_client import IPFSClient, ContentAddress

# Create client
client = IPFSClient()

# Add data with custom content addressing
data = b"Sensor data"
hash_result = client.add_data(data, cid_version=1, hash_function="sha2-256")

# Get content address information
content_address = ContentAddress.from_hash(hash_result.hash)
print(f"CID Version: {content_address.version}")
print(f"Hash Function: {content_address.hash_function}")
print(f"Multibase: {content_address.multibase}")
```

### Metadata Management

```python
from kova_ipfs_client import IPFSClient, Metadata

# Create client
client = IPFSClient()

# Add data with metadata
data = b"Sensor data"
metadata = Metadata(
    sensor_id="camera_001",
    timestamp="2024-01-01T00:00:00Z",
    data_type="image",
    quality_score=0.95
)

hash_result = client.add_data_with_metadata(data, metadata)

# Retrieve metadata
retrieved_metadata = client.get_metadata(hash_result.hash)
print(f"Sensor ID: {retrieved_metadata.sensor_id}")
print(f"Quality Score: {retrieved_metadata.quality_score}")
```

### Batch Operations

```python
from kova_ipfs_client import IPFSClient, BatchOperation

# Create client
client = IPFSClient()

# Batch add data
data_items = [
    b"Sensor data 1",
    b"Sensor data 2", 
    b"Sensor data 3"
]

batch_result = client.add_batch(data_items)
print(f"Added {len(batch_result.hashes)} items")

# Batch get data
retrieved_data = client.get_batch(batch_result.hashes)

# Batch pin operations
pin_result = client.pin_batch(batch_result.hashes)
print(f"Pinned {pin_result.success_count} items")
```

### Progress Tracking

```python
from kova_ipfs_client import IPFSClient, ProgressCallback

# Create client with progress tracking
client = IPFSClient(enable_progress=True)

# Define progress callback
def progress_callback(progress):
    print(f"Progress: {progress.percentage:.1f}% - {progress.message}")

# Add large file with progress tracking
hash_result = client.add_file_with_progress(
    "large_sensor_data.bin",
    progress_callback=progress_callback
)
```

## CLI Tools

### Basic CLI

```bash
# Add file to IPFS
kova-ipfs add sensor_data.json

# Get file from IPFS
kova-ipfs get QmHash... --output downloaded_data.json

# Pin content
kova-ipfs pin QmHash...

# Unpin content
kova-ipfs unpin QmHash...

# List pinned content
kova-ipfs list-pins
```

### Advanced CLI

```bash
# Add directory with metadata
kova-ipfs add-dir sensor_data/ --metadata '{"sensor_id": "camera_001"}'

# Batch add files
kova-ipfs add-batch data/*.json --output hashes.txt

# Get with progress
kova-ipfs get QmHash... --output data/ --progress

# Sync with remote IPFS node
kova-ipfs sync --remote-node /ip4/192.168.1.100/tcp/5001
```

### Configuration CLI

```bash
# Set configuration
kova-ipfs config set api_url http://localhost:5001
kova-ipfs config set gateway_url http://localhost:8080
kova-ipfs config set timeout 30

# Show configuration
kova-ipfs config show

# Test connection
kova-ipfs test-connection
```

## Integration Examples

### With Kova Core

```python
from kova_ipfs_client import IPFSClient
from kova_core import SensorData, BlockchainManager

# Initialize IPFS client
ipfs_client = IPFSClient()

# Initialize blockchain manager
blockchain_manager = BlockchainManager()

# Process sensor data
def process_sensor_data(sensor_data: SensorData):
    # Store on IPFS
    hash_result = ipfs_client.add_data(sensor_data.data)
    
    # Submit to blockchain with IPFS hash
    contribution = Contribution(
        sensor_data_hash=hash_result.hash,
        validator_signature=sensor_data.signature,
        timestamp=sensor_data.timestamp,
        quality_score=sensor_data.quality_score
    )
    
    blockchain_manager.submit_contribution(contribution)
```

### With ROS2 Bridge

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from kova_ipfs_client import IPFSClient

class KovaIPFSNode(Node):
    def __init__(self):
        super().__init__('kova_ipfs_node')
        
        # Initialize IPFS client
        self.ipfs_client = IPFSClient()
        
        # Subscribe to sensor data
        self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
    
    def image_callback(self, msg):
        # Convert ROS2 message to bytes
        data = self.bridge.imgmsg_to_cv2(msg)
        data_bytes = cv2.imencode('.jpg', data)[1].tobytes()
        
        # Store on IPFS
        hash_result = self.ipfs_client.add_data(data_bytes)
        
        self.get_logger().info(f"Image stored with hash: {hash_result.hash}")

def main():
    rclpy.init()
    node = KovaIPFSNode()
    rclpy.spin(node)
    rclpy.shutdown()
```

### With Sensor Utils

```python
from kova_ipfs_client import IPFSClient
from kova_sensor_utils import ImageProcessor, PointCloudProcessor

# Initialize processors
image_processor = ImageProcessor()
pc_processor = PointCloudProcessor()
ipfs_client = IPFSClient()

# Process and store image
def process_and_store_image(image_path):
    # Process image
    processed_image = image_processor.enhance(image_path)
    
    # Convert to bytes
    image_bytes = processed_image.tobytes()
    
    # Store on IPFS
    hash_result = ipfs_client.add_data(image_bytes)
    
    return hash_result.hash

# Process and store point cloud
def process_and_store_pointcloud(pc_path):
    # Process point cloud
    processed_pc = pc_processor.filter_outliers(pc_path)
    
    # Convert to bytes
    pc_bytes = processed_pc.serialize()
    
    # Store on IPFS
    hash_result = ipfs_client.add_data(pc_bytes)
    
    return hash_result.hash
```

## Error Handling

### Exception Types

```python
from kova_ipfs_client import (
    IPFSError,
    ConnectionError,
    TimeoutError,
    ValidationError,
    NotFoundError
)

try:
    client = IPFSClient()
    data = client.get_data("invalid_hash")
except NotFoundError:
    print("Content not found")
except TimeoutError:
    print("Operation timed out")
except ConnectionError:
    print("Failed to connect to IPFS node")
except IPFSError as e:
    print(f"IPFS error: {e}")
```

### Retry Mechanisms

```python
from kova_ipfs_client import IPFSClient, RetryConfig

# Configure retry behavior
retry_config = RetryConfig(
    max_attempts=5,
    base_delay=1.0,
    max_delay=60.0,
    exponential_backoff=True
)

client = IPFSClient(retry_config=retry_config)

# Operations will automatically retry on failure
hash_result = client.add_data(b"data")
```

## Performance Optimization

### Connection Pooling

```python
from kova_ipfs_client import IPFSClient, ConnectionPoolConfig

# Configure connection pooling
pool_config = ConnectionPoolConfig(
    max_connections=10,
    max_keepalive_connections=5,
    keepalive_timeout=30
)

client = IPFSClient(connection_pool_config=pool_config)
```

### Caching

```python
from kova_ipfs_client import IPFSClient, CacheConfig

# Configure caching
cache_config = CacheConfig(
    enable_cache=True,
    max_cache_size=1000,
    cache_ttl=3600  # 1 hour
)

client = IPFSClient(cache_config=cache_config)
```

### Compression

```python
from kova_ipfs_client import IPFSClient, CompressionConfig

# Configure compression
compression_config = CompressionConfig(
    enable_compression=True,
    compression_level=6,
    min_size_for_compression=1024  # 1KB
)

client = IPFSClient(compression_config=compression_config)
```

## Testing

### Unit Tests

```bash
# Run unit tests
pytest tests/unit/

# Run with coverage
pytest --cov=kova_ipfs_client tests/unit/
```

### Integration Tests

```bash
# Run integration tests (requires IPFS node)
pytest tests/integration/

# Run with specific IPFS node
IPFS_API_URL=http://localhost:5001 pytest tests/integration/
```

### Performance Tests

```bash
# Run performance tests
pytest tests/performance/

# Run benchmark
python -m kova_ipfs_client.benchmark
```

## Monitoring

### Metrics

```python
from kova_ipfs_client import IPFSClient, MetricsCollector

# Enable metrics collection
metrics = MetricsCollector()
client = IPFSClient(metrics_collector=metrics)

# Get metrics
metrics_data = metrics.get_metrics()
print(f"Total operations: {metrics_data.total_operations}")
print(f"Success rate: {metrics_data.success_rate:.2%}")
print(f"Average latency: {metrics_data.average_latency:.2f}s")
```

### Logging

```python
import logging
from kova_ipfs_client import IPFSClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('kova_ipfs_client')

# Create client with logging
client = IPFSClient(logger=logger)
```

## Deployment

### Docker

```dockerfile
FROM python:3.9-slim

# Install IPFS
RUN apt-get update && apt-get install -y \
    wget \
    && wget https://dist.ipfs.io/go-ipfs/v0.14.0/go-ipfs_v0.14.0_linux-amd64.tar.gz \
    && tar -xzf go-ipfs_v0.14.0_linux-amd64.tar.gz \
    && mv go-ipfs/ipfs /usr/local/bin/ \
    && rm -rf go-ipfs*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . /app
WORKDIR /app

# Start IPFS daemon and application
CMD ["sh", "-c", "ipfs daemon & python app.py"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kova-ipfs-client
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kova-ipfs-client
  template:
    metadata:
      labels:
        app: kova-ipfs-client
    spec:
      containers:
      - name: kova-ipfs-client
        image: kovasystems/kova-ipfs-client:latest
        env:
        - name: IPFS_API_URL
          value: "http://ipfs-node:5001"
        - name: IPFS_GATEWAY_URL
          value: "http://ipfs-gateway:8080"
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "200m"
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment
4. Install development dependencies
5. Make your changes
6. Add tests
7. Run the test suite
8. Submit a pull request

```bash
git clone https://github.com/your-username/kova-ipfs-client.git
cd kova-ipfs-client
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Website](https://www.kova.systems/)
- [Documentation](https://docs.kova.systems/ipfs-client/)
- [Discord](https://discord.gg/kova)
- [Twitter](https://twitter.com/KovaSystems)

## Acknowledgments

- The IPFS team for the InterPlanetary File System
- The Python community for excellent networking libraries
- The Kova Systems team for the integration requirements

---

**Made with ❤️ by the Kova Systems team**