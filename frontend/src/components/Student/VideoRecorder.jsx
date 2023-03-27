import React, { useState } from 'react';
import { ReactMediaRecorder } from 'react-media-recorder';

function VideoRecorder() {
  const [isRecording, setIsRecording] = useState(false);

  function handleStart() {
    setIsRecording(true);
  }

  function handleStop() {
    setIsRecording(false);
  }

  function handleOnData(recordedBlob) {
    // Do something with the recorded video blob
    console.log('Recorded Blob:', recordedBlob);
  }

  return (
    <div>
      <ReactMediaRecorder
        video
        render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
          <div>
            <video src={mediaBlobUrl} autoPlay />
            {status === 'recording' && <p>Recording...</p>}
            {status === 'stopped' && (
              <button onClick={startRecording}>Start Recording</button>
            )}
            {status === 'recording' && (
              <button onClick={stopRecording}>Stop Recording</button>
            )}
          </div>
        )}
        onStart={handleStart}
        onStop={handleStop}
        onData={handleOnData}
      />
    </div>
  );
}

export default VideoRecorder;
