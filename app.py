from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'glitzme-rentals-secret-key-2024')

# Add security headers like Maurion.Online
@app.after_request
def add_security_headers(response):
    # Set comprehensive CSP that allows necessary resources
    csp = (
        "default-src 'self'; "
        "font-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "script-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https:;"
    )
    response.headers['Content-Security-Policy'] = csp
    
    # Set permissions policy
    permissions = (
        "geolocation=(), "
        "microphone=(), "
        "camera=(), "
        "payment=(), "
        "usb=(), "
        "fullscreen=*, "
        "autoplay=*, "
        "picture-in-picture=*, "
        "encrypted-media=*"
    )
    response.headers['Permissions-Policy'] = permissions
    return response

@app.route('/')
def index():
    """Homepage route"""
    return render_template('index.html')

@app.route('/rentals', methods=['GET', 'POST'])
def rentals():
    """Rentals page route with pagination"""
    # List of all rental items
    rental_items = [
        {
            'name': 'Arcade Games',
            'image': 'Images/SingularRentals/GMR (Arcade Games)(1).png',
            'price': 200,
            'deposit': 100,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Canopy Tents',
            'image': 'Images/SingularRentals/GMR (Canopy Tent)(1).png',
            'price': "70 - $130 (Depends on Size)",
            'deposit': 100,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Red Carpet',
            'image': 'Images/SingularRentals/GMR (Red Carpet)(1).png',
            'price': 80,
            'deposit': 50,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Soft Play Jump House',
            'image': 'Images/SingularRentals/GMR (Soft Play Jump House)(1).png',
            'price': 55,
            'deposit': 70,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Black Carpet',
            'image': 'Images/SingularRentals/GMR (Black Carpet)(1).png',
            'price': 80,
            'deposit': 50,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Nacho Machine',
            'image': 'Images/SingularRentals/GMR (Nacho Machine)(1).png',
            'price': 85,
            'deposit': 50,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Work Lights',
            'image': 'Images/SingularRentals/GMR (Work Lights)(1).png',
            'price': "10 E.A",
            'deposit': 25,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Tables & Chairs',
            'image': 'Images/SingularRentals/GMR (Tables & Chairs)(1).png',
            'price': "8 Per Table, $2 Per Chair",
            'deposit': "25 - $150",
            'price_text': 'Prices',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': "Shot O' Clock Chiller",
            'image': "Images/SingularRentals/GMR (Shot O' Clock Chiller)(1).png",
            'price': 80,
            'deposit': 50,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Mobile Bars',
            'image': 'Images/SingularRentals/GMR (Mobile Bars)(1).png',
            'price': "30 - $60 (Depends on Quantity)",
            'deposit': 100,
            'price_text': 'Prices Vary',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Round Tables',
            'image': 'Images/SingularRentals/GMR (Round Tables)(1).png',
            'price': "10 per table",
            'deposit': "25 - $150",
            'price_text': 'Prices',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Kids Throne Chair',
            'image': 'Images/SingularRentals/GMR (Kids Throne Chair)(1).png',
            'price': 44,
            'deposit': 50,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Snow Machine',
            'image': 'Images/SingularRentals/GMR (Snow Machine)(1).png',
            'price': 45,
            'deposit': 25,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Refundable)'
        }
    ]

    # Pagination
    items_per_page = 4
    total_items = len(rental_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page  # Ceiling division

    # Get current page from request
    current_page = request.args.get('page', 1, type=int)
    if current_page < 1:
        current_page = 1
    elif current_page > total_pages:
        current_page = total_pages

    # Calculate start and end indices for the current page
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)

    # Get items for the current page
    current_items = rental_items[start_idx:end_idx]

    return render_template('rentals.html', 
                         rentals=current_items,
                         current_page=current_page,
                         total_pages=total_pages)

@app.route('/packages')
def packages():
    """Packages page route with pagination"""
    # List of all package items
    package_items = [
        {
            'name': 'Boy Soft Play Extreme',
            'image': 'Images/Packages/GMR (Boy Soft Play Extreme)(1).png',
            'price': 275,
            'deposit': 100,
            'price_text': 'Price Per Event',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Girl Soft Play Extreme',
            'image': 'Images/Packages/GMR (Girl Soft Play Extreme)(1).png',
            'price': 275,
            'deposit': 100,
            'price_text': 'Price Per Event',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Super Simple Soft Play',
            'image': 'Images/Packages/GMR (Super Simple Soft Play)(1).png',
            'price': 150,
            'deposit': 100,
            'price_text': 'Price Per Event',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Game Room Extreme',
            'image': 'Images/Packages/GMR (Game Room Extreme)(1).png',
            'price': 450,
            'deposit': 200,
            'price_text': 'Package Price',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Game Package',
            'image': 'Images/Packages/GMR (Game Package)(1).png',
            'price': 260,
            'deposit': 100,
            'price_text': 'Price Per Day',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Spooky Walkway',
            'image': 'Images/Packages/GMR (Spooky Walkway)(1).png',
            'price': 350,
            'deposit': 100,
            'price_text': 'Experience Price',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Winter Wonderland',
            'image': 'Images/Packages/GMR (Winter Wonderland)(1).png',
            'price': 350,
            'deposit': 100,
            'price_text': 'Experience Price',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Day Party Package (Jump House)',
            'image': 'Images/Packages/GMR (Day Party Packages, Jump House)(1).png',
            'price': 152,
            'deposit': 100,
            'price_text': 'Package Price',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Day Party Package (Waterslide)',
            'image': 'Images/Packages/GMR (Day Party Package, Waterslide)(1).png',
            'price': 250,
            'deposit': 100,
            'price_text': 'Package Price',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
        {
            'name': 'Mobile Bar Experience',
            'image': 'Images/Packages/GMR (Mobile Bar Experience)(1).png',
            'price': 200,
            'deposit': 100,
            'price_text': 'Experience Price',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Hot Cocoa Stand',
            'image': 'Images/Packages/GMR (Hot Cocoa Stand)(1).png',
            'price': 250,
            'deposit': 100,
            'price_text': 'Price Per Event',
            'deposit_text': 'Required Deposit (Non-Refundable)'
        },
    ]

    # Pagination
    items_per_page = 4
    total_items = len(package_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page  # Ceiling division

    # Get current page from request
    current_page = request.args.get('page', 1, type=int)
    if current_page < 1:
        current_page = 1
    elif current_page > total_pages:
        current_page = total_pages

    # Calculate start and end indices for the current page
    start_idx = (current_page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_items)

    # Get items for the current page
    current_items = package_items[start_idx:end_idx]

    return render_template('packages.html', 
                         packages=current_items,
                         current_page=current_page,
                         total_pages=total_pages)

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    """Gallery page route"""
    # Get list of all event photos
    event_photos_dir = os.path.join(app.static_folder, 'Images/EventPhotos')
    event_photos = [f for f in os.listdir(event_photos_dir) if f.endswith('.jpg')]
    
    # Randomly select 16 photos
    selected_photos = random.sample(event_photos, min(16, len(event_photos)))
    
    return render_template('gallery.html', photos=selected_photos)

@app.route('/contact')
def contact_page():
    """Contact page route"""
    return render_template('contact.html')

@app.route('/contact/submit', methods=['POST'])
def contact_submit():
    """Handle contact form submissions"""
    # Get form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()
    event_date = request.form.get('event_date', '').strip()
    event_type = request.form.get('event_type', '').strip()
    message = request.form.get('message', '').strip()
    
    # Basic validation
    if not name or not email or not message:
        flash('Please fill in all required fields (Name, Email, and Message).', 'error')
        return redirect(url_for('contact_page'))
    
    # For now, we'll just show a success message
    flash('Thank you for your inquiry! We will contact you within 24 hours to discuss your event needs.', 'success')
    
    return redirect(url_for('contact_page'))

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'GlitzME Rentals',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return "Internal server error", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6001))
    app.run(host='0.0.0.0', port=port, debug=True) 