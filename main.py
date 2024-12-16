#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File Converter - Main Application Entry Point
Made with LOVE by FodiYes
"""

import logging
from modules.ui import MainWindow

def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Initialize and run the application."""
    setup_logging()
    app = MainWindow()
    app.run()

if __name__ == '__main__':
    main()
