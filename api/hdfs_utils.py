from hdfs import InsecureClient
from time import sleep
import logging

logger = logging.getLogger(__name__)

class HDFSClient:
    def __init__(self, namenode_url, max_retries=5):
        self.max_retries = max_retries
        self.client = self._connect_with_retry(namenode_url)
        self._ensure_directories()
    
    def _connect_with_retry(self, namenode_url):
        for attempt in range(self.max_retries):
            try:
                client = InsecureClient(namenode_url, user="root", timeout=30)
                client.status("/")  # Test connection
                return client
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                sleep(2 ** attempt)
                logger.warning(f"Intento {attempt + 1} de conexión a HDFS fallido. Reintentando...")
    
    def _ensure_directories(self):
        required_dirs = ["/uploads", "/processed"]
        for directory in required_dirs:
            if not self.client.status(directory, strict=False):
                self.client.makedirs(directory)
    
    def save_file(self, hdfs_path, local_path):
        try:
            return self.client.upload(hdfs_path, local_path, overwrite=True)
        except Exception as e:
            logger.error(f"Error guardando archivo en HDFS: {str(e)}")
            raise
    
    def read_file(self, hdfs_path):
        try:
            with self.client.read(hdfs_path) as reader:
                return reader.read()
        except Exception as e:
            logger.error(f"Error leyendo archivo de HDFS: {str(e)}")
            raise
    
    def delete_file(self, hdfs_path):
        try:
            self.client.delete(hdfs_path, recursive=True)
        except Exception as e:
            logger.error(f"Error eliminando archivo de HDFS: {str(e)}")
            raise