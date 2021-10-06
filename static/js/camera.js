
var video = document.getElementById('video');

// Get access to the camera!
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function (stream) {
        //video.src = window.URL.createObjectURL(stream);
        video.srcObject = stream;
        video.play();
        var ele = document.getElementById("camera-msg");
        ele.setAttribute("style", "border:solid 0px;");
        // document.getElementById("camera-msg").disabled = true;
    })
  .catch(function(err) {
    console.log("camera not showed");
    var body = document.getElementById("exam-wrap");
    // $("#exam-wrap").attr('disabled','disabled');

    body.setAttribute("style", "background: rgba(200,200,200,0.5); display: none;");
    // alert("Please allow camera access and refresh page to start exam");
    document.getElementById("camera-msg").innerHTML="Please allow camera access and refresh page to start exam";
    // body.css(styles);
    // console.log(error)
  });
}