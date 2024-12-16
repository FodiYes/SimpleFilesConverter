#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Loader Module - Handles file operations and format validation
Made with LOVE by FodiYes
"""

import os
import json
import logging
import pandas as pd
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
from PIL import Image

class FileType:
    """File type constants."""
    TEXT = "text"
    IMAGE = "image"

class FileLoader:
    """Handles file loading, validation, and format management."""
    
    def __init__(self):
        """Initialize FileLoader with supported formats."""
        self.logger = logging.getLogger(__name__)
        self._init_formats()
    
    def _init_formats(self):
        """Initialize supported file formats."""
        self.formats = {
            FileType.TEXT: {
                'csv': {'ext': '.csv', 'name': 'CSV File'},
                'json': {'ext': '.json', 'name': 'JSON File'},
                'xml': {'ext': '.xml', 'name': 'XML File'},
                'txt': {'ext': '.txt', 'name': 'Text File'}
            },
            FileType.IMAGE: {
                'jpg': {'ext': '.jpg', 'name': 'JPEG Image'},
                'jpeg': {'ext': '.jpeg', 'name': 'JPEG Image'},
                'png': {'ext': '.png', 'name': 'PNG Image'},
                'bmp': {'ext': '.bmp', 'name': 'BMP Image'},
                'gif': {'ext': '.gif', 'name': 'GIF Image'},
                'tiff': {'ext': '.tiff', 'name': 'TIFF Image'}
            }
        }

    def get_format_type(self, file_path: str) -> Optional[str]:
        """
        Determine file type based on extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type or None if not supported
        """
        ext = os.path.splitext(file_path)[1][1:].lower()
        
        for type_name, formats in self.formats.items():
            if ext in [fmt['ext'][1:] for fmt in formats.values()]:
                return type_name
        return None

    def get_supported_formats(self) -> Dict[str, Dict]:
        """Get dictionary of supported formats."""
        return self.formats

    def validate_file(self, file_path: str) -> bool:
        """
        Validate file existence and format.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if file is valid, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                return False

            ext = os.path.splitext(file_path)[1][1:].lower()
            file_type = self.get_format_type(file_path)

            if file_type == FileType.TEXT:
                return self._validate_text_file(file_path, ext)
            elif file_type == FileType.IMAGE:
                return self._validate_image_file(file_path)
            
            return False

        except Exception as e:
            self.logger.error(f"File validation error: {str(e)}")
            return False
    
    def _validate_text_file(self, file_path: str, ext: str) -> bool:
        """Validate text-based file formats."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if ext == 'json':
                    json.load(f)
                elif ext == 'xml':
                    ET.parse(f)
                elif ext == 'csv':
                    pd.read_csv(f)
                else:
                    f.read()
            return True
        except Exception:
            return False
    
    def _validate_image_file(self, file_path: str) -> bool:
        """Validate image file formats."""
        try:
            with Image.open(file_path) as img:
                img.verify()
            return True
        except Exception:
            return False

    def load_file(self, file_path: str) -> Optional[str]:
        """
        Load and validate file.
        
        Args:
            file_path: Path to the file to load
            
        Returns:
            File path if successful, None otherwise
        """
        try:
            if not self.validate_file(file_path):
                return None
            
            self.logger.info(f"File {file_path} successfully loaded")
            return file_path
            
        except Exception as e:
            self.logger.error(f"File loading error: {str(e)}")
            return None
