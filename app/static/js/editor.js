const NUM_REVERTS = 4;
const history = [];
let cropper;

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.editor-options button:not(#revertButton):not(#enhanceButton)').forEach(button => {
        button.addEventListener('click', (event) => {
            const id = event.target.id;

            if (event.target.classList.contains("data-active")) {
                restoreButtons();
                event.target.classList.remove("data-active");
                if (id === "cropZoomButton") {
                    cleanupCropper();
                    event.target.textContent = "Crop Image";  // Set text to 'Crop Image'
                }
            } else {
                hideButtons(id);
                event.target.classList.add("data-active");
                if (id === "cropZoomButton") {
                    openCropper();
                    event.target.textContent = "Apply Crop";  // Set text to 'Apply Crop'
                }
            }
        });
    });
});

const restoreButtons = () => {
    document.querySelectorAll('.editor-options button:not(#revertButton)').forEach(button => {
        button.disabled = false;
        if (button.id === "cropZoomButton") {
            button.textContent = "Crop Image";  // Reset text to 'Crop Image' when buttons are restored
        }
    });
}

const hideButtons = (exception) => {
    document.querySelectorAll(`.editor-options button:not(#${exception})`).forEach(button => button.disabled = true);
}

const saveCurrentState = () => {
    if (history.length >= NUM_REVERTS) history.shift();
    history.push(document.getElementById('mergedImage').src);
    document.getElementById('revertButton').disabled = false;
}

const revertImage = () => {
    if (history.length) {
        document.getElementById('mergedImage').src = history.pop();
        document.getElementById('revertButton').disabled = history.length === 0;
    } else {
        console.log("No more edits to revert");
    }
}

const enhanceImage = () => {
    document.getElementById('loader-overlay').style.display = 'block';
    saveCurrentState();
    const input_image = document.getElementById('mergedImage').src;

    fetch('/studio/enhance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input_image })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('mergedImage').src = data.result;
        document.getElementById('loader-overlay').style.display = 'none';
    })
    .catch(error => console.error('Error:', error));
}

const openCropper = () => {
    const image = document.getElementById('mergedImage');
    cropper = new Cropper(image, {
        crop(event) {
            document.getElementById('cropWidth').value = "width: " + event.detail.width.toFixed(2) + " px";
            document.getElementById('cropHeight').value = "height: " + event.detail.height.toFixed(2) + " px";
        },
    });

    document.querySelector('.cropMenu').style.display = "block";
    const confirmButton = document.getElementById('confirmButton');
    confirmButton.textContent = "Apply Crop";  // Change button text to 'Apply Crop'
    confirmButton.onclick = applyCrop;
}

const applyCrop = () => {
    if (cropper) {
        saveCurrentState();
        document.getElementById('mergedImage').src = cropper.getCroppedCanvas().toDataURL();
        restoreButtons();
        cleanupCropper();
    }
}

const cleanupCropper = () => {
    if (cropper) {
        cropper.destroy();
        cropper = null;
    }

    document.querySelector('.cropMenu').style.display = "none";
    const confirmButton = document.getElementById('confirmButton');
    confirmButton.textContent = "Download";  // Change button text to 'Download'
    confirmButton.onclick = saveImage;
}

const saveImage = () => {
    const link = document.createElement('a');
    link.href = document.getElementById('mergedImage').src;
    link.download = 'fusionX_output.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
