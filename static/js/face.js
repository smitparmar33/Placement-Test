var video = document.getElementById("video");
let model;
let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
const setupcamera = () => {
    navigator.mediaDevices.getUserMedia({
        video: {width: 600, height: 400},
        audio: false,
    }).then(stream => {
        video.srcObject = stream;
    });
};

const detectFaces = async () => {
    const prediction = await model.estimateFaces(video, false);
    if (prediction["length"]!=0){
        document.getElementById("detect").innerHTML= "";
    }
    else{
        document.getElementById("detect").innerHTML= "Face is not visible";
    }
    ctx.drawImage(video, 0, 0, 600, 400);
    prediction.forEach((pred) => {
        
        ctx.beginPath();
        ctx.lineWidth = "8";
        ctx.strokeStyle = "blue";
        ctx.rect(
            pred.topLeft[0],
            pred.topLeft[1],
            pred.bottomRight[0] - pred.topLeft[0],
            pred.bottomRight[1] - pred.topLeft[1]
        );
        ctx.stroke();
    });
};

setupcamera();
video.addEventListener('loadeddata', async () => {
    model = await blazeface.load();
    setInterval(detectFaces, 100);
});
