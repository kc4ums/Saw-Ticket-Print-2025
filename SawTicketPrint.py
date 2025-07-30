#   Ticket Print program for printing tickets attached to MDF units
#   Copyright (C) 2025 Timothy L. Gray
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#   Requirements
#   Install Python https://www.python.org/
# 

import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from reportlab.lib import colors
from reportlab.lib.pagesizes import LEGAL, landscape
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import os
import webbrowser
from datetime import datetime

class MaterialInputGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Material and Production Input")
        self.root.geometry("450x300")  # Wider window for grid layout
        
        # Dictionary to store input fields
        self.entries = {}
        self.shift_vars = {}  # For OptionMenu variables
        
        # Labels and input fields
        fields = [
            ("Grade:", "grade", tk.Entry),
            ("Thickness:", "thickness", tk.Entry),
            ("Width:", "width", tk.Entry),
            ("Length:", "length", tk.Entry),
            ("Date Produced:", "date_produced", DateEntry),
            ("Shift Produced:", "shift_produced", None),  # OptionMenu
            ("Date Sanded:", "date_sanded", DateEntry),
            ("Shift Sanded:", "shift_sanded", None),  # OptionMenu
            ("Date Sawed:", "date_sawed", DateEntry),
            ("Shift Sawed:", "shift_sawed", None),  # OptionMenu
            ("Piece Count:", "piece_count", tk.Entry)
        ]
        
        # Option for Shifts
        shift_options = ["A", "B", "C", "D"]
        
        # Split fields into two columns
        left_fields = fields[:6]  # First 6 fields
        right_fields = fields[6:]  # Last 5 fields
        
        # Left column (columns 0 and 1)
        for idx, (label_text, field_name, widget_type) in enumerate(left_fields):
            tk.Label(root, text=label_text).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            if widget_type == tk.Entry:
                entry = tk.Entry(root)
                entry.grid(row=idx, column=1, padx=5, pady=5)
                self.entries[field_name] = entry
            elif widget_type == DateEntry:
                entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='mm/dd/yyyy')
                entry.grid(row=idx, column=1, padx=5, pady=5)
                self.entries[field_name] = entry
            else:  # OptionMenu for shifts
                var = tk.StringVar(root)
                var.set("A")  # Default value
                entry = tk.OptionMenu(root, var, *shift_options)
                entry.grid(row=idx, column=1, padx=5, pady=5, sticky="ew")
                self.entries[field_name] = entry
                self.shift_vars[field_name] = var
        
        # Right column (columns 2 and 3)
        for idx, (label_text, field_name, widget_type) in enumerate(right_fields):
            tk.Label(root, text=label_text).grid(row=idx, column=2, padx=5, pady=5, sticky="e")
            if widget_type == tk.Entry:
                entry = tk.Entry(root)
                entry.grid(row=idx, column=3, padx=5, pady=5)
                self.entries[field_name] = entry
            elif widget_type == DateEntry:
                entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='mm/dd/yyyy')
                entry.grid(row=idx, column=3, padx=5, pady=5)
                self.entries[field_name] = entry
            else:  # OptionMenu for shifts
                var = tk.StringVar(root)
                var.set("A")  # Default value
                entry = tk.OptionMenu(root, var, *shift_options)
                entry.grid(row=idx, column=3, padx=5, pady=5, sticky="ew")
                self.entries[field_name] = entry
                self.shift_vars[field_name] = var
        
        # Submit button (spanning all columns)
        tk.Button(root, text="Submit and Generate Ticket PDF", command=self.submit).grid(row=6, column=0, columnspan=4, pady=10)
    
    def submit(self):
        try:
            # Collect and validate inputs
            data = {}
            data['grade'] = self.entries['grade'].get().strip()
            data['thickness'] = self.entries['thickness'].get().strip()
            data['width'] = self.entries['width'].get().strip()
            data['length'] = self.entries['length'].get().strip()   
            data['piece_count'] = self.entries['piece_count'].get().strip()
             
            # Get shift selections
            data['shift_produced'] = self.shift_vars['shift_produced'].get()
            data['shift_sanded'] = self.shift_vars['shift_sanded'].get()
            data['shift_sawed'] = self.shift_vars['shift_sawed'].get()
            
            # Validate positive numbers
            #for field in ['width', 'length', 'piece_count']:
            #    if data[field] < 0:
            #       raise ValueError(f"{field} cannot be negative")
            
            # Get dates from DateEntry widgets
            data['date_produced'] = self.entries['date_produced'].get_date().strftime('%Y-%m-%d')
            data['date_sanded'] = self.entries['date_sanded'].get_date().strftime('%Y-%m-%d')
            data['date_sawed'] = self.entries['date_sawed'].get_date().strftime('%Y-%m-%d')
            
            # Display results in message box
            #result = "\n".join(f"{key}: {value}" for key, value in data.items())
            #messagebox.showinfo("Input Data", f"Collected Data:\n\n{result}")
            
            # Generate PDF ticket with ad-hoc layout
            pdf_filename = "material_ticket.pdf"
            ticket_size = landscape(LEGAL)  # Legal paper (8.5x14 in) in landscape
            c = canvas.Canvas(pdf_filename, pagesize=ticket_size)
            
            # Ad-hoc layout with manual positioning
            #y_position = 7.5 * inch  # Starting y-coordinate
            #line_height = 0.75 * inch  # Adjusted for larger font sizes
            
            # Larger and bold font for grade, thickness, width, length
            c.setFont("Helvetica-Bold", 55)
            c.setFillColor(colors.black)

            c.drawString(0.65 * inch, 4.9375 * inch, f"{data['grade']}")        
            c.drawString(0.65 * inch, 4.1875 * inch, f"{data['thickness']}")    
            c.drawString(0.65 * inch, 3.4375 * inch, f"{data['width']}")        
            c.drawString(4.25 * inch, 4.1875 * inch, f"{data['piece_count']}")  
            c.drawString(4.25 * inch, 3.4375 * inch, f"{data['length']}")       

            c.drawString(7.65 * inch, 4.9375 * inch, f"{data['grade']}")        
            c.drawString(7.65 * inch, 4.1875 * inch, f"{data['thickness']}")    
            c.drawString(7.65 * inch, 3.4375 * inch, f"{data['width']}")        
            c.drawString(11.25 * inch, 4.1875 * inch, f"{data['piece_count']}") 
            c.drawString(11.25 * inch, 3.4375 * inch, f"{data['length']}")      

            # Smaller non-bold font for remaining fields
            c.setFont("Helvetica", 16)
            c.drawString(1.927 * inch, 3.125 * inch, f"{data['shift_produced']}")
            c.drawString(2.125 * inch, 3.125 * inch , f"{data['date_produced']}")
            c.drawString(1.927 * inch, 2.875 * inch, f"{data['shift_sanded']}")
            c.drawString(2.125 * inch, 2.875 * inch , f"{data['date_sanded']}")
            c.drawString(5.25 * inch, 3.125 * inch, f"{data['shift_sawed']}")
            c.drawString(5.448 * inch, 3.125 * inch , f"{data['date_sawed']}")

            c.drawString(9 * inch, 3.125 * inch, f"{data['shift_produced']}")
            c.drawString(9.198 * inch, 3.125 * inch , f"{data['date_produced']}")
            c.drawString(9 * inch, 2.875 * inch, f"{data['shift_sanded']}")
            c.drawString(9.198 * inch, 2.875 * inch , f"{data['date_sanded']}")
            c.drawString(12.25 * inch, 3.125 * inch, f"{data['shift_sawed']}")
            c.drawString(12.448 * inch, 3.125 * inch , f"{data['date_sawed']}")
            
             # Smaller non-bold font for small tear of tickets at bottom
            c.setFont("Helvetica", 12)
            c.drawString(0.65 * inch, .75 * inch, f"PRO: {data['shift_produced']}")
            c.drawString(1.27 * inch, .75 * inch, f"{data['date_produced']}")
            c.drawString(0.65 * inch, .5 * inch, f"SND: {data['shift_sanded']}")
            c.drawString(1.27 * inch, .5 * inch, f"{data['date_sanded']}")
            c.drawString(0.65 * inch, .25 * inch, f"SAW: {data['shift_sawed']}")
            c.drawString(1.27 * inch, .25 * inch, f"{data['date_sawed']}")

            c.drawString(2.5 * inch, .75 * inch, f"THK: {data['thickness']}")
            c.drawString(2.5 * inch, .5 * inch, f"WID: {data['width']}")
            c.drawString(2.5 * inch, .25 * inch, f"LEN: {data['length']}")
          
            c.drawString(3.75 * inch, .75 * inch, f"GRD: {data['grade']}")
            c.drawString(3.75 * inch, .5 * inch, f"PCS: {data['piece_count']}")

            c.drawString(7.65 * inch, .75 * inch, f"PRO: {data['shift_produced']}")
            c.drawString(8.27 * inch, .75 * inch, f"{data['date_produced']}")
            c.drawString(7.65 * inch, .5 * inch, f"SND: {data['shift_sanded']}")
            c.drawString(8.27 * inch, .5 * inch, f"{data['date_sanded']}")
            c.drawString(7.65 * inch, .25 * inch, f"SAW: {data['shift_sawed']}")
            c.drawString(8.27 * inch, .25 * inch, f"{data['date_sawed']}")


            c.drawString(9.5 * inch, .75 * inch, f"THK: {data['thickness']}")
            c.drawString(9.5 * inch, .5 * inch, f"WID: {data['width']}")
            c.drawString(9.5 * inch, .25 * inch, f"LEN: {data['length']}")
          
            c.drawString(10.75 * inch, .75 * inch, f"GRD: {data['grade']}")
            c.drawString(10.75 * inch, .5 * inch, f"PCS: {data['piece_count']}")
            
                        
            # Save the PDF
            c.showPage()
            c.save()
            
            # Open the PDF in the default web browser
            pdf_path = os.path.abspath(pdf_filename)
            webbrowser.open(f"file://{pdf_path}")
            
            #messagebox.showinfo("Success", f"Ticket PDF has been generated as {pdf_filename} and opened in your web browser.")
                
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate or open PDF: {str(e)}")

def main():
    root = tk.Tk()
    app = MaterialInputGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()