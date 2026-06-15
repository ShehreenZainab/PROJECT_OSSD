"""
 Seed Data Module
Module: seed_data.py
Purpose: Insert comprehensive sample/test data into all tables on first run
"""

from database import get_connection, close_connection
import datetime
import random


# ==============================================
# HELPER FUNCTIONS
# ==============================================

def is_data_exists(conn):
    """Checks if data already exists in the database."""
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM Resident")
        result = cursor.fetchone()
        return result['count'] > 0
    except Exception:
        return False


def get_current_timestamp():
    """Returns current timestamp for database insertion"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_current_date():
    """Returns current date for database insertion"""
    return datetime.datetime.now().strftime("%Y-%m-%d")


def generate_order_number():
    """Generate a unique order number"""
    return f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100, 999)}"


# ==============================================
# MAIN SEEDING FUNCTION
# ==============================================

def seed_all():
    """Inserts comprehensive sample/test data into all 15 tables."""
    
    conn = get_connection()
    
    if conn is None:
        print("[Seed Error] Cannot seed data - database connection failed")
        return False
    
    try:
        if is_data_exists(conn):
            print("[Seed] Data already exists in database. Skipping seeding.")
            return True
        
        print("[Seed] Starting to seed comprehensive sample data...")
        
        cursor = conn.cursor()
        
        # ==============================================
        # TABLE 1: ProcessStage
        # ==============================================
        print("  [1/15] Seeding ProcessStage...")
        process_stages = [
            (1, 'Washing', 1, 45, 1),
            (2, 'Drying', 2, 60, 1),
            (3, 'Ironing', 3, 30, 1),
            (4, 'Packing', 4, 15, 1),
            (5, 'Quality Check', 5, 20, 1),
            (6, 'Delivery', 6, 120, 1),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO ProcessStage (stage_id, stage_name, stage_order, estimated_minutes, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', process_stages)
        
        # ==============================================
        # TABLE 2: Services
        # ==============================================
        print("  [2/15] Seeding Services...")
        services = [
            (1, 'Standard Wash', 'Regular washing with standard detergent', 50.00, None, 1),
            (2, 'Premium Wash', 'Premium detergent with fabric softener', 80.00, None, 1),
            (3, 'Dry Cleaning', 'Professional dry cleaning service', 150.00, None, 1),
            (4, 'Iron Only', 'Pressing and ironing service only', 30.00, None, 1),
            (5, 'Fold & Pack', 'Neat folding and packaging', 25.00, None, 1),
            (6, 'Bulk Laundry', 'Per kg pricing for bulk items', None, 80.00, 1),
            (7, 'Stain Removal', 'Specialized stain treatment', 100.00, None, 1),
            (8, 'Eco-Friendly Wash', 'Eco-friendly detergents and low water usage', 70.00, None, 1),
            (9, 'Express Service', '24-hour express service', 120.00, None, 1),
            (10, 'Wedding Attire', 'Special care for wedding dresses and suits', 250.00, None, 1),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Services (service_id, service_name, description, base_price, price_per_kg, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', services)
        
        # ==============================================
        # TABLE 3: DeliverySlots
        # ==============================================
        print("  [3/15] Seeding DeliverySlots...")
        delivery_slots = [
            (1, '2026-06-10', '08:00 AM - 10:00 AM', 10, 3, 1),
            (2, '2026-06-10', '10:00 AM - 12:00 PM', 10, 5, 1),
            (3, '2026-06-10', '12:00 PM - 02:00 PM', 10, 2, 1),
            (4, '2026-06-10', '02:00 PM - 04:00 PM', 10, 4, 1),
            (5, '2026-06-10', '04:00 PM - 06:00 PM', 10, 1, 1),
            (6, '2026-06-11', '08:00 AM - 10:00 AM', 10, 2, 1),
            (7, '2026-06-11', '10:00 AM - 12:00 PM', 10, 3, 1),
            (8, '2026-06-11', '12:00 PM - 02:00 PM', 10, 0, 1),
            (9, '2026-06-11', '02:00 PM - 04:00 PM', 10, 1, 1),
            (10, '2026-06-11', '04:00 PM - 06:00 PM', 10, 0, 1),
            (11, '2026-06-12', '08:00 AM - 10:00 AM', 10, 0, 1),
            (12, '2026-06-12', '10:00 AM - 12:00 PM', 10, 0, 1),
            (13, '2026-06-12', '12:00 PM - 02:00 PM', 10, 0, 1),
            (14, '2026-06-12', '02:00 PM - 04:00 PM', 10, 0, 1),
            (15, '2026-06-12', '04:00 PM - 06:00 PM', 10, 0, 1),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO DeliverySlots (slot_id, slot_date, slot_time, max_orders, booked_orders, is_available)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', delivery_slots)
        
        # ==============================================
        # TABLE 4: Staff
        # ==============================================
        print("  [4/15] Seeding Staff...")
        staff_data = [
            (1, 'John Smith', 'john.smith@teddyshine.com', '9876543210', 'Washer', '2024-01-15', 25000.00, 1),
            (2, 'Sarah Johnson', 'sarah.j@teddyshine.com', '9876543211', 'Washer', '2024-01-20', 24000.00, 1),
            (3, 'Mike Wilson', 'mike.w@teddyshine.com', '9876543212', 'Dryer', '2024-02-01', 23000.00, 1),
            (4, 'Emma Davis', 'emma.d@teddyshine.com', '9876543213', 'Ironer', '2024-02-10', 22000.00, 1),
            (5, 'David Brown', 'david.b@teddyshine.com', '9876543214', 'Packer', '2024-02-15', 26000.00, 1),
            (6, 'Lisa Anderson', 'lisa.a@teddyshine.com', '9876543215', 'Washer', '2024-03-01', 27000.00, 1),
            (7, 'Robert Taylor', 'robert.t@teddyshine.com', '9876543216', 'Delivery', '2024-03-10', 28000.00, 1),
            (8, 'Maria Garcia', 'maria.g@teddyshine.com', '9876543217', 'Delivery', '2024-03-15', 28000.00, 1),
            (9, 'James Wilson', 'james.w@teddyshine.com', '9876543218', 'Admin', '2024-01-01', 50000.00, 1),
            (10, 'Patricia Moore', 'patricia.m@teddyshine.com', '9876543219', 'Ironer', '2024-02-20', 22000.00, 1),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Staff (staff_id, full_name, email, phone, role, hire_date, salary, is_available)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', staff_data)
        
        # ==============================================
        # TABLE 5: Resident
        # ==============================================
        print("  [5/15] Seeding Resident...")
        residents = [
            (1, 'Alice Johnson', 'alice.johnson@example.com', '9876543220', '101', 'A', 1),
            (2, 'Bob Williams', 'bob.williams@example.com', '9876543221', '102', 'A', 1),
            (3, 'Carol Brown', 'carol.brown@example.com', '9876543222', '103', 'A', 1),
            (4, 'David Lee', 'david.lee@example.com', '9876543223', '104', 'A', 1),
            (5, 'Emma Watson', 'emma.watson@example.com', '9876543224', '105', 'A', 1),
            (6, 'Frank Miller', 'frank.miller@example.com', '9876543225', '201', 'B', 1),
            (7, 'Grace Davis', 'grace.davis@example.com', '9876543226', '202', 'B', 1),
            (8, 'Henry Wilson', 'henry.wilson@example.com', '9876543227', '203', 'B', 1),
            (9, 'Ivy Martinez', 'ivy.martinez@example.com', '9876543228', '204', 'B', 1),
            (10, 'Jack Anderson', 'jack.anderson@example.com', '9876543229', '205', 'B', 1),
            (11, 'Kelly Thomas', 'kelly.thomas@example.com', '9876543230', '301', 'C', 1),
            (12, 'Leo Taylor', 'leo.taylor@example.com', '9876543231', '302', 'C', 1),
            (13, 'Mia Moore', 'mia.moore@example.com', '9876543232', '303', 'C', 1),
            (14, 'Noah Jackson', 'noah.jackson@example.com', '9876543233', '304', 'C', 1),
            (15, 'Olivia White', 'olivia.white@example.com', '9876543234', '305', 'C', 1),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Resident (resident_id, full_name, email, phone, room_number, block_name, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', residents)
        
        # ==============================================
        # TABLE 6: SignUp
        # ==============================================
        print("  [6/15] Seeding SignUp...")
        signups = [
            (1, 1, 'alice_j', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your pet name?', 'Fluffy'),
            (2, 2, 'bob_w', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your mother maiden name?', 'Smith'),
            (3, 3, 'carol_b', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your birth city?', 'New York'),
            (4, 4, 'david_l', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What was your first school?', 'Sunrise School'),
            (5, 5, 'emma_w', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your favorite color?', 'Blue'),
            (6, 6, 'frank_m', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your pet name?', 'Max'),
            (7, 7, 'grace_d', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your mother maiden name?', 'Johnson'),
            (8, 8, 'henry_w', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your birth city?', 'Boston'),
            (9, 9, 'ivy_m', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What was your first school?', 'Park Avenue'),
            (10, 10, 'jack_a', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your favorite color?', 'Green'),
            (11, 11, 'kelly_t', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your pet name?', 'Bella'),
            (12, 12, 'leo_t', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your mother maiden name?', 'Brown'),
            (13, 13, 'mia_m', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your birth city?', 'Chicago'),
            (14, 14, 'noah_j', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What was your first school?', 'Lincoln Elementary'),
            (15, 15, 'olivia_w', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 'What is your favorite color?', 'Purple'),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO SignUp (signup_id, resident_id, username, password_hash, security_question, security_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', signups)
        
        # ==============================================
        # TABLE 7: LaundryItem
        # ==============================================
        print("  [7/15] Seeding LaundryItem...")
        laundry_items = [
            (1, 'Cotton Shirt', 'Clothing', 35.00, 1),
            (2, 'Formal Pants', 'Clothing', 45.00, 1),
            (3, 'Silk Saree', 'Traditional', 120.00, 1),
            (4, 'Cotton Saree', 'Traditional', 80.00, 1),
            (5, 'King Size Bed Sheet', 'Linen', 80.00, 1),
            (6, 'Queen Size Bed Sheet', 'Linen', 70.00, 1),
            (7, 'Bath Towel', 'Linen', 30.00, 1),
            (8, 'Hand Towel', 'Linen', 20.00, 1),
            (9, 'Denim Jeans', 'Clothing', 55.00, 1),
            (10, 'Leather Jacket', 'Outerwear', 150.00, 1),
            (11, 'Woolen Blanket', 'Linen', 140.00, 1),
            (12, 'T-Shirt', 'Clothing', 25.00, 1),
            (13, 'Winter Coat', 'Outerwear', 180.00, 1),
            (14, 'Pillow Cover', 'Linen', 15.00, 1),
            (15, 'Duvet Cover', 'Linen', 90.00, 1),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO LaundryItem (laundry_item_id, item_name, category, base_price, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', laundry_items)
        
        # TABLE 8: Orders
        print("  [8/15] Seeding Orders...")
        orders = [
            (1, 'ORD-001', 1, 1, 1, 2.5, 125.00, 10.00, 115.00, 'Completed', '2026-05-01 10:30:00', '2026-05-03', '2026-05-03', 'Handle with care'),
            (2, 'ORD-002', 2, 3, 2, 3.0, 240.00, 20.00, 220.00, 'Completed', '2026-05-05 11:00:00', '2026-05-07', '2026-05-07', 'Urgent delivery'),
            (3, 'ORD-003', 3, 4, 3, 1.5, 150.00, 15.00, 135.00, 'Completed', '2026-05-08 14:30:00', '2026-05-10', '2026-05-10', 'Deliver after 5 PM'),
            (4, 'ORD-004', 4, 5, 4, 4.0, 320.00, 30.00, 290.00, 'Completed', '2026-05-12 09:15:00', '2026-05-14', '2026-05-14', 'Separate whites and colors'),
            (5, 'ORD-005', 5, 6, 5, 2.0, 200.00, 20.00, 180.00, 'Completed', '2026-05-15 16:45:00', '2026-05-17', '2026-05-17', 'Use eco-friendly products'),
            (6, 'ORD-006', 6, 2, 6, 3.5, 280.00, 25.00, 255.00, 'Processing', '2026-05-20 10:00:00', '2026-05-22', None, 'Fragile items'),
            (7, 'ORD-007', 7, 7, 7, 2.0, 160.00, 10.00, 150.00, 'Processing', '2026-05-21 11:30:00', '2026-05-23', None, 'Express delivery requested'),
            (8, 'ORD-008', 8, 8, 8, 1.8, 140.00, 0.00, 140.00, 'Processing', '2026-05-22 09:45:00', '2026-05-24', None, None),
            (9, 'ORD-009', 9, 9, 9, 2.2, 180.00, 15.00, 165.00, 'Pending', '2026-05-23 14:00:00', '2026-05-25', None, 'Call before delivery'),
            (10, 'ORD-010', 10, 1, 10, 3.0, 250.00, 20.00, 230.00, 'Pending', '2026-05-24 08:30:00', '2026-05-26', None, 'Use hypoallergenic detergent'),
            (11, 'ORD-011', 11, 2, 11, 1.5, 120.00, 0.00, 120.00, 'Pending', '2026-05-25 12:15:00', '2026-05-27', None, None),
            (12, 'ORD-012', 12, 3, 12, 2.8, 220.00, 30.00, 190.00, 'Pending', '2026-05-26 15:30:00', '2026-05-28', None, 'Wedding attire - urgent'),
            (13, 'ORD-013', 13, 4, 13, 1.2, 95.00, 5.00, 90.00, 'Pending', '2026-06-03 09:00:00', '2026-06-05', None, 'Quick wash needed'),
            (14, 'ORD-014', 14, 5, 14, 4.5, 360.00, 40.00, 320.00, 'Pending', '2026-06-04 11:00:00', '2026-06-06', None, 'Multiple items - heavy load'),
            (15, 'ORD-015', 15, 6, 15, 2.3, 185.00, 15.00, 170.00, 'Pending', '2026-06-05 13:45:00', '2026-06-07', None, 'Business attire - no folds'),
            (16, 'ORD-016', 1, 7, 1, 1.0, 80.00, 0.00, 80.00, 'Cancelled', '2026-05-25 16:00:00', '2026-05-27', None, 'Customer cancelled'),
            (17, 'ORD-017', 2, 8, 2, 2.0, 160.00, 0.00, 160.00, 'Cancelled', '2026-05-26 10:00:00', '2026-05-28', None, 'Duplicate order'),
            (18, 'ORD-018', 3, 9, 3, 1.8, 145.00, 10.00, 135.00, 'Delivered', '2026-05-28 11:00:00', '2026-05-30', '2026-05-30', 'Received by security'),
            (19, 'ORD-019', 4, 1, 4, 3.2, 260.00, 25.00, 235.00, 'Delivered', '2026-05-29 14:30:00', '2026-05-31', '2026-05-31', 'Left at doorstep'),
            (20, 'ORD-020', 5, 2, 5, 2.5, 200.00, 0.00, 200.00, 'Delivered', '2026-05-30 09:15:00', '2026-06-01', '2026-06-01', 'Signed by resident'),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Orders (order_id, order_number, resident_id, staff_id, slot_id, total_weight_kg, total_amount, discount_amount, final_amount, status, order_date, expected_delivery_date, actual_delivery_date, special_instructions)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', orders)
        
        # TABLE 9: OrderItems
        print("  [9/15] Seeding OrderItems...")
        order_items = [
            (1, 1, 1, 1, 2, 35.00, 70.00),
            (2, 1, 2, 1, 1, 45.00, 45.00),
            (3, 1, 5, 6, 1, 80.00, 80.00),
            (4, 2, 9, 1, 3, 55.00, 165.00),
            (5, 2, 12, 1, 2, 25.00, 50.00),
            (6, 2, 6, 6, 2, 70.00, 140.00),
            (7, 3, 3, 3, 1, 120.00, 120.00),
            (8, 3, 7, 4, 2, 30.00, 60.00),
            (9, 4, 5, 1, 2, 80.00, 160.00),
            (10, 4, 15, 1, 1, 90.00, 90.00),
            (11, 4, 7, 4, 3, 30.00, 90.00),
            (12, 5, 4, 6, 2, 70.00, 140.00),
            (13, 5, 8, 4, 2, 20.00, 40.00),
            (14, 6, 2, 1, 2, 45.00, 90.00),
            (15, 6, 9, 1, 3, 55.00, 165.00),
            (16, 6, 5, 6, 1, 80.00, 80.00),
            (17, 7, 12, 1, 4, 25.00, 100.00),
            (18, 7, 1, 1, 2, 35.00, 70.00),
            (19, 8, 11, 3, 1, 25.00, 25.00),
            (20, 8, 6, 6, 2, 70.00, 140.00),
            (21, 9, 3, 3, 1, 120.00, 120.00),
            (22, 9, 8, 4, 2, 20.00, 40.00),
            (23, 9, 14, 4, 1, 15.00, 15.00),
            (24, 10, 1, 1, 3, 35.00, 105.00),
            (25, 10, 2, 1, 2, 45.00, 90.00),
            (26, 10, 7, 4, 1, 30.00, 30.00),
            (27, 11, 12, 1, 2, 25.00, 50.00),
            (28, 11, 5, 6, 1, 80.00, 80.00),
            (29, 12, 9, 1, 1, 55.00, 55.00),
            (30, 12, 13, 3, 1, 25.00, 25.00),
            (31, 12, 14, 4, 2, 15.00, 30.00),
            (32, 13, 12, 1, 1, 25.00, 25.00),
            (33, 13, 1, 1, 2, 35.00, 70.00),
            (34, 14, 2, 1, 2, 45.00, 90.00),
            (35, 14, 5, 6, 2, 80.00, 160.00),
            (36, 14, 7, 4, 3, 30.00, 90.00),
            (37, 15, 3, 3, 1, 120.00, 120.00),
            (38, 15, 8, 4, 2, 20.00, 40.00),
            (39, 16, 1, 1, 1, 35.00, 35.00),
            (40, 17, 2, 1, 2, 45.00, 90.00),
            (41, 18, 3, 3, 1, 120.00, 120.00),
            (42, 19, 4, 1, 2, 45.00, 90.00),
            (43, 19, 5, 6, 1, 80.00, 80.00),
            (44, 20, 5, 1, 2, 45.00, 90.00),
            (45, 20, 12, 1, 2, 25.00, 50.00),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO OrderItems (order_item_id, order_id, laundry_item_id, service_id, quantity, unit_price, subtotal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', order_items)
        
        # ==============================================
        # TABLE 10: Tracking
        # ==============================================
        print("  [10/15] Seeding Tracking...")
        tracking = [
            (1, 1, 1, 1, '2026-05-01 11:00:00', '2026-05-01 12:00:00', 'Completed', None),
            (2, 1, 2, 2, '2026-05-01 12:00:00', '2026-05-01 13:30:00', 'Completed', None),
            (3, 1, 3, 3, '2026-05-01 13:30:00', '2026-05-01 14:00:00', 'Completed', None),
            (4, 1, 4, 4, '2026-05-01 14:00:00', '2026-05-01 14:15:00', 'Completed', None),
            (5, 1, 5, 5, '2026-05-01 14:15:00', '2026-05-01 14:30:00', 'Completed', None),
            (6, 1, 6, 6, '2026-05-02 09:00:00', '2026-05-03 10:00:00', 'Completed', 'Delivered to door'),
            (7, 2, 1, 2, '2026-05-05 11:30:00', '2026-05-05 12:30:00', 'Completed', None),
            (8, 2, 2, 4, '2026-05-05 12:30:00', '2026-05-05 13:45:00', 'Completed', None),
            (9, 2, 3, 5, '2026-05-05 13:45:00', '2026-05-05 14:00:00', 'Completed', None),
            (10, 2, 4, 6, '2026-05-05 14:00:00', '2026-05-06 09:00:00', 'Completed', None),
            (11, 6, 1, 1, '2026-05-20 11:00:00', '2026-05-20 12:00:00', 'Completed', None),
            (12, 6, 2, 2, '2026-05-20 12:00:00', '2026-05-20 13:30:00', 'Completed', None),
            (13, 6, 3, 3, '2026-05-20 14:00:00', None, 'InProgress', None),
            (14, 7, 1, 7, '2026-05-21 11:30:00', '2026-05-21 12:30:00', 'Completed', None),
            (15, 7, 2, 1, '2026-05-21 12:30:00', None, 'InProgress', None),
            (16, 8, 1, 1, '2026-05-22 10:00:00', None, 'InProgress', None),
            (17, 9, 1, 1, None, None, 'Pending', 'Waiting for pickup'),
            (18, 10, 1, 1, None, None, 'Pending', 'Waiting for pickup'),
            (19, 11, 1, 1, None, None, 'Pending', 'Waiting for pickup'),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Tracking (tracking_id, order_id, stage_id, staff_id, start_time, end_time, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', tracking)
        
        # ==============================================
        # TABLE 11: Invoice
        # ==============================================
        print("  [11/15] Seeding Invoice...")
        invoices = [
            (1, 1, 'INV-001', 125.00, 10.00, 0.00, 115.00, 115.00, 0.00, 'Paid', '2026-05-01 15:00:00', '2026-05-10', '2026-05-02 10:00:00'),
            (2, 2, 'INV-002', 240.00, 20.00, 0.00, 220.00, 220.00, 0.00, 'Paid', '2026-05-05 16:00:00', '2026-05-14', '2026-05-06 11:00:00'),
            (3, 3, 'INV-003', 150.00, 15.00, 0.00, 135.00, 135.00, 0.00, 'Paid', '2026-05-08 17:00:00', '2026-05-17', '2026-05-09 14:00:00'),
            (4, 4, 'INV-004', 320.00, 30.00, 0.00, 290.00, 290.00, 0.00, 'Paid', '2026-05-12 13:00:00', '2026-05-21', '2026-05-13 09:00:00'),
            (5, 5, 'INV-005', 200.00, 20.00, 0.00, 180.00, 180.00, 0.00, 'Paid', '2026-05-15 18:00:00', '2026-05-24', '2026-05-16 10:00:00'),
            (6, 6, 'INV-006', 280.00, 25.00, 0.00, 255.00, 150.00, 105.00, 'Partial', '2026-05-20 12:00:00', '2026-05-29', None),
            (7, 7, 'INV-007', 160.00, 10.00, 0.00, 150.00, 100.00, 50.00, 'Partial', '2026-05-21 13:00:00', '2026-05-30', None),
            (8, 8, 'INV-008', 140.00, 0.00, 0.00, 140.00, 0.00, 140.00, 'Unpaid', '2026-05-22 10:30:00', '2026-05-31', None),
            (9, 9, 'INV-009', 180.00, 15.00, 0.00, 165.00, 0.00, 165.00, 'Unpaid', '2026-05-23 14:30:00', '2026-06-01', None),
            (10, 10, 'INV-010', 250.00, 20.00, 0.00, 230.00, 0.00, 230.00, 'Unpaid', '2026-05-24 09:00:00', '2026-06-02', None),
            (11, 11, 'INV-011', 120.00, 0.00, 0.00, 120.00, 0.00, 120.00, 'Unpaid', '2026-05-25 13:00:00', '2026-06-03', None),
            (12, 12, 'INV-012', 220.00, 30.00, 0.00, 190.00, 0.00, 190.00, 'Unpaid', '2026-05-26 16:00:00', '2026-06-04', None),
            (13, 13, 'INV-013', 95.00, 5.00, 0.00, 90.00, 0.00, 90.00, 'Unpaid', '2026-06-03 10:00:00', '2026-06-12', None),
            (14, 14, 'INV-014', 360.00, 40.00, 0.00, 320.00, 0.00, 320.00, 'Unpaid', '2026-06-04 12:00:00', '2026-06-13', None),
            (15, 15, 'INV-015', 185.00, 15.00, 0.00, 170.00, 0.00, 170.00, 'Unpaid', '2026-06-05 14:30:00', '2026-06-14', None),
            (16, 16, 'INV-016', 80.00, 0.00, 0.00, 80.00, 0.00, 80.00, 'Unpaid', '2026-05-25 17:00:00', '2026-06-03', None),
            (17, 17, 'INV-017', 160.00, 0.00, 0.00, 160.00, 0.00, 160.00, 'Unpaid', '2026-05-26 11:00:00', '2026-06-04', None),
            (18, 18, 'INV-018', 145.00, 10.00, 0.00, 135.00, 135.00, 0.00, 'Paid', '2026-05-28 12:00:00', '2026-06-06', '2026-05-29 09:00:00'),
            (19, 19, 'INV-019', 260.00, 25.00, 0.00, 235.00, 235.00, 0.00, 'Paid', '2026-05-29 15:00:00', '2026-06-07', '2026-05-30 10:00:00'),
            (20, 20, 'INV-020', 200.00, 0.00, 0.00, 200.00, 200.00, 0.00, 'Paid', '2026-05-30 10:00:00', '2026-06-08', '2026-05-31 09:00:00'),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Invoice (invoice_id, order_id, invoice_number, subtotal, discount_amount, tax_amount, total_amount, amount_paid, balance_due, status, generated_date, due_date, paid_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', invoices)
        
        # ==============================================
        # TABLE 12: Payments
        # ==============================================
        print("  [12/15] Seeding Payments...")
        payments = [
            (1, 1, 1, 115.00, 'Cash', '2026-05-02 10:00:00', 'TXN-001', 'Completed', 'Full payment received'),
            (2, 2, 2, 220.00, 'Card', '2026-05-06 11:00:00', 'TXN-002', 'Completed', 'Full payment'),
            (3, 3, 3, 135.00, 'Online', '2026-05-09 14:00:00', 'TXN-003', 'Completed', 'Paid via UPI'),
            (4, 4, 4, 290.00, 'Cash', '2026-05-13 09:00:00', 'TXN-004', 'Completed', 'Full payment in cash'),
            (5, 5, 5, 180.00, 'Card', '2026-05-16 10:00:00', 'TXN-005', 'Completed', 'Credit card payment'),
            (6, 6, 6, 100.00, 'Cash', '2026-05-21 11:00:00', 'TXN-006', 'Completed', 'First installment'),
            (7, 6, 6, 50.00, 'Online', '2026-05-23 14:00:00', 'TXN-007', 'Completed', 'Second installment'),
            (8, 7, 7, 100.00, 'Card', '2026-05-22 10:00:00', 'TXN-008', 'Completed', 'Partial payment'),
            (18, 18, 18, 135.00, 'Online', '2026-05-29 09:00:00', 'TXN-018', 'Completed', 'Paid via app'),
            (19, 19, 19, 235.00, 'Cash', '2026-05-30 10:00:00', 'TXN-019', 'Completed', 'Cash payment'),
            (20, 20, 20, 200.00, 'Card', '2026-05-31 09:00:00', 'TXN-020', 'Completed', 'Card on delivery'),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Payments (payment_id, invoice_id, order_id, amount, payment_method, payment_date, transaction_id, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', payments)
        
        # ==============================================
        # TABLE 13: Records
        # ==============================================
        print("  [13/15] Seeding Records...")
        records = [
            (1, 1, 'Created', None, 'Order created', 'Resident', 1, '2026-05-01 10:30:00', '192.168.1.1'),
            (2, 1, 'Status_Changed', 'Pending', 'Processing', 'Staff', 1, '2026-05-01 11:00:00', '192.168.1.100'),
            (3, 1, 'Status_Changed', 'Processing', 'Completed', 'Staff', 1, '2026-05-03 10:00:00', '192.168.1.100'),
            (4, 1, 'Payment', None, 'Received 115.00', 'Admin', 9, '2026-05-02 10:05:00', '192.168.1.100'),
            (5, 2, 'Created', None, 'Order created', 'Resident', 2, '2026-05-05 11:00:00', '192.168.1.2'),
            (6, 2, 'Payment', None, 'Received 220.00', 'Admin', 9, '2026-05-06 11:05:00', '192.168.1.100'),
            (7, 3, 'Created', None, 'Order created', 'Resident', 3, '2026-05-08 14:30:00', '192.168.1.3'),
            (8, 4, 'Created', None, 'Order created', 'Resident', 4, '2026-05-12 09:15:00', '192.168.1.4'),
            (9, 5, 'Created', None, 'Order created', 'Resident', 5, '2026-05-15 16:45:00', '192.168.1.5'),
            (10, 6, 'Created', None, 'Order created', 'Resident', 6, '2026-05-20 10:00:00', '192.168.1.6'),
            (11, 6, 'Status_Changed', 'Pending', 'Processing', 'Staff', 1, '2026-05-20 11:00:00', '192.168.1.100'),
            (12, 6, 'Payment', None, 'Received 100.00', 'Admin', 9, '2026-05-21 11:00:00', '192.168.1.100'),
            (13, 7, 'Created', None, 'Order created', 'Resident', 7, '2026-05-21 11:30:00', '192.168.1.7'),
            (14, 8, 'Created', None, 'Order created', 'Resident', 8, '2026-05-22 09:45:00', '192.168.1.8'),
            (15, 9, 'Created', None, 'Order created', 'Resident', 9, '2026-05-23 14:00:00', '192.168.1.9'),
            (16, 10, 'Created', None, 'Order created', 'Resident', 10, '2026-05-24 08:30:00', '192.168.1.10'),
            (17, 11, 'Created', None, 'Order created', 'Resident', 11, '2026-05-25 12:15:00', '192.168.1.11'),
            (18, 12, 'Created', None, 'Order created', 'Resident', 12, '2026-05-26 15:30:00', '192.168.1.12'),
            (19, 13, 'Created', None, 'Order created', 'Resident', 13, '2026-06-03 09:00:00', '192.168.1.13'),
            (20, 14, 'Created', None, 'Order created', 'Resident', 14, '2026-06-04 11:00:00', '192.168.1.14'),
            (21, 15, 'Created', None, 'Order created', 'Resident', 15, '2026-06-05 13:45:00', '192.168.1.15'),
            (22, 16, 'Created', None, 'Order created', 'Resident', 1, '2026-05-25 16:00:00', '192.168.1.1'),
            (23, 16, 'Status_Changed', 'Pending', 'Cancelled', 'Resident', 1, '2026-05-25 17:00:00', '192.168.1.1'),
            (24, 17, 'Created', None, 'Order created', 'Resident', 2, '2026-05-26 10:00:00', '192.168.1.2'),
            (25, 17, 'Status_Changed', 'Pending', 'Cancelled', 'Admin', 9, '2026-05-26 11:00:00', '192.168.1.100'),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Records (record_id, order_id, action_type, old_value, new_value, changed_by, changed_by_id, timestamp, ip_address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', records)
        
        # ==============================================
        # TABLE 14: Print
        # ==============================================
        print("  [14/15] Seeding Print...")
        prints = [
            (1, 1, 'RCP-001', 'Admin User', 9, '2026-05-02 10:05:00', '/receipts/INV-001.pdf', 1, 'Success'),
            (2, 2, 'RCP-002', 'Admin User', 9, '2026-05-06 11:05:00', '/receipts/INV-002.pdf', 1, 'Success'),
            (3, 3, 'RCP-003', 'Admin User', 9, '2026-05-09 14:05:00', '/receipts/INV-003.pdf', 1, 'Success'),
            (4, 4, 'RCP-004', 'Admin User', 9, '2026-05-13 09:05:00', '/receipts/INV-004.pdf', 2, 'Success'),
            (5, 5, 'RCP-005', 'Admin User', 9, '2026-05-16 10:05:00', '/receipts/INV-005.pdf', 1, 'Success'),
            (6, 6, 'RCP-006', 'Staff', 1, '2026-05-21 11:05:00', '/receipts/INV-006.pdf', 1, 'Success'),
            (7, 18, 'RCP-018', 'Admin User', 9, '2026-05-29 09:05:00', '/receipts/INV-018.pdf', 1, 'Success'),
            (8, 19, 'RCP-019', 'Staff', 7, '2026-05-30 10:05:00', '/receipts/INV-019.pdf', 1, 'Success'),
            (9, 20, 'RCP-020', 'Admin User', 9, '2026-05-31 09:05:00', '/receipts/INV-020.pdf', 1, 'Success'),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Print (print_id, invoice_id, receipt_number, printed_by, printed_by_id, print_time, file_path, copies, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', prints)
        
        # ==============================================
        # TABLE 15: Login
        # ==============================================
        print("  [15/15] Seeding Login...")
        logins = [
            (1, 1, 'resident', '2026-05-01 10:00:00', '192.168.1.1', 'token_001', 0),
            (2, 1, 'resident', '2026-05-02 09:30:00', '192.168.1.1', 'token_002', 0),
            (3, 2, 'resident', '2026-05-05 10:00:00', '192.168.1.2', 'token_003', 0),
            (4, 3, 'resident', '2026-05-08 14:00:00', '192.168.1.3', 'token_004', 0),
            (5, 4, 'resident', '2026-05-12 09:00:00', '192.168.1.4', 'token_005', 0),
            (6, 5, 'resident', '2026-05-15 16:00:00', '192.168.1.5', 'token_006', 0),
            (7, 6, 'resident', '2026-05-20 09:00:00', '192.168.1.6', 'token_007', 0),
            (8, 9, 'admin', '2026-05-01 08:00:00', '192.168.1.100', 'admin_token_001', 0),
            (9, 9, 'admin', '2026-05-15 09:00:00', '192.168.1.100', 'admin_token_002', 0),
            (10, 9, 'admin', '2026-05-20 08:30:00', '192.168.1.100', 'admin_token_003', 1),
            (11, 1, 'staff', '2026-05-20 08:00:00', '192.168.1.101', 'staff_token_001', 0),
            (12, 2, 'staff', '2026-05-20 09:00:00', '192.168.1.102', 'staff_token_002', 0),
        ]
        cursor.executemany('''
            INSERT OR IGNORE INTO Login (login_id, user_id, user_type, login_time, ip_address, session_token, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', logins)
        
        conn.commit()
        
        print("[Seed] All sample data seeded successfully!")
        
        print("\n" + "="*50)
        print("  Seeded Data Summary:")
        print("="*50)
        print(f"  • ProcessStage: {len(process_stages)} stages")
        print(f"  • Services: {len(services)} services")
        print(f"  • DeliverySlots: {len(delivery_slots)} slots")
        print(f"  • Staff: {len(staff_data)} members")
        print(f"  • Residents: {len(residents)} residents")
        print(f"  • SignUp: {len(signups)} accounts")
        print(f"  • LaundryItem: {len(laundry_items)} items")
        print(f"  • Orders: {len(orders)} orders")
        print(f"  • OrderItems: {len(order_items)} items")
        print(f"  • Tracking: {len(tracking)} tracking records")
        print(f"  • Invoice: {len(invoices)} invoices")
        print(f"  • Payments: {len(payments)} payments")
        print(f"  • Records: {len(records)} records")
        print(f"  • Print: {len(prints)} receipts")
        print(f"  • Login: {len(logins)} sessions")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"[Seed Error] Failed to seed data: {e}")
        if conn:
            conn.rollback()
        return False
    
    finally:
        close_connection(conn)


# ==============================================
# GET DATA COUNT (for verification)
# ==============================================

def get_data_counts():
    """Returns a dictionary with record counts for each table."""
    tables = [
        'ProcessStage', 'Services', 'DeliverySlots', 'Staff', 'Resident',
        'SignUp', 'LaundryItem', 'Orders', 'OrderItems',
        'Tracking', 'Invoice', 'Payments', 'Records', 'Print', 'Login'
    ]
    
    conn = get_connection()
    counts = {}
    
    if conn:
        try:
            cursor = conn.cursor()
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                result = cursor.fetchone()
                counts[table] = result['count'] if result else 0
        except Exception as e:
            print(f"[Count Error] {e}")
            counts = {table: -1 for table in tables}
        finally:
            close_connection(conn)
    else:
        counts = {table: -1 for table in tables}
    
    return counts

