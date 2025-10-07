"""
FastAPI Fundamentals Lab - Main Application
"""

from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging

from routers import books

# Create FastAPI instance
app = FastAPI(
    title="FastAPI Fundamentals Lab",
    description="""
    A hands-on lab to learn FastAPI basics through a book library API.
    
    ## Features
    
    * **Books**: Full CRUD operations for managing books
    * **Validation**: Comprehensive data validation with Pydantic
    * **Documentation**: Automatic interactive API documentation
    * **Filtering**: Advanced book filtering and pagination
    
    ## Getting Started
    
    1. Create some books using the POST /books/ endpoint
    2. Retrieve books using GET /books/ with optional filters
    3. Update or delete books using PUT and DELETE endpoints
    4. Check library statistics at /books/stats/summary
    """,
    version="1.0.0",
    contact={
        "name": "FastAPI Lab Support",
        "email": "support@fastapi-lab.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "invalid_value": error.get("input")
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation failed",
            "errors": errors,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    """Handle unexpected server errors."""
    logging.exception("Internal server error occurred")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

# Include routers
app.include_router(books.router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to FastAPI Fundamentals Lab!",
        "api_version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "docs": "/docs",
        "redoc": "/redoc",
        "features": [
            "Book management CRUD operations",
            "Advanced filtering and pagination", 
            "Automatic data validation",
            "Interactive API documentation",
            "Library statistics"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)