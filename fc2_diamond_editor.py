import tkinter as tk
from tkinter import filedialog, messagebox
import struct
import os
import shutil


class DiamondEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Far Cry 2 Diamond Editor | Version 1.0 | Made By: Jasper Zebra")
        self.root.geometry("800x600")
        self.root.configure(bg="#2b1810")
        
        # Set window icon
        try:
            self.root.iconbitmap("assets/fc2_icon.ico")
        except:
            pass  # If icon file not found, continue without it
        
        self.file_path = None
        self.diamond_offset = 0x0006817B
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2b1810")
        title_frame.pack(pady=20)
        
        title = tk.Label(
            title_frame,
            text="Far Cry 2 Diamond Editor",
            font=("Arial", 24, "bold"),
            bg="#2b1810",
            fg="#ffb347"
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Edit your diamonds instantly",
            font=("Arial", 10),
            bg="#2b1810",
            fg="#d2691e"
        )
        subtitle.pack()
        
        # File selection
        file_frame = tk.Frame(self.root, bg="#2b1810")
        file_frame.pack(pady=20, padx=30, fill="x")
        
        tk.Label(
            file_frame,
            text="Save File:",
            font=("Arial", 11, "bold"),
            bg="#2b1810",
            fg="#ffb347"
        ).pack(anchor="w", pady=(0, 5))
        
        file_inner = tk.Frame(file_frame, bg="#2b1810")
        file_inner.pack(fill="x")
        
        self.file_label = tk.Label(
            file_inner,
            text="No file selected",
            bg="#3d2517",
            fg="#ffffff",
            relief="sunken",
            anchor="w",
            padx=10,
            pady=8,
            font=("Arial", 9)
        )
        self.file_label.pack(side="left", fill="x", expand=True)
        
        browse_btn = tk.Button(
            file_inner,
            text="Browse",
            command=self.browse_file,
            bg="#d2691e",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="raised",
            cursor="hand2",
            padx=15
        )
        browse_btn.pack(side="right", padx=(10, 0))
        
        # Diamond display and edit
        diamond_frame = tk.LabelFrame(
            self.root,
            text="Diamond Count",
            font=("Arial", 12, "bold"),
            bg="#2b1810",
            fg="#ffb347",
            relief="solid",
            borderwidth=2
        )
        diamond_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        # Current diamonds
        current_frame = tk.Frame(diamond_frame, bg="#2b1810")
        current_frame.pack(pady=15)
        
        tk.Label(
            current_frame,
            text="Current Diamonds:",
            font=("Arial", 11),
            bg="#2b1810",
            fg="#ffb347"
        ).pack()
        
        self.current_diamonds_label = tk.Label(
            current_frame,
            text="--",
            font=("Arial", 32, "bold"),
            bg="#2b1810",
            fg="#90EE90"
        )
        self.current_diamonds_label.pack(pady=5)
        
        # Separator
        separator = tk.Frame(diamond_frame, bg="#d2691e", height=2)
        separator.pack(fill="x", padx=20, pady=10)
        
        # New diamonds input
        new_frame = tk.Frame(diamond_frame, bg="#2b1810")
        new_frame.pack(pady=15)
        
        tk.Label(
            new_frame,
            text="New Diamond Count:",
            font=("Arial", 11),
            bg="#2b1810",
            fg="#ffb347"
        ).pack()
        
        self.new_diamonds_entry = tk.Entry(
            new_frame,
            font=("Arial", 18),
            bg="#3d2517",
            fg="#ffffff",
            insertbackground="#ffffff",
            justify="center",
            width=15
        )
        self.new_diamonds_entry.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="#2b1810")
        button_frame.pack(pady=20, padx=30, fill="x")
        
        write_btn = tk.Button(
            button_frame,
            text="Save Changes",
            command=self.write_diamonds,
            bg="#228B22",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="raised",
            cursor="hand2",
            padx=20,
            pady=10
        )
        write_btn.pack(expand=True, fill="x")
        
        # Info footer
        info_frame = tk.Frame(self.root, bg="#3d2517", relief="solid", borderwidth=1)
        info_frame.pack(pady=(0, 10), padx=30, fill="x")
        
        info_text = f"Diamond Offset: 0x{self.diamond_offset:08X} ({self.diamond_offset})"
        tk.Label(
            info_frame,
            text=info_text,
            font=("Courier", 9),
            bg="#3d2517",
            fg="#d2691e"
        ).pack(padx=10, pady=5)
    
    def browse_file(self):
        # Get the user's Documents folder
        documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
        # Construct the Far Cry 2 save folder path
        fc2_save_folder = os.path.join(documents_folder, "My Games", "Far Cry 2", "Saved Games")
        
        # Use the FC2 save folder as initial directory if it exists
        initial_dir = fc2_save_folder if os.path.exists(fc2_save_folder) else documents_folder
        
        file_path = filedialog.askopenfilename(
            title="Select Far Cry 2 Save File",
            initialdir=initial_dir,
            filetypes=[("All Files", "*.*"), ("Save Files", "*.sav")]
        )
        if file_path:
            self.file_path = file_path
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024
            self.file_label.config(text=f"{file_name} ({file_size:.2f} KB)")
            # Automatically read diamonds when file is selected
            self.read_diamonds()
    
    def read_diamonds(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a save file first!")
            return
        
        try:
            with open(self.file_path, 'rb') as f:
                f.seek(self.diamond_offset)
                bytes_data = f.read(4)
                
                if len(bytes_data) < 4:
                    raise ValueError("File too small or invalid offset")
                
                diamond_count = struct.unpack('<I', bytes_data)[0]
                self.current_diamonds_label.config(text=f"{diamond_count:,}")
                self.new_diamonds_entry.delete(0, tk.END)
                self.new_diamonds_entry.insert(0, str(diamond_count))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read diamonds: {str(e)}")
            self.current_diamonds_label.config(text="Error")
    
    def write_diamonds(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a save file first!")
            return
        
        try:
            new_value = int(self.new_diamonds_entry.get())
            if new_value < 0 or new_value > 0xFFFFFFFF:
                raise ValueError("Value must be between 0 and 4,294,967,295")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid value: {str(e)}")
            return
        
        # Confirm change
        confirm = messagebox.askyesno(
            "Confirm Changes",
            f"Change diamonds to {new_value:,}?\n\nA backup will be created automatically."
        )
        
        if not confirm:
            return
        
        try:
            # Create backup
            backup_path = self.file_path + ".backup"
            shutil.copy2(self.file_path, backup_path)
            
            # Read file
            with open(self.file_path, 'rb') as f:
                data = bytearray(f.read())
            
            # Write new value at offset
            new_bytes = struct.pack('<I', new_value)
            for i, b in enumerate(new_bytes):
                data[self.diamond_offset + i] = b
            
            # Write file
            with open(self.file_path, 'wb') as f:
                f.write(data)
            
            messagebox.showinfo(
                "Success",
                f"Diamonds changed to {new_value:,} successfully!\n\nBackup saved as:\n{os.path.basename(backup_path)}"
            )
            
            # Refresh display
            self.read_diamonds()
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DiamondEditor(root)
    root.mainloop()