import React from 'react';
import VideoRecorder from 'react-video-recorder'
import AudioRec from './AudioRec';


function VideoRec(props) {

  const [isRecVideo, setIsRecVideo] = React.useState(false);

  const submitVideo = (videoFile) => {
    // console.log(videoFile)
    // console.log(props.testName)
    const formData = new FormData();
		formData.append('file', videoFile);
    formData.append('testName', props.testName);
    console.log(formData.get('testName'), formData.get('file'))
    fetch('http://localhost:5000/video-upload', {
      method: 'POST',
      headers: {
        //'content-type': 'multipart/form-data',
        'Authorization': localStorage.getItem('token')
      },
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
      <h2>{props.testName}</h2>
      <AudioRec testName = {props.testName} isRecVideo={isRecVideo}/>
      <VideoRecorder 
        isFlipped={false}
        countdownTime={0}
        mimeType="video/webm;codecs=vp8,opus"
        onStartRecording={() => {
          // call API for question
          setIsRecVideo(true);
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
          setIsRecVideo(false);      
        }}
      />  
    </div>
  );
}

export default VideoRec;