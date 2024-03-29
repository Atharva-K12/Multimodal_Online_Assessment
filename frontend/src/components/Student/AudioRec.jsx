import React from "react";
import vmsg from "vmsg";
 
const recorder = new vmsg.Recorder({
  wasmURL: "https://unpkg.com/vmsg@0.3.0/vmsg.wasm"
});

const sendData = async (audioBlob, testName, question) => {
  const audioFile = new File([audioBlob], "audio.mp3", {
    type: "audio/mpeg"
  })
  const url = 'http://localhost:5010/upload-answer'
  const formData = new FormData();
  formData.append('file', audioFile);
  formData.append('testName', testName);
  formData.append('question', localStorage.getItem('question'));
  formData.append('questionNumber', localStorage.getItem('questionNumber'));
  await fetch(url, {
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
      localStorage.setItem('questionNumber', data.questionNumber);
      localStorage.setItem('question', data.question);
      return data
    })
    .catch(error => console.error('Error:', error))
}
 
class AudioRec extends React.Component {
  state = {
    isLoading: false,
    isRecording: false,
    recordings: [],
    question: '',
    questionNumber: 1
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
      let question = sendData(blob, this.props.testName, this.state.question);
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
    if(localStorage.getItem('questionNumber') !== null) {
      localStorage.setItem('questionNumber', 1);
    }
    const formData = new FormData();
    formData.append('testName', this.props.testName);
  
    fetch('http://localhost:5010/upload-answer',{
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
      localStorage.setItem('questionNumber', data.questionNumber);
      localStorage.setItem('question', data.question);
    })
    .catch(error => console.error('Error:', error))
  }

  render() {
    const { isLoading, isRecording, recordings, question, questionNumber } = this.state;
    return (
      <div>
      {isRecording ? <h2>
        {localStorage.getItem('question')}
      </h2>:''}
      <h2>{this.state.questionNumber}</h2>
      <React.Fragment>
        <button disabled={!this.props.isRecVideo} onClick={this.record}>
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