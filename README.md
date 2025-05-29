# GlitzME Party Rentals

A luxury event rental website built with Flask, featuring a modern and elegant design for premium event services.

## Features

- **Modern Design**: Beautiful, responsive website with luxury aesthetics
- **Service Showcase**: Display of premium rental services including furniture, tableware, lighting, and decor
- **Contact Form**: Integrated contact form for customer inquiries
- **Mobile Responsive**: Optimized for all device sizes
- **SEO Optimized**: Proper meta tags and semantic HTML structure

## Services Offered

- **Luxury Furniture**: Premium sofas, chairs, tables, and lounge furniture
- **Elegant Tableware**: Fine china, crystal glassware, and premium cutlery
- **Ambient Lighting**: Professional lighting solutions for perfect atmosphere
- **Decor & Styling**: Exquisite decorative pieces and styling services
- **Audio Visual**: High-quality sound systems and visual equipment
- **Full Service**: Complete event planning and setup services

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern gradients and animations
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Playfair Display, Inter)
- **Deployment**: Docker with Gunicorn

## Local Development

### Prerequisites

- Python 3.10+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd GlitzME-Rentals
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Docker Deployment

### Build and Run

```bash
# Build the Docker image
docker build -t glitzme-rentals .

# Run the container
docker run -p 6000:6000 glitzme-rentals
```

### Docker Compose

The application is configured to run as part of a multi-service Docker Compose setup:

```bash
docker-compose up -d
```

## Production Deployment

The application is configured to run with:
- **Port**: 6000
- **Domain**: glitzmerentals.com
- **Reverse Proxy**: Caddy
- **Process Manager**: Gunicorn with 4 workers
- **Health Checks**: Built-in health monitoring

## Environment Variables

- `FLASK_APP`: app.py
- `FLASK_ENV`: production/development
- `SECRET_KEY`: Application secret key
- `PORT`: Application port (default: 6000)

## API Endpoints

- `GET /`: Homepage
- `POST /contact`: Contact form submission
- `GET /health`: Health check endpoint
- `GET /services`: Redirects to services section
- `GET /gallery`: Redirects to gallery section

## Contact Information

- **Phone**: +1 (555) 123-4567
- **Email**: hello@glitzmerentals.com
- **Address**: 123 Luxury Lane, Event City, EC 12345

## License

© 2024 GlitzME Rentals. All rights reserved. 