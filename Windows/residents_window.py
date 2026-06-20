"""
TeddyShine Laundry Management System - Residents Window Module
Color Theme: Light Greenish-Gray (#E8F0E6 background style)
Module: residents_window.py
Purpose: Full CRUD operations for Resident management
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database.database import get_connection, close_connection
from utils.auth import is_admin, get_current_user
from utils.helpers import (
    show_error, show_success, show_confirm, center_window,
    validate_email, validate_phone, clear_frame, safe_int
)


class ResidentsWindow(tk.Frame):
    """
    Residents Window - Manage all resident profiles.
    Provides Add, Update, Delete, and View functionality.
    """
    
    # Modern color theme
    COLORS = {
        'bg': '#E8F0E6',           # Light greenish-gray background
        'card_bg': '#FFFFFF',       # White for cards
        'primary': '#2E7D32',       # Dark green
        'primary_dark': '#1B5E20',  # Darker green for hover
        'primary_light': '#4CAF50', # Light green
        'accent': '#81C784',        # Soft green accent
        'text': '#1B5E20',          # Dark green text
        'text_secondary': '#555555', # Secondary text
        'text_light': '#FFFFFF',    # Light text for buttons
        'border': '#C8E6C9',        # Light green border
        'danger': '#F44336',        # Danger red
        'danger_dark': '#D32F2F',   # Darker red
        'warning': '#FF9800',       # Warning orange
        'success': '#4CAF50',       # Success green
        'header_bg': '#F5F9F4'      # Light header background
    }
    
    def __init__(self, parent, go_back_callback):
        """
        Initialize the Residents Window.
        
        Args:
            parent: The parent window (tk.Tk or tk.Frame)
            go_back_callback: Function to call when back button is clicked
        """
        super().__init__(parent, bg=self.COLORS['bg'])
        self.parent = parent
        self.go_back_callback = go_back_callback
        self.current_resident_id = None
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Main content
        self.grid_columnconfigure(0, weight=1)
        
        # Create UI sections
        self.create_header()
        self.create_main_content()
        
        # Load residents data
        self.load_residents()
        
    def create_header(self):
        """Creates the header bar with title and back button."""
        header_frame = tk.Frame(
            self,
            bg=self.COLORS['primary'],
            height=70
        )
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)
        
        # Configure columns
        header_frame.grid_columnconfigure(0, weight=0)  # Back button
        header_frame.grid_columnconfigure(1, weight=1)  # Title
        header_frame.grid_columnconfigure(2, weight=0)  # Stats
        
        # Back button
        back_btn = tk.Button(
            header_frame,
            text="← Back to Dashboard",
            font=('Helvetica', 11, 'bold'),
            bg=self.COLORS['primary_dark'],
            fg=self.COLORS['text_light'],
            activebackground=self.COLORS['primary'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=8,
            command=self.go_back_callback
        )
        back_btn.grid(row=0, column=0, padx=20, pady=15, sticky='w')
        
        # Hover effect
        def on_enter(e):
            back_btn.config(bg=self.COLORS['primary'])
            
        def on_leave(e):
            back_btn.config(bg=self.COLORS['primary_dark'])
            
        back_btn.bind("<Enter>", on_enter)
        back_btn.bind("<Leave>", on_leave)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Resident Management",
            font=('Helvetica', 20, 'bold'),
            bg=self.COLORS['primary'],
            fg=self.COLORS['text_light']
        )
        title_label.grid(row=0, column=1, padx=20, pady=15)
        
        # Stats label (will be updated)
        self.stats_label = tk.Label(
            header_frame,
            text="Total Residents: 0",
            font=('Helvetica', 11),
            bg=self.COLORS['primary'],
            fg=self.COLORS['text_light']
        )
        self.stats_label.grid(row=0, column=2, padx=20, pady=15, sticky='e')
        
    def create_main_content(self):
        """Creates the main content area with form and table."""
        main_container = tk.Frame(self, bg=self.COLORS['bg'])
        main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)  # Left panel (form)
        main_container.grid_columnconfigure(1, weight=2)  # Right panel (table)
        
        # Left Panel - Form
        self.create_form_panel(main_container)
        
        # Right Panel - Table
        self.create_table_panel(main_container)
        
    def create_form_panel(self, parent):
        """Creates the form panel for adding/editing residents."""
        form_frame = tk.Frame(
            parent,
            bg=self.COLORS['card_bg'],
            relief='flat',
            highlightbackground=self.COLORS['border'],
            highlightthickness=1
        )
        form_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Form title
        title_frame = tk.Frame(form_frame, bg=self.COLORS['header_bg'])
        title_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="📝 Resident Information",
            font=('Helvetica', 14, 'bold'),
            bg=self.COLORS['header_bg'],
            fg=self.COLORS['primary']
        )
        title_label.pack(pady=10)
        
        # Form fields container - using grid for better alignment
        fields_frame = tk.Frame(form_frame, bg=self.COLORS['card_bg'])
        fields_frame.pack(fill='both', padx=15, pady=10)
        
        # Create form fields with proper grid layout
        self.create_form_fields(fields_frame)
        
    def create_form_fields(self, parent):
        """Creates all form input fields with proper alignment."""
        # Use grid with consistent column weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        
        # Row 0: First Name & Last Name
        tk.Label(
            parent,
            text="First Name *:",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=0, column=0, sticky='w', pady=(5, 2))
        
        self.first_name_var = tk.StringVar()
        self.first_name_entry = tk.Entry(
            parent,
            textvariable=self.first_name_var,
            font=('Helvetica', 10),
            bg='#FAFAFA',
            relief='solid',
            bd=1
        )
        self.first_name_entry.grid(row=1, column=0, sticky='ew', padx=(0, 5), pady=(0, 10), ipady=5)
        
        tk.Label(
            parent,
            text="Last Name *:",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=0, column=1, sticky='w', pady=(5, 2))
        
        self.last_name_var = tk.StringVar()
        self.last_name_entry = tk.Entry(
            parent,
            textvariable=self.last_name_var,
            font=('Helvetica', 10),
            bg='#FAFAFA',
            relief='solid',
            bd=1
        )
        self.last_name_entry.grid(row=1, column=1, sticky='ew', padx=(5, 0), pady=(0, 10), ipady=5)
        
        # Row 2: Phone & Email
        tk.Label(
            parent,
            text="Phone Number *:",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=2, column=0, sticky='w', pady=(5, 2))
        
        self.phone_var = tk.StringVar()
        self.phone_entry = tk.Entry(
            parent,
            textvariable=self.phone_var,
            font=('Helvetica', 10),
            bg='#FAFAFA',
            relief='solid',
            bd=1
        )
        self.phone_entry.grid(row=3, column=0, sticky='ew', padx=(0, 5), pady=(0, 10), ipady=5)
        
        tk.Label(
            parent,
            text="Email *:",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=2, column=1, sticky='w', pady=(5, 2))
        
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(
            parent,
            textvariable=self.email_var,
            font=('Helvetica', 10),
            bg='#FAFAFA',
            relief='solid',
            bd=1
        )
        self.email_entry.grid(row=3, column=1, sticky='ew', padx=(5, 0), pady=(0, 10), ipady=5)
        
        # Row 4: Block & Room Number
        tk.Label(
            parent,
            text="Block *:",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=4, column=0, sticky='w', pady=(5, 2))
        
        self.block_var = tk.StringVar()
        self.block_entry = tk.Entry(
            parent,
            textvariable=self.block_var,
            font=('Helvetica', 10),
            bg='#FAFAFA',
            relief='solid',
            bd=1,
            width=10
        )
        self.block_entry.grid(row=5, column=0, sticky='w', padx=(0, 5), pady=(0, 10), ipady=5)
        
        tk.Label(
            parent,
            text="Room Number *:",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=4, column=1, sticky='w', pady=(5, 2))
        
        self.room_var = tk.StringVar()
        self.room_entry = tk.Entry(
            parent,
            textvariable=self.room_var,
            font=('Helvetica', 10),
            bg='#FAFAFA',
            relief='solid',
            bd=1,
            width=10
        )
        self.room_entry.grid(row=5, column=1, sticky='w', padx=(5, 0), pady=(0, 10), ipady=5)
        
        # Address label
        tk.Label(
            parent,
            text="Address Details:",
            font=('Helvetica', 11, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['primary']
        ).grid(row=6, column=0, columnspan=2, sticky='w', pady=(10, 5))
        
        # Status Radio Buttons
        status_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        status_frame.grid(row=7, column=0, columnspan=2, sticky='w', pady=(5, 10))
        
        self.status_var = tk.StringVar(value="active")
        
        active_radio = tk.Radiobutton(
            status_frame,
            text="Active",
            variable=self.status_var,
            value="active",
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text'],
            selectcolor=self.COLORS['card_bg']
        )
        active_radio.pack(side='left', padx=(0, 20))
        
        inactive_radio = tk.Radiobutton(
            status_frame,
            text="Inactive",
            variable=self.status_var,
            value="inactive",
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text'],
            selectcolor=self.COLORS['card_bg']
        )
        inactive_radio.pack(side='left')
        
        # Required fields hint
        tk.Label(
            parent,
            text="* Required fields",
            font=('Helvetica', 8, 'italic'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text_secondary']
        ).grid(row=8, column=0, columnspan=2, sticky='w', pady=(0, 10))
        
        # Buttons
        button_frame = tk.Frame(parent, bg=self.COLORS['card_bg'])
        button_frame.grid(row=9, column=0, columnspan=2, sticky='ew', pady=(5, 0))
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
        # Add Button
        self.add_btn = tk.Button(
            button_frame,
            text="➕ Add Resident",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['success'],
            fg='white',
            activebackground='#45A049',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=10,
            pady=8,
            command=self.add_resident
        )
        self.add_btn.grid(row=0, column=0, padx=3, pady=5, sticky='ew')
        
        # Update Button
        self.update_btn = tk.Button(
            button_frame,
            text="✏️ Update Resident",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['primary'],
            fg='white',
            activebackground=self.COLORS['primary_dark'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=10,
            pady=8,
            state='disabled',
            command=self.update_resident
        )
        self.update_btn.grid(row=0, column=1, padx=3, pady=5, sticky='ew')
        
        # Clear Button
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear Form",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['warning'],
            fg='white',
            activebackground='#FB8C00',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=10,
            pady=8,
            command=self.clear_form
        )
        self.clear_btn.grid(row=0, column=2, padx=3, pady=5, sticky='ew')
        
    def create_table_panel(self, parent):
        """Creates the table panel for displaying residents."""
        table_frame = tk.Frame(
            parent,
            bg=self.COLORS['card_bg'],
            relief='flat',
            highlightbackground=self.COLORS['border'],
            highlightthickness=1
        )
        table_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Table title
        title_frame = tk.Frame(table_frame, bg=self.COLORS['header_bg'])
        title_frame.pack(fill='x', pady=(0, 10))
        
        title_label = tk.Label(
            title_frame,
            text="📋 Registered Residents",
            font=('Helvetica', 14, 'bold'),
            bg=self.COLORS['header_bg'],
            fg=self.COLORS['primary']
        )
        title_label.pack(pady=10)
        
        # Search bar
        search_frame = tk.Frame(table_frame, bg=self.COLORS['card_bg'])
        search_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        tk.Label(
            search_frame,
            text="Search:",
            font=('Helvetica', 10),
            bg=self.COLORS['card_bg']
        ).pack(side='left', padx=(0, 10))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.search_residents())
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Helvetica', 10),
            bg='#FAFAFA',
            relief='solid',
            bd=1
        )
        search_entry.pack(side='left', fill='x', expand=True, ipady=5)
        
        # Treeview frame with scrollbar
        tree_frame = tk.Frame(table_frame)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Create Treeview with proper column widths
        columns = ('ID', 'Name', 'Phone', 'Email', 'Block', 'Room', 'Status')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define headings with proper text
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Full Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Block', text='Block')
        self.tree.heading('Room', text='Room No')
        self.tree.heading('Status', text='Status')
        
        # Define column widths - wider to prevent overlapping
        self.tree.column('ID', width=50, anchor='center', minwidth=40)
        self.tree.column('Name', width=180, minwidth=120)
        self.tree.column('Phone', width=120, anchor='center', minwidth=90)
        self.tree.column('Email', width=200, minwidth=150)
        self.tree.column('Block', width=70, anchor='center', minwidth=50)
        self.tree.column('Room', width=80, anchor='center', minwidth=60)
        self.tree.column('Status', width=100, anchor='center', minwidth=80)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_row_select)
        
        # Delete button at bottom
        delete_frame = tk.Frame(table_frame, bg=self.COLORS['card_bg'])
        delete_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.delete_btn = tk.Button(
            delete_frame,
            text="🗑️ Delete Selected Resident",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['danger'],
            fg='white',
            activebackground=self.COLORS['danger_dark'],
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=10,
            pady=8,
            state='disabled',
            command=self.delete_resident
        )
        self.delete_btn.pack(fill='x')
        
    def load_residents(self, search_term=None):
        """Loads all residents from database into treeview."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            if search_term:
                query = """
                    SELECT resident_id, full_name, phone, email, block_name, room_number, is_active
                    FROM Resident
                    WHERE full_name LIKE ? OR email LIKE ? OR phone LIKE ?
                    ORDER BY resident_id
                """
                search_pattern = f"%{search_term}%"
                cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            else:
                cursor.execute("""
                    SELECT resident_id, full_name, phone, email, block_name, room_number, is_active
                    FROM Resident
                    ORDER BY resident_id
                """)
            
            rows = cursor.fetchall()
            
            for row in rows:
                status_text = "✅ Active" if row['is_active'] == 1 else "❌ Inactive"
                
                self.tree.insert('', 'end', values=(
                    row['resident_id'],
                    row['full_name'],
                    row['phone'],
                    row['email'],
                    row['block_name'],
                    row['room_number'],
                    status_text
                ))
            
            # Update stats
            self.stats_label.config(text=f"Total Residents: {len(rows)}")
            
        except Exception as e:
            print(f"[ResidentsWindow] Error loading residents: {e}")
            show_error(f"Failed to load residents: {str(e)}")
        finally:
            close_connection(conn)
            
    def search_residents(self):
        """Filters residents based on search term."""
        search_term = self.search_var.get().strip()
        self.load_residents(search_term if search_term else None)
        
    def add_resident(self):
        """Adds a new resident to the database."""
        # Get form values
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        block = self.block_var.get().strip().upper()
        room = self.room_var.get().strip()
        
        # Validate required fields
        if not all([first_name, last_name, phone, email, block, room]):
            show_error("Please fill in all required fields (*)")
            return
            
        if not validate_phone(phone):
            show_error("Please enter a valid 10-digit phone number")
            return
            
        if not validate_email(email):
            show_error("Please enter a valid email address")
            return
            
        # Check if email already exists
        if self.email_exists(email):
            show_error("A resident with this email already exists")
            return
            
        full_name = f"{first_name} {last_name}"
        is_active = 1 if self.status_var.get() == "active" else 0
        
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Resident (full_name, email, phone, block_name, room_number, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (full_name, email, phone, block, room, is_active))
            conn.commit()
            
            show_success(f"Resident {full_name} added successfully!")
            self.clear_form()
            self.load_residents()
            
        except Exception as e:
            print(f"[ResidentsWindow] Error adding resident: {e}")
            show_error(f"Failed to add resident: {str(e)}")
        finally:
            close_connection(conn)
            
    def update_resident(self):
        """Updates the selected resident."""
        if not self.current_resident_id:
            show_error("Please select a resident to update")
            return
            
        # Get form values
        first_name = self.first_name_var.get().strip()
        last_name = self.last_name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        block = self.block_var.get().strip().upper()
        room = self.room_var.get().strip()
        
        # Validate required fields
        if not all([first_name, last_name, phone, email, block, room]):
            show_error("Please fill in all required fields (*)")
            return
            
        if not validate_phone(phone):
            show_error("Please enter a valid 10-digit phone number")
            return
            
        if not validate_email(email):
            show_error("Please enter a valid email address")
            return
            
        full_name = f"{first_name} {last_name}"
        is_active = 1 if self.status_var.get() == "active" else 0
        
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Resident
                SET full_name = ?, email = ?, phone = ?, block_name = ?, room_number = ?, is_active = ?
                WHERE resident_id = ?
            """, (full_name, email, phone, block, room, is_active, self.current_resident_id))
            conn.commit()
            
            show_success(f"Resident {full_name} updated successfully!")
            self.clear_form()
            self.load_residents()
            
        except Exception as e:
            print(f"[ResidentsWindow] Error updating resident: {e}")
            show_error(f"Failed to update resident: {str(e)}")
        finally:
            close_connection(conn)
            
    def delete_resident(self):
        """Deletes the selected resident after confirmation."""
        if not self.current_resident_id:
            show_error("Please select a resident to delete")
            return
            
        # Get resident name for confirmation
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], 'values')
            resident_name = values[1] if values else "this resident"
            
            if show_confirm(f"Are you sure you want to delete {resident_name}?\nThis action cannot be undone."):
                conn = get_connection()
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Resident WHERE resident_id = ?", (self.current_resident_id,))
                    conn.commit()
                    
                    show_success(f"Resident deleted successfully!")
                    self.clear_form()
                    self.load_residents()
                    
                except Exception as e:
                    print(f"[ResidentsWindow] Error deleting resident: {e}")
                    show_error(f"Failed to delete resident: {str(e)}")
                finally:
                    close_connection(conn)
                    
    def on_row_select(self, event):
        """Handles row selection in treeview."""
        selected = self.tree.selection()
        if not selected:
            return
            
        values = self.tree.item(selected[0], 'values')
        if values:
            self.current_resident_id = safe_int(values[0])
            
            # Split full name into first and last
            full_name = values[1].split(' ', 1)
            first_name = full_name[0]
            last_name = full_name[1] if len(full_name) > 1 else ""
            
            # Populate form fields
            self.first_name_var.set(first_name)
            self.last_name_var.set(last_name)
            self.phone_var.set(values[2])
            self.email_var.set(values[3])
            self.block_var.set(values[4])
            self.room_var.set(values[5])
            
            # Set status
            status_text = values[6]
            is_active = "active" if "Active" in status_text else "inactive"
            self.status_var.set(is_active)
            
            # Enable update and delete buttons
            self.update_btn.config(state='normal')
            self.delete_btn.config(state='normal')
            self.add_btn.config(state='disabled')
            
    def clear_form(self):
        """Clears all form fields and resets button states."""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.block_var.set("")
        self.room_var.set("")
        self.status_var.set("active")
        self.current_resident_id = None
        
        self.update_btn.config(state='disabled')
        self.delete_btn.config(state='disabled')
        self.add_btn.config(state='normal')
        
        # Clear treeview selection
        self.tree.selection_remove(self.tree.selection())
        
    def email_exists(self, email, exclude_id=None):
        """Checks if an email already exists in the database."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if exclude_id:
                cursor.execute(
                    "SELECT COUNT(*) as count FROM Resident WHERE email = ? AND resident_id != ?",
                    (email, exclude_id)
                )
            else:
                cursor.execute("SELECT COUNT(*) as count FROM Resident WHERE email = ?", (email,))
            result = cursor.fetchone()
            return result['count'] > 0
        except Exception:
            return False
        finally:
            close_connection(conn)