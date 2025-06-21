import os
import sqlite3
from pathlib import Path

def get_database_path():
    """
    Get the appropriate database path based on environment.
    For Railway, use a persistent volume or in-memory fallback.
    """
    # Check if we're in Railway environment
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        # Try to use Railway's persistent storage if available
        railway_db_path = '/opt/render/project/src/data/enrichment_activities.db'
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(railway_db_path), exist_ok=True)
        
        return railway_db_path
    else:
        # Local development
        return 'enrichment_activities.db'

def ensure_database_directory():
    """Ensure the database directory exists"""
    db_path = get_database_path()
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    return db_path
