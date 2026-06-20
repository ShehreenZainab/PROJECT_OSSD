"""
TeddyShine Laundry Management System - Orders Window Module
Color Theme: Light Greenish-Gray (#E8F0E6 background style)
Module: orders_window.py
Purpose: Place new orders and view/manage existing orders
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

from database.database import get_connection, close_connection
from utils.auth import is_admin, get_current_user
from utils.helpers import (
    show_error, show_success, show_confirm, center_window,
    format_date, format_currency, safe_int, safe_float
)


class OrdersWindow(tk.Frame):
    """Provides tabs for New Order creation and View/Manage existing orders."""
    
    COLORS = {
        'bg': '#E8F0E6',           
        'card_bg': '#FFFFFF',       
        'primary': '#2E7D32',       
        'primary_dark': '#1B5E20',  
        'primary_light': '#4CAF50',
        'accent': '#81C784',        
        'text': '#1B5E20',         
        'text_secondary': '#555555',
        'text_light': '#FFFFFF',   
        'border': '#C8E6C9',        
        'danger': '#F44336',       
        'danger_dark': '#D32F2F',  
        'warning': '#FF9800',       
        'success': '#4CAF50',       
        'info': '#2196F3',          
        'header_bg': '#F5F9F4'      
    }
    
    ORDER_STATUSES = ['Pending', 'Processing', 'Completed', 'Cancelled', 'Delivered']
    
    def __init__(self, parent, go_back_callback):
        super().__init__(parent, bg=self.COLORS['bg'])
        self.parent = parent
        self.go_back_callback = go_back_callback
        
        self.order_items = []
        self.current_total = 0.0
        
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Main content
        self.grid_columnconfigure(0, weight=1)
        
        # Create UI sections
        self.create_header()
        self.create_main_content()
        
        # Load data
        self.load_residents()
        self.load_staff()
        self.load_delivery_slots()
        self.load_services()
        self.load_orders()
        
    def create_header(self):
        header_frame = tk.Frame(
            self,
            bg=self.COLORS['primary'],
            height=70
        )
        header_frame.grid(row=0, column=0, sticky="ew")
        header_frame.grid_propagate(False)

        header_frame.grid_columnconfigure(0, weight=0)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=0)
        

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
        
        title_label = tk.Label(
            header_frame,
            text="Order Management",
            font=('Helvetica', 20, 'bold'),
            bg=self.COLORS['primary'],
            fg=self.COLORS['text_light']
        )
        title_label.grid(row=0, column=1, padx=20, pady=15)
        
        # Stats label (will be updated)
        self.stats_label = tk.Label(
            header_frame,
            text="Total Orders: 0",
            font=('Helvetica', 11),
            bg=self.COLORS['primary'],
            fg=self.COLORS['text_light']
        )
        self.stats_label.grid(row=0, column=2, padx=20, pady=15, sticky='e')
        
    def create_main_content(self):
        """Creates the main content area with notebook tabs."""
        main_container = tk.Frame(self, bg=self.COLORS['bg'])
        main_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Create Notebook
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Helvetica', 11))
        
        # Tab 1: New Order
        self.new_order_frame = tk.Frame(self.notebook, bg=self.COLORS['bg'])
        self.notebook.add(self.new_order_frame, text="📝 New Order")
        self.create_new_order_tab()
        
        # Tab 2: View Orders
        self.view_orders_frame = tk.Frame(self.notebook, bg=self.COLORS['bg'])
        self.notebook.add(self.view_orders_frame, text="📋 View Orders")
        self.create_view_orders_tab()
        
    def create_new_order_tab(self):
        """Creates the New Order form tab."""
        main_frame = tk.Frame(self.new_order_frame, bg=self.COLORS['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left Panel - Order Details
        left_panel = tk.Frame(main_frame, bg=self.COLORS['bg'])
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right Panel - Order Items
        right_panel = tk.Frame(main_frame, bg=self.COLORS['bg'])
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.create_order_details_panel(left_panel)
        self.create_order_items_panel(right_panel)
        
    def create_order_details_panel(self, parent):
        """Creates the order details form panel."""
        card = tk.Frame(
            parent,
            bg=self.COLORS['card_bg'],
            relief='flat',
            highlightbackground=self.COLORS['border'],
            highlightthickness=1
        )
        card.pack(fill='both', expand=True)
        
        title_frame = tk.Frame(card, bg=self.COLORS['header_bg'])
        title_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            title_frame,
            text="📋 Order Information",
            font=('Helvetica', 14, 'bold'),
            bg=self.COLORS['header_bg'],
            fg=self.COLORS['primary']
        ).pack(pady=12)
        
        form_frame = tk.Frame(card, bg=self.COLORS['card_bg'])
        form_frame.pack(fill='both', padx=20, pady=15)
        
        # Resident Selection
        tk.Label(
            form_frame, text="Resident *:",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=0, column=0, sticky='w', pady=(0, 5))
        
        self.resident_combo = ttk.Combobox(
            form_frame,
            font=('Helvetica', 10),
            state='readonly',
            width=35
        )
        self.resident_combo.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(0, 15), ipady=5)
        
        # Staff Selection
        tk.Label(
            form_frame, text="Assign Staff:",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=2, column=0, sticky='w', pady=(0, 5))
        
        self.staff_combo = ttk.Combobox(
            form_frame,
            font=('Helvetica', 10),
            state='readonly',
            width=35
        )
        self.staff_combo.grid(row=3, column=0, columnspan=2, sticky='ew', pady=(0, 15), ipady=5)
        
        # Delivery Slot Selection
        tk.Label(
            form_frame, text="Delivery Slot *:",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=4, column=0, sticky='w', pady=(0, 5))
        
        self.slot_combo = ttk.Combobox(
            form_frame,
            font=('Helvetica', 10),
            state='readonly',
            width=35
        )
        self.slot_combo.grid(row=5, column=0, columnspan=2, sticky='ew', pady=(0, 15), ipady=5)
        
        # Weight 
        tk.Label(
            form_frame, text="Total Weight (kg):",
            font=('Helvetica', 10),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=6, column=0, sticky='w', pady=(0, 5))
        
        self.weight_entry = tk.Entry(
            form_frame,
            font=('Helvetica', 10),
            bg='#FAFAFA',
            relief='solid',
            bd=1,
            width=20
        )
        self.weight_entry.grid(row=7, column=0, sticky='w', pady=(0, 15), ipady=5)
        
        # Special Instructions
        tk.Label(
            form_frame, text="Special Instructions:",
            font=('Helvetica', 10),
            bg=self.COLORS['card_bg'],
            fg=self.COLORS['text']
        ).grid(row=8, column=0, sticky='w', pady=(0, 5))
        
        self.instructions_text = tk.Text(
            form_frame,
            font=('Helvetica', 10),
            bg='#FAFAFA',
            relief='solid',
            bd=1,
            height=4,
            width=35
        )
        self.instructions_text.grid(row=9, column=0, columnspan=2, sticky='ew', pady=(0, 15))
        
        # Place Order Button
        self.place_order_btn = tk.Button(
            form_frame,
            text="✅ Place Order",
            font=('Helvetica', 12, 'bold'),
            bg=self.COLORS['success'],
            fg='white',
            activebackground='#45A049',
            activeforeground='white',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            command=self.place_order
        )
        self.place_order_btn.grid(row=10, column=0, columnspan=2, pady=(10, 0), sticky='ew')
        
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_columnconfigure(1, weight=0)
        
    def create_order_items_panel(self, parent):
        """Creates the order items selection panel."""
        card = tk.Frame(
            parent,
            bg=self.COLORS['card_bg'],
            relief='flat',
            highlightbackground=self.COLORS['border'],
            highlightthickness=1
        )
        card.pack(fill='both', expand=True)
        
        title_frame = tk.Frame(card, bg=self.COLORS['header_bg'])
        title_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            title_frame,
            text="🛍️ Order Items",
            font=('Helvetica', 14, 'bold'),
            bg=self.COLORS['header_bg'],
            fg=self.COLORS['primary']
        ).pack(pady=12)
        
        # Add item section
        add_frame = tk.Frame(card, bg=self.COLORS['card_bg'])
        add_frame.pack(fill='x', padx=20, pady=10)
        
        # Service selection
        tk.Label(
            add_frame, text="Service:",
            font=('Helvetica', 10),
            bg=self.COLORS['card_bg']
        ).grid(row=0, column=0, sticky='w', padx=(0, 10))
        
        self.service_combo = ttk.Combobox(
            add_frame,
            font=('Helvetica', 10),
            state='readonly',
            width=25
        )
        self.service_combo.grid(row=0, column=1, padx=(0, 10), sticky='ew')
        
        # Quantity
        tk.Label(
            add_frame, text="Qty:",
            font=('Helvetica', 10),
            bg=self.COLORS['card_bg']
        ).grid(row=0, column=2, sticky='w', padx=(0, 10))
        
        self.qty_spinbox = tk.Spinbox(
            add_frame,
            from_=1,
            to=99,
            width=5,
            font=('Helvetica', 10)
        )
        self.qty_spinbox.grid(row=0, column=3, padx=(0, 10))
        
        # Add button
        add_item_btn = tk.Button(
            add_frame,
            text="➕ Add Item",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['primary'],
            fg='white',
            activebackground=self.COLORS['primary_dark'],
            relief='flat',
            cursor='hand2',
            padx=10,
            pady=5,
            command=self.add_item_to_list
        )
        add_item_btn.grid(row=0, column=4, padx=(10, 0))
        
        add_frame.grid_columnconfigure(1, weight=1)
        
        # Items listbox with scrollbar
        list_frame = tk.Frame(card, bg=self.COLORS['card_bg'])
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.items_listbox = tk.Listbox(
            list_frame,
            font=('Helvetica', 10),
            bg='#FAFAFA',
            yscrollcommand=scrollbar.set,
            height=10
        )
        self.items_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.items_listbox.yview)
        
        # Remove item button
        remove_btn = tk.Button(
            card,
            text="🗑️ Remove Selected Item",
            font=('Helvetica', 10),
            bg=self.COLORS['danger'],
            fg='white',
            activebackground=self.COLORS['danger_dark'],
            relief='flat',
            cursor='hand2',
            padx=10,
            pady=5,
            command=self.remove_item
        )
        remove_btn.pack(pady=(5, 10))
        
        # Total amount display
        total_frame = tk.Frame(card, bg=self.COLORS['header_bg'])
        total_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        tk.Label(
            total_frame,
            text="Total Amount:",
            font=('Helvetica', 12, 'bold'),
            bg=self.COLORS['header_bg'],
            fg=self.COLORS['text']
        ).pack(side='left', padx=10, pady=10)
        
        self.total_label = tk.Label(
            total_frame,
            text="₹ 0.00",
            font=('Helvetica', 16, 'bold'),
            bg=self.COLORS['header_bg'],
            fg=self.COLORS['primary']
        )
        self.total_label.pack(side='right', padx=10, pady=10)
        
    def create_view_orders_tab(self):
        """Creates the View Orders tab with filtering and management."""
        main_frame = tk.Frame(self.view_orders_frame, bg=self.COLORS['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Filter bar
        filter_frame = tk.Frame(main_frame, bg=self.COLORS['card_bg'], relief='flat')
        filter_frame.pack(fill='x', pady=(0, 15), ipady=10)
        
        tk.Label(
            filter_frame,
            text="Filter by Status:",
            font=('Helvetica', 10, 'bold'),
            bg=self.COLORS['card_bg']
        ).pack(side='left', padx=(15, 10))
        
        self.status_filter = ttk.Combobox(
            filter_frame,
            values=['All'] + self.ORDER_STATUSES,
            state='readonly',
            width=15
        )
        self.status_filter.set('All')
        self.status_filter.pack(side='left', padx=(0, 15))
        self.status_filter.bind('<<ComboboxSelected>>', lambda e: self.load_orders())
        
        # Refresh button
        refresh_btn = tk.Button(
            filter_frame,
            text="🔄 Refresh",
            font=('Helvetica', 10),
            bg=self.COLORS['info'],
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=15,
            pady=5,
            command=self.load_orders
        )
        refresh_btn.pack(side='right', padx=15)
        
        # Treeview frame
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('Order ID', 'Order No', 'Resident', 'Date', 'Delivery Date', 'Amount', 'Status')
        self.orders_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        self.orders_tree.heading('Order ID', text='ID')
        self.orders_tree.heading('Order No', text='Order No')
        self.orders_tree.heading('Resident', text='Resident')
        self.orders_tree.heading('Date', text='Order Date')
        self.orders_tree.heading('Delivery Date', text='Delivery Date')
        self.orders_tree.heading('Amount', text='Amount')
        self.orders_tree.heading('Status', text='Status')
        
        # Define column widths
        self.orders_tree.column('Order ID', width=50, anchor='center')
        self.orders_tree.column('Order No', width=100, anchor='center')
        self.orders_tree.column('Resident', width=150)
        self.orders_tree.column('Date', width=100, anchor='center')
        self.orders_tree.column('Delivery Date', width=100, anchor='center')
        self.orders_tree.column('Amount', width=100, anchor='center')
        self.orders_tree.column('Status', width=100, anchor='center')
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.orders_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.orders_tree.xview)
        self.orders_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.orders_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        action_frame = tk.Frame(main_frame, bg=self.COLORS['bg'])
        action_frame.pack(fill='x', pady=(15, 0))
        
        # Mark Complete button
        self.complete_btn = tk.Button(
            action_frame,
            text="✅ Mark as Completed",
            font=('Helvetica', 11, 'bold'),
            bg=self.COLORS['success'],
            fg='white',
            activebackground='#45A049',
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            command=self.mark_complete
        )
        self.complete_btn.pack(side='left', padx=5)
        
        # Delete Order button
        self.delete_order_btn = tk.Button(
            action_frame,
            text="🗑️ Delete Order",
            font=('Helvetica', 11, 'bold'),
            bg=self.COLORS['danger'],
            fg='white',
            activebackground=self.COLORS['danger_dark'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=8,
            command=self.delete_order
        )
        self.delete_order_btn.pack(side='left', padx=5)
        
    # ==============================================
    # DATA LOADING FUNCTIONS
    # ==============================================
    
    def load_residents(self):
        """Loads residents into the combobox."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT resident_id, full_name, block_name, room_number
                FROM Resident WHERE is_active = 1 ORDER BY full_name
            """)
            residents = cursor.fetchall()
            
            self.resident_list = []
            for r in residents:
                display_text = f"{r['full_name']} - {r['block_name']}{r['room_number']}"
                self.resident_list.append({
                    'id': r['resident_id'],
                    'display': display_text
                })
            
            self.resident_combo['values'] = [r['display'] for r in self.resident_list]
            
        except Exception as e:
            print(f"[OrdersWindow] Error loading residents: {e}")
        finally:
            close_connection(conn)
            
    def load_staff(self):
        """Loads staff members into the combobox."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT staff_id, full_name, role
                FROM Staff WHERE is_available = 1
                ORDER BY full_name
            """)
            staff = cursor.fetchall()
            
            self.staff_list = []
            for s in staff:
                display_text = f"{s['full_name']} ({s['role']})"
                self.staff_list.append({
                    'id': s['staff_id'],
                    'display': display_text
                })
            
            self.staff_combo['values'] = ['None'] + [s['display'] for s in self.staff_list]
            self.staff_combo.set('None')
            
        except Exception as e:
            print(f"[OrdersWindow] Error loading staff: {e}")
        finally:
            close_connection(conn)
            
    def load_delivery_slots(self):
        """Loads available delivery slots into the combobox."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT slot_id, slot_date, slot_time, booked_orders, max_orders
                FROM DeliverySlots WHERE is_available = 1
                ORDER BY slot_date, slot_time
            """)
            slots = cursor.fetchall()
            
            self.slot_list = []
            for s in slots:
                available = s['max_orders'] - s['booked_orders']
                display_text = f"{s['slot_date']} {s['slot_time']} ({available} slots left)"
                self.slot_list.append({
                    'id': s['slot_id'],
                    'display': display_text
                })
            
            self.slot_combo['values'] = [s['display'] for s in self.slot_list]
            
        except Exception as e:
            print(f"[OrdersWindow] Error loading slots: {e}")
        finally:
            close_connection(conn)
            
    def load_services(self):
        """Loads services into the combobox."""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT service_id, service_name, base_price, price_per_kg
                FROM Services WHERE is_active = 1
                ORDER BY service_name
            """)
            services = cursor.fetchall()
            
            self.service_list = []
            for s in services:
                price = s['price_per_kg'] if s['price_per_kg'] else s['base_price']
                display_text = f"{s['service_name']} - ₹{price}"
                self.service_list.append({
                    'id': s['service_id'],
                    'name': s['service_name'],
                    'price': price,
                    'display': display_text
                })
            
            self.service_combo['values'] = [s['display'] for s in self.service_list]
            
        except Exception as e:
            print(f"[OrdersWindow] Error loading services: {e}")
        finally:
            close_connection(conn)
            
    def load_orders(self):
        """Loads orders into the treeview with optional status filter."""
        # Clear existing items
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        filter_status = self.status_filter.get()
        
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            if filter_status != 'All':
                query = """
                    SELECT o.order_id, o.order_number, r.full_name, o.order_date,
                           o.expected_delivery_date, o.final_amount, o.status
                    FROM Orders o
                    JOIN Resident r ON o.resident_id = r.resident_id
                    WHERE o.status = ?
                    ORDER BY o.order_id DESC
                """
                cursor.execute(query, (filter_status,))
            else:
                query = """
                    SELECT o.order_id, o.order_number, r.full_name, o.order_date,
                           o.expected_delivery_date, o.final_amount, o.status
                    FROM Orders o
                    JOIN Resident r ON o.resident_id = r.resident_id
                    ORDER BY o.order_id DESC
                """
                cursor.execute(query)
            
            rows = cursor.fetchall()
            
            # Status emoji mapping
            status_emoji = {
                'Pending': '⏳ Pending',
                'Processing': '⚙️ Processing',
                'Completed': '✅ Completed',
                'Cancelled': '❌ Cancelled',
                'Delivered': '🚚 Delivered'
            }
            
            for row in rows:
                self.orders_tree.insert('', 'end', values=(
                    row['order_id'],
                    row['order_number'],
                    row['full_name'],
                    format_date(row['order_date']),
                    format_date(row['expected_delivery_date']),
                    format_currency(row['final_amount']),
                    status_emoji.get(row['status'], row['status'])
                ))
            
            # Update stats
            self.stats_label.config(text=f"Total Orders: {len(rows)}")
            
        except Exception as e:
            print(f"[OrdersWindow] Error loading orders: {e}")
        finally:
            close_connection(conn)
            
    # ==============================================
    # ORDER ITEMS MANAGEMENT
    # ==============================================
    
    def add_item_to_list(self):
        """Adds a selected service with quantity to the order items list."""
        selection = self.service_combo.current()
        if selection < 0:
            show_error("Please select a service")
            return
            
        try:
            quantity = int(self.qty_spinbox.get())
            if quantity <= 0:
                show_error("Quantity must be greater than 0")
                return
        except ValueError:
            show_error("Please enter a valid quantity")
            return
            
        service = self.service_list[selection]
        subtotal = service['price'] * quantity
        
        item = {
            'service_id': service['id'],
            'service_name': service['name'],
            'quantity': quantity,
            'unit_price': service['price'],
            'subtotal': subtotal
        }
        
        self.order_items.append(item)
        self.update_items_listbox()
        
        # Reset quantity spinbox
        self.qty_spinbox.delete(0, tk.END)
        self.qty_spinbox.insert(0, "1")
        
    def remove_item(self):
        """Removes selected item from the order items list."""
        selection = self.items_listbox.curselection()
        if not selection:
            show_error("Please select an item to remove")
            return
            
        index = selection[0]
        del self.order_items[index]
        self.update_items_listbox()
        
    def update_items_listbox(self):
        """Updates the listbox display and recalculates total."""
        self.items_listbox.delete(0, tk.END)
        self.current_total = 0.0
        
        for item in self.order_items:
            display = f"{item['quantity']}x {item['service_name']} - {format_currency(item['subtotal'])}"
            self.items_listbox.insert(tk.END, display)
            self.current_total += item['subtotal']
            
        self.total_label.config(text=format_currency(self.current_total))
        
    # ==============================================
    # ORDER CRUD OPERATIONS
    # ==============================================
    
    def place_order(self):
        """Places a new order with all items."""
        # Validate required fields
        resident_selection = self.resident_combo.current()
        if resident_selection < 0:
            show_error("Please select a resident")
            return
            
        slot_selection = self.slot_combo.current()
        if slot_selection < 0:
            show_error("Please select a delivery slot")
            return
            
        if len(self.order_items) == 0:
            show_error("Please add at least one item to the order")
            return
            
        # Get selected IDs
        resident_id = self.resident_list[resident_selection]['id']
        slot_id = self.slot_list[slot_selection]['id']
        
        # Get staff ID (if selected)
        staff_id = None
        staff_selection = self.staff_combo.current()
        if staff_selection > 0:  # First item is 'None'
            staff_id = self.staff_list[staff_selection - 1]['id']
            
        # Get weight
        weight_text = self.weight_entry.get().strip()
        total_weight = safe_float(weight_text) if weight_text else 0.0
        
        # Get special instructions
        instructions = self.instructions_text.get("1.0", tk.END).strip()
        
        # Generate order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate totals
        discount = 0.0  # Can be enhanced later
        final_amount = self.current_total - discount
        
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Insert order
            cursor.execute("""
                INSERT INTO Orders (order_number, resident_id, staff_id, slot_id,
                                   total_weight_kg, total_amount, discount_amount,
                                   final_amount, status, order_date,
                                   expected_delivery_date, special_instructions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'), date('now', '+3 days'), ?)
            """, (order_number, resident_id, staff_id, slot_id, total_weight,
                  self.current_total, discount, final_amount, 'Pending', instructions))
            
            order_id = cursor.lastrowid
            
            # Insert order items
            for item in self.order_items:
                cursor.execute("""
                    INSERT INTO OrderItems (order_id, service_id, quantity, unit_price, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                """, (order_id, item['service_id'], item['quantity'],
                      item['unit_price'], item['subtotal']))
                    
            # Update delivery slot booked count
            cursor.execute("""
                UPDATE DeliverySlots SET booked_orders = booked_orders + 1
                WHERE slot_id = ?
            """, (slot_id,))
            
            # Create invoice record
            invoice_number = f"INV-{order_id:06d}"
            cursor.execute("""
                INSERT INTO Invoice (order_id, invoice_number, subtotal, discount_amount,
                                    total_amount, amount_paid, balance_due, status,
                                    due_date, generated_date)
                VALUES (?, ?, ?, ?, ?, 0, ?, 'Unpaid', date('now', '+7 days'), datetime('now'))
            """, (order_id, invoice_number, self.current_total, discount,
                  final_amount, final_amount))
            
            conn.commit()
            
            show_success(f"Order {order_number} placed successfully!\nTotal: {format_currency(final_amount)}")
            
            # Reset form
            self.reset_new_order_form()
            
            # Refresh orders list
            self.load_orders()
            
            # Switch to view orders tab
            self.notebook.select(1)
            
        except Exception as e:
            print(f"[OrdersWindow] Error placing order: {e}")
            show_error(f"Failed to place order: {str(e)}")
            conn.rollback()
        finally:
            close_connection(conn)
            
    def reset_new_order_form(self):
        """Resets the new order form."""
        self.resident_combo.set('')
        self.staff_combo.set('None')
        self.slot_combo.set('')
        self.weight_entry.delete(0, tk.END)
        self.instructions_text.delete("1.0", tk.END)
        self.order_items = []
        self.update_items_listbox()
        
    def mark_complete(self):
        """Marks the selected order as completed."""
        selected = self.orders_tree.selection()
        if not selected:
            show_error("Please select an order to mark as completed")
            return
            
        values = self.orders_tree.item(selected[0], 'values')
        if not values:
            return
            
        order_id = values[0]
        order_no = values[1]
        current_status = values[6].replace('✅ ', '').replace('⏳ ', '').replace('⚙️ ', '').replace('❌ ', '').replace('🚚 ', '')
        
        if current_status == 'Completed':
            show_error("Order is already completed")
            return
            
        if current_status == 'Cancelled':
            show_error("Cannot complete a cancelled order")
            return
            
        if show_confirm(f"Mark order {order_no} as completed?"):
            conn = get_connection()
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE Orders SET status = 'Completed', actual_delivery_date = date('now')
                    WHERE order_id = ?
                """, (order_id,))
                conn.commit()
                
                show_success(f"Order {order_no} marked as completed!")
                self.load_orders()
                
            except Exception as e:
                print(f"[OrdersWindow] Error marking complete: {e}")
                show_error(f"Failed to update order: {str(e)}")
            finally:
                close_connection(conn)
                
    def delete_order(self):
        """Deletes the selected order after confirmation."""
        selected = self.orders_tree.selection()
        if not selected:
            show_error("Please select an order to delete")
            return
            
        values = self.orders_tree.item(selected[0], 'values')
        if not values:
            return
            
        order_id = values[0]
        order_no = values[1]
        
        if show_confirm(f"Are you sure you want to delete order {order_no}?\nThis action cannot be undone."):
            conn = get_connection()
            try:
                cursor = conn.cursor()
                
                # Get slot_id to update booked count
                cursor.execute("SELECT slot_id FROM Orders WHERE order_id = ?", (order_id,))
                result = cursor.fetchone()
                if result and result['slot_id']:
                    cursor.execute("""
                        UPDATE DeliverySlots SET booked_orders = booked_orders - 1
                        WHERE slot_id = ?
                    """, (result['slot_id'],))
                
                # Delete order (cascade will handle OrderItems, Invoice, Payments)
                cursor.execute("DELETE FROM Orders WHERE order_id = ?", (order_id,))
                conn.commit()
                
                show_success(f"Order {order_no} deleted successfully!")
                self.load_orders()
                
            except Exception as e:
                print(f"[OrdersWindow] Error deleting order: {e}")
                show_error(f"Failed to delete order: {str(e)}")
            finally:
                close_connection(conn)