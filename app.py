from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, send_from_directory, session
from flask_compress import Compress
import os
from datetime import datetime, timedelta
import random
import secrets
import hashlib
from database import (get_rental_items, get_package_items, get_team_members, get_site_settings, get_carousel_items,
                     db_manager)

try:
    from dotenv import load_dotenv, find_dotenv  # type: ignore
    # Load .env explicitly from the project root (same dir as this file)
    dotenv_path = find_dotenv(filename='.env', usecwd=True) or os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path, override=False)
except Exception:
    # If python-dotenv isn't installed or fails, rely on OS env vars
    pass

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'glitzme-rentals-secret-key-2024')

# Admin configuration
# Read secrets from environment (use .env in development). No hardcoded defaults.
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
if not ADMIN_PASSWORD:
    raise RuntimeError(
        "ADMIN_PASSWORD is not set. Create a .env file in the project root and define ADMIN_PASSWORD, or set it as an environment variable."
    )
ADMIN_TOKEN_EXPIRY = 3600  # 1 hour in seconds

# Template and loader behavior
# Enable template auto-reload in development so edited templates reflect without full restarts
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = False

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

# Performance optimizations
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 604800  # 7 days cache for static files

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
    # Get dynamic content from database
    team_members = get_team_members()
    site_settings = get_site_settings()
    carousel_items = get_carousel_items()
    
    return render_template('index.html', 
                         team_members=team_members,
                         site_settings=site_settings,
                         carousel_items=carousel_items)

@app.route('/rentals', methods=['GET', 'POST'])
def rentals():
    """Rentals page route with pagination"""
    # Get rental items from database
    rental_items = get_rental_items()
    
    # Convert database format to template format (add 'image' key for compatibility)
    for item in rental_items:
        item['image'] = item['image_path']

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
    # Get package items from database
    package_items = get_package_items()
    
    # Convert database format to template format (add 'image' key for compatibility)
    for item in package_items:
        item['image'] = item['image_path']

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

@app.route('/sitemap.xml')
def sitemap():
    """Generate sitemap for SEO"""
    from flask import Response
    
    sitemap_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://glitzmerentals.com/</loc>
        <lastmod>{}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://glitzmerentals.com/rentals</loc>
        <lastmod>{}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://glitzmerentals.com/packages</loc>
        <lastmod>{}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
    <url>
        <loc>https://glitzmerentals.com/about</loc>
        <lastmod>{}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.6</priority>
    </url>
    <url>
        <loc>https://glitzmerentals.com/gallery</loc>
        <lastmod>{}</lastmod>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>
    <url>
        <loc>https://glitzmerentals.com/contact</loc>
        <lastmod>{}</lastmod>
        <changefreq>monthly</changefreq>
        <priority>0.5</priority>
    </url>
</urlset>'''.format(*([datetime.now().strftime('%Y-%m-%d')] * 6))
    
    return Response(sitemap_xml, mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    """Serve robots.txt for SEO"""
    return send_from_directory(app.root_path, 'robots.txt')

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

# AUTHENTICATION HELPERS
def generate_admin_token():
    """Generate a secure token for admin access"""
    return secrets.token_urlsafe(32)

def is_admin_authenticated():
    """Check if current session is authenticated as admin"""
    return session.get('admin_authenticated') == True and \
           session.get('admin_token') and \
           session.get('admin_expires', 0) > datetime.now().timestamp()

def require_admin_auth(f):
    """Decorator to require admin authentication"""
    def decorated_function(*args, **kwargs):
        if not is_admin_authenticated():
            flash('Please log in to access the admin area.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# ADMIN AUTHENTICATION ROUTES
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        
        if password == ADMIN_PASSWORD:
            # Set session data
            session['admin_authenticated'] = True
            session['admin_token'] = generate_admin_token()
            session['admin_expires'] = datetime.now().timestamp() + ADMIN_TOKEN_EXPIRY
            session.permanent = True
            
            flash('Successfully logged in to admin area!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid password. Please try again.', 'error')
    
    # Get site settings for the login page
    site_settings = get_site_settings()
    return render_template('admin_login.html', site_settings=site_settings)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_authenticated', None)
    session.pop('admin_token', None)
    session.pop('admin_expires', None)
    flash('Successfully logged out of admin area.', 'success')
    return redirect(url_for('index'))

# ADMIN ROUTES
@app.route('/admin')
@require_admin_auth
def admin_dashboard():
    """Admin dashboard homepage"""
    # Get counts for dashboard overview
    rental_count = len(get_rental_items(active_only=False))
    package_count = len(get_package_items(active_only=False))
    team_count = len(get_team_members(active_only=False))
    
    return render_template('admin/dashboard.html',
                         rental_count=rental_count,
                         package_count=package_count,
                         team_count=team_count)

# Friendly aliases to prevent accidental 404s (e.g., trailing slash or pluralization)
@app.route('/admin/')
def admin_dashboard_trailing_slash():
    """Allow /admin/ to resolve correctly by redirecting to /admin"""
    if not is_admin_authenticated():
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/rentals')
@require_admin_auth
def admin_rentals():
    """Admin page for managing rental items"""
    rentals = get_rental_items(active_only=False)
    return render_template('admin/rentals.html', rentals=rentals)

@app.route('/admin/rentals/add', methods=['GET', 'POST'])
@require_admin_auth
def admin_rentals_add():
    """Add new rental item"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        image_path = request.form.get('image_path', '').strip()
        price = request.form.get('price', '').strip()
        deposit = request.form.get('deposit', '').strip()
        price_text = request.form.get('price_text', 'Price').strip()
        deposit_text = request.form.get('deposit_text', 'Required Deposit (Refundable)').strip()
        category = request.form.get('category', 'general').strip()
        description = request.form.get('description', '').strip()
        
        if name and image_path and price:
            db_manager.add_rental_item(
                name=name, image_path=image_path, price=price, deposit=deposit,
                price_text=price_text, deposit_text=deposit_text,
                category=category, description=description or None
            )
            flash('Rental item added successfully!', 'success')
            return redirect(url_for('admin_rentals'))
        else:
            flash('Please fill in all required fields (Name, Image Path, Price).', 'error')
    
    return render_template('admin/rental_form.html', rental=None, action='Add')

@app.route('/admin/rentals/<int:rental_id>/edit', methods=['GET', 'POST'])
@require_admin_auth
def admin_rentals_edit(rental_id):
    """Edit rental item"""
    rental = db_manager.get_rental_item(rental_id)
    if not rental:
        flash('Rental item not found.', 'error')
        return redirect(url_for('admin_rentals'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        image_path = request.form.get('image_path', '').strip()
        price = request.form.get('price', '').strip()
        deposit = request.form.get('deposit', '').strip()
        price_text = request.form.get('price_text', 'Price').strip()
        deposit_text = request.form.get('deposit_text', 'Required Deposit (Refundable)').strip()
        category = request.form.get('category', 'general').strip()
        description = request.form.get('description', '').strip()
        is_active = bool(request.form.get('is_active'))
        
        if name and image_path and price:
            db_manager.update_rental_item(
                rental_id,
                name=name, image_path=image_path, price=price, deposit=deposit,
                price_text=price_text, deposit_text=deposit_text,
                category=category, description=description or None,
                is_active=is_active
            )
            flash('Rental item updated successfully!', 'success')
            return redirect(url_for('admin_rentals'))
        else:
            flash('Please fill in all required fields (Name, Image Path, Price).', 'error')
    
    return render_template('admin/rental_form.html', rental=rental, action='Edit')

@app.route('/admin/rentals/<int:rental_id>/delete', methods=['POST'])
@require_admin_auth
def admin_rentals_delete(rental_id):
    """Delete rental item"""
    if db_manager.delete_rental_item(rental_id):
        flash('Rental item deleted successfully!', 'success')
    else:
        flash('Error deleting rental item.', 'error')
    return redirect(url_for('admin_rentals'))

@app.route('/admin/packages')
@require_admin_auth
def admin_packages():
    """Admin page for managing package items"""
    packages = get_package_items(active_only=False)
    return render_template('admin/packages.html', packages=packages)

@app.route('/admin/package')
@require_admin_auth
def admin_packages_alias():
    """Alias singular /admin/package to plural route"""
    return redirect(url_for('admin_packages'))

@app.route('/admin/packages/add', methods=['GET', 'POST'])
@require_admin_auth
def admin_packages_add():
    """Add new package item"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        image_path = request.form.get('image_path', '').strip()
        price = request.form.get('price', '').strip()
        price_text = request.form.get('price_text', 'Contact For Details').strip()
        description = request.form.get('description', '').strip()
        
        if name and image_path and price:
            db_manager.add_package_item(
                name=name, image_path=image_path, price=price,
                price_text=price_text, description=description or None
            )
            flash('Package item added successfully!', 'success')
            return redirect(url_for('admin_packages'))
        else:
            flash('Please fill in all required fields (Name, Image Path, Price).', 'error')
    
    return render_template('admin/package_form.html', package=None, action='Add')

@app.route('/admin/packages/<int:package_id>/edit', methods=['GET', 'POST'])
@require_admin_auth
def admin_packages_edit(package_id):
    """Edit package item"""
    package = db_manager.get_package_item(package_id)
    if not package:
        flash('Package item not found.', 'error')
        return redirect(url_for('admin_packages'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        image_path = request.form.get('image_path', '').strip()
        price = request.form.get('price', '').strip()
        price_text = request.form.get('price_text', 'Contact For Details').strip()
        description = request.form.get('description', '').strip()
        is_active = bool(request.form.get('is_active'))
        
        if name and image_path and price:
            db_manager.update_package_item(
                package_id,
                name=name, image_path=image_path, price=price,
                price_text=price_text, description=description or None,
                is_active=is_active
            )
            flash('Package item updated successfully!', 'success')
            return redirect(url_for('admin_packages'))
        else:
            flash('Please fill in all required fields (Name, Image Path, Price).', 'error')
    
    return render_template('admin/package_form.html', package=package, action='Edit')

@app.route('/admin/packages/<int:package_id>/delete', methods=['POST'])
@require_admin_auth
def admin_packages_delete(package_id):
    """Delete package item"""
    if db_manager.delete_package_item(package_id):
        flash('Package item deleted successfully!', 'success')
    else:
        flash('Error deleting package item.', 'error')
    return redirect(url_for('admin_packages'))

@app.route('/admin/team')
@require_admin_auth
def admin_team():
    """Admin page for managing team members"""
    team = get_team_members(active_only=False)
    return render_template('admin/team.html', team=team)

@app.route('/admin/teams')
@require_admin_auth
def admin_team_alias():
    """Alias /admin/teams to the canonical /admin/team route"""
    return redirect(url_for('admin_team'))

@app.route('/admin/team/add', methods=['GET', 'POST'])
@require_admin_auth
def admin_team_add():
    """Add new team member"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '').strip()
        image_path = request.form.get('image_path', '').strip()
        mobile_image_path = request.form.get('mobile_image_path', '').strip()
        
        if name and role and image_path:
            db_manager.add_team_member(
                name=name, role=role, image_path=image_path,
                mobile_image_path=mobile_image_path or None
            )
            flash('Team member added successfully!', 'success')
            return redirect(url_for('admin_team'))
        else:
            flash('Please fill in all required fields (Name, Role, Image Path).', 'error')
    
    return render_template('admin/team_form.html', member=None, action='Add')

@app.route('/admin/team/<int:member_id>/edit', methods=['GET', 'POST'])
@require_admin_auth
def admin_team_edit(member_id):
    """Edit team member"""
    member = db_manager.get_team_member(member_id)
    if not member:
        flash('Team member not found.', 'error')
        return redirect(url_for('admin_team'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        role = request.form.get('role', '').strip()
        image_path = request.form.get('image_path', '').strip()
        mobile_image_path = request.form.get('mobile_image_path', '').strip()
        is_active = bool(request.form.get('is_active'))
        
        if name and role and image_path:
            db_manager.update_team_member(
                member_id,
                name=name, role=role, image_path=image_path,
                 mobile_image_path=mobile_image_path or None,
                 is_active=is_active
            )
            flash('Team member updated successfully!', 'success')
            return redirect(url_for('admin_team'))
        else:
            flash('Please fill in all required fields (Name, Role, Image Path).', 'error')
    
    return render_template('admin/team_form.html', member=member, action='Edit')

@app.route('/admin/team/<int:member_id>/delete', methods=['POST'])
@require_admin_auth
def admin_team_delete(member_id):
    """Delete team member"""
    if db_manager.delete_team_member(member_id):
        flash('Team member deleted successfully!', 'success')
    else:
        flash('Error deleting team member.', 'error')
    return redirect(url_for('admin_team'))

@app.route('/admin/api/images')
@require_admin_auth
def admin_api_images():
    """API endpoint to get all available images"""
    import glob
    
    image_folders = [
        'static/Images/SingularRentals/*.webp',
        'static/Images/Packages/*.webp',
        'static/Images/Team/*.webp',
        'static/Images/HomePageAdverts/*.webp',
        'static/Images/Logos/*.webp'
    ]
    
    all_images = []
    for folder_pattern in image_folders:
        images = glob.glob(folder_pattern)
        for img_path in images:
            # Convert to relative path from static folder
            relative_path = img_path.replace('static/', '')
            all_images.append(relative_path)
    
    return jsonify(sorted(all_images))

@app.route('/admin/settings', methods=['GET', 'POST'])
@require_admin_auth
def admin_settings():
    """Admin page for managing site settings"""
    if request.method == 'POST':
        # Get all form data and update settings
        settings_to_update = [
            'business_name', 'business_description', 'phone_primary', 'phone_secondary',
            'email', 'address', 'tagline', 'instagram_url', 'meta_description',
            'meta_keywords', 'team_section_quote'
        ]
        
        for setting_key in settings_to_update:
            value = request.form.get(setting_key, '').strip()
            if value:  # Only update if value is provided
                db_manager.set_site_setting(setting_key, value)
        
        flash('Site settings updated successfully!', 'success')
        return redirect(url_for('admin_settings'))
    
    settings = get_site_settings()
    return render_template('admin/settings.html', settings=settings)

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return "Internal server error", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6001))
    app.run(host='0.0.0.0', port=port, debug=True) 