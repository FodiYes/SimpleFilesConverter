# Made with LOVE by FodiYes

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from typing import List, Dict, Any
import threading
from .file_loader import FileLoader, FileType
from .converter import FormatConverter
import logging

class ConversionThread:
    def __init__(self, files: List[str], output_format: str, settings: Dict[str, Any],
                 output_dir: str):
        self.files = files
        self.output_format = output_format
        self.settings = settings
        self.output_dir = output_dir
        self.file_loader = FileLoader()
        self.converter = FormatConverter()
        self.logger = logging.getLogger(__name__)

    def run(self):
        try:
            total_files = len(self.files)
            for i, file_path in enumerate(self.files, 1):
                try:
                    file_type = os.path.splitext(file_path)[1][1:].lower()
                    
                    data = self.file_loader.load_file(file_path)
                    if data is None:
                        raise Exception(f"Error loading file: {file_path}")

                    converted_content = self.converter.convert(data, self.output_format,
                                                            self.settings)
                    if not converted_content:
                        raise Exception(f"Error converting file: {file_path}")

                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_path = os.path.join(
                        self.output_dir,
                        f"{base_name}.{self.output_format}"
                    )

                    if not self.converter.save_file(converted_content, output_path):
                        raise Exception(f"Error saving file: {output_path}")

                    progress = (i / total_files) * 100
                    yield progress

                except Exception as e:
                    self.logger.error(f"Error processing file {file_path}: {str(e)}")
                    raise

        except Exception as e:
            self.logger.error(f"Conversion thread error: {str(e)}")
            raise

class MainWindow:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.window = tk.Tk()
        self.file_loader = FileLoader()
        self.converter = FormatConverter()
        self.init_ui()

    def init_ui(self):
        self.window.title('File Converter')
        self.window.geometry('600x400')

        self.selected_files = []
        self.output_dir = ""

        file_frame = ttk.Frame(self.window)
        file_frame.pack(fill='x', padx=5, pady=5)
        
        self.file_label = ttk.Label(file_frame, text='No files selected')
        self.file_label.pack(side='left')
        
        select_button = ttk.Button(file_frame, text='Select Files', command=self.select_files)
        select_button.pack(side='right')

        format_frame = ttk.Frame(self.window)
        format_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(format_frame, text='Output Format:').pack(side='left')
        
        formats = []
        supported_formats = self.file_loader.get_supported_formats()
        
        formats.append("=== Text Formats ===")
        formats.extend(supported_formats[FileType.TEXT].keys())
        
        formats.append("=== Image Formats ===")
        formats.extend(supported_formats[FileType.IMAGE].keys())
        
        self.format_combo = ttk.Combobox(format_frame, values=formats, state='readonly')
        self.format_combo.set(list(supported_formats[FileType.TEXT].keys())[0])
        self.format_combo.pack(side='right')

        settings_frame = ttk.LabelFrame(self.window, text='Settings')
        settings_frame.pack(fill='x', padx=5, pady=5)

        csv_frame = ttk.Frame(settings_frame)
        csv_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(csv_frame, text='CSV separator:').pack(side='left')
        self.csv_separator = ttk.Entry(csv_frame)
        self.csv_separator.insert(0, ',')
        self.csv_separator.pack(side='right')

        xml_frame = ttk.Frame(settings_frame)
        xml_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(xml_frame, text='XML root tag:').pack(side='left')
        self.xml_root = ttk.Entry(xml_frame)
        self.xml_root.insert(0, 'root')
        self.xml_root.pack(side='right')

        json_frame = ttk.Frame(settings_frame)
        json_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(json_frame, text='JSON indent:').pack(side='left')
        self.json_indent = ttk.Entry(json_frame)
        self.json_indent.insert(0, '2')
        self.json_indent.pack(side='right')

        output_frame = ttk.Frame(self.window)
        output_frame.pack(fill='x', padx=5, pady=5)
        
        self.output_label = ttk.Label(output_frame, text='Output directory not selected')
        self.output_label.pack(side='left')
        
        output_button = ttk.Button(output_frame, text='Select Output Directory', 
                                 command=self.select_output_dir)
        output_button.pack(side='right')

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.window, variable=self.progress_var,
                                          maximum=100)
        self.progress_bar.pack(fill='x', padx=5, pady=5)

        self.convert_button = ttk.Button(self.window, text='Convert',
                                       command=self.start_conversion, state='disabled')
        self.convert_button.pack(pady=5)

    def select_files(self):
        filetypes = [("All supported", "*.*")]
        
        for type_name, formats in self.file_loader.get_supported_formats().items():
            extensions = [fmt['ext'] for fmt in formats.values()]
            type_desc = "Text files" if type_name == FileType.TEXT else "Images"
            filetypes.append((type_desc, ";".join("*" + ext for ext in extensions)))
        
        files = filedialog.askopenfilenames(
            title="Select files",
            filetypes=filetypes
        )
        
        if files:
            valid_files = []
            for file_path in files:
                if self.file_loader.validate_file(file_path):
                    valid_files.append(file_path)
                else:
                    messagebox.showwarning(
                        "Warning",
                        f"File {os.path.basename(file_path)} is not supported or corrupted"
                    )
            
            self.selected_files = valid_files
            if valid_files:
                self.file_label.config(text=f'{len(valid_files)} files selected')
                self.update_convert_button()
            else:
                self.file_label.config(text='No files selected')

    def select_output_dir(self):
        directory = filedialog.askdirectory(title="Select output directory")
        if directory:
            self.output_dir = directory
            self.output_label.config(text=directory)
            self.update_convert_button()

    def update_convert_button(self):
        if self.selected_files and self.output_dir:
            self.convert_button.config(state='normal')
        else:
            self.convert_button.config(state='disabled')

    def get_settings(self) -> Dict[str, Any]:
        return {
            'separator': self.csv_separator.get(),
            'xml_root': self.xml_root.get(),
            'json_indent': self.json_indent.get()
        }

    def start_conversion(self):
        try:
            self.convert_button.config(state='disabled')
            output_format = self.format_combo.get()
            settings = self.get_settings()
            
            for file_path in self.selected_files:
                input_format = os.path.splitext(file_path)[1][1:].lower()
                if not self.converter.can_convert(input_format, output_format):
                    messagebox.showerror(
                        "Error",
                        f"Cannot convert {os.path.basename(file_path)} to {output_format}"
                    )
                    return
            
            self.progress_var.set(0)
            
            thread = threading.Thread(target=self.conversion_thread,
                                   args=(settings,))
            thread.daemon = True
            thread.start()

        except Exception as e:
            self.logger.error(f"Error starting conversion: {str(e)}")
            messagebox.showerror("Error", f"Error starting conversion: {str(e)}")
            self.convert_button.config(state='normal')

    def conversion_thread(self, settings: Dict[str, Any]):
        try:
            total_files = len(self.selected_files)
            output_format = self.format_combo.get()

            for i, file_path in enumerate(self.selected_files, 1):
                try:
                    converted_content = self.converter.convert(
                        file_path,
                        output_format,
                        settings
                    )
                    
                    if not converted_content:
                        self.window.after(0, messagebox.showerror, "Error",
                                       f"Error converting file: {file_path}")
                        continue

                    base_name = os.path.splitext(os.path.basename(file_path))[0]
                    output_path = os.path.join(
                        self.output_dir,
                        f"{base_name}.{output_format}"
                    )

                    if not self.converter.save_file(converted_content, output_path):
                        self.window.after(0, messagebox.showerror, "Error",
                                       f"Error saving file: {output_path}")
                        continue

                    progress = (i / total_files) * 100
                    self.window.after(0, self.progress_var.set, progress)

                except Exception as e:
                    self.logger.error(f"Error processing file {file_path}: {str(e)}")
                    self.window.after(0, messagebox.showerror, "Error",
                                   f"Error processing file {file_path}: {str(e)}")

            self.window.after(0, self.conversion_finished)

        except Exception as e:
            self.logger.error(f"Error in conversion thread: {str(e)}")
            self.window.after(0, messagebox.showerror, "Error",
                           f"Error in conversion thread: {str(e)}")
            self.window.after(0, lambda: self.convert_button.config(state='normal'))

    def conversion_finished(self):
        self.convert_button.config(state='normal')
        self.progress_var.set(0)
        messagebox.showinfo("Success", "Conversion completed successfully!")

    def run(self):
        self.window.mainloop()
