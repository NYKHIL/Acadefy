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
        this.loadDocuments();
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
        
        // File upload listeners
        this.setupFileUploadListeners();
    }
    
    setupFileUploadListeners() {
        const fileInput = document.getElementById('document-files');
        const dropZone = document.getElementById('file-drop-zone');
        
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileSelection(e));
        }
        
        if (dropZone) {
            // Drag and drop functionality
            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('drag-over');
            });
            
            dropZone.addEventListener('dragleave', (e) => {
                e.preventDefault();
                dropZone.classList.remove('drag-over');
            });
            
            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('drag-over');
                
                const files = Array.from(e.dataTransfer.files);
                this.handleDroppedFiles(files);
            });
            
            // Click to select files
            dropZone.addEventListener('click', () => {
                fileInput.click();
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
    
    async loadDocuments() {
        try {
            const response = await window.AcadefyApp.apiRequest('/documents');
            
            if (response.success && response.data.documents) {
                this.renderDocuments(response.data.documents);
            }
        } catch (error) {
            console.error('Error loading documents:', error);
        }
    }
    
    renderDocuments(documents) {
        const documentsList = document.getElementById('documents-list');
        if (!documentsList) return;
        
        if (documents.length === 0) {
            documentsList.innerHTML = `
                <div class="empty-content">
                    <i class="fas fa-book"></i>
                    <p>No reference documents added yet. Add some documents above to enhance your AI tutor's knowledge!</p>
                </div>
            `;
            return;
        }
        
        documentsList.innerHTML = documents.map(doc => `
            <div class="document-item">
                <div class="document-info">
                    <h4 class="document-title">${window.AcadefyUtils.sanitizeHtml(doc.title)}</h4>
                    <p class="document-meta">
                        <span><i class="fas fa-link"></i> ${doc.url}</span>
                        <span><i class="fas fa-file"></i> ${doc.chunks_count} chunks</span>
                        <span><i class="fas fa-tags"></i> ${doc.keywords_count} keywords</span>
                    </p>
                </div>
                <div class="document-actions">
                    <button class="btn btn-sm btn-danger" onclick="profileInstance.removeDocument('${doc.id}')">
                        <i class="fas fa-trash"></i>
                        Remove
                    </button>
                </div>
            </div>
        `).join('');
    }
    
    async addDocumentFromUrl() {
        const urlInput = document.getElementById('document-url');
        const titleInput = document.getElementById('document-title');
        
        if (!urlInput || !urlInput.value.trim()) {
            window.AcadefyApp.showToast('Please enter a valid URL', 'error');
            return;
        }
        
        const url = urlInput.value.trim();
        const title = titleInput.value.trim();
        
        try {
            window.AcadefyApp.showToast('Adding document...', 'info', 1000);
            
            const response = await window.AcadefyApp.apiRequest('/documents/add-url', {
                method: 'POST',
                body: JSON.stringify({ url, title })
            });
            
            if (response.success) {
                window.AcadefyApp.showToast('Document added successfully!', 'success');
                urlInput.value = '';
                titleInput.value = '';
                this.loadDocuments();
            } else {
                window.AcadefyApp.showToast(response.data.error || 'Failed to add document', 'error');
            }
        } catch (error) {
            console.error('Error adding document:', error);
            window.AcadefyApp.showToast('Failed to add document', 'error');
        }
    }
    
    handleFileSelection(event) {
        const files = Array.from(event.target.files);
        this.validateAndDisplayFiles(files);
    }
    
    handleDroppedFiles(files) {
        // Update the file input with dropped files
        const fileInput = document.getElementById('document-files');
        if (fileInput) {
            const dt = new DataTransfer();
            files.forEach(file => dt.items.add(file));
            fileInput.files = dt.files;
        }
        
        this.validateAndDisplayFiles(files);
    }
    
    validateAndDisplayFiles(files) {
        const maxFiles = 5;
        const maxSize = 10 * 1024 * 1024; // 10MB
        const allowedExtensions = ['.pdf', '.docx', '.pptx', '.txt'];
        
        // Check file count
        if (files.length > maxFiles) {
            window.AcadefyApp.showToast(`Maximum ${maxFiles} files allowed`, 'error');
            return;
        }
        
        const validFiles = [];
        const errors = [];
        
        files.forEach(file => {
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
            
            // Check file type
            if (!allowedExtensions.includes(fileExtension)) {
                errors.push(`${file.name}: Unsupported file type`);
                return;
            }
            
            // Check file size
            if (file.size > maxSize) {
                errors.push(`${file.name}: File too large (max 10MB)`);
                return;
            }
            
            validFiles.push(file);
        });
        
        // Show errors if any
        if (errors.length > 0) {
            window.AcadefyApp.showToast(errors.join(', '), 'error');
        }
        
        // Display valid files
        this.displaySelectedFiles(validFiles);
        
        // Enable/disable upload button
        const uploadBtn = document.getElementById('upload-files-btn');
        if (uploadBtn) {
            uploadBtn.disabled = validFiles.length === 0;
        }
    }
    
    displaySelectedFiles(files) {
        const selectedFilesList = document.getElementById('selected-files');
        if (!selectedFilesList) return;
        
        if (files.length === 0) {
            selectedFilesList.innerHTML = '';
            return;
        }
        
        selectedFilesList.innerHTML = `
            <div class="selected-files-header">
                <h4>Selected Files (${files.length}/${5}):</h4>
            </div>
            <div class="files-grid">
                ${files.map((file, index) => `
                    <div class="file-item">
                        <div class="file-info">
                            <i class="fas fa-${this.getFileIcon(file.name)}"></i>
                            <span class="file-name">${file.name}</span>
                            <span class="file-size">${this.formatFileSize(file.size)}</span>
                        </div>
                        <button class="btn-remove" onclick="profileInstance.removeSelectedFile(${index})" title="Remove file">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    removeSelectedFile(index) {
        const fileInput = document.getElementById('document-files');
        if (!fileInput || !fileInput.files) return;
        
        const files = Array.from(fileInput.files);
        files.splice(index, 1);
        
        // Update file input
        const dt = new DataTransfer();
        files.forEach(file => dt.items.add(file));
        fileInput.files = dt.files;
        
        this.validateAndDisplayFiles(files);
    }
    
    getFileIcon(filename) {
        const extension = filename.split('.').pop().toLowerCase();
        const iconMap = {
            'pdf': 'file-pdf',
            'docx': 'file-word',
            'pptx': 'file-powerpoint',
            'txt': 'file-alt'
        };
        return iconMap[extension] || 'file';
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    async addDocumentFromFiles() {
        const fileInput = document.getElementById('document-files');
        
        if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
            window.AcadefyApp.showToast('Please select files to upload', 'error');
            return;
        }
        
        const files = Array.from(fileInput.files);
        const uploadBtn = document.getElementById('upload-files-btn');
        
        try {
            // Disable upload button
            if (uploadBtn) {
                uploadBtn.disabled = true;
                uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Uploading...';
            }
            
            window.AcadefyApp.showToast(`Uploading ${files.length} file(s)...`, 'info', 2000);
            
            const results = [];
            
            // Upload files one by one
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                
                try {
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('title', file.name);
                    
                    console.log('Uploading file:', file.name);
                    console.log('FormData contents:', Array.from(formData.entries()));
                    
                    const response = await fetch('/api/upload-direct', {
                        method: 'POST',
                        body: formData
                    });
                    
                    console.log('Response status:', response.status);
                    console.log('Response headers:', response.headers);
                    
                    const result = await response.json();
                    console.log('Upload result:', result);
                    results.push({ file: file.name, success: result.success, error: result.error });
                    
                    // Update progress
                    window.AcadefyApp.showToast(`Uploaded ${i + 1}/${files.length}: ${file.name}`, 'info', 1000);
                    
                } catch (error) {
                    results.push({ file: file.name, success: false, error: error.message });
                }
            }
            
            // Show final results
            const successful = results.filter(r => r.success).length;
            const failed = results.filter(r => !r.success).length;
            
            if (successful > 0) {
                window.AcadefyApp.showToast(`Successfully uploaded ${successful} file(s)!`, 'success');
                
                // Clear file input and display
                fileInput.value = '';
                this.displaySelectedFiles([]);
                this.loadDocuments();
            }
            
            if (failed > 0) {
                const failedFiles = results.filter(r => !r.success).map(r => r.file).join(', ');
                window.AcadefyApp.showToast(`Failed to upload: ${failedFiles}`, 'error');
            }
            
        } catch (error) {
            console.error('Error uploading files:', error);
            window.AcadefyApp.showToast('Failed to upload files', 'error');
        } finally {
            // Re-enable upload button
            if (uploadBtn) {
                uploadBtn.disabled = false;
                uploadBtn.innerHTML = '<i class="fas fa-upload"></i> Upload Selected Files';
            }
        }
    }

    async addDocumentFromText() {
        const textInput = document.getElementById('document-text');
        const titleInput = document.getElementById('text-title');
        
        if (!textInput || !textInput.value.trim()) {
            window.AcadefyApp.showToast('Please enter some text content', 'error');
            return;
        }
        
        if (!titleInput || !titleInput.value.trim()) {
            window.AcadefyApp.showToast('Please enter a document title', 'error');
            return;
        }
        
        const content = textInput.value.trim();
        const title = titleInput.value.trim();
        
        try {
            window.AcadefyApp.showToast('Adding document...', 'info', 1000);
            
            const response = await window.AcadefyApp.apiRequest('/documents/add-text', {
                method: 'POST',
                body: JSON.stringify({ content, title })
            });
            
            if (response.success) {
                window.AcadefyApp.showToast('Document added successfully!', 'success');
                textInput.value = '';
                titleInput.value = '';
                this.loadDocuments();
            } else {
                window.AcadefyApp.showToast(response.data.error || 'Failed to add document', 'error');
            }
        } catch (error) {
            console.error('Error adding document:', error);
            window.AcadefyApp.showToast('Failed to add document', 'error');
        }
    }
    
    async removeDocument(docId) {
        this.showConfirmationModal(
            'Remove Document',
            'Are you sure you want to remove this document from the knowledge base?',
            async () => {
                try {
                    const response = await window.AcadefyApp.apiRequest(`/documents/${docId}`, {
                        method: 'DELETE'
                    });
                    
                    if (response.success) {
                        window.AcadefyApp.showToast('Document removed successfully', 'success');
                        this.loadDocuments();
                    } else {
                        window.AcadefyApp.showToast('Failed to remove document', 'error');
                    }
                } catch (error) {
                    console.error('Error removing document:', error);
                    window.AcadefyApp.showToast('Failed to remove document', 'error');
                }
            }
        );
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

window.addDocumentFromUrl = function() {
    if (window.profileInstance) {
        window.profileInstance.addDocumentFromUrl();
    }
};

window.addDocumentFromFiles = function() {
    if (window.profileInstance) {
        window.profileInstance.addDocumentFromFiles();
    }
};

window.addDocumentFromText = function() {
    if (window.profileInstance) {
        window.profileInstance.addDocumentFromText();
    }
};

// Initialize profile when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.profile-page')) {
        window.profileInstance = new AcadefyProfile();
    }
});