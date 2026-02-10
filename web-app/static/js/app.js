// Agent Dashboard Web App
// JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    console.log('Agent Dashboard loaded');
    
    // Add active class to current nav item
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        if (item.getAttribute('href') === currentPath) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
});

// API helper functions
const API = {
    async updateLog(data) {
        try {
            const response = await fetch('/api/log', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('Error updating log:', error);
            return { status: 'error', message: error.message };
        }
    }
};
