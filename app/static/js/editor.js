const NUM_REVERTS = 4;
const history = [];

let cropper;



// toggle
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.editor-options button');

    buttons.forEach(button => {
        if(button.id !== "revertButton" && button.id !== "enhanceButton"){
            button.addEventListener('click', function () {
                let pressedButton = event.target;
                let id = pressedButton.id;

                // close menu & re-enable other buttons
                if (pressedButton.classList.contains("data-active")) {
                    restoreButtons();

                    pressedButton.classList.remove("data-active");

                    if (id === "cropZoomButton"){
                        cleanupCropper();
                    }
                    else if (id === "colorToneButton"){

                    }
                    else if (id === "filterButton"){

                    }
                } else {

                    hideButtons(id);

                    pressedButton.classList.add("data-active");

                    if (id === "cropZoomButton"){
                        openCropper();
                    }
                    else if (id === "colorToneButton"){

                    }
                    else if (id === "filterButton"){

                    }
                }
            });
        }
    });
});

function restoreButtons(){
    document.querySelectorAll('.editor-options button').forEach(button => {
        if (button.id !== "revertButton")
        button.disabled = false;
    });
}

function hideButtons(exception){
    document.querySelectorAll('.editor-options button').forEach(button => {
        if (button.id !== exception)
            button.disabled = true;
    });
}
/* state of the image stack */
function saveCurrentState() {
    if (history.length >= NUM_REVERTS)
        history.shift();
    history.push(document.getElementById('mergedImage').src);
    document.getElementById('revertButton').disabled = false;

}
function revertImage() {

    if (history.length > 0)
        document.getElementById('mergedImage').src = history.pop();
        if(history.length === 0)
            document.getElementById('revertButton').disabled = true;
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
        alert("done");
    }).catch(error => {
        console.error('Error:', error);
    });
}

/* cropper */

function cleanupCropper(){
    if(cropper) {
        cropper.destroy();
        cropper = null;
    }

    document.querySelector('.cropMenu').style.display = "none";
}

function openCropper() {
    const button = document.getElementById("cropZoomButton");
    const cropMenu = document.querySelector('.cropMenu');


    const image = document.getElementById('mergedImage');

    cropper = new Cropper(image, {
        crop(event) {
            document.getElementById('cropWidth').value = "width: " + event.detail.width.toFixed(2) + " px";
            document.getElementById('cropHeight').value = "height: " + event.detail.height.toFixed(2) + " px";
            },
    });

    cropMenu.style.display = "block";
}

function applyCrop() {
    if (cropper) {

        saveCurrentState();

        document.getElementById('mergedImage').src = cropper.getCroppedCanvas().toDataURL();


        restoreButtons();

        cleanupCropper();
        document.getElementById("cropZoomButton").classList.remove("data-active");

    }
}