import React from 'react';
import VideoRecorder from 'react-video-recorder'

function VideoRec() {

  return (
    <div style={{ width: "100%", maxWidth: 1000, height: 500 , margin: "auto"}}>
      <h1 style={{textAlign: 'center'}}>Test Window</h1>
      <VideoRecorder 
        isFlipped={false}
        countdownTime={0}
        mimeType="video/webm;codecs=vp8,opus"
        onStartRecording={() => console.log('started recording')}
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
          // Do something with the video...
          console.log('videoBlob', videoBlob)
        }}
      />
    </div>
  );
}

export default VideoRec;