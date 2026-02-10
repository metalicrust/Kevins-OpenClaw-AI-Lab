// Agent Dashboard - Feature 2: Daily Log CRUD
// Frontend JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    console.log('Agent Dashboard - Feature 2 loaded');
    
    // Auto-hide alerts after 3 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 3000);
    });
    
    // Set active nav item based on URL
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-item').forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
    
    // Confirm before delete
    document.querySelectorAll('form[action*="delete"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Delete this task?')) {
                e.preventDefault();
            }
        });
    });
});

// Add loading states to buttons
document.querySelectorAll('button[type="submit"]').forEach(button => {
    button.addEventListener('click', function() {
        this.style.opacity = '0.7';
    });
});
