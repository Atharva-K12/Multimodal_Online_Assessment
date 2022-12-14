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

const FromVideoRecorder = ({ push, setQuestion, getQue }) => {

  const submitForm = (videoFile) => {
    const formData = new FormData();
		formData.append('file', videoFile);
    formData.append('question', getQue());
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
          width: { exact: 500, ideal: 480 },
          height: { exact: 500, ideal: 640 },
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
  function getQuestion(){
    return question.question;
  }

  return (

    <div className="App">
      <h3>Record Your Video</h3>
      <p>{question?.question}</p>
      <div style={{ width: "100%", maxWidth: 1000, height: 500 , margin: "auto"}}>
        <FromVideoRecorder push={props.history.push} setQuestion={setQuestion} getQue = {getQuestion} />
      </div>
    </div>
  );
};

const VideoPreviewPage = (props) => {
  return (
    <div className="App">
      <h3>Video Preview</h3>
      {props.location.state && props.location.state.videoBlob && (
        <div style={{ width: "100%", maxWidth: 480, height: 400, margin:"auto" }}>
          <video
            src={window.URL.createObjectURL(props.location.state.videoBlob)}
            width={480}
            height={400}
            autoPlay
            loop
            controls
          />
        </div>
      )}
      <Link className="btn m-3 btn-sm btn-primary" to="/score">View Score</Link>
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
