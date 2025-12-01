// ============================================================================
// SITE RESCUE - ELITE INTERACTIONS v2.0
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize AOS
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: true,
        offset: 100
    });
    
    // ========================================================================
    // NAVIGATION SCROLL EFFECT
    // ========================================================================
    
    const navbar = document.getElementById('navbar');
    const floatingCta = document.getElementById('floatingCta');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
            floatingCta.classList.add('visible');
        } else {
            navbar.classList.remove('scrolled');
            floatingCta.classList.remove('visible');
        }
    });
    
    // ========================================================================
    // MOBILE MENU TOGGLE
    // ========================================================================
    
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            
            const spans = navToggle.querySelectorAll('span');
            if (navMenu.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translateY(8px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translateY(-8px)';
            } else {
                spans[0].style.transform = '';
                spans[1].style.opacity = '1';
                spans[2].style.transform = '';
            }
        });
        
        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                const spans = navToggle.querySelectorAll('span');
                spans[0].style.transform = '';
                spans[1].style.opacity = '1';
                spans[2].style.transform = '';
            });
        });
    }
    
    // ========================================================================
    // PARTICLE CANVAS ANIMATION
    // ========================================================================
    
    const canvas = document.getElementById('particleCanvas');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const particles = [];
        const particleCount = 50;
        
        class Particle {
            constructor() {
                this.reset();
            }
            
            reset() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 3 + 1;
                this.speedX = Math.random() * 2 - 1;
                this.speedY = Math.random() * 2 - 1;
                this.opacity = Math.random() * 0.5 + 0.1;
            }
            
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                
                if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
                if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;
            }
            
            draw() {
                ctx.fillStyle = `rgba(99, 102, 241, ${this.opacity})`;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }
        
        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(particle => {
                particle.update();
                particle.draw();
            });
            requestAnimationFrame(animate);
        }
        
        animate();
        
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    }
    
    // ========================================================================
    // ANIMATED COUNTERS
    // ========================================================================
    
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };
    
    const animateCounter = (element) => {
        const target = parseFloat(element.getAttribute('data-count'));
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;
        
        const updateCounter = () => {
            current += increment;
            if (current < target) {
                element.textContent = target % 1 === 0 ? Math.ceil(current) : current.toFixed(1);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target % 1 === 0 ? target : target.toFixed(1);
            }
        };
        
        updateCounter();
    };
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
                animateCounter(entry.target);
                entry.target.classList.add('animated');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.stat-number').forEach(counter => {
        counterObserver.observe(counter);
    });
    
    // ========================================================================
    // ROI CALCULATOR
    // ========================================================================
    
    const visitorsInput = document.getElementById('monthlyVisitors');
    const conversionInput = document.getElementById('conversionRate');
    const orderValueInput = document.getElementById('avgOrderValue');
    
    if (visitorsInput && conversionInput && orderValueInput) {
        function calculateROI() {
            const visitors = parseFloat(visitorsInput.value) || 0;
            const currentConversion = parseFloat(conversionInput.value) || 0;
            const orderValue = parseFloat(orderValueInput.value) || 0;
            
            const currentLeads = visitors * (currentConversion / 100);
            const currentRevenue = currentLeads * orderValue;
            
            const improvedConversion = currentConversion * 1.8; // Realistic 80% improvement
            const improvedLeads = visitors * (improvedConversion / 100);
            const potentialRevenue = improvedLeads * orderValue;
            
            const monthlyLoss = potentialRevenue - currentRevenue;
            const annualLoss = monthlyLoss * 12;
            
            document.getElementById('currentRevenue').textContent = '$' + currentRevenue.toLocaleString();
            document.getElementById('potentialRevenue').textContent = '$' + potentialRevenue.toLocaleString();
            document.getElementById('monthlyLoss').textContent = '$' + monthlyLoss.toLocaleString() + '/month';
            document.getElementById('annualLoss').textContent = '$' + annualLoss.toLocaleString();
        }
        
        visitorsInput.addEventListener('input', calculateROI);
        conversionInput.addEventListener('input', calculateROI);
        orderValueInput.addEventListener('input', calculateROI);
        
        calculateROI();
    }
    
    // ========================================================================
    // SMOOTH SCROLLING
    // ========================================================================
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            
            if (target) {
                const offsetTop = target.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // ========================================================================
    // MULTIPLE BEFORE/AFTER COMPARISON SLIDERS
    // ========================================================================
    
    const comparisonSliders = document.querySelectorAll('.comparison-slider');
    
    comparisonSliders.forEach(slider => {
        const afterImage = slider.querySelector('.after');
        const handle = slider.querySelector('.comparison-slider-handle');
        let isDragging = false;
        
        const updateSlider = (x) => {
            const rect = slider.getBoundingClientRect();
            const offsetX = x - rect.left;
            const percentage = Math.max(0, Math.min(100, (offsetX / rect.width) * 100));
            
            afterImage.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`;
            handle.style.left = `${percentage}%`;
        };
        
        handle.addEventListener('mousedown', () => {
            isDragging = true;
        });
        
        document.addEventListener('mousemove', (e) => {
            if (isDragging && slider.contains(e.target)) {
                updateSlider(e.clientX);
            }
        });
        
        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
        
        handle.addEventListener('touchstart', (e) => {
            isDragging = true;
            e.preventDefault();
        });
        
        document.addEventListener('touchmove', (e) => {
            if (isDragging) {
                const touch = e.touches[0];
                updateSlider(touch.clientX);
            }
        });
        
        document.addEventListener('touchend', () => {
            isDragging = false;
        });
        
        slider.addEventListener('click', (e) => {
            if (!isDragging) {
                updateSlider(e.clientX);
            }
        });
    });
    
    // ========================================================================
    // MULTI-STEP FORM
    // ========================================================================
    
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        let currentStep = 1;
        const totalSteps = 3;
        const steps = contactForm.querySelectorAll('.form-step');
        const progressFill = document.getElementById('progressFill');
        const currentStepText = document.getElementById('currentStep');
        
        function updateProgress() {
            const percentage = (currentStep / totalSteps) * 100;
            progressFill.style.width = percentage + '%';
            currentStepText.textContent = currentStep;
        }
        
        function showStep(stepNumber) {
            steps.forEach((step, index) => {
                if (index + 1 === stepNumber) {
                    step.classList.add('active');
                } else {
                    step.classList.remove('active');
                }
            });
            updateProgress();
        }
        
        contactForm.querySelectorAll('.next-step').forEach(button => {
            button.addEventListener('click', () => {
                const activeStep = contactForm.querySelector('.form-step.active');
                const inputs = activeStep.querySelectorAll('input[required]');
                let isValid = true;
                
                inputs.forEach(input => {
                    if (!input.value.trim()) {
                        isValid = false;
                        input.style.borderColor = '#ef4444';
                        setTimeout(() => {
                            input.style.borderColor = '';
                        }, 2000);
                    }
                });
                
                if (isValid && currentStep < totalSteps) {
                    currentStep++;
                    showStep(currentStep);
                }
            });
        });
        
        contactForm.querySelectorAll('.prev-step').forEach(button => {
            button.addEventListener('click', () => {
                if (currentStep > 1) {
                    currentStep--;
                    showStep(currentStep);
                }
            });
        });
        
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                business: document.getElementById('business').value,
                website: document.getElementById('website').value,
                phone: document.getElementById('phone').value,
                concern: document.getElementById('concern').value,
                message: document.getElementById('message').value,
                timestamp: new Date().toISOString()
            };
            
            const submitButton = contactForm.querySelector('button[type="submit"]');
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Sending...</span>';
            submitButton.disabled = true;
            
            setTimeout(() => {
                showSuccessMessage('Success! Check your email for your free audit. We\'ll contact you within 24 hours.');
                
                contactForm.reset();
                currentStep = 1;
                showStep(1);
                
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
                
                console.log('Form submitted:', formData);
            }, 1500);
        });
        
        // Email validation
        const emailInput = document.getElementById('email');
        if (emailInput) {
            emailInput.addEventListener('blur', function() {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (this.value && !emailRegex.test(this.value)) {
                    this.style.borderColor = '#ef4444';
                } else {
                    this.style.borderColor = '';
                }
            });
        }
        
        // Phone formatting
        const phoneInput = document.getElementById('phone');
        if (phoneInput) {
            phoneInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.length > 0) {
                    if (value.length <= 3) {
                        value = value;
                    } else if (value.length <= 6) {
                        value = value.slice(0, 3) + '-' + value.slice(3);
                    } else {
                        value = value.slice(0, 3) + '-' + value.slice(3, 6) + '-' + value.slice(6, 10);
                    }
                }
                e.target.value = value;
            });
        }
    }
    
    // ========================================================================
    // SUCCESS MESSAGE
    // ========================================================================
    
    function showSuccessMessage(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `
            <i class="fas fa-check-circle" style="margin-right: 10px;"></i>
            ${message}
        `;
        
        document.body.appendChild(successDiv);
        
        setTimeout(() => {
            successDiv.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(() => successDiv.remove(), 300);
        }, 5000);
    }
    
    // ========================================================================
    // EXIT INTENT POPUP
    // ========================================================================
    
    const exitPopup = document.getElementById('exitPopup');
    const exitPopupClose = document.getElementById('exitPopupClose');
    const exitPopupOverlay = document.getElementById('exitPopupOverlay');
    let exitIntentShown = false;
    
    document.addEventListener('mouseleave', (e) => {
        if (e.clientY <= 0 && !exitIntentShown) {
            exitPopup.classList.add('active');
            exitIntentShown = true;
            
            // Track event
            console.log('Exit intent triggered');
        }
    });
    
    if (exitPopupClose) {
        exitPopupClose.addEventListener('click', () => {
            exitPopup.classList.remove('active');
        });
    }
    
    if (exitPopupOverlay) {
        exitPopupOverlay.addEventListener('click', () => {
            exitPopup.classList.remove('active');
        });
    }
    
    // Close popup when clicking CTA
    const exitPopupCta = document.querySelector('.exit-popup-cta');
    if (exitPopupCta) {
        exitPopupCta.addEventListener('click', () => {
            exitPopup.classList.remove('active');
        });
    }
    
    // ========================================================================
    // 3D CARD TILT EFFECT
    // ========================================================================
    
    const cards = document.querySelectorAll('.glass-card, .pricing-card, .testimonial-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
        });
        
        card.addEventListener('mouseleave', function() {
            card.style.transform = '';
        });
    });
    
    // ========================================================================
    // LAZY LOADING FOR IMAGES
    // ========================================================================
    
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.getAttribute('data-src');
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // ========================================================================
    // TRACK ANALYTICS EVENTS
    // ========================================================================
    
    function trackEvent(eventName, data) {
        if (typeof gtag !== 'undefined') {
            gtag('event', eventName, data);
        }
        console.log('Event tracked:', eventName, data);
    }
    
    // Track button clicks
    document.querySelectorAll('.btn-primary, .btn-secondary').forEach(button => {
        button.addEventListener('click', () => {
            trackEvent('button_click', {
                button_text: button.textContent.trim(),
                button_location: button.closest('section')?.id || 'unknown'
            });
        });
    });
    
    // Track form interactions
    if (contactForm) {
        const formInputs = contactForm.querySelectorAll('input, select, textarea');
        formInputs.forEach(input => {
            let interacted = false;
            input.addEventListener('focus', () => {
                if (!interacted) {
                    trackEvent('form_started', {
                        form_name: 'contact_form'
                    });
                    interacted = true;
                }
            });
        });
    }
    
    // Track calculator usage
    if (visitorsInput) {
        let calculatorUsed = false;
        [visitorsInput, conversionInput, orderValueInput].forEach(input => {
            input.addEventListener('input', () => {
                if (!calculatorUsed) {
                    trackEvent('calculator_used', {
                        location: 'roi_calculator'
                    });
                    calculatorUsed = true;
                }
            });
        });
    }
    
});

// ============================================================================
// FUTURE ENHANCEMENTS
// ============================================================================

// Function to integrate with backend API
async function sendToBackend(formData) {
    try {
        const response = await fetch('/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            return { success: true };
        } else {
            throw new Error('Failed to send message');
        }
    } catch (error) {
        console.error('Error:', error);
        return { success: false, error: error.message };
    }
}
