from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
from datetime import datetime

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

@app.route('/contact', methods=['POST'])
def contact():
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
        return redirect(url_for('index') + '#contact')
    
    # For now, we'll just show a success message
    flash('Thank you for your inquiry! We will contact you within 24 hours to discuss your event needs.', 'success')
    
    return redirect(url_for('index') + '#contact')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'GlitzMe Rentals',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/services')
def services():
    """Services page route (future expansion)"""
    return redirect(url_for('index') + '#services')

@app.route('/gallery')
def gallery():
    """Gallery page route (future expansion)"""
    return redirect(url_for('index') + '#gallery')

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
    app.run(host='0.0.0.0', port=port, debug=False) 