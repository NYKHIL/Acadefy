/**
 * Acadefy - Main JavaScript
 * Core functionality and utilities
 */

// Global app state
window.AcadefyApp = {
    sessionId: localStorage.getItem('acadefy_session_id') || null,
    apiBaseUrl: '/api',
    
    // Initialize the application
    init() {
        this.setupEventListeners();
        this.generateSessionId();
        console.log('Acadefy app initialized');
    },
    
    // Generate or retrieve session ID
    generateSessionId() {
        if (!this.sessionId) {
            this.sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('acadefy_session_id', this.sessionId);
        }
        return this.sessionId;
    },
    
    // Setup global event listeners
    setupEventListeners() {
        // Handle navigation active states
        this.updateActiveNavigation();
        
        // Handle responsive navigation
        this.setupResponsiveNavigation();
        
        // Handle keyboard shortcuts
        document.addEventListener('keydown', this.handleKeyboardShortcuts.bind(this));
    },
    
    // Update active navigation state
    updateActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPath || (currentPath === '/' && href === '/')) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    },
    
    // Setup responsive navigation
    setupResponsiveNavigation() {
        // Add mobile menu toggle if needed
        const navbar = document.querySelector('.navbar');
        if (navbar && window.innerWidth <= 768) {
            // Mobile navigation logic can be added here
        }
    },
    
    // Handle keyboard shortcuts
    handleKeyboardShortcuts(event) {
        // Ctrl/Cmd + K to focus search or chat input
        if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
            event.preventDefault();
            const chatInput = document.getElementById('message-input');
            if (chatInput) {
                chatInput.focus();
            }
        }
        
        // Escape to close modals
        if (event.key === 'Escape') {
            this.closeAllModals();
        }
    },
    
    // Close all open modals
    closeAllModals() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            if (modal.style.display !== 'none') {
                modal.style.display = 'none';
            }
        });
    },
    
    // API request helper
    async apiRequest(endpoint, options = {}) {
        const url = `${this.apiBaseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, config);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('API request failed:', error);
            return { success: false, error: error.message };
        }
    },
    
    // Show toast notification
    showToast(message, type = 'success', duration = 3000) {
        // Remove existing toasts
        const existingToasts = document.querySelectorAll('.toast');
        existingToasts.forEach(toast => toast.remove());
        
        // Create new toast
        const toast = document.createElement('div');
        toast.className = `toast ${type}-toast`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Hide toast
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },
    
    // Show loading state
    showLoading(element, text = 'Loading...') {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        
        if (element) {
            element.innerHTML = `
                <div class="loading-state">
                    <div class="spinner"></div>
                    <p>${text}</p>
                </div>
            `;
        }
    },
    
    // Format date for display
    formatDate(date, options = {}) {
        const defaultOptions = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        
        const config = { ...defaultOptions, ...options };
        return new Date(date).toLocaleDateString('en-US', config);
    },
    
    // Format time ago
    formatTimeAgo(date) {
        const now = new Date();
        const past = new Date(date);
        const diffInSeconds = Math.floor((now - past) / 1000);
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
        if (diffInSeconds < 2592000) return `${Math.floor(diffInSeconds / 86400)}d ago`;
        
        return this.formatDate(date, { year: 'numeric', month: 'short', day: 'numeric' });
    },
    
    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // Animate element
    animateElement(element, animation, duration = 300) {
        if (typeof element === 'string') {
            element = document.getElementById(element);
        }
        
        if (element) {
            element.style.animation = `${animation} ${duration}ms ease`;
            setTimeout(() => {
                element.style.animation = '';
            }, duration);
        }
    },
    
    // Smooth scroll to element
    scrollToElement(elementId, offset = 0) {
        const element = document.getElementById(elementId);
        if (element) {
            const elementPosition = element.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - offset;
            
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    },
    
    // Local storage helpers
    storage: {
        set(key, value) {
            try {
                localStorage.setItem(`acadefy_${key}`, JSON.stringify(value));
                return true;
            } catch (error) {
                console.error('Failed to save to localStorage:', error);
                return false;
            }
        },
        
        get(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(`acadefy_${key}`);
                return item ? JSON.parse(item) : defaultValue;
            } catch (error) {
                console.error('Failed to read from localStorage:', error);
                return defaultValue;
            }
        },
        
        remove(key) {
            try {
                localStorage.removeItem(`acadefy_${key}`);
                return true;
            } catch (error) {
                console.error('Failed to remove from localStorage:', error);
                return false;
            }
        },
        
        clear() {
            try {
                const keys = Object.keys(localStorage).filter(key => key.startsWith('acadefy_'));
                keys.forEach(key => localStorage.removeItem(key));
                return true;
            } catch (error) {
                console.error('Failed to clear localStorage:', error);
                return false;
            }
        }
    }
};

// Utility functions
window.AcadefyUtils = {
    // Validate email
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },
    
    // Sanitize HTML
    sanitizeHtml(str) {
        const temp = document.createElement('div');
        temp.textContent = str;
        return temp.innerHTML;
    },
    
    // Generate random ID
    generateId(prefix = 'id') {
        return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    },
    
    // Copy text to clipboard
    async copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (error) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            const success = document.execCommand('copy');
            document.body.removeChild(textArea);
            return success;
        }
    },
    
    // Download data as file
    downloadAsFile(data, filename, type = 'application/json') {
        const blob = new Blob([data], { type });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    },
    
    // Format file size
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.AcadefyApp.init();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        console.log('Page hidden');
    } else {
        console.log('Page visible');
        // Refresh data if needed
    }
});

// Handle online/offline status
window.addEventListener('online', function() {
    window.AcadefyApp.showToast('Connection restored', 'success');
});

window.addEventListener('offline', function() {
    window.AcadefyApp.showToast('Connection lost', 'error');
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AcadefyApp: window.AcadefyApp, AcadefyUtils: window.AcadefyUtils };
}