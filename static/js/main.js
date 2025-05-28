// GlitzMe Rentals - Main JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    
    // Mobile menu toggle functionality
    function initMobileMenu() {
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');

        if (hamburger && navMenu) {
            hamburger.addEventListener('click', () => {
                hamburger.classList.toggle('active');
                navMenu.classList.toggle('active');
            });
        }
    }

    // Smooth scrolling for anchor links
    function initSmoothScrolling() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Navbar scroll effect
    function initNavbarScrollEffect() {
        window.addEventListener('scroll', () => {
            const navbar = document.querySelector('.navbar');
            if (navbar) {
                if (window.scrollY > 100) {
                    navbar.classList.add('scrolled');
                } else {
                    navbar.classList.remove('scrolled');
                }
            }
        });
    }

    // Services Section Interactive Functionality
    function initServicesSection() {
        
        // Check if we're on mobile or desktop
        function isMobile() {
            return window.innerWidth <= 768 || window.innerHeight <= 600;
        }

        // Mobile functionality - Accordion style
        function initMobileServices() {
            const serviceItems = document.querySelectorAll('.service-item');
            
            serviceItems.forEach(item => {
                const card = item.querySelector('.service-selector-card');
                const detail = item.querySelector('.service-detail-mobile');
                
                if (card && detail) {
                    card.addEventListener('click', function() {
                        const isActive = card.classList.contains('active');
                        
                        // Close all other services
                        serviceItems.forEach(otherItem => {
                            const otherCard = otherItem.querySelector('.service-selector-card');
                            const otherDetail = otherItem.querySelector('.service-detail-mobile');
                            if (otherCard && otherDetail) {
                                otherCard.classList.remove('active');
                                otherDetail.classList.remove('active');
                            }
                        });
                        
                        // Toggle current service
                        if (!isActive) {
                            card.classList.add('active');
                            detail.classList.add('active');
                            
                            // Smooth scroll to show the opened content
                            setTimeout(() => {
                                card.scrollIntoView({ 
                                    behavior: 'smooth', 
                                    block: 'start'
                                });
                            }, 100);
                        } else {
                            card.classList.remove('active');
                            detail.classList.remove('active');
                        }
                    });
                }
            });
            
            // Initialize first service as open on mobile
            const firstItem = serviceItems[0];
            if (firstItem) {
                const firstCard = firstItem.querySelector('.service-selector-card');
                const firstDetail = firstItem.querySelector('.service-detail-mobile');
                if (firstCard && firstDetail) {
                    firstCard.classList.add('active');
                    firstDetail.classList.add('active');
                }
            }
        }

        // Desktop functionality - Split view
        function initDesktopServices() {
            const selectorCards = document.querySelectorAll('.services-desktop .service-selector-card');
            const serviceDetails = document.querySelectorAll('.service-detail');

            selectorCards.forEach(card => {
                card.addEventListener('click', () => {
                    const serviceId = card.getAttribute('data-service');
                    
                    // Remove active class from all cards and details
                    selectorCards.forEach(c => c.classList.remove('active'));
                    serviceDetails.forEach(d => d.classList.remove('active'));
                    
                    // Add active class to clicked card and corresponding detail
                    card.classList.add('active');
                    document.getElementById(serviceId).classList.add('active');
                });
            });
        }

        // Mobile Service Accordion
        const mobileSelectorCards = document.querySelectorAll('.services-list .service-selector-card');
        const mobileServiceDetails = document.querySelectorAll('.service-detail-mobile');

        mobileSelectorCards.forEach(card => {
            card.addEventListener('click', () => {
                const serviceId = card.getAttribute('data-service') + '-mobile';
                const detail = document.getElementById(serviceId);
                
                // Toggle active state
                card.classList.toggle('active');
                if (detail.classList.contains('active')) {
                    detail.classList.remove('active');
                } else {
                    mobileServiceDetails.forEach(d => d.classList.remove('active'));
                    detail.classList.add('active');
                }
            });
        });

        // Gallery Thumbnail Switching
        const thumbnails = document.querySelectorAll('.thumbnail');
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', () => {
                const gallery = thumb.closest('.service-gallery');
                const mainImage = gallery.querySelector('.main-image');
                const thumbImage = thumb.querySelector('.image-placeholder').innerHTML;
                
                // Update main image
                mainImage.querySelector('.image-placeholder').innerHTML = thumbImage;
                
                // Update active state of thumbnails
                gallery.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
                thumb.classList.add('active');
            });
        });

        // Initialize based on screen size
        function initServices() {
            const servicesDesktop = document.querySelector('.services-desktop');
            const servicesList = document.querySelector('.services-list');
            
            if (isMobile()) {
                // Hide desktop version, show mobile version
                if (servicesDesktop) servicesDesktop.style.display = 'none';
                if (servicesList) servicesList.style.display = 'block';
                initMobileServices();
            } else {
                // Hide mobile version, show desktop version
                if (servicesList) servicesList.style.display = 'none';
                if (servicesDesktop) servicesDesktop.style.display = 'grid';
                initDesktopServices();
            }
        }

        // Initialize on load
        initServices();

        // Reinitialize on window resize with debouncing
        let resizeTimeout;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(function() {
                initServices();
            }, 250);
        });
    }

    // Initialize all functionality
    function init() {
        initMobileMenu();
        initSmoothScrolling();
        initNavbarScrollEffect();
        initServicesSection();
    }

    // Start the application
    init();
});

// Additional utility functions
const GlitzMeUtils = {
    // Function to add image switching functionality when real images are added
    switchGalleryImage: function(galleryElement, imageIndex, imageSrc) {
        const mainImage = galleryElement.querySelector('.main-image img');
        if (mainImage) {
            mainImage.src = imageSrc;
            mainImage.alt = `Service image ${imageIndex + 1}`;
        }
    },
    
    // Function to check if element is in viewport
    isInViewport: function(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },
    
    // Function to animate elements on scroll (for future use)
    animateOnScroll: function() {
        const elements = document.querySelectorAll('[data-animate]');
        elements.forEach(element => {
            if (this.isInViewport(element)) {
                element.classList.add('animate');
            }
        });
    }
};

// Export for potential future module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GlitzMeUtils };
} 