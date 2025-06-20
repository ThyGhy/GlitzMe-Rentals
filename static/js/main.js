// GlitzME Rentals - Main JavaScript Functionality
// Optimized for performance and accessibility

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

    // Transcript data from SRT files
    const transcripts = {
        'Testimonial1.mp4': `Okay, listen, let me tell y'all something.
It is a little after 11 o'clock.
My event, 11 p.m.
My event is tomorrow at 7:30.
Raven came through, like, listen.
I'm gonna get these to you tonight
so you can be set up on time in the morning
because if you know me, I do not like giving up
at me in no time, but Raven came through
with the chairs and tables.
We are hosting my first ECW class tomorrow.
So if you're interested, let us know.
But if you also look at the tables and chairs
and all things, Raven got you
and we'll get you all the way together, okay?`,

        'Testimonial2.mp4': `What's up guys, had the opportunity to team up with GlitzME Rentals, great place, great
people, had the opportunity to, for them to drop off the item, use it in my party, people
loved it.
So check them out, they're a great, great team and they have great prices.
So by all means, guys, look up on IG and any other platform, GlitzME Rentals, thanks
guys, See Yall Later!`,

        'Testimonial3.mp4': `It's my 21st and we rented from GlitzME Rentals, thank y'all so much for coming out.
They came out and delivered to chairs and tables, I'm very grateful.
Appreciate y'all.`,

        'Testimonial4.mp4': `Hey y'all, we just wanted to say hey,
to GlitzME Rentals, big shoutout to them,
renting some tables and chairs for my son's 21st birthday party,
she told me to be camera ready and I'm like,
I woke up like this,
it's what you get, girl, I love you.`,

        'Testimonial5.mp4': `What's going on all y'all? My name is Brandon Marshall. I rented from GlitzME Rentals for
my daughter's birthday party. It was amazing. She had a blast. I got the tables, the chairs,
and the bounce house. All the kids had a good time and so you know I would 100% recommend
you rent from GlitzME. I would do it again. I've done it multiple times. Actually this
is the first time that I'm actually doing a review for her. But I've done it multiple times.
The services are immaculate. It's great. So y'all rent from GlitzME Rentals.`,

        'Testimonial6.mp4': `Hi, my name is Ernest Mitchell, this is Nicole Mitchell, We rented from GltizME Rentals
and the spirits fabulous. The Kids Enjoy themselves
their bouncing up the yin-yang, we have a fabulous time
please, if you feel free, rent from them and you'll be satisfied!`
    };

    // Transcript Modal Functions
    function openTranscript(videoFile) {
        const modal = document.getElementById('transcriptModal');
        const transcriptText = document.getElementById('transcript-text');
        
        if (modal && transcriptText) {
            transcriptText.textContent = transcripts[videoFile];
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';

            // Focus the close button
            const closeButton = modal.querySelector('.modal-close');
            if (closeButton) {
                closeButton.focus();
            }
        }
    }

    function closeTranscript() {
        const modal = document.getElementById('transcriptModal');
        if (modal) {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }
    }

    // Make transcript functions globally available
    window.openTranscript = openTranscript;
    window.closeTranscript = closeTranscript;

    // Close modal when clicking overlay
    const modalOverlay = document.querySelector('.modal-overlay');
    if (modalOverlay) {
        modalOverlay.addEventListener('click', closeTranscript);
    }

    // Close modal on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            closeTranscript();
        }
    });

    // Ensure modal is hidden by default
    const modal = document.getElementById('transcriptModal');
    if (modal) {
        modal.style.display = 'none';
    }

    // Testimonial Carousel Functionality
    const carousel = document.querySelector('.testimonial-carousel');
    if (carousel) {
        const slides = carousel.querySelectorAll('.carousel-slide');
        const prevButton = carousel.querySelector('.prev');
        const nextButton = carousel.querySelector('.next');
        const dots = document.querySelectorAll('.carousel-dot');
        let currentIndex = 0;
        let autoplayInterval;
        const autoplayDelay = 30000; // 30 seconds

        function showSlide(index) {
            slides.forEach(slide => {
                slide.classList.remove('active');
                slide.setAttribute('aria-hidden', 'true');
            });
            dots.forEach(dot => {
                dot.classList.remove('active');
                dot.setAttribute('aria-selected', 'false');
            });

            slides[index].classList.add('active');
            slides[index].removeAttribute('aria-hidden');
            dots[index].classList.add('active');
            dots[index].setAttribute('aria-selected', 'true');

            slides.forEach(slide => {
                const video = slide.querySelector('video');
                if (video) video.pause();
            });

            currentIndex = index;
        }

        function nextSlide() {
            showSlide((currentIndex + 1) % slides.length);
        }

        function prevSlide() {
            showSlide((currentIndex - 1 + slides.length) % slides.length);
        }

        function startAutoplay() {
            stopAutoplay();
            autoplayInterval = setInterval(nextSlide, autoplayDelay);
        }

        function stopAutoplay() {
            if (autoplayInterval) {
                clearInterval(autoplayInterval);
            }
        }

        prevButton.addEventListener('click', () => {
            prevSlide();
            startAutoplay();
        });

        nextButton.addEventListener('click', () => {
            nextSlide();
            startAutoplay();
        });

        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                showSlide(index);
                startAutoplay();
            });
        });

        slides.forEach(slide => {
            const video = slide.querySelector('video');
            if (video) {
                video.addEventListener('play', stopAutoplay);
                video.addEventListener('pause', startAutoplay);
            }
        });

        showSlide(0);
        startAutoplay();
    }

    // Add audio description track if available
    document.querySelectorAll('video').forEach(video => {
        const descriptionTrack = document.createElement('track');
        descriptionTrack.kind = 'descriptions';
        descriptionTrack.label = 'Audio Descriptions';
        descriptionTrack.srclang = 'en';
        
        video.addEventListener('play', function() {
            this.setAttribute('aria-label', 'Playing: Customer testimonial video');
        });
        
        video.addEventListener('pause', function() {
            this.setAttribute('aria-label', 'Paused: Customer testimonial video');
        });
        
        // Ensure captions are enabled by default
        if (video.textTracks[0]) {
            video.textTracks[0].mode = 'showing';
        }
    });

    // Initialize all functionality
    function init() {
        initMobileMenu();
        initSmoothScrolling();
        initNavbarScrollEffect();
        initServicesSection();
        initCarousels();
    }
    
    // Carousel initialization function
    function initCarousels() {
        // Initialize all carousels on the page
        const carousels = document.querySelectorAll('.testimonial-carousel');
        
        carousels.forEach((carousel, carouselIndex) => {
            const track = carousel.querySelector('.carousel-track');
            const slides = carousel.querySelectorAll('.carousel-slide');
            
            // Get all navigation buttons (desktop and mobile)
            const prevButtons = carousel.parentElement.querySelectorAll('.prev');
            const nextButtons = carousel.parentElement.querySelectorAll('.next');
            const dotContainers = carousel.closest('.video-gallery').querySelectorAll('.carousel-dots');
            
            let currentIndex = 0;
            let autoplayInterval;
            const autoplayDelay = 30000; // 30 seconds

            function showSlide(index) {
                slides.forEach((slide, i) => {
                    slide.classList.toggle('active', i === index);
                    slide.setAttribute('aria-hidden', i !== index);
                });
                
                // Update all dot containers (desktop and mobile)
                dotContainers.forEach(dotsContainer => {
                    const dots = dotsContainer.querySelectorAll('.carousel-dot');
                    dots.forEach((dot, i) => {
                        dot.classList.toggle('active', i === index);
                        dot.setAttribute('aria-selected', i === index);
                    });
                });

                // Pause all videos in this carousel
                slides.forEach(slide => {
                    const video = slide.querySelector('video');
                    if (video) video.pause();
                });

                currentIndex = index;
            }

            function nextSlide() {
                showSlide((currentIndex + 1) % slides.length);
            }

            function prevSlide() {
                showSlide((currentIndex - 1 + slides.length) % slides.length);
            }

            function startAutoplay() {
                stopAutoplay();
                autoplayInterval = setInterval(nextSlide, autoplayDelay);
            }

            function stopAutoplay() {
                if (autoplayInterval) {
                    clearInterval(autoplayInterval);
                }
            }

            // Event listeners for all navigation buttons
            prevButtons.forEach(button => {
                button.addEventListener('click', () => {
                    prevSlide();
                    startAutoplay();
                });
            });

            nextButtons.forEach(button => {
                button.addEventListener('click', () => {
                    nextSlide();
                    startAutoplay();
                });
            });

            // Event listeners for all dot containers
            dotContainers.forEach(dotsContainer => {
                const dots = dotsContainer.querySelectorAll('.carousel-dot');
                dots.forEach((dot, index) => {
                    dot.addEventListener('click', () => {
                        showSlide(index);
                        startAutoplay();
                    });
                });
            });

            // Pause autoplay when video is playing
            slides.forEach(slide => {
                const video = slide.querySelector('video');
                if (video) {
                    video.addEventListener('play', stopAutoplay);
                    video.addEventListener('pause', startAutoplay);
                }
            });

            // Initialize first slide and start autoplay
            if (slides.length > 0) {
                showSlide(0);
                startAutoplay();
            }
        });
    }

    // Call init to start all functionality
    init();
});

// Additional utility functions
const GlitzMEUtils = {
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
    module.exports = { GlitzMEUtils };
}

// Video Carousel Functionality has been moved to the main init() function above 