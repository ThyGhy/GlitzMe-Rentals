from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, send_from_directory
from flask_compress import Compress
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'glitzme-rentals-secret-key-2024')

# Initialize gzip compression
compress = Compress()
compress.init_app(app)

# Configure compression settings
app.config['COMPRESS_MIMETYPES'] = [
    'text/html',
    'text/css',
    'text/xml',
    'text/javascript',
    'application/javascript',
    'application/xml',
    'application/rss+xml',
    'application/atom+xml',
    'image/svg+xml',
    'application/json',
    'text/plain'
]
app.config['COMPRESS_LEVEL'] = 6  # Compression level 1-9 (6 is optimal balance)
app.config['COMPRESS_MIN_SIZE'] = 500  # Only compress files larger than 500 bytes

# Add security and caching headers
@app.after_request
def add_headers(response):
    # Existing security headers
    csp = (
        "default-src 'self'; "
        "font-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; "
        "script-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "connect-src 'self' https:;"
    )
    response.headers['Content-Security-Policy'] = csp
    
    # Existing permissions policy
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

    # Add caching headers for static files
    if request.path.startswith('/static/'):
        # Cache static files for 1 week
        response.cache_control.max_age = 604800  # 7 days in seconds
        response.cache_control.public = True
        response.headers['Vary'] = 'Accept-Encoding'
        
        # Add expires header
        expires_date = datetime.utcnow() + timedelta(days=7)
        response.headers['Expires'] = expires_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
    else:
        # For HTML pages, shorter cache with revalidation
        response.cache_control.max_age = 3600  # 1 hour
        response.cache_control.must_revalidate = True
        response.headers['Vary'] = 'Accept-Encoding'

    # Add compression hints for better performance
    if response.content_type.startswith(('text/', 'application/javascript', 'application/json')):
        response.headers['Vary'] = 'Accept-Encoding'

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
            'name': 'Tables & Chairs',
            'image': 'Images/SingularRentals/GMR (Tables & Chairs)(1).webp',
            'price': 'Tables $5-$14 per (Depends On Table Type), Chairs $1-$6 per (Depends On Chair Type), Ask for Details',
            'deposit': '$25.00 - $150.00 Required Deposit',
            'price_text': 'Prices',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Jump Houses',
            'image': 'Images/SingularRentals/GMR(JumpHouses).webp',
            'price': '$65.00/Day Rental',
            'deposit': '$100.00 Required Refundable Deposit',
            'price_text': 'Price',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Double Water Slide',
            'image': 'Images/SingularRentals/GMR (Double Water Slide)(1).webp',
            'price': '$225.00/Day Rental',
            'deposit': '$100.00 Required Deposit',
            'price_text': 'Price',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Arcade Games',
            'image': 'Images/SingularRentals/GMR (Arcade Games)(1).webp',
            'price': '$200.00/Day Rental',
            'deposit': '$100.00 Required Deposit',
            'price_text': 'Price',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Canopy Tents',
            'image': 'Images/SingularRentals/GMR (Canopy Tent)(1).webp',
            'price': 'Starting at $70',
            'deposit': '$100.00 Required Refundable Deposit',
            'price_text': 'Prices Vary',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Red Carpet',
            'image': 'Images/SingularRentals/GMR (Red Carpet)(1).webp',
            'price': '$80.00/Day Rental',
            'deposit': '$50.00 Required Deposit',
            'price_text': 'Price',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Black Carpet',
            'image': 'Images/SingularRentals/GMR (Black Carpet)(1).webp',
            'price': '$80/Day Rental',
            'deposit': '$50 Required Deposit',
            'price_text': 'Price',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Nacho Machine',
            'image': 'Images/SingularRentals/GMR (Nacho Machine)(1).webp',
            'price': '$60/Day Rental',
            'deposit': '$50 Required Deposit',
            'price_text': 'Price',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Mobile Bars',
            'image': 'Images/SingularRentals/GMR (Mobile Bars)(1).webp',
            'price': 'Starting at $30',
            'deposit': '$100 Required Deposit',
            'price_text': 'Prices Vary',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Queens/Throne Chair',
            'image': 'Images/SingularRentals/GMR (Kids Throne Chair)(1).webp',
            'price': '$44/Day Rental',
            'deposit': '$50 Required Deposit',
            'price_text': 'Price',
            'deposit_text': 'Required Deposit (Refundable)'
        },
        {
            'name': 'Snow Machine',
            'image': 'Images/SingularRentals/GMR (Snow Machine)(1).webp',
            'price': '$45/Day Rental',
            'deposit': '$25 Required Deposit',
            'price_text': 'Price',
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
    # Default price settings for all packages
    DEFAULT_PRICE = 'Contact For Details'
    
    # List of package configurations
    package_items = [
        {
            'name': 'Movie Theater Experience',
            'image': 'Images/Packages/GMR (Movie Theater Experience)(1).webp',
            'price': DEFAULT_PRICE,
            'price_text': DEFAULT_PRICE
        },
        {
            'name': 'Boy Soft Play Extreme',
            'image': 'Images/Packages/GMR (Boy Soft Play Extreme)(1).webp',
            'price': DEFAULT_PRICE,
            'price_text': DEFAULT_PRICE
        },
        {
            'name': 'Girl Soft Play Extreme',
            'image': 'Images/Packages/GMR (Girl Soft Play Extreme)(1).webp',
            'price': DEFAULT_PRICE,
            'price_text': DEFAULT_PRICE
        },
        {
            'name': 'Super Simple Soft Play',
            'image': 'Images/Packages/GMR (Super Simple Soft Play)(1).webp',
            'price': DEFAULT_PRICE,
            'price_text': DEFAULT_PRICE
        },
        {
            'name': 'Game Room Extreme',
            'image': 'Images/Packages/GMR (Game Room Extreme)(1).webp',
            'price': DEFAULT_PRICE,
            'price_text': DEFAULT_PRICE
        },
        {
            'name': 'Game Package',
            'image': 'Images/Packages/GMR (Game Package)(1).webp',
            'price': DEFAULT_PRICE,
            'price_text': DEFAULT_PRICE
        },
        {
            'name': 'Spooky Walkway',
            'image': 'Images/Packages/GMR (Spooky Walkway)(1).webp',
            'price': DEFAULT_PRICE,
            'price_text': DEFAULT_PRICE
        },
        {
            'name': 'Winter Wonderland',
            'image': 'Images/Packages/GMR (Winter Wonderland)(1).webp',
            'price': DEFAULT_PRICE,
            'price_text': DEFAULT_PRICE
        },
        {
            'name': 'Treasure Package',
            'image': 'Images/Packages/coming-soon-placeholder.png',
            'price': DEFAULT_PRICE,
            'price_text': DEFAULT_PRICE,
            'image_placeholder': 'Image Coming Soon'
        },
        {
            'name': 'Mobile Bar Experience',
            'image': 'Images/Packages/GMR (Mobile Bar Experience)(1).webp',
            'price': DEFAULT_PRICE,
            'price_text': DEFAULT_PRICE
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
    # Get list of all event photos (now using .webp files)
    event_photos_dir = os.path.join(app.static_folder, 'Images/EventPhotos')
    event_photos = [f for f in os.listdir(event_photos_dir) if f.endswith('.webp')]
    
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