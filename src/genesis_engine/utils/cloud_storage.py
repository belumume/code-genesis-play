"""
Cloud Storage Utility for AI Genesis Engine v2.3
Handles persistent storage of generated games using S3-compatible services.
"""
import os
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from botocore.config import Config

logger = logging.getLogger(__name__)

class CloudStorageManager:
    """
    Manages cloud storage operations for generated games.
    Supports S3-compatible services (AWS S3, Cloudflare R2, etc.)
    """
    
    def __init__(self):
        self.bucket_name = os.getenv("CLOUD_BUCKET_NAME", "ai-genesis-games")
        self.endpoint_url = os.getenv("CLOUD_ENDPOINT_URL")  # For R2 or other S3-compatible
        self.region_name = os.getenv("CLOUD_REGION", "auto")  # R2 uses "auto"
        self.public_url_base = os.getenv("CLOUD_PUBLIC_URL_BASE")  # Custom domain or R2 public URL
        
        # Initialize S3 client
        self.s3_client = self._init_s3_client()
        self._ensure_bucket_exists()
    
    def _init_s3_client(self):
        """Initialize S3 client with credentials from environment."""
        try:
            # Get credentials from environment
            access_key = os.getenv("CLOUD_ACCESS_KEY_ID")
            secret_key = os.getenv("CLOUD_SECRET_ACCESS_KEY")
            
            if not access_key or not secret_key:
                logger.warning("Cloud storage credentials not found in environment")
                return None
            
            # Configure client
            config_args = {
                "aws_access_key_id": access_key,
                "aws_secret_access_key": secret_key,
                "region_name": self.region_name,
                "config": Config(
                    signature_version='s3v4',
                    retries={'max_attempts': 3, 'mode': 'standard'}
                )
            }
            
            # Add endpoint URL if using S3-compatible service like R2
            if self.endpoint_url:
                config_args["endpoint_url"] = self.endpoint_url
            
            return boto3.client('s3', **config_args)
            
        except Exception as e:
            logger.error(f"Failed to initialize S3 client: {str(e)}")
            return None
    
    def _ensure_bucket_exists(self):
        """Ensure the bucket exists, create if it doesn't."""
        if not self.s3_client:
            return
        
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Bucket '{self.bucket_name}' exists and is accessible")
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                # Bucket doesn't exist, create it
                try:
                    if self.endpoint_url:  # R2 or similar
                        self.s3_client.create_bucket(Bucket=self.bucket_name)
                    else:  # AWS S3
                        if self.region_name == 'us-east-1':
                            self.s3_client.create_bucket(Bucket=self.bucket_name)
                        else:
                            self.s3_client.create_bucket(
                                Bucket=self.bucket_name,
                                CreateBucketConfiguration={'LocationConstraint': self.region_name}
                            )
                    logger.info(f"Created bucket '{self.bucket_name}'")
                except Exception as create_error:
                    logger.error(f"Failed to create bucket: {str(create_error)}")
            else:
                logger.error(f"Bucket access error: {str(e)}")
    
    def upload_game(self, local_file_path: Path, game_name: str) -> Optional[str]:
        """
        Upload a game file to cloud storage.
        
        Args:
            local_file_path: Path to the local game.html file
            game_name: Name of the game (used as folder in bucket)
            
        Returns:
            Public URL of the uploaded game, or None if upload failed
        """
        if not self.s3_client:
            logger.error("S3 client not initialized - cloud storage disabled")
            return None
        
        try:
            # Construct S3 key (path in bucket)
            file_name = local_file_path.name
            s3_key = f"games/{game_name}/{file_name}"
            
            # Read file content
            with open(local_file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content.encode('utf-8'),
                ContentType='text/html',
                CacheControl='public, max-age=3600'  # Cache for 1 hour
            )
            
            logger.info(f"Successfully uploaded {file_name} to cloud storage")
            
            # Generate public URL
            public_url = self._generate_public_url(s3_key)
            return public_url
            
        except FileNotFoundError:
            logger.error(f"File not found: {local_file_path}")
            return None
        except NoCredentialsError:
            logger.error("AWS credentials not available")
            return None
        except Exception as e:
            logger.error(f"Failed to upload game to cloud storage: {str(e)}")
            return None
    
    def upload_game_files(self, project_path: Path) -> Dict[str, str]:
        """
        Upload all game files from a project directory.
        
        Args:
            project_path: Path to the game project directory
            
        Returns:
            Dictionary mapping file names to their public URLs
        """
        uploaded_files = {}
        
        if not self.s3_client:
            logger.error("S3 client not initialized - cloud storage disabled")
            return uploaded_files
        
        game_name = project_path.name
        
        # Files to upload
        files_to_upload = [
            "game.html",
            "GDD.md",
            "TECH_PLAN.md",
            "README.md"
        ]
        
        for file_name in files_to_upload:
            file_path = project_path / file_name
            if file_path.exists():
                public_url = self.upload_game(file_path, game_name)
                if public_url:
                    uploaded_files[file_name] = public_url
        
        return uploaded_files
    
    def _generate_public_url(self, s3_key: str) -> str:
        """Generate public URL for an uploaded file."""
        if self.public_url_base:
            # Use custom domain or R2 public URL
            return f"{self.public_url_base.rstrip('/')}/{s3_key}"
        elif self.endpoint_url and "r2.cloudflarestorage.com" in self.endpoint_url:
            # Cloudflare R2 public URL pattern
            account_id = self.endpoint_url.split("//")[1].split(".")[0]
            return f"https://pub-{account_id}.r2.dev/{s3_key}"
        else:
            # Standard S3 URL
            return f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/{s3_key}"
    
    def get_game_url(self, game_name: str, file_name: str = "game.html") -> Optional[str]:
        """
        Get the public URL for a previously uploaded game.
        
        Args:
            game_name: Name of the game
            file_name: Name of the file (default: game.html)
            
        Returns:
            Public URL or None if not found
        """
        s3_key = f"games/{game_name}/{file_name}"
        
        try:
            # Check if object exists
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return self._generate_public_url(s3_key)
        except ClientError:
            return None
    
    def list_games(self) -> List[Dict[str, Any]]:
        """
        List all games in cloud storage.
        
        Returns:
            List of game metadata dictionaries
        """
        games = []
        
        if not self.s3_client:
            return games
        
        try:
            # List objects with prefix
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix="games/",
                Delimiter="/"
            )
            
            # Extract game names from "directories"
            if 'CommonPrefixes' in response:
                for prefix in response['CommonPrefixes']:
                    game_name = prefix['Prefix'].split('/')[-2]
                    games.append({
                        "name": game_name,
                        "url": self.get_game_url(game_name)
                    })
            
            return games
            
        except Exception as e:
            logger.error(f"Failed to list games: {str(e)}")
            return []
    
    def delete_game(self, game_name: str) -> bool:
        """
        Delete all files for a game from cloud storage.
        
        Args:
            game_name: Name of the game to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.s3_client:
            return False
        
        try:
            # List all objects for this game
            prefix = f"games/{game_name}/"
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            
            if 'Contents' in response:
                # Delete all objects
                objects = [{'Key': obj['Key']} for obj in response['Contents']]
                self.s3_client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={'Objects': objects}
                )
                logger.info(f"Deleted game '{game_name}' from cloud storage")
                return True
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete game: {str(e)}")
            return False
    
    def is_available(self) -> bool:
        """Check if cloud storage is available and configured."""
        return self.s3_client is not None


# Singleton instance
_cloud_storage_instance = None

def get_cloud_storage() -> CloudStorageManager:
    """Get the singleton cloud storage manager instance."""
    global _cloud_storage_instance
    if _cloud_storage_instance is None:
        _cloud_storage_instance = CloudStorageManager()
    return _cloud_storage_instance 