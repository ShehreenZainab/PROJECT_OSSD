"""
TeddyShine Laundry Management System - Main Application Entry Point
Color Theme: Light Greenish-Gray (#E8F0E6 background style)
Module: main.py
Purpose: App entry point - initializes everything and manages window switching
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import database initialization modules
from database.database import get_connection, close_connection
from database.schema import create_tables
from database.seed_data import seed_all

# Import all window classes
from Windows.login_window import LoginWindow
from Windows.dashboard_window import DashboardWindow
from Windows.residents_window import ResidentsWindow
from Windows.orders_window import OrdersWindow
from Windows.services_window import ServicesWindow
from Windows.staff_window import StaffWindow
from Windows.tracking_window import TrackingWindow
from Windows.invoice_window import InvoiceWindow
from Windows.payments_window import PaymentsWindow
from Windows.reports_window import ReportsWindow

# Import helpers
from utils.helpers import center_window, show_error, show_success


class App(tk.Tk):
    """
    Main Application Class - Entry point for TeddyShine Laundry Management System.
    Manages window switching and acts as the router between all screens.
    """
    
    # Application metadata
    APP_NAME = "TeddyShine Laundry Management System"
    APP_VERSION = "1.0.0"
    APP_WIDTH = 1200
    APP_HEIGHT = 700
    
    # Logo file path
    LOGO_PATH = "logo.png"
    
    # Color theme
    COLORS = {
        'bg': '#E8F0E6',           # Light greenish-gray background
        'primary': '#2E7D32',       # Dark green
        'text': '#1B5E20',          # Dark green text
        'text_light': '#FFFFFF'     # Light text
    }
    
    # Screen name to window class mapping (Router configuration)
    SCREENS = {
        "dashboard": DashboardWindow,
        "residents": ResidentsWindow,
        "orders": OrdersWindow,
        "services": ServicesWindow,
        "staff": StaffWindow,
        "tracking": TrackingWindow,
        "invoices": InvoiceWindow,
        "payments": PaymentsWindow,
        "reports": ReportsWindow
    }
    
    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        
        # Configure the main window
        self.title(f"{self.APP_NAME} v{self.APP_VERSION}")
        self.geometry(f"{self.APP_WIDTH}x{self.APP_HEIGHT}")
        self.configure(bg=self.COLORS['bg'])
        
        # Center the window on screen
        center_window(self, self.APP_WIDTH, self.APP_HEIGHT)
        
        # Set minimum window size
        self.minsize(900, 600)
        
        # Initialize database
        self.initialize_database()
        
        # Create main container frame
        self.container = tk.Frame(self, bg=self.COLORS['bg'])
        self.container.pack(fill='both', expand=True)
        
        # Current active screen tracking
        self.current_screen = None
        self.current_screen_name = None
        
        # Start with login screen
        self.show_login()
        
        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def load_logo(self, size=(80, 80)):
        """
        Load and resize the PNG logo.
        
        Args:
            size (tuple): Desired logo size (width, height)
        
        Returns:
            PhotoImage: Resized logo image or None if not found
        """
        try:
            # Try multiple possible locations for the logo
            possible_paths = [
                self.LOGO_PATH,
                os.path.join(os.path.dirname(__file__), "logo.png"),
                os.path.join(os.path.dirname(__file__), "assets", "logo.png"),
                os.path.join(os.path.dirname(__file__), "images", "logo.png"),
                "assets/logo.png",
                "images/logo.png",
                "../logo.png"
            ]
            
            logo_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    logo_path = path
                    print(f"[Main] Logo found at: {path}")
                    break
                    
            if logo_path:
                # Open and resize the image
                image = Image.open(logo_path)
                image = image.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
            else:
                print("[Main] ERROR: Logo file not found in any expected location!")
                print(f"[Main] Tried paths: {possible_paths}")
                return None
                
        except Exception as e:
            print(f"[Main] Error loading logo: {e}")
            return None
            
    def initialize_database(self):
        """
        Initialize the database by creating tables and seeding sample data.
        Shows progress messages to the user.
        """
        # Create a splash screen for database initialization
        splash = tk.Toplevel(self)
        splash.title("Initializing...")
        splash.geometry("400x300")
        splash.configure(bg=self.COLORS['bg'])
        center_window(splash, 400, 300)
        splash.overrideredirect(True)  # Remove window decorations
        splash.lift()
        splash.focus_force()
        
        # Loading message frame
        main_frame = tk.Frame(splash, bg=self.COLORS['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Load and display logo (PNG only)
        self.splash_logo = self.load_logo(size=(80, 80))
        
        if self.splash_logo:
            # Display the PNG logo
            logo_label = tk.Label(
                main_frame,
                image=self.splash_logo,
                bg=self.COLORS['bg']
            )
            logo_label.pack(pady=(0, 10))
            # Keep a reference to prevent garbage collection
            logo_label.image = self.splash_logo
        else:
            # If logo not found, show error message
            error_label = tk.Label(
                main_frame,
                text="⚠️ LOGO FILE NOT FOUND ⚠️\n\nPlease ensure 'logo.png' is in the\napplication directory.",
                font=('Helvetica', 10),
                bg=self.COLORS['bg'],
                fg='red'
            )
            error_label.pack(pady=(0, 10))
        
        # Title
        title_label = tk.Label(
            main_frame,
            text=self.APP_NAME,
            font=('Helvetica', 14, 'bold'),
            bg=self.COLORS['bg'],
            fg=self.COLORS['primary']
        )
        title_label.pack()
        
        # Status label
        self.splash_status = tk.Label(
            main_frame,
            text="Initializing database...",
            font=('Helvetica', 10),
            bg=self.COLORS['bg'],
            fg=self.COLORS['text']
        )
        self.splash_status.pack(pady=(15, 5))
        
        # Progress bar (simple text-based)
        self.progress_label = tk.Label(
            main_frame,
            text="▱▱▱▱▱▱▱▱▱▱",
            font=('Courier', 12),
            bg=self.COLORS['bg'],
            fg=self.COLORS['primary']
        )
        self.progress_label.pack(pady=5)
        
        splash.update()
        
        try:
            # Step 1: Create tables
            self.update_splash_status(splash, "Creating database tables...", 2)
            print("[Main] Creating database tables...")
            
            if create_tables():
                self.update_splash_status(splash, "Tables created successfully!", 4)
                print("[Main] Tables created successfully.")
            else:
                self.update_splash_status(splash, "Warning: Table creation had issues", 4)
                print("[Main] Warning: Table creation had issues")
            
            # Step 2: Seed sample data
            self.update_splash_status(splash, "Seeding sample data...", 6)
            print("[Main] Seeding sample data...")
            
            if seed_all():
                self.update_splash_status(splash, "Sample data seeded!", 8)
                print("[Main] Sample data seeded successfully.")
            else:
                self.update_splash_status(splash, "Warning: Sample data seeding had issues", 8)
                print("[Main] Warning: Sample data seeding had issues")
            
            # Complete
            self.update_splash_status(splash, "Ready!", 10)
            
            # Keep splash for a moment to show completion
            splash.after(800, splash.destroy)
            
        except Exception as e:
            print(f"[Main] Database initialization error: {e}")
            self.splash_status.config(text=f"Error: {str(e)[:50]}", fg='red')
            splash.after(2000, splash.destroy)
            self.after(100, lambda: show_error(f"Database initialization failed:\n{str(e)}\n\nThe application may not function correctly."))
            
    def update_splash_status(self, splash, message, progress):
        """Updates the splash screen status and progress bar."""
        if splash and splash.winfo_exists():
            self.splash_status.config(text=message)
            
            # Update progress bar (10 blocks = 100%)
            filled = progress // 10
            empty = 10 - filled
            progress_text = "█" * filled + "▱" * empty
            self.progress_label.config(text=progress_text)
            splash.update()
            
    def clear_container(self):
        """Destroy all widgets in the main container."""
        if self.current_screen:
            self.current_screen.destroy()
            self.current_screen = None
            
    def show_login(self):
        """Show the login screen."""
        self.clear_container()
        self.current_screen_name = "login"
        self.current_screen = LoginWindow(self.container, self.show_dashboard)
        self.current_screen.pack(fill='both', expand=True)
        
    def show_dashboard(self):
        """Show the main dashboard screen."""
        self.clear_container()
        self.current_screen_name = "dashboard"
        self.current_screen = DashboardWindow(self.container, self.navigate)
        self.current_screen.pack(fill='both', expand=True)
        
    def navigate(self, screen_name):
        """
        Navigate to a different screen.
        
        Args:
            screen_name (str): Name of the screen to navigate to.
                               Special values: "logout", "dashboard"
        """
        # Handle special navigation cases
        if screen_name == "logout":
            self.show_login()
            return
            
        if screen_name == "dashboard":
            self.show_dashboard()
            return
            
        # Check if screen exists in router mapping
        if screen_name in self.SCREENS:
            self.clear_container()
            self.current_screen_name = screen_name
            # Pass the go_back callback (which is show_dashboard)
            self.current_screen = self.SCREENS[screen_name](self.container, self.show_dashboard)
            self.current_screen.pack(fill='both', expand=True)
        else:
            print(f"[Main] Error: Unknown screen '{screen_name}'")
            show_error(f"Cannot navigate to '{screen_name}'. Screen not found.")
            
    def on_closing(self):
        """Handle window close event - ask for confirmation."""
        if messagebox.askokcancel("Quit", "Are you sure you want to quit TeddyShine Laundry System?"):
            print("[Main] Application closing...")
            
            # Close any open database connections
            try:
                conn = get_connection()
                if conn:
                    close_connection(conn)
            except:
                pass
                
            self.quit()
            self.destroy()


# ==============================================
# APPLICATION ENTRY POINT
# ==============================================

if __name__ == "__main__":
    print("=" * 60)
    print(f"  {App.APP_NAME}")
    print(f"  Version {App.APP_VERSION}")
    print("=" * 60)
    print("  Starting application...")
    print("")
    
    try:
        # Create and run the application
        app = App()
        print("[Main] Application window created.")
        print("[Main] Entering main loop...")
        app.mainloop()
        print("[Main] Application closed.")
        
    except KeyboardInterrupt:
        print("\n[Main] Application interrupted by user.")
    except Exception as e:
        print(f"[Main] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        messagebox.showerror(
            "Fatal Error",
            f"An unexpected error occurred:\n\n{str(e)}\n\nThe application will now close."
        )
        sys.exit(1)