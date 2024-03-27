const NUM_REVERTS = 4;
const history = [];

let cropper;

/* state of the image stack */
function saveCurrentState() {
    if (history.length >= NUM_REVERTS)
        history.shift();
    history.push(document.getElementById('mergedImage').src);
}
function revertImage() {

    if (history.length > 0)
        document.getElementById('mergedImage').src = history.pop();
    else
        console.log("No more edits to revert");
}

function enhanceImage() {

    saveCurrentState();

    const input_image = document.getElementById('mergedImage').src;

    fetch('/studio/enhance', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input_image })
    })
    .then(response => response.json())
    .then(data => {
        // The src attribute of the img tag can handle base64 encoded images
        document.getElementById('mergedImage').src = data.result;
    }).catch(error => {
        console.error('Error:', error);
    });
}

/* cropper */
function restoreButtons(){
        document.getElementById("revertButton").disabled = false
        document.getElementById("enhanceButton").disabled = false;
        document.getElementById("brightnessButton").disabled = false;
        document.getElementById("contrastButton").disabled = false;
        document.getElementById("saturationButton").disabled = false;
        document.getElementById("filterButton").disabled = false;
}
function cleanupCropper(cropMenu, button){
    if(cropper) {
        cropper.destroy();
        cropper = null;
    }

    restoreButtons();

    cropMenu.style.display = "none";
    button.innerText = "Open Crop / Zoom";
    button.setAttribute("data-toggle", "0");

}

function toggleCropMenu() {
    const button = document.getElementById("cropZoomButton");
    const cropMenu = document.querySelector('.cropMenu');

    if (button.getAttribute("data-toggle") === "0"){

        const image = document.getElementById('mergedImage');

        cropper = new Cropper(image, {
            crop(event) {
                document.getElementById('cropWidth').value = event.detail.width.toFixed(2);
                document.getElementById('cropHeight').value = event.detail.height.toFixed(2);
            },
        });

        document.getElementById("revertButton").disabled = true;
        document.getElementById("enhanceButton").disabled = true;
        document.getElementById("brightnessButton").disabled = true;
        document.getElementById("contrastButton").disabled = true;
        document.getElementById("saturationButton").disabled = true;
        document.getElementById("filterButton").disabled = true;



        // toggle set text boxes visible
        cropMenu.style.display = "block";
        button.innerText = "Close Crop / Zoom";
        button.setAttribute("data-toggle", "1");

    }
    else {
        cleanupCropper(cropMenu, button);
    }
}

function applyCrop() {
    if (cropper) {

        saveCurrentState();

        document.getElementById('mergedImage').src = cropper.getCroppedCanvas().toDataURL();

        const cropMenu = document.querySelector('.cropMenu'),
            button = document.getElementById("cropZoomButton");

        cleanupCropper(cropMenu, button);
    }
}
