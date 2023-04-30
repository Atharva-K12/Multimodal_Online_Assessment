import React from 'react';
import VideoRecorder from 'react-video-recorder'
import AudioRec from './AudioRec';


function VideoRec() {

  const submitVideo = (videoFile) => {
    const formData = new FormData();
		formData.append('file', videoFile);
    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .then((data) => {
      console.log('Success:', data);
      })
    .catch(error => console.error('Error:', error))
  }

  return (
    <div style={{ width: "100%", maxWidth: 1000, height: 500 , margin: "auto"}}>
      <h1 style={{textAlign: 'center'}}>Test Window</h1>
      <AudioRec/>
      <VideoRecorder 
        isFlipped={false}
        countdownTime={0}
        mimeType="video/webm;codecs=vp8,opus"
        onStartRecording={() => {
          // call API for question
          console.log('started recording')
        }}
        constraints={{
          audio: true,
          video: {
            width: { exact: 500, ideal: 480 },
            height: { exact: 500, ideal: 640 },
            aspectRatio: { exact: 0.7500000001, ideal: 0.7500000001 },
            resizeMode: "crop-and-scale"
          }
        }}
        
        onRecordingComplete={(videoBlob) => {
          const videoFile = new File([videoBlob], "video.mp4", {
            type: "video/mp4"
          });
          submitVideo(videoFile);        
        }}
      />  
    </div>
  );
}

export default VideoRec;