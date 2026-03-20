// Mobile menu toggle (Production safe)
document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ JS loaded - Mobile menu ready');
    
    // Mobile menu button
    const menuBtn = document.querySelector('.menu-toggle');
    const mobileMenu = document.querySelector('.mobile-nav');
    const navLinks = document.querySelectorAll('.nav-link');
    
    if (menuBtn && mobileMenu) {
        console.log('✅ Mobile menu elements found');
        
        menuBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('🍔 Mobile menu clicked');
            
            menuBtn.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });
        
        // Close on outside click
        document.addEventListener('click', function(e) {
            if (!menuBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
                menuBtn.classList.remove('active');
                mobileMenu.classList.remove('active');
            }
        });
        
        // Close on link click
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                menuBtn.classList.remove('active');
                mobileMenu.classList.remove('active');
            });
        });
    }
    
    // Form submission
    const form = document.getElementById('quoteForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('📤 Form submitted');
            
            const formData = {
                name: document.getElementById('name').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                business: document.getElementById('business').value,
                message: document.getElementById('message').value
            };
            
            fetch('/submit-quote', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                console.log('✅ Form response:', data);
                alert(data.message || 'Thank you!');
                form.reset();
            })
            .catch(error => {
                console.error('❌ Form error:', error);
                alert('Please try WhatsApp below');
            });
        });
    }
    
    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});
