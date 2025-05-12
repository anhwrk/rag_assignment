from core.exceptions.base import CustomException
from http import HTTPStatus

class MongoDBBaseException(CustomException):
    """Base exception for MongoDB related errors"""
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = "MongoDB operation failed"

class MongoDBConnectionException(MongoDBBaseException):
    """Raised when unable to connect to MongoDB"""
    message = "Failed to establish connection with MongoDB"

class MongoDBIndexException(MongoDBBaseException):
    """Raised when there are issues with MongoDB indexes"""
    message = "MongoDB index operation failed"

class VectorIndexNotFoundException(MongoDBIndexException):
    """Raised when vector index is not found"""
    error_code = HTTPStatus.NOT_FOUND
    message = "Vector search index not found"

class VectorSearchException(MongoDBBaseException):
    """Raised when vector search operation fails"""
    message = "Vector search operation failed"

class InvalidVectorDimensionException(MongoDBBaseException):
    """Raised when vector dimensions don't match index requirements"""
    error_code = HTTPStatus.BAD_REQUEST
    message = "Invalid vector dimensions for search operation"

class MongoDBQueryException(MongoDBBaseException):
    """Raised when MongoDB query execution fails"""
    message = "MongoDB query execution failed"

class MongoDBTimeoutException(MongoDBBaseException):
    """Raised when MongoDB operation times out"""
    error_code = HTTPStatus.REQUEST_TIMEOUT
    message = "MongoDB operation timed out"

class MongoDBAuthenticationException(MongoDBBaseException):
    """Raised when MongoDB authentication fails"""
    error_code = HTTPStatus.UNAUTHORIZED
    message = "MongoDB authentication failed"

class MongoDBValidationException(MongoDBBaseException):
    """Raised when MongoDB document validation fails"""
    error_code = HTTPStatus.BAD_REQUEST
    message = "MongoDB document validation failed"

class MongoDBParameterException(MongoDBBaseException):
    """Raised when MongoDB parameter validation fails"""
    error_code = HTTPStatus.BAD_REQUEST
    message = "MongoDB parameter validation failed"

class MongoDBVectorSearchException(MongoDBBaseException):
    """Raised when MongoDB vector search operation fails"""
    message = "MongoDB vector search operation failed"

