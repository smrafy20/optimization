/**
 * PDF Text Extractor - Main JavaScript
 * Handles additional UI interactions and animations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check for browser compatibility with File API
    if (window.File && window.FileReader && window.FileList && window.Blob) {
        console.log('File API is fully supported in this browser');
    } else {
        console.warn('The File APIs are not fully supported in this browser.');
    }

    // Add animation to the header
    const header = document.querySelector('.card-header');
    if (header) {
        header.classList.add('animate__animated', 'animate__fadeIn');
    }

    // Get DOM elements
    const form = document.getElementById('pdf-form');
    const processingOverlay = document.getElementById('processing-overlay');
    const processingStatus = document.getElementById('processing-status');
    const statusMessage = document.getElementById('status-message');
    const successAnimation = document.getElementById('success-animation');
    const flashMessages = document.getElementById('flash-messages');
    const docxFormatContainer = document.getElementById('docx_format_container');
    const formatHelpText = document.getElementById('format_help_text');
    const processingMethods = document.querySelectorAll('input[name="processing_method"]');
    
    // Show DOCX option for all methods
    if (docxFormatContainer) docxFormatContainer.style.display = 'inline-block';
    if (formatHelpText) formatHelpText.textContent = 'Choose between TXT or DOCX output formats';
    
    // Hide flash messages if we're returning from download page
    if (flashMessages && (localStorage.getItem('suppressFlashMessages') === 'true' || localStorage.getItem('downloadInitiated') === 'true')) {
        flashMessages.style.display = 'none';
        localStorage.removeItem('suppressFlashMessages');
    }
    
    // Track processing time
    let processingStartTime = 0;
    
    // Check if we're in the middle of processing
    const isProcessing = localStorage.getItem('pdfProcessing') === 'true';
    const downloadInitiated = localStorage.getItem('downloadInitiated') === 'true';
    
    // Handle form submission
    if (form) {
        form.addEventListener('submit', function() {
            processingStartTime = Date.now();
            // Store start time in localStorage to track processing duration
            localStorage.setItem('processingStartTime', processingStartTime);
            localStorage.setItem('pdfProcessing', 'true');
            localStorage.setItem('downloadInitiated', 'false');
            
            // Set a flag to show success animation when complete
            localStorage.setItem('showSuccessAnimation', 'true');
        });
    }
    
    // Listen for the beforeunload event to detect when download dialog appears
    window.addEventListener('beforeunload', function(e) {
        // If we're processing and not yet downloaded, this might be the download dialog
        if (isProcessing && !downloadInitiated) {
            // Mark that download was initiated
            localStorage.setItem('downloadInitiated', 'true');
            
            // Show success animation
            if (processingOverlay) {
                const spinner = processingOverlay.querySelector('.spinner-border');
                if (spinner) spinner.style.display = 'none';
                
                if (successAnimation) successAnimation.style.display = 'block';
                if (processingStatus) processingStatus.textContent = 'Complete Conversion!';
            }
            
            // Don't actually trigger the beforeunload dialog
            delete e.returnValue;
        }
    });
    
    // Function to show download complete
    function showDownloadComplete() {
        if (processingOverlay) {
            processingOverlay.style.display = 'none';
        }
        
        // Hide any flash messages - they're redundant with our success message
        if (flashMessages) {
            flashMessages.style.display = 'none';
        }
        
        // Show success message
        showStatus('Complete Conversion! Your file has been successfully processed and downloaded.', 'success');
        
        // Calculate and display processing time
        if (localStorage.getItem('processingStartTime')) {
            const startTime = parseInt(localStorage.getItem('processingStartTime'));
            const endTime = Date.now();
            const duration = Math.round((endTime - startTime) / 1000); // in seconds
            
            // Display processing time
            if (statusMessage) {
                const timeMessage = document.createElement('div');
                timeMessage.className = 'mt-2 small text-muted';
                timeMessage.textContent = `Processing completed in ${duration} seconds`;
                statusMessage.appendChild(timeMessage);
                
                // Add animation to the status message
                statusMessage.classList.add('animate__animated', 'animate__bounceIn');
            }
        }
        
        // Clear all processing flags
        localStorage.removeItem('pdfProcessing');
        localStorage.removeItem('downloadInitiated');
        localStorage.removeItem('processingStartTime');
        localStorage.removeItem('showSuccessAnimation');
    }
    
    // If the page is reloaded after a download, show completion
    if (downloadInitiated) {
        showDownloadComplete();
    }
    
    // Detect if we're on the download page
    const isDownloadPage = window.location.pathname.includes('/download/');
    if (isDownloadPage) {
        // Store that download was initiated
        localStorage.setItem('downloadInitiated', 'true');
        
        // Add a listener for when the download completes
        setTimeout(function() {
            // After a short delay, redirect back to the home page
            window.location.href = '/';
        }, 1000);
    }
    
    // Show status message
    function showStatus(message, type) {
        if (!statusMessage) return;
        
        statusMessage.textContent = message;
        statusMessage.className = 'status-message mb-4 alert alert-' + type;
        statusMessage.style.display = 'block';
        
        // Auto-hide after 5 seconds for success messages
        if (type === 'success') {
            setTimeout(() => {
                statusMessage.style.display = 'none';
            }, 5000);
        }
    }
    
    // Add drag-and-drop highlighting effects to all processing options
    const processingOptions = document.querySelectorAll('.processing-option');
    processingOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove active class from all options
            processingOptions.forEach(opt => opt.classList.remove('processing-active'));
            // Add active class to clicked option
            this.classList.add('processing-active');
        });
    });
}); 