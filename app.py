from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'glitzme-rentals-secret-key-2024')

# Configuration
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'

@app.route('/')
def index():
    """Homepage route"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index page: {str(e)}")
        return "Error loading page", 500

@app.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submissions"""
    try:
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
        
        # Log the contact form submission
        logger.info(f"Contact form submission from {name} ({email})")
        logger.info(f"Event Type: {event_type}, Date: {event_date}")
        logger.info(f"Message: {message[:100]}...")
        
        # Here you would typically:
        # 1. Save to database
        # 2. Send email notification
        # 3. Send confirmation email to customer
        
        # For now, we'll just log it and show a success message
        flash('Thank you for your inquiry! We will contact you within 24 hours to discuss your event needs.', 'success')
        
        return redirect(url_for('index') + '#contact')
        
    except Exception as e:
        logger.error(f"Error processing contact form: {str(e)}")
        flash('Sorry, there was an error processing your request. Please try again or call us directly.', 'error')
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
    logger.warning(f"404 error: {request.url}")
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"500 error: {str(error)}")
    return "Internal server error", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting GlitzMe Rentals app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug) 