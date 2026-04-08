document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const removeBtn = document.getElementById('remove-btn');
    const submitBtn = document.getElementById('submit-btn');
    const uploadForm = document.getElementById('upload-form');
    
    const resultContent = document.getElementById('result-content');
    const errorMessage = document.getElementById('error-message');
    const resultAge = document.getElementById('result-age');
    
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');

    let currentFile = null;

    // Handle Drag and Drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('dragover');
    }

    function unhighlight() {
        dropZone.classList.remove('dragover');
    }

    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    // Handle Click to Upload
    dropZone.addEventListener('click', (e) => {
        if(e.target !== removeBtn) {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length === 0) return;
        
        const file = files[0];
        if (!file.type.startsWith('image/')) {
            showError('Please upload an image file (JPEG, PNG).');
            return;
        }

        currentFile = file;
        
        // Show preview
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function() {
            imagePreview.src = reader.result;
            previewContainer.classList.remove('hidden');
            submitBtn.disabled = false;
            hideResult();
        };
    }

    removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        currentFile = null;
        fileInput.value = '';
        previewContainer.classList.add('hidden');
        imagePreview.src = '#';
        submitBtn.disabled = true;
        hideResult();
    });

    // Handle Form Submit
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!currentFile) return;

        setLoading(true);
        hideResult();

        const formData = new FormData();
        formData.append('file', currentFile);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            // Trying to parse JSON response.
            let data;
            try {
                data = await response.json();
            } catch (err) {
                // If it isn't JSON, throw generic error.
                throw new Error('Server returned an invalid response.');
            }

            if (!response.ok) {
                throw new Error(data.detail || data.error || 'Server error occurred');
            }

            showResult(data.age_bracket);
        } catch (error) {
            showError(error.message);
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        if (isLoading) {
            btnText.classList.add('hidden');
            loader.classList.remove('hidden');
        } else {
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    }

    function showResult(age) {
        resultAge.textContent = age;
        resultContent.classList.remove('hidden');
        errorMessage.classList.add('hidden');
    }

    function showError(msg) {
        errorMessage.textContent = msg || 'An error occurred. Please try again.';
        errorMessage.classList.remove('hidden');
        resultContent.classList.add('hidden');
    }

    function hideResult() {
        resultContent.classList.add('hidden');
        errorMessage.classList.add('hidden');
    }
});
