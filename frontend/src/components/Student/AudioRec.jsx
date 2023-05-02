import React from "react";
import vmsg from "vmsg";
 
const recorder = new vmsg.Recorder({
  wasmURL: "https://unpkg.com/vmsg@0.3.0/vmsg.wasm"
});

const sendData = (audioFile) => {
  const url = 'http://localhost:5000/upload-answer'
  const formData = new FormData();
  formData.append('file', audioFile);
  fetch(url, {
    method: 'POST',
    body: {
      question_id: 1,
      file:formData
    }
    .then(response => response.json())
    .then((data) => {
      return data.question
    })
    .catch(error => console.error('Error:', error))
  })
}
 
class AudioRec extends React.Component {
  state = {
    isLoading: false,
    isRecording: false,
    recordings: []
  };
  record = async () => {
    this.setState({ isLoading: true });
 
    if (this.state.isRecording) {
      const blob = await recorder.stopRecording();
      this.setState({
        isLoading: false,
        isRecording: false,
        recordings: this.state.recordings.concat(URL.createObjectURL(blob))
      });
      sendData(blob);
    } else {
      try {
        await recorder.initAudio();
        await recorder.initWorker();
        recorder.startRecording();
        this.setState({ isLoading: false, isRecording: true });
      } catch (e) {
        console.error(e);
        this.setState({ isLoading: false });
      }
    }
  };
  render() {
    const { isLoading, isRecording, recordings } = this.state;
    return (
      <div>
        {/* <h2>{this.props.testName}</h2> */}
      {/* <h4>What is constructor?</h4> */}
      <React.Fragment>
        <button disabled={isLoading} onClick={this.record}>
          {isRecording ? "Stop" : "Record"}
        </button>
        <ul style={{ listStyle: "none", padding: 0 }}>
          {recordings.map(url => (
            <li key={url}>
              <audio src={url} controls />
            </li>
          ))}
        </ul>
      </React.Fragment>
      </div>
    );
  }
}
 
export default AudioRec;