"""
Custom exceptions for Kova IPFS Client
"""


class IPFSError(Exception):
    """Base exception for IPFS operations"""
    pass


class IPFSConnectionError(IPFSError):
    """Exception raised when connection to IPFS daemon fails"""
    pass


class IPFSTimeoutError(IPFSError):
    """Exception raised when IPFS operation times out"""
    pass
