"""
IPFS Client implementation for Kova Systems
"""

import asyncio
import json
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
import aiohttp
import ipfshttpclient
from .exceptions import IPFSError, IPFSConnectionError, IPFSTimeoutError


class IPFSClient:
    """Main IPFS client for the Kova ecosystem"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 5001, protocol: str = "http"):
        """
        Initialize IPFS client
        
        Args:
            host: IPFS daemon host
            port: IPFS daemon port
            protocol: Protocol to use (http/https)
        """
        self.host = host
        self.port = port
        self.protocol = protocol
        self.api_url = f"{protocol}://{host}:{port}/api/v0"
        self._client = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
        
    async def connect(self):
        """Connect to IPFS daemon"""
        try:
            self._client = ipfshttpclient.connect(f"/{self.protocol}/{self.host}/{self.port}")
        except Exception as e:
            raise IPFSConnectionError(f"Failed to connect to IPFS daemon: {e}")
            
    async def close(self):
        """Close connection to IPFS daemon"""
        if self._client:
            self._client.close()
            
    async def add_file(self, file_path: Union[str, Path], pin: bool = True) -> str:
        """
        Add a file to IPFS
        
        Args:
            file_path: Path to file to add
            pin: Whether to pin the file
            
        Returns:
            IPFS hash of the added file
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise IPFSError(f"File not found: {file_path}")
                
            result = self._client.add(str(file_path), pin=pin)
            return result["Hash"]
            
        except Exception as e:
            raise IPFSError(f"Failed to add file: {e}")
            
    async def add_data(self, data: Union[str, bytes, dict], pin: bool = True) -> str:
        """
        Add data to IPFS
        
        Args:
            data: Data to add (string, bytes, or dict)
            pin: Whether to pin the data
            
        Returns:
            IPFS hash of the added data
        """
        try:
            if isinstance(data, dict):
                data = json.dumps(data).encode()
            elif isinstance(data, str):
                data = data.encode()
                
            result = self._client.add_bytes(data, pin=pin)
            return result
            
        except Exception as e:
            raise IPFSError(f"Failed to add data: {e}")
            
    async def get_file(self, hash: str, output_path: Optional[Union[str, Path]] = None) -> bytes:
        """
        Get file from IPFS
        
        Args:
            hash: IPFS hash of the file
            output_path: Optional path to save the file
            
        Returns:
            File content as bytes
        """
        try:
            data = self._client.cat(hash)
            
            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(data)
                
            return data
            
        except Exception as e:
            raise IPFSError(f"Failed to get file: {e}")
            
    async def get_data(self, hash: str) -> Union[str, dict]:
        """
        Get data from IPFS and try to parse as JSON
        
        Args:
            hash: IPFS hash of the data
            
        Returns:
            Parsed data (string or dict)
        """
        try:
            data = self._client.cat(hash)
            
            # Try to parse as JSON
            try:
                return json.loads(data.decode())
            except (json.JSONDecodeError, UnicodeDecodeError):
                return data.decode()
                
        except Exception as e:
            raise IPFSError(f"Failed to get data: {e}")
            
    async def pin(self, hash: str) -> bool:
        """
        Pin content to local node
        
        Args:
            hash: IPFS hash to pin
            
        Returns:
            True if successful
        """
        try:
            self._client.pin.add(hash)
            return True
        except Exception as e:
            raise IPFSError(f"Failed to pin content: {e}")
            
    async def unpin(self, hash: str) -> bool:
        """
        Unpin content from local node
        
        Args:
            hash: IPFS hash to unpin
            
        Returns:
            True if successful
        """
        try:
            self._client.pin.rm(hash)
            return True
        except Exception as e:
            raise IPFSError(f"Failed to unpin content: {e}")
            
    async def list_pins(self) -> List[str]:
        """
        List all pinned hashes
        
        Returns:
            List of pinned IPFS hashes
        """
        try:
            pins = self._client.pin.ls(type="recursive")
            return [pin["Hash"] for pin in pins["Keys"].values()]
        except Exception as e:
            raise IPFSError(f"Failed to list pins: {e}")
            
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get IPFS node statistics
        
        Returns:
            Node statistics
        """
        try:
            return self._client.stats.bw()
        except Exception as e:
            raise IPFSError(f"Failed to get stats: {e}")
            
    async def is_connected(self) -> bool:
        """
        Check if connected to IPFS daemon
        
        Returns:
            True if connected
        """
        try:
            self._client.id()
            return True
        except:
            return False
