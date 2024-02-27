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
        reader.onload = function(e) {
            document.getElementById(imgId).src = e.target.result;
            document.getElementById(placeholderId).style.display = 'none';
            checkBothImagesLoaded();
        };
        reader.readAsDataURL(file);
    }
}

function checkBothImagesLoaded() {
    const contentImage = document.getElementById('contentImage').src;
    const styleImage = document.getElementById('styleImage').src;

    // Check if both images are not just placeholders anymore
    if (contentImage && styleImage && contentImage.length > 0 && styleImage.length > 0) {
        document.getElementById('mergeButton').style.display = 'block';
    } else {
        document.getElementById('mergeButton').style.display = 'none';
    }
}

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
    const contentImage = document.getElementById('contentImage').src;
    const styleImage = document.getElementById('styleImage').src;

    fetch('/studio/merge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ contentImage, styleImage })
    })
    .then(response => response.json())
    .then(data => {
        // The src attribute of the img tag can handle base64 encoded images
        document.getElementById('resultImage').src = data.result;
        document.getElementById('resultImage').style.display = 'block';
    }).catch(error => {
        console.error('Error:', error);
    });
}
