/**
 * Acadefy Dashboard JavaScript
 * Handles dashboard functionality, progress tracking, and recommendations
 */

class AcadefyDashboard {
    constructor() {
        this.sessionId = window.AcadefyApp.sessionId;
        this.progressData = null;
        this.recommendationsData = null;
        this.analyticsData = null;
        
        this.init();
    }
    
    init() {
        console.log('Initializing dashboard...');
        this.loadDashboardData();
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Refresh button
        const refreshBtn = document.querySelector('[onclick="refreshDashboard()"]');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.refreshDashboard());
        }
    }
    
    async loadDashboardData() {
        const loadingState = document.getElementById('loading-state');
        const dashboardContent = document.getElementById('dashboard-content');
        const emptyState = document.getElementById('empty-state');
        
        if (loadingState) loadingState.style.display = 'block';
        if (dashboardContent) dashboardContent.style.display = 'none';
        if (emptyState) emptyState.style.display = 'none';
        
        try {
            // Load progress data
            await this.loadProgressData();
            
            // Load recommendations
            await this.loadRecommendations();
            
            // Load analytics
            await this.loadAnalytics();
            
            // Check if we have any data
            if (this.hasData()) {
                this.renderDashboard();
                if (loadingState) loadingState.style.display = 'none';
                if (dashboardContent) dashboardContent.style.display = 'block';
            } else {
                this.showEmptyState();
            }
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showError('Failed to load dashboard data');
        }
    }
    
    async loadProgressData() {
        const response = await window.AcadefyApp.apiRequest(`/progress?session_id=${this.sessionId}`);
        
        if (response.success) {
            this.progressData = response.data;
            console.log('Progress data loaded:', this.progressData);
        } else {
            console.error('Failed to load progress data:', response.error);
        }
    }
    
    async loadRecommendations() {
        const response = await window.AcadefyApp.apiRequest(`/recommendations?session_id=${this.sessionId}`);
        
        if (response.success) {
            this.recommendationsData = response.data;
            console.log('Recommendations loaded:', this.recommendationsData);
        } else {
            console.error('Failed to load recommendations:', response.error);
        }
    }
    
    async loadAnalytics() {
        const response = await window.AcadefyApp.apiRequest(`/analytics?session_id=${this.sessionId}&days=7`);
        
        if (response.success) {
            this.analyticsData = response.data;
            console.log('Analytics loaded:', this.analyticsData);
        } else {
            console.error('Failed to load analytics:', response.error);
        }
    }
    
    hasData() {
        return this.progressData && 
               this.progressData.progress && 
               this.progressData.progress.length > 0;
    }
    
    renderDashboard() {
        this.renderOverviewCards();
        this.renderProgressSection();
        this.renderRecommendations();
        this.renderAnalytics();
    }
    
    renderOverviewCards() {
        if (!this.progressData || !this.progressData.overall_stats) return;
        
        const stats = this.progressData.overall_stats;
        
        // Update overview cards
        this.updateElement('total-subjects', stats.total_subjects);
        this.updateElement('avg-skill-level', stats.average_skill_level);
        this.updateElement('total-interactions', stats.total_interactions);
        this.updateElement('overall-completion', `${stats.overall_completion}%`);
    }
    
    renderProgressSection() {
        const progressList = document.getElementById('progress-list');
        if (!progressList || !this.progressData || !this.progressData.progress) return;
        
        const progressItems = this.progressData.progress.map(item => this.createProgressItem(item));
        progressList.innerHTML = progressItems.join('');
        
        // Animate progress bars
        setTimeout(() => {
            this.animateProgressBars();
        }, 100);
    }
    
    createProgressItem(progress) {
        const accuracyColor = progress.accuracy_rate >= 80 ? 'var(--secondary-color)' : 
                             progress.accuracy_rate >= 60 ? 'var(--accent-color)' : 'var(--danger-color)';
        
        return `
            <div class="progress-item">
                <div class="progress-header">
                    <div class="progress-title">${this.capitalizeFirst(progress.subject)}</div>
                    <div class="skill-badge">Level ${progress.skill_level}</div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" data-width="${progress.completion_percentage}" style="width: 0%;"></div>
                </div>
                <div class="progress-stats">
                    <span>${progress.completion_percentage}% Complete</span>
                    <span>${progress.interactions_count} interactions</span>
                    <span style="color: ${accuracyColor}">${progress.accuracy_rate.toFixed(1)}% accuracy</span>
                </div>
            </div>
        `;
    }
    
    renderRecommendations() {
        const recommendationsList = document.getElementById('recommendations-list');
        if (!recommendationsList) return;
        
        if (!this.recommendationsData || !this.recommendationsData.recommendations || 
            this.recommendationsData.recommendations.length === 0) {
            recommendationsList.innerHTML = `
                <div class="empty-content">
                    <i class="fas fa-lightbulb"></i>
                    <p>No recommendations available yet. Continue learning to get personalized suggestions!</p>
                </div>
            `;
            return;
        }
        
        const recommendations = this.recommendationsData.recommendations
            .slice(0, 6) // Show top 6 recommendations
            .map(item => this.createRecommendationItem(item));
        
        recommendationsList.innerHTML = recommendations.join('');
    }
    
    createRecommendationItem(recommendation) {
        const typeColors = {
            'skill_improvement': 'var(--primary-color)',
            'subject_expansion': 'var(--secondary-color)',
            'review': 'var(--accent-color)',
            'challenge': 'var(--danger-color)',
            'support': 'var(--warning-color)',
            'getting_started': 'var(--gray-600)'
        };
        
        const typeColor = typeColors[recommendation.type] || 'var(--gray-600)';
        
        return `
            <div class="recommendation-item">
                <div class="recommendation-header">
                    <div>
                        <div class="recommendation-title">${recommendation.title}</div>
                        <div class="recommendation-type" style="background: ${typeColor}">
                            ${this.formatRecommendationType(recommendation.type)}
                        </div>
                    </div>
                </div>
                <div class="recommendation-description">
                    ${recommendation.description}
                </div>
                <div class="recommendation-meta">
                    <span><i class="fas fa-clock"></i> ${recommendation.estimated_time}</span>
                    <span><i class="fas fa-signal"></i> Difficulty ${recommendation.difficulty}/10</span>
                </div>
            </div>
        `;
    }
    
    renderAnalytics() {
        if (!this.analyticsData || !this.analyticsData.analytics) return;
        
        const analytics = this.analyticsData.analytics;
        
        // Update analytics cards
        this.updateElement('learning-streak', analytics.learning_streak || 0);
        this.updateElement('avg-response-time', analytics.average_response_time || 0);
        
        // Find most active subject
        const subjectStats = analytics.subject_statistics || {};
        const mostActiveSubject = Object.keys(subjectStats).reduce((a, b) => 
            (subjectStats[a]?.interactions || 0) > (subjectStats[b]?.interactions || 0) ? a : b, 
            Object.keys(subjectStats)[0] || 'None'
        );
        
        this.updateElement('active-subject', this.capitalizeFirst(mostActiveSubject));
        
        // Update subject icon
        const subjectIcon = document.getElementById('active-subject-icon');
        if (subjectIcon) {
            const iconMap = {
                'mathematics': 'fa-calculator',
                'science': 'fa-flask',
                'english': 'fa-book',
                'programming': 'fa-code',
                'history': 'fa-landmark'
            };
            subjectIcon.className = `fas ${iconMap[mostActiveSubject] || 'fa-book'}`;
        }
    }
    
    animateProgressBars() {
        const progressBars = document.querySelectorAll('.progress-fill');
        progressBars.forEach((bar, index) => {
            setTimeout(() => {
                const width = bar.getAttribute('data-width');
                bar.style.width = `${width}%`;
            }, index * 100);
        });
    }
    
    showEmptyState() {
        const loadingState = document.getElementById('loading-state');
        const dashboardContent = document.getElementById('dashboard-content');
        const emptyState = document.getElementById('empty-state');
        
        if (loadingState) loadingState.style.display = 'none';
        if (dashboardContent) dashboardContent.style.display = 'none';
        if (emptyState) emptyState.style.display = 'block';
    }
    
    showError(message) {
        const loadingState = document.getElementById('loading-state');
        if (loadingState) {
            loadingState.innerHTML = `
                <div class="error-state">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h3>Error Loading Dashboard</h3>
                    <p>${message}</p>
                    <button class="btn btn-primary" onclick="location.reload()">
                        <i class="fas fa-refresh"></i>
                        Try Again
                    </button>
                </div>
            `;
        }
    }
    
    async refreshDashboard() {
        window.AcadefyApp.showToast('Refreshing dashboard...', 'info', 1000);
        await this.loadDashboardData();
        window.AcadefyApp.showToast('Dashboard updated!', 'success');
    }
    
    // Utility methods
    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }
    
    capitalizeFirst(str) {
        if (!str) return '';
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
    
    formatRecommendationType(type) {
        const typeMap = {
            'skill_improvement': 'Practice',
            'subject_expansion': 'Explore',
            'review': 'Review',
            'challenge': 'Challenge',
            'support': 'Support',
            'getting_started': 'Start'
        };
        return typeMap[type] || 'Learn';
    }
}

// Global functions for HTML onclick handlers
window.refreshDashboard = function() {
    if (window.dashboardInstance) {
        window.dashboardInstance.refreshDashboard();
    }
};

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.dashboard')) {
        window.dashboardInstance = new AcadefyDashboard();
    }
});