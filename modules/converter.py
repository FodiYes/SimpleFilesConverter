#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Format Converter Module - Handles file format conversions
Made with LOVE by FodiYes
"""

import os
import json
import logging
import pandas as pd
import xml.etree.ElementTree as ET
from PIL import Image
from typing import Dict, Any, Optional
from .file_loader import FileType

class FormatConverter:
    """Handles conversion between different file formats."""
    
    def __init__(self):
        """Initialize converter with supported format conversions."""
        self.logger = logging.getLogger(__name__)
        self._init_conversion_map()
    
    def _init_conversion_map(self):
        """Initialize the format conversion mapping."""
        self.conversion_map = {
            FileType.TEXT: {
                'csv': ['json', 'xml', 'txt'],
                'json': ['csv', 'xml', 'txt'],
                'xml': ['json', 'csv', 'txt'],
                'txt': ['json', 'csv', 'xml']
            },
            FileType.IMAGE: {
                'jpg': ['png', 'bmp', 'gif', 'tiff'],
                'jpeg': ['png', 'bmp', 'gif', 'tiff'],
                'png': ['jpg', 'bmp', 'gif', 'tiff'],
                'bmp': ['jpg', 'png', 'gif', 'tiff'],
                'gif': ['jpg', 'png', 'bmp', 'tiff'],
                'tiff': ['jpg', 'png', 'bmp', 'gif']
            }
        }

    def can_convert(self, input_format: str, output_format: str) -> bool:
        """
        Check if conversion between formats is possible.
        
        Args:
            input_format: Source file format
            output_format: Target file format
            
        Returns:
            True if conversion is possible, False otherwise
        """
        for type_formats in self.conversion_map.values():
            if input_format in type_formats:
                return output_format in type_formats[input_format]
        return False

    def convert(self, input_path: str, output_format: str, settings: Dict[str, Any]) -> Any:
        """
        Convert file to specified format.
        
        Args:
            input_path: Path to input file
            output_format: Target format
            settings: Conversion settings
            
        Returns:
            Converted content or None if conversion failed
        """
        try:
            input_format = os.path.splitext(input_path)[1][1:].lower()
            
            if input_format in self.conversion_map[FileType.TEXT]:
                return self._convert_text(input_path, input_format, output_format, settings)
            elif input_format in self.conversion_map[FileType.IMAGE]:
                return self._convert_image(input_path, output_format)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Conversion error: {str(e)}")
            return None

    def _convert_text(self, input_path: str, input_format: str, output_format: str, settings: Dict[str, Any]) -> Any:
        """Convert between text-based formats."""
        try:
            data = self._load_text_data(input_path, input_format)
            
            if data is None:
                return None
            
            return self._save_text_data(data, output_format, settings)
            
        except Exception as e:
            self.logger.error(f"Text conversion error: {str(e)}")
            return None
    
    def _load_text_data(self, input_path: str, input_format: str) -> Any:
        """Load data from text-based file formats."""
        if input_format == 'csv':
            return pd.read_csv(input_path).to_dict('records')
        elif input_format == 'json':
            with open(input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif input_format == 'xml':
            tree = ET.parse(input_path)
            return self._xml_to_dict(tree.getroot())
        elif input_format == 'txt':
            with open(input_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def _save_text_data(self, data: Any, output_format: str, settings: Dict[str, Any]) -> str:
        """Convert data to specified text format."""
        if output_format == 'csv':
            return pd.DataFrame(data).to_csv(index=False)
        elif output_format == 'json':
            return json.dumps(data, indent=int(settings.get('json_indent', 2)))
        elif output_format == 'xml':
            root = ET.Element(settings.get('xml_root', 'root'))
            self._dict_to_xml(data, root)
            return ET.tostring(root, encoding='unicode', method='xml')
        elif output_format == 'txt':
            return str(data)
        return None

    def _convert_image(self, input_path: str, output_format: str) -> Optional[Image.Image]:
        """
        Convert image to specified format.
        
        Handles RGBA/LA images by converting them to RGB with white background.
        """
        try:
            image = Image.open(input_path)
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            return image
        except Exception as e:
            self.logger.error(f"Image conversion error: {str(e)}")
            return None

    def save_file(self, content: Any, output_path: str) -> bool:
        """
        Save converted content to file.
        
        Args:
            content: Converted file content
            output_path: Path to save the file
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            if isinstance(content, str):
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            elif isinstance(content, Image.Image):
                content.save(output_path)
            else:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Save error: {str(e)}")
            return False

    def _xml_to_dict(self, element: ET.Element) -> Dict:
        """Convert XML element to dictionary."""
        result = {}
        
        for child in element:
            if len(child) == 0:
                result[child.tag] = child.text
            else:
                result[child.tag] = self._xml_to_dict(child)
        
        return result

    def _dict_to_xml(self, data: Any, parent: ET.Element):
        """Convert dictionary/list to XML elements."""
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, str(key))
                self._dict_to_xml(value, child)
        elif isinstance(data, list):
            for item in data:
                child = ET.SubElement(parent, 'item')
                self._dict_to_xml(item, child)
        else:
            parent.text = str(data)
