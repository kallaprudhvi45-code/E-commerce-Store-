// UI Utility functions
const UI = {
    showToast(message, type = 'success') {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerText = message;

        container.appendChild(toast);

        setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s ease reverse forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    showError(message) {
        this.showToast(message, 'error');
    },

    showLoading(elementId) {
        const el = document.getElementById(elementId);
        if (el) {
            el.innerHTML = '<div class="spinner"></div>';
        }
    },

    updateNav() {
        const authLinks = document.getElementById('auth-links');
        if (!authLinks) return;

        if (ApiService.isAuthenticated()) {
            authLinks.innerHTML = `
                <a href="cart.html">Cart</a>
                <a href="orders.html">Orders</a>
                <a href="profile.html">Profile</a>
                <a href="#" id="logout-btn">Logout</a>
            `;
            
            document.getElementById('logout-btn').addEventListener('click', (e) => {
                e.preventDefault();
                ApiService.logout();
            });
        } else {
            authLinks.innerHTML = `
                <a href="login.html">Login</a>
                <a href="register.html" class="btn btn-primary" style="color: white">Sign Up</a>
            `;
        }
    },

    setupMobileNav() {
        const btn = document.querySelector('.mobile-menu-btn');
        const links = document.querySelector('.nav-links');
        if (btn && links) {
            btn.addEventListener('click', () => {
                links.classList.toggle('active');
            });
        }
    }
};

// Initialize common UI elements on load
document.addEventListener('DOMContentLoaded', () => {
    UI.updateNav();
    UI.setupMobileNav();
});
