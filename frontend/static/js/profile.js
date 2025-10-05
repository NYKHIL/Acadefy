/**
 * Acadefy Profile JavaScript
 * Handles user profile, preferences, and settings
 */

class AcadefyProfile {
    constructor() {
        this.sessionId = window.AcadefyApp.sessionId;
        this.preferences = {};
        this.goals = [];
        this.statistics = {};
        
        this.init();
    }
    
    init() {
        console.log('Initializing profile...');
        this.loadPreferences();
        this.loadGoals();
        this.loadStatistics();
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Preference change listeners
        const preferenceInputs = document.querySelectorAll('#difficulty-preference, #learning-style, #session-length');
        preferenceInputs.forEach(input => {
            input.addEventListener('change', () => this.onPreferenceChange());
        });
        
        const checkboxes = document.querySelectorAll('#detailed-explanations, #practice-problems, #progress-notifications');
        checkboxes.forEach(checkbox => {
            checkbox.addEventListener('change', () => this.onPreferenceChange());
        });
        
        // Goal input
        const goalInput = document.getElementById('new-goal');
        if (goalInput) {
            goalInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.addGoal();
                }
            });
        }
    }
    
    loadPreferences() {
        // Load from localStorage or set defaults
        this.preferences = window.AcadefyApp.storage.get('user_preferences', {
            difficulty: 'intermediate',
            learningStyle: 'mixed',
            sessionLength: 'medium',
            detailedExplanations: true,
            practiceProblems: true,
            progressNotifications: false
        });
        
        this.applyPreferencesToUI();
    }
    
    applyPreferencesToUI() {
        // Apply preferences to form elements
        const difficultySelect = document.getElementById('difficulty-preference');
        if (difficultySelect) {
            difficultySelect.value = this.preferences.difficulty || 'intermediate';
        }
        
        const learningStyleSelect = document.getElementById('learning-style');
        if (learningStyleSelect) {
            learningStyleSelect.value = this.preferences.learningStyle || 'mixed';
        }
        
        const sessionLengthSelect = document.getElementById('session-length');
        if (sessionLengthSelect) {
            sessionLengthSelect.value = this.preferences.sessionLength || 'medium';
        }
        
        const detailedExplanations = document.getElementById('detailed-explanations');
        if (detailedExplanations) {
            detailedExplanations.checked = this.preferences.detailedExplanations !== false;
        }
        
        const practiceProblems = document.getElementById('practice-problems');
        if (practiceProblems) {
            practiceProblems.checked = this.preferences.practiceProblems !== false;
        }
        
        const progressNotifications = document.getElementById('progress-notifications');
        if (progressNotifications) {
            progressNotifications.checked = this.preferences.progressNotifications === true;
        }
    }
    
    onPreferenceChange() {
        // Update preferences object
        this.preferences = {
            difficulty: document.getElementById('difficulty-preference')?.value || 'intermediate',
            learningStyle: document.getElementById('learning-style')?.value || 'mixed',
            sessionLength: document.getElementById('session-length')?.value || 'medium',
            detailedExplanations: document.getElementById('detailed-explanations')?.checked || false,
            practiceProblems: document.getElementById('practice-problems')?.checked || false,
            progressNotifications: document.getElementById('progress-notifications')?.checked || false
        };
        
        // Auto-save preferences
        this.savePreferences(false); // Don't show toast for auto-save
    }
    
    savePreferences(showToast = true) {
        // Save to localStorage
        window.AcadefyApp.storage.set('user_preferences', this.preferences);
        
        if (showToast) {
            window.AcadefyApp.showToast('Preferences saved successfully!', 'success');
        }
        
        console.log('Preferences saved:', this.preferences);
    }
    
    resetPreferences() {
        this.showConfirmationModal(
            'Reset Preferences',
            'Are you sure you want to reset all preferences to default values?',
            () => {
                // Reset to defaults
                this.preferences = {
                    difficulty: 'intermediate',
                    learningStyle: 'mixed',
                    sessionLength: 'medium',
                    detailedExplanations: true,
                    practiceProblems: true,
                    progressNotifications: false
                };
                
                this.applyPreferencesToUI();
                this.savePreferences();
                window.AcadefyApp.showToast('Preferences reset to default', 'success');
            }
        );
    }
    
    loadGoals() {
        this.goals = window.AcadefyApp.storage.get('learning_goals', [
            'Master algebra fundamentals',
            'Improve writing skills',
            'Learn basic programming'
        ]);
        
        this.renderGoals();
    }
    
    renderGoals() {
        const goalsList = document.getElementById('goals-list');
        if (!goalsList) return;
        
        if (this.goals.length === 0) {
            goalsList.innerHTML = `
                <div class="empty-content">
                    <i class="fas fa-target"></i>
                    <p>No learning goals set yet. Add your first goal above!</p>
                </div>
            `;
            return;
        }
        
        goalsList.innerHTML = this.goals.map((goal, index) => `
            <div class="goal-item">
                <span class="goal-text">${window.AcadefyUtils.sanitizeHtml(goal)}</span>
                <div class="goal-actions">
                    <button onclick="profileInstance.editGoal(${index})" title="Edit goal">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button onclick="profileInstance.removeGoal(${index})" title="Remove goal">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    addGoal() {
        const goalInput = document.getElementById('new-goal');
        if (!goalInput) return;
        
        const goalText = goalInput.value.trim();
        if (!goalText) {
            window.AcadefyApp.showToast('Please enter a goal', 'error');
            return;
        }
        
        if (goalText.length > 100) {
            window.AcadefyApp.showToast('Goal is too long (max 100 characters)', 'error');
            return;
        }
        
        this.goals.push(goalText);
        goalInput.value = '';
        
        this.saveGoals();
        this.renderGoals();
        
        window.AcadefyApp.showToast('Goal added successfully!', 'success');
    }
    
    editGoal(index) {
        const currentGoal = this.goals[index];
        const newGoal = prompt('Edit your goal:', currentGoal);
        
        if (newGoal !== null && newGoal.trim() !== '') {
            if (newGoal.trim().length > 100) {
                window.AcadefyApp.showToast('Goal is too long (max 100 characters)', 'error');
                return;
            }
            
            this.goals[index] = newGoal.trim();
            this.saveGoals();
            this.renderGoals();
            
            window.AcadefyApp.showToast('Goal updated successfully!', 'success');
        }
    }
    
    removeGoal(index) {
        this.showConfirmationModal(
            'Remove Goal',
            `Are you sure you want to remove this goal: "${this.goals[index]}"?`,
            () => {
                this.goals.splice(index, 1);
                this.saveGoals();
                this.renderGoals();
                window.AcadefyApp.showToast('Goal removed', 'success');
            }
        );
    }
    
    saveGoals() {
        window.AcadefyApp.storage.set('learning_goals', this.goals);
    }
    
    async loadStatistics() {
        try {
            // Load progress data for statistics
            const progressResponse = await window.AcadefyApp.apiRequest(`/progress?session_id=${this.sessionId}`);
            const analyticsResponse = await window.AcadefyApp.apiRequest(`/analytics?session_id=${this.sessionId}&days=30`);
            
            let stats = {
                daysActive: 0,
                totalMessages: 0,
                subjectsExplored: 0,
                achievements: 0
            };
            
            if (progressResponse.success && progressResponse.data) {
                stats.subjectsExplored = progressResponse.data.overall_stats?.total_subjects || 0;
                stats.totalMessages = progressResponse.data.overall_stats?.total_interactions || 0;
            }
            
            if (analyticsResponse.success && analyticsResponse.data) {
                const analytics = analyticsResponse.data.analytics;
                stats.daysActive = Object.keys(analytics.daily_interactions || {}).length;
                
                // Calculate achievements based on progress
                const subjectStats = analytics.subject_statistics || {};
                stats.achievements = Object.values(subjectStats).filter(stat => 
                    stat.skill_level >= 7 || stat.completion >= 80
                ).length;
            }
            
            this.statistics = stats;
            this.renderStatistics();
            
        } catch (error) {
            console.error('Error loading statistics:', error);
            this.renderStatistics(); // Render with default values
        }
    }
    
    renderStatistics() {
        // Update statistics display
        this.updateElement('days-active', this.statistics.daysActive || 0);
        this.updateElement('total-messages', this.statistics.totalMessages || 0);
        this.updateElement('subjects-explored', this.statistics.subjectsExplored || 0);
        this.updateElement('achievements', this.statistics.achievements || 0);
    }
    
    exportData() {
        const userData = {
            sessionId: this.sessionId,
            exportDate: new Date().toISOString(),
            preferences: this.preferences,
            goals: this.goals,
            statistics: this.statistics,
            chatHistory: window.AcadefyApp.storage.get('chat_history', [])
        };
        
        const dataStr = JSON.stringify(userData, null, 2);
        const filename = `acadefy-profile-${new Date().toISOString().split('T')[0]}.json`;
        
        window.AcadefyUtils.downloadAsFile(dataStr, filename);
        window.AcadefyApp.showToast('Profile data exported successfully!', 'success');
    }
    
    clearHistory() {
        this.showConfirmationModal(
            'Clear Chat History',
            'This will permanently delete all your chat history. This action cannot be undone.',
            () => {
                window.AcadefyApp.storage.remove('chat_history');
                window.AcadefyApp.showToast('Chat history cleared', 'success');
            }
        );
    }
    
    resetProgress() {
        this.showConfirmationModal(
            'Reset All Progress',
            'This will permanently delete ALL your learning progress, chat history, goals, and preferences. This action cannot be undone!',
            () => {
                // Clear all stored data
                window.AcadefyApp.storage.clear();
                
                // Reset current state
                this.preferences = {};
                this.goals = [];
                this.statistics = {};
                
                // Reload page to reset everything
                window.location.reload();
            },
            'danger'
        );
    }
    
    showConfirmationModal(title, message, onConfirm, type = 'danger') {
        const modal = document.getElementById('confirmation-modal');
        const titleElement = document.getElementById('modal-title');
        const messageElement = document.getElementById('modal-message');
        const confirmButton = document.getElementById('confirm-button');
        
        if (modal && titleElement && messageElement && confirmButton) {
            titleElement.textContent = title;
            messageElement.textContent = message;
            confirmButton.className = `btn btn-${type}`;
            
            // Store the callback
            this.pendingConfirmAction = onConfirm;
            
            modal.style.display = 'flex';
        }
    }
    
    closeConfirmationModal() {
        const modal = document.getElementById('confirmation-modal');
        if (modal) {
            modal.style.display = 'none';
            this.pendingConfirmAction = null;
        }
    }
    
    confirmAction() {
        if (this.pendingConfirmAction) {
            this.pendingConfirmAction();
            this.pendingConfirmAction = null;
        }
        this.closeConfirmationModal();
    }
    
    // Utility method
    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    }
}

// Global functions for HTML onclick handlers
window.savePreferences = function() {
    if (window.profileInstance) {
        window.profileInstance.savePreferences();
    }
};

window.resetPreferences = function() {
    if (window.profileInstance) {
        window.profileInstance.resetPreferences();
    }
};

window.addGoal = function() {
    if (window.profileInstance) {
        window.profileInstance.addGoal();
    }
};

window.exportData = function() {
    if (window.profileInstance) {
        window.profileInstance.exportData();
    }
};

window.clearHistory = function() {
    if (window.profileInstance) {
        window.profileInstance.clearHistory();
    }
};

window.resetProgress = function() {
    if (window.profileInstance) {
        window.profileInstance.resetProgress();
    }
};

window.closeConfirmationModal = function() {
    if (window.profileInstance) {
        window.profileInstance.closeConfirmationModal();
    }
};

window.confirmAction = function() {
    if (window.profileInstance) {
        window.profileInstance.confirmAction();
    }
};

// Initialize profile when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.profile-page')) {
        window.profileInstance = new AcadefyProfile();
    }
});