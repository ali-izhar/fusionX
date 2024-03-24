// ----------------------------------------------------------------------------------- //
// ---------------------- Utility Functions for Image Handling ----------------------- //
// ----------------------------------------------------------------------------------- //
function triggerFileInput(id) {
    document.getElementById(id).click();
}

function dragOverEvent(event) {
    event.preventDefault();
    event.stopPropagation();
    event.target.closest('.drop-zone').style.backgroundColor = '#f0f0f0';
}

function dragLeaveEvent(event) {
    event.preventDefault();
    event.stopPropagation();
    event.target.closest('.drop-zone').style.backgroundColor = '';
}

function dropEvent(event, imgId, placeholderId) {
    event.preventDefault();
    event.stopPropagation();
    const dropZone = event.target.closest('.drop-zone');
    dropZone.style.backgroundColor = '';
    const files = event.dataTransfer.files;
    if (files.length) {
        previewImage({ target: { files: files } }, imgId, placeholderId);
    }
}

function previewImage(event, imgId, placeholderId) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById(imgId).src = e.target.result;
            document.getElementById(placeholderId).style.display = 'none';
            checkBothImagesLoaded();
        };
        reader.readAsDataURL(file);
    }
}

function selectStyleImage(imageUrl) {
    localStorage.setItem('selectedStyleImage', imageUrl);
    window.location.href = '/studio';
}

function checkBothImagesLoaded() {
    const contentImage = document.getElementById('contentImage').src;
    const styleImage = document.getElementById('styleImage').src;
    if (contentImage && styleImage && contentImage.length > 0 && styleImage.length > 0) {
        document.getElementById('mergeBlock').style.display = 'block';
    } else {
        document.getElementById('mergeBlock').style.display = 'none';
    }
}


// ----------------------------------------------------------------------------------- //
// ------------------------- Event Listeners for Drag and Drop ----------------------- //
// ----------------------------------------------------------------------------------- //
function setupDragAndDropListeners() {
    document.querySelectorAll('.drop-zone').forEach(dropZone => {
        dropZone.addEventListener('dragover', dragOverEvent);
        dropZone.addEventListener('dragleave', dragLeaveEvent);
        dropZone.addEventListener('drop', function(event) {
            let imgId = this.querySelector('img').id;
            let placeholderId = this.querySelector('p').id;
            dropEvent(event, imgId, placeholderId);
        });
    });
}


// ----------------------------------------------------------------------------------- //
// ------------------------------ Function to Merge Images --------------------------- //
// ----------------------------------------------------------------------------------- //
function mergeImages() {
    event.preventDefault(); // Assuming 'event' is passed to this function
    document.getElementById('loader-overlay').style.display = 'block';

    // Collect Image URLs and Settings
    const contentImage = document.getElementById('contentImage').src;
    const styleImage = document.getElementById('styleImage').src;
    const settings = gatherSettings();

    fetch('/studio/merge', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ contentImage, styleImage, settings })
    })
    .then(response => response.json())
    .then(handleMergeResponse)
    .catch(handleMergeError);
}

function gatherSettings() {
    return {
        nstIterations: document.getElementById('nstIterations').value,
        nstContentWeight: document.getElementById('nstContentWeight').value,
        nstStyleWeight: document.getElementById('nstStyleWeight').value,
        nstTotalVariationWeight: document.getElementById('nstTotalVariationWeight').value,
        nstImageHeight: document.getElementById('nstImageHeight').value,
        outputFileName: document.getElementById('outputFileName').value,
        outputImageFormat: document.getElementById('outputImageFormat').value
    };
}

function handleMergeResponse(data) {
    document.getElementById('loader-overlay').style.display = 'none';
    localStorage.setItem('resultImage', data.result);
    window.location.href = '/studio/result';
}

function handleMergeError(error) {
    console.error('Error:', error);
    document.getElementById('loader-overlay').style.display = 'none';
}


// ----------------------------------------------------------------------------------- //
// -------------------- DOMContentLoaded Listener for Initial Setup ------------------ //
// ----------------------------------------------------------------------------------- //
document.addEventListener('DOMContentLoaded', function() {
    setupDragAndDropListeners();

    // Restore selected style image from localStorage
    const selectedImage = localStorage.getItem('selectedStyleImage');
    if (selectedImage) {
        document.getElementById('styleImage').src = selectedImage;
        localStorage.removeItem('selectedStyleImage');
        document.getElementById('stylePlaceholder').style.display = 'none';
    }

    // Event Listeners for Generate Buttons
    document.getElementById('generate-btn-content').addEventListener('click', function(event) {
        generateImage(event, 'prompt-content', 'contentImage', 'contentPlaceholder');
    });
    
    document.getElementById('generate-btn-style').addEventListener('click', function(event) {
        generateImage(event, 'prompt-style', 'styleImage', 'stylePlaceholder');
    });

    // Setup for the merge button, if it exists
    const mergeButton = document.getElementById('merge-btn');
    if (mergeButton) {
        mergeButton.addEventListener('click', mergeImages);
    }

   // Initial check to display the merge button if both images are already loaded
    checkBothImagesLoaded();

    // Setup model selection popup interactions
    handleModelSelectionPopup();
});

// Handling Image Generation Request
function generateImage(event, promptId, imageId, placeholderId) {
    event.preventDefault(); // Prevent form submission

    const prompt = document.getElementById(promptId).value;
    if (prompt.length < 10 || prompt.length > 200) {
        alert("Prompt must be between 10 and 200 characters.");
        return;
    }
    
    const modelInput = document.getElementById('model_input').value;
    const data = {
        prompt: prompt,
        model: modelInput,
    };
    
    document.getElementById('loader-overlay').style.display = 'block';
    fetch('/studio/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.result) {
            document.getElementById(imageId).src = data.result;
            document.getElementById(placeholderId).style.display = 'none';
            checkBothImagesLoaded();
        } else {
            alert("Failed to generate image.");
        }
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        document.getElementById('loader-overlay').style.display = 'none';
    });
}

// Model Selection Popup Handling
function handleModelSelectionPopup() {
    const modelModal = document.getElementById('modelModal');
    const modelButtons = document.querySelectorAll('.model-item');

    modelButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            const modelName = button.dataset.model;
            updateModelName(modelName);
        });
    });
    
    function updateModelName(modelName) {
        const titleCaseModelName = modelName.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        const modelButtonText = document.getElementById('modelButtonText');
        modelButtonText.textContent = titleCaseModelName;
        const modelInput = document.getElementById('model_input');
        modelInput.value = modelName;
        const modelModal = new bootstrap.Modal(document.getElementById('modelModal'));
        modelModal.hide();
    }
}

// Ensuring the cleanup and display logic after images are generated or merged
document.addEventListener('DOMContentLoaded', () => {
    const resultImageData = localStorage.getItem('resultImage');
    if (resultImageData) {
        const imageElement = document.getElementById('mergedImage');
        imageElement.src = resultImageData;
        imageElement.style.display = 'block'; // Show the image
    } else {
        console.error('No result image data found in localStorage.');
        // Handle the case where there is no image data. Maybe display a message?
    }
    // Clear the data from localStorage
    localStorage.removeItem('resultImage');
});


document.addEventListener('DOMContentLoaded', function() {
    const selectedImage = localStorage.getItem('selectedStyleImage');
    if (selectedImage) {
        // Set the image source
        document.getElementById('styleImage').src = selectedImage;
        // Optionally, clear the selected image from storage
        localStorage.removeItem('selectedStyleImage');
        // Hide the placeholder
        document.getElementById('stylePlaceholder').style.display = 'none';
    }
});
