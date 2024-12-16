import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self._setup_logger()

    def _setup_logger(self):
        """Setup logging configuration."""
        os.makedirs(self.log_dir, exist_ok=True)
        
        log_file = os.path.join(
            self.log_dir,
            f"converter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Logger initialized")
