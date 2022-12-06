import React from "react";
import VideoRecorder from "react-video-recorder";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Redirect,
  Link
} from "react-router-dom";
import "./styles.css";
import Score from "./Score";

const FromVideoRecorder = ({ push, setQuestion }) => {

  const submitForm = (videoFile) => {
    const formData = new FormData();
		formData.append('file', videoFile);
    fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData
    })
    .then(response => response.json())
    .catch(error => console.error('Error:', error))
  }

  const getQuestion = () => {
    fetch('http://127.0.0.1:5000/get-question')
    .then(response => response.json())
    .then(data => setQuestion(data))
    .catch(error => console.error('Error:', error))
  }

  return (
    <VideoRecorder
      isFlipped={false}
      countdownTime={0}
      mimeType="video/webm;codecs=vp8,opus"
      onStartRecording={() => getQuestion()}
      constraints={{
        audio: true,
        video: {
          width: { exact: 480, ideal: 480 },
          height: { exact: 640, ideal: 640 },
          aspectRatio: { exact: 0.7500000001, ideal: 0.7500000001 },
          resizeMode: "crop-and-scale"
        }
      }}
      onRecordingComplete={(videoBlob) => {
        //  extract video in mp4 format from videoblob
        const videoFile = new File([videoBlob], "video.mp4", {
          type: "video/mp4"
        });
        submitForm(videoFile);
        console.log("videoBlob", videoFile);
        push("/videoPreview", { videoBlob });
      }}
    />
  );
};

const VideoRecordPage = (props) => {

  const [question, setQuestion] = React.useState({});
  return (

    <div className="App">
      <h1>Video record</h1>
      <p>{question?.question}</p>
      <div style={{ width: "100%", maxWidth: 480, height: 640 }}>
        <FromVideoRecorder push={props.history.push} setQuestion={setQuestion} />
      </div>
    </div>
  );
};

const VideoPreviewPage = (props) => {
  return (
    <div className="App">
      <h1>Video preview</h1>

      {props.location.state && props.location.state.videoBlob && (
        <div style={{ width: "100%", maxWidth: 480, height: 640 }}>
          <video
            src={window.URL.createObjectURL(props.location.state.videoBlob)}
            width={480}
            height={640}
            autoPlay
            loop
            controls
          />
        </div>
      )}
      <Link to="/score">View Score</Link>
    </div>
  );
};

export default function App() {
  return (
    <Router>
      <Switch>
        <Redirect to="/videoRecord" exact path="/" />
        <Route path="/videoRecord" component={VideoRecordPage} />
        <Route path="/videoPreview" component={VideoPreviewPage} />
        <Route path="/score" component={Score} />
      </Switch>
    </Router>
  );
}
