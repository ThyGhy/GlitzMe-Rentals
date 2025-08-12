import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Union

DATABASE_PATH = 'glitzme_rentals.db'

class DatabaseManager:
    """
    Database manager for GlitzME Rentals website
    Handles all database operations including initialization, CRUD operations,
    and data management for the admin dashboard.
    """
    
    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection with row factory for easier access"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create rental_items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rental_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image_path TEXT NOT NULL,
                price TEXT NOT NULL,
                deposit TEXT,
                price_text TEXT DEFAULT 'Price',
                deposit_text TEXT DEFAULT 'Required Deposit (Refundable)',
                category TEXT DEFAULT 'general',
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                display_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create package_items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS package_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                image_path TEXT NOT NULL,
                price TEXT NOT NULL,
                price_text TEXT DEFAULT 'Contact For Details',
                description TEXT,
                is_active BOOLEAN DEFAULT 1,
                display_order INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create team_members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                image_path TEXT NOT NULL,
                mobile_image_path TEXT,
                display_order INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create site_settings table for configurable site content
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS site_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL,
                setting_value TEXT,
                setting_type TEXT DEFAULT 'text',
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create gallery_images table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS gallery_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                alt_text TEXT,
                category TEXT DEFAULT 'event',
                is_featured BOOLEAN DEFAULT 0,
                display_order INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create content_pages table for dynamic page content
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_identifier TEXT UNIQUE NOT NULL,
                section_key TEXT NOT NULL,
                content TEXT NOT NULL,
                content_type TEXT DEFAULT 'text',
                display_order INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create carousel_items table for homepage carousel
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS carousel_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                image_path TEXT NOT NULL,
                mobile_image_path TEXT,
                alt_text TEXT NOT NULL,
                link_url TEXT,
                link_text TEXT,
                display_order INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Initialize with default data if tables are empty
        self._populate_default_data()
    
    def _populate_default_data(self):
        """Populate database with existing hardcoded data"""
        # Check if we need to populate data
        if self.get_rental_items():
            return  # Data already exists
        
        # Insert default rental items
        default_rentals = [
            {
                'name': 'Tables & Chairs',
                'image_path': 'Images/SingularRentals/GMR (Tables & Chairs)(1).webp',
                'price': 'Tables $5-$14 per (Depends On Table Type), Chairs $1-$6 per (Depends On Chair Type), Ask for Details',
                'deposit': '$25.00 - $150.00 Required Deposit',
                'price_text': 'Prices',
                'category': 'furniture'
            },
            {
                'name': 'Arcade Games',
                'image_path': 'Images/SingularRentals/GMR (Arcade Games)(1).webp',
                'price': '$200.00/Day Rental',
                'deposit': '$100.00 Required Deposit',
                'price_text': 'Price',
                'category': 'entertainment'
            },
            {
                'name': 'Canopy Tents',
                'image_path': 'Images/SingularRentals/GMR (Canopy Tent)(1).webp',
                'price': 'Starting at $70',
                'deposit': '$100.00 Required Refundable Deposit',
                'price_text': 'Prices Vary',
                'category': 'shelter'
            },
            {
                'name': 'Red Carpet',
                'image_path': 'Images/SingularRentals/GMR (Red Carpet)(1).webp',
                'price': '$80.00/Day Rental',
                'deposit': '$50.00 Required Deposit',
                'price_text': 'Price',
                'category': 'decor'
            },
            {
                'name': 'Black Carpet',
                'image_path': 'Images/SingularRentals/GMR (Black Carpet)(1).webp',
                'price': '$80/Day Rental',
                'deposit': '$50 Required Deposit',
                'price_text': 'Price',
                'category': 'decor'
            },
            {
                'name': 'Nacho Machine',
                'image_path': 'Images/SingularRentals/GMR (Nacho Machine)(1).webp',
                'price': '$60/Day Rental',
                'deposit': '$50 Required Deposit',
                'price_text': 'Price',
                'category': 'food_beverage'
            },
            {
                'name': 'Mobile Bars',
                'image_path': 'Images/SingularRentals/GMR (Mobile Bars)(1).webp',
                'price': 'Starting at $30',
                'deposit': '$100 Required Deposit',
                'price_text': 'Prices Vary',
                'category': 'food_beverage'
            },
            {
                'name': 'Queens/Throne Chair',
                'image_path': 'Images/SingularRentals/GMR (Kids Throne Chair)(1).webp',
                'price': '$44/Day Rental',
                'deposit': '$50 Required Deposit',
                'price_text': 'Price',
                'category': 'furniture'
            },
            {
                'name': 'Snow Machine',
                'image_path': 'Images/SingularRentals/GMR (Snow Machine)(1).webp',
                'price': '$45/Day Rental',
                'deposit': '$25 Required Deposit',
                'price_text': 'Price',
                'category': 'effects'
            }
        ]
        
        for i, rental in enumerate(default_rentals):
            rental['display_order'] = i
            self.add_rental_item(**rental)
        
        # Insert default package items
        default_packages = [
            {
                'name': 'Movie Theater Experience',
                'image_path': 'Images/Packages/GMR (Movie Theater Experience)(1).webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Boy Soft Play Extreme',
                'image_path': 'Images/Packages/GMR (Boy Soft Play Extreme)(1).webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Girl Soft Play Extreme',
                'image_path': 'Images/Packages/GMR (Girl Soft Play Extreme)(1).webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Super Simple Soft Play',
                'image_path': 'Images/Packages/GMR (Super Simple Soft Play)(1).webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Extreme Party Bundle',
                'image_path': 'Images/Packages/ExtremePartyBundle.webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Extreme Party Bundle (Game Package)',
                'image_path': 'Images/Packages/ExtremePartyBundle(Game Package).webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Extreme Party Bundle (Waterslide)',
                'image_path': 'Images/Packages/ExtremePartyBundle(Waterslide).webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Game Room Extreme',
                'image_path': 'Images/Packages/GMR (Game Room Extreme)(1).webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Game Package',
                'image_path': 'Images/Packages/GMR (Game Package)(1).webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Spooky Walkway',
                'image_path': 'Images/Packages/GMR (Spooky Walkway)(1).webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Winter Wonderland',
                'image_path': 'Images/Packages/GMR (Winter Wonderland)(1).webp',
                'price': 'Contact For Details'
            },
            {
                'name': 'Mobile Bar Experience',
                'image_path': 'Images/Packages/GMR (Mobile Bar Experience)(1).webp',
                'price': 'Contact For Details'
            }
        ]
        
        for i, package in enumerate(default_packages):
            package['display_order'] = i
            self.add_package_item(**package)
        
        # Insert default team members
        default_team = [
            {
                'name': 'Ravin Herring',
                'role': 'Founder & Creative Director',
                'image_path': 'Images/Team/RavinGMR.webp',
                'mobile_image_path': 'Images/Team/RavinGMR-mobile.webp',
                'display_order': 0
            },
            {
                'name': 'Deshawn Proby',
                'role': 'Co-Founder & Photographer',
                'image_path': 'Images/Team/DeshawnGMR.webp',
                'mobile_image_path': 'Images/Team/DeshawnGMR-mobile.webp',
                'display_order': 1
            },
            {
                'name': 'Marvin Herring',
                'role': 'Co-Founder & Business Development',
                'image_path': 'Images/Team/MarvinGMR.webp',
                'mobile_image_path': 'Images/Team/MarvinGMR-mobile.webp',
                'display_order': 2
            }
        ]
        
        for member in default_team:
            self.add_team_member(**member)
        
        # Insert default site settings
        default_settings = [
            ('business_name', 'GlitzME Rentals', 'text', 'Business name'),
            ('business_description', 'Local Family Owned party rental business serving the Las Vegas Valley. Creating memorable experiences with exceptional customer service - there\'s no other way but the GlitzME WAY!', 'textarea', 'Main business description'),
            ('phone_primary', '(702) 344-4717', 'text', 'Primary phone number'),
            ('phone_secondary', '(702) 622-0425', 'text', 'Secondary phone number'),
            ('email', 'Glitzme.rentals21@gmail.com', 'email', 'Business email'),
            ('address', 'Las Vegas, NV', 'text', 'Business address'),
            ('tagline', 'Family Owned & Operated', 'text', 'Business tagline'),
            ('instagram_url', 'https://www.instagram.com/glitzme_rentals/', 'url', 'Instagram URL'),
            ('meta_description', 'Las Vegas premier party rental company. Family-owned business offering bounce houses, waterslides, tables, chairs, arcade games & complete party packages. Professional service, competitive prices.', 'textarea', 'Site meta description'),
            ('meta_keywords', 'Las Vegas party rentals, bounce house rental, waterslide rental, table chair rental, party equipment, arcade games, Las Vegas events, family business', 'textarea', 'Site meta keywords'),
            ('team_section_quote', '"None of us is as smart as all of us." - Ken Blanchard', 'text', 'Team section quote'),
        ]
        
        for key, value, setting_type, description in default_settings:
            self.set_site_setting(key, value, setting_type, description)
        
        # Insert default carousel items
        default_carousel = [
            {
                'title': 'GlitzME Rentals Main Logo',
                'image_path': 'Images/Logos/glitzme-hero-main.webp',
                'mobile_image_path': 'Images/Logos/glitzme-hero-mobile.webp',
                'alt_text': 'GlitzME Rentals - Offering Tables, Chairs, and more fun items for your events!',
                'display_order': 0
            },
            {
                'title': 'Summer Sale',
                'image_path': 'Images/HomePageAdverts/SumemrSaleGM.webp',
                'mobile_image_path': 'Images/HomePageAdverts/SumemrSaleGM.webp',
                'alt_text': 'Summer Sale at GlitzME Rentals',
                'link_url': '/contact',
                'link_text': 'View Summer Sale - Contact us for details',
                'display_order': 1
            }
        ]
        
        for item in default_carousel:
            self.add_carousel_item(**item)
    
    # RENTAL ITEMS METHODS
    def get_rental_items(self, active_only: bool = True, category: str = None) -> List[Dict]:
        """Get all rental items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM rental_items"
        params = []
        conditions = []
        
        if active_only:
            conditions.append("is_active = 1")
        if category:
            conditions.append("category = ?")
            params.append(category)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY display_order, name"
        
        cursor.execute(query, params)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items
    
    def get_rental_item(self, item_id: int) -> Optional[Dict]:
        """Get single rental item by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rental_items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def add_rental_item(self, name: str, image_path: str, price: str, deposit: str = None, 
                       price_text: str = 'Price', deposit_text: str = 'Required Deposit (Refundable)',
                       category: str = 'general', description: str = None, display_order: int = 0) -> int:
        """Add new rental item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO rental_items 
            (name, image_path, price, deposit, price_text, deposit_text, category, description, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, image_path, price, deposit, price_text, deposit_text, category, description, display_order))
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id
    
    def update_rental_item(self, item_id: int, **kwargs) -> bool:
        """Update rental item"""
        if not kwargs:
            return False
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic update query
        set_clauses = []
        values = []
        for key, value in kwargs.items():
            if key in ['name', 'image_path', 'price', 'deposit', 'price_text', 'deposit_text', 
                      'category', 'description', 'is_active', 'display_order']:
                set_clauses.append(f"{key} = ?")
                values.append(value)
        
        if not set_clauses:
            conn.close()
            return False
        
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        values.append(item_id)
        
        query = f"UPDATE rental_items SET {', '.join(set_clauses)} WHERE id = ?"
        cursor.execute(query, values)
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def delete_rental_item(self, item_id: int) -> bool:
        """Delete rental item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rental_items WHERE id = ?", (item_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # PACKAGE ITEMS METHODS
    def get_package_items(self, active_only: bool = True) -> List[Dict]:
        """Get all package items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM package_items"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY display_order, name"
        
        cursor.execute(query)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items
    
    def get_package_item(self, item_id: int) -> Optional[Dict]:
        """Get single package item by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM package_items WHERE id = ?", (item_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def add_package_item(self, name: str, image_path: str, price: str, 
                        price_text: str = 'Contact For Details', description: str = None, 
                        display_order: int = 0) -> int:
        """Add new package item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO package_items (name, image_path, price, price_text, description, display_order)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, image_path, price, price_text, description, display_order))
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id
    
    def update_package_item(self, item_id: int, **kwargs) -> bool:
        """Update package item"""
        if not kwargs:
            return False
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        set_clauses = []
        values = []
        for key, value in kwargs.items():
            if key in ['name', 'image_path', 'price', 'price_text', 'description', 'is_active', 'display_order']:
                set_clauses.append(f"{key} = ?")
                values.append(value)
        
        if not set_clauses:
            conn.close()
            return False
        
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        values.append(item_id)
        
        query = f"UPDATE package_items SET {', '.join(set_clauses)} WHERE id = ?"
        cursor.execute(query, values)
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def delete_package_item(self, item_id: int) -> bool:
        """Delete package item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM package_items WHERE id = ?", (item_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # TEAM MEMBERS METHODS
    def get_team_members(self, active_only: bool = True) -> List[Dict]:
        """Get all team members"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM team_members"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY display_order, name"
        
        cursor.execute(query)
        members = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return members
    
    def get_team_member(self, member_id: int) -> Optional[Dict]:
        """Get single team member by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM team_members WHERE id = ?", (member_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def add_team_member(self, name: str, role: str, image_path: str, 
                       mobile_image_path: str = None,
                       display_order: int = 0) -> int:
        """Add new team member"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO team_members (name, role, image_path, mobile_image_path, display_order)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, role, image_path, mobile_image_path, display_order))
        member_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return member_id
    
    def update_team_member(self, member_id: int, **kwargs) -> bool:
        """Update team member"""
        if not kwargs:
            return False
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        set_clauses = []
        values = []
        for key, value in kwargs.items():
            if key in ['name', 'role', 'image_path', 'mobile_image_path', 'is_active', 'display_order']:
                set_clauses.append(f"{key} = ?")
                values.append(value)
        
        if not set_clauses:
            conn.close()
            return False
        
        set_clauses.append("updated_at = CURRENT_TIMESTAMP")
        values.append(member_id)
        
        query = f"UPDATE team_members SET {', '.join(set_clauses)} WHERE id = ?"
        cursor.execute(query, values)
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    def delete_team_member(self, member_id: int) -> bool:
        """Delete team member"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM team_members WHERE id = ?", (member_id,))
        success = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return success
    
    # SITE SETTINGS METHODS
    def get_site_setting(self, key: str) -> Optional[str]:
        """Get site setting value"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT setting_value FROM site_settings WHERE setting_key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        return row['setting_value'] if row else None
    
    def get_all_site_settings(self) -> Dict[str, str]:
        """Get all site settings as dict"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT setting_key, setting_value FROM site_settings")
        settings = {row['setting_key']: row['setting_value'] for row in cursor.fetchall()}
        conn.close()
        return settings
    
    def set_site_setting(self, key: str, value: str, setting_type: str = 'text', description: str = None) -> bool:
        """Set or update site setting"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO site_settings (setting_key, setting_value, setting_type, description, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (key, value, setting_type, description))
        conn.commit()
        conn.close()
        return True
    
    # CAROUSEL METHODS
    def get_carousel_items(self, active_only: bool = True) -> List[Dict]:
        """Get carousel items"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM carousel_items"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY display_order"
        
        cursor.execute(query)
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return items
    
    def add_carousel_item(self, title: str, image_path: str, alt_text: str, 
                         mobile_image_path: str = None, link_url: str = None, 
                         link_text: str = None, display_order: int = 0) -> int:
        """Add carousel item"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO carousel_items 
            (title, image_path, mobile_image_path, alt_text, link_url, link_text, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, image_path, mobile_image_path, alt_text, link_url, link_text, display_order))
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id


# Singleton instance
db_manager = DatabaseManager()

# Convenience functions for easy imports
def get_rental_items(**kwargs):
    return db_manager.get_rental_items(**kwargs)

def get_package_items(**kwargs):
    return db_manager.get_package_items(**kwargs)

def get_team_members(**kwargs):
    return db_manager.get_team_members(**kwargs)

def get_site_settings():
    return db_manager.get_all_site_settings()

def get_carousel_items(**kwargs):
    return db_manager.get_carousel_items(**kwargs)