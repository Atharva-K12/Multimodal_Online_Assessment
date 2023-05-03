import React from "react";
import vmsg from "vmsg";
 
const recorder = new vmsg.Recorder({
  wasmURL: "https://unpkg.com/vmsg@0.3.0/vmsg.wasm"
});

const sendData = (audioBlob, testName) => {
  const audioFile = new File([audioBlob], "audio.mp3", {
    type: "audio/mpeg"
  })

  const url = 'http://localhost:5000/upload-answer'
  const formData = new FormData();
  formData.append('file', audioFile);
  formData.append('testName', testName);
  formData.append('question', 'What is constructor?');
  formData.append('question_number', 1);
  fetch(url, {
    method: 'POST',
    headers: {
      //'content-type': 'multipart/form-data',
      'Authorization': localStorage.getItem('token')
    },
    body: formData
  })
    .then(response => response.json())
    .then((data) => {
      console.log('Success:', data)
      return data.question
    })
    .catch(error => console.error('Error:', error))
}
 
class AudioRec extends React.Component {
  state = {
    isLoading: false,
    isRecording: false,
    recordings: [],
    question: ''
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
      question = sendData(blob, this.props.testName);
      this.setState({question: question})
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

  componentDidMount() {
    const formData = new FormData();
    formData.append('testName', this.props.testName);
  
    fetch('http://localhost:5000/upload-answer',{
      method: 'POST',
      headers: {
        //'content-type': 'multipart/form-data',
        'Authorization': localStorage.getItem('token')
      },
      body: formData
    })
    .then(response => response.json())
    .then((data) => {
      console.log('Success:', data)
      this.setState({question:data.question})
    })
    .catch(error => console.error('Error:', error))
  }

  render() {
    const { isLoading, isRecording, recordings, question } = this.state;
    return (
      <div>
      {isRecording ? <h2>
        {this.state.question}
      </h2>:''}
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