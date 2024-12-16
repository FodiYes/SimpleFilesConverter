# File Converter

A powerful and user-friendly file conversion tool built with Python. Convert between various text and image formats with ease.

![Made with Love by DAN](https://forthebadge.com/images/badges/built-with-love.svg)

## Features

- **Multi-Format Support**:
  - Text Formats: CSV, JSON, XML, TXT
  - Image Formats: JPG/JPEG, PNG, BMP, GIF, TIFF
  
- **User-Friendly Interface**:
  - Intuitive GUI built with Tkinter
  - Progress tracking for conversions
  - Clear error messages and warnings
  
- **Batch Processing**:
  - Convert multiple files at once
  - Maintain original file names
  
- **Customizable Settings**:
  - CSV separator configuration
  - XML root tag customization
  - JSON indentation control

## Installation

1. Clone the repository:
```bash
git clone https://github.com/FodiYes/SimpleFilesConverter.git
cd SimpleFilesConverter
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. **Select Files**:
   - Click "Select Files" button
   - Choose one or multiple files to convert
   - Supported files will be automatically validated

2. **Choose Output Format**:
   - Select desired output format from dropdown
   - Formats are grouped by type (Text/Image)
   - Invalid conversions are prevented automatically

3. **Configure Settings** (if needed):
   - CSV separator (default: ',')
   - XML root tag (default: 'root')
   - JSON indent size (default: 2)

4. **Select Output Directory**:
   - Choose where to save converted files
   - Original filenames are preserved with new extensions

5. **Convert**:
   - Click "Convert" button
   - Progress bar shows conversion status
   - Success/error messages provide feedback

## Project Structure

```
FileConverter/
├── main.py              # Application entry point
├── requirements.txt     # Project dependencies
├── README.md           # Project documentation
├── modules/
│   ├── converter.py    # File conversion logic
│   ├── file_loader.py  # File handling and validation
│   └── ui.py          # User interface components
└── logs/               # Application logs
```

## Dependencies

- **Pillow**: Image processing
- **pandas**: CSV handling
- **tkinter**: GUI framework
- **json**: JSON processing
- **xml**: XML handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with ❤️ by DAN
- Inspired by the need for a simple, yet powerful file converter
- Thanks to all contributors and users

---

**Note**: Make sure you have all required dependencies installed before running the application. For any issues or feature requests, please open an issue on GitHub.
