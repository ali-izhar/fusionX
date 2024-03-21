// Select a content image from the gallery
function triggerFileInput(id) {
    document.getElementById(id).click();
}

// Handle the drag over event
function dragOverEvent(event) {
    event.preventDefault();
    event.stopPropagation();
    event.target.closest('.drop-zone').style.backgroundColor = '#f0f0f0';
}

// Handle the drag leave event
function dragLeaveEvent(event) {
    event.preventDefault();
    event.stopPropagation();
    event.target.closest('.drop-zone').style.backgroundColor = '';
}

// Handle the drop event
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

// Preview the selected image
function previewImage(event, imgId, placeholderId) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById(imgId).src = e.target.result;
            document.getElementById(placeholderId).style.display = 'none';
            checkBothImagesLoaded();
        };
        reader.readAsDataURL(file);
    }
}

// Select a style image from the gallery
function selectStyleImage(imageUrl) {
    // Store the image URL in localStorage or pass as query parameter
    localStorage.setItem('selectedStyleImage', imageUrl);
    // Redirect to the studio page
    window.location.href = '/studio';
}
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

// Check if both images are loaded
function checkBothImagesLoaded() {
    const contentImage = document.getElementById('contentImage').src;
    const styleImage = document.getElementById('styleImage').src;

    // Check if both images are not just placeholders anymore
    if (contentImage && styleImage && contentImage.length > 0 && styleImage.length > 0) {
        document.getElementById('mergeBlock').style.display = 'block';
    } else {
        document.getElementById('mergeBlock').style.display = 'none';
    }
}

// Add event listeners for drag and drop
document.querySelectorAll('.drop-zone').forEach(dropZone => {
    dropZone.addEventListener('dragover', dragOverEvent);
    dropZone.addEventListener('dragleave', dragLeaveEvent);
    dropZone.addEventListener('drop', function(event) {
        let imgId = this.querySelector('img').id;
        let placeholderId = this.querySelector('p').id;
        dropEvent(event, imgId, placeholderId);
    });
});

function mergeImages() {
    // Prevent the form from submitting if called on form submission
    event.preventDefault();

    // Display a loading indicator
    document.getElementById('loader-overlay').style.display = 'block';

    const contentImage = document.getElementById('contentImage').src;
    const styleImage = document.getElementById('styleImage').src;

    // Retrieve the values from the settings form inputs
    const nstIterations = document.getElementById('nstIterations').value;
    const nstContentWeight = document.getElementById('nstContentWeight').value;
    const nstStyleWeight = document.getElementById('nstStyleWeight').value;
    const nstTotalVariationWeight = document.getElementById('nstTotalVariationWeight').value;
    const nstImageHeight = document.getElementById('nstImageHeight').value;
    const outputFileName = document.getElementById('outputFileName').value;
    const outputImageFormat = document.getElementById('outputImageFormat').value;

    // Construct the settings object
    const settings = {
        nstIterations,
        nstContentWeight,
        nstStyleWeight,
        nstTotalVariationWeight,
        nstImageHeight,
        outputFileName,
        outputImageFormat
    };

    // Include the settings in the fetch request
    fetch('/studio/merge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ contentImage, styleImage, settings }) // Include settings in the payload
    })
    .then(response => response.json())
    .then(data => {
        // Hide loading indicator
        document.getElementById('loader-overlay').style.display = 'none';

        // Use LocalStorage or another method to pass the image to result.html
        localStorage.setItem('resultImage', data.result);

        // Navigate to result.html
        window.location.href = '/studio/result';
    })
    .catch(error => {
        console.error('Error:', error);
        // Hide loading indicator and possibly show an error message
        document.getElementById('loader-overlay').style.display = 'none';
    });
}



// Display the result image
document.addEventListener('DOMContentLoaded', (event) => {
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


window.onload = function() {
    // Retrieve the image data from LocalStorage
    const resultImage = localStorage.getItem('resultImage');
    if (resultImage) {
        document.getElementById('resultImage').src = resultImage;
        document.getElementById('resultImage').style.display = 'block';

        // Optionally, clear the image data from LocalStorage after displaying it
        localStorage.removeItem('resultImage');
    }
};