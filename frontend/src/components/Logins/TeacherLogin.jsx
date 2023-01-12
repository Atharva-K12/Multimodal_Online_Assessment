import React, {useState} from 'react'
import '../../css/Logins/Login.css'
import Navbar from './Navbar'

export default function TeacherLogin(props) {
    const location = props.location

    const [login, setLogin] = useState({})
    const handleChange = (e) => {
        const {name,value} = e.target
        setLogin({
            ...login,
            [name]:value
        })
    }

    const handleSubmit = (e) => {
        if(login === {}){
            alert('Please fill in the form')
        }else{
            let url = location + '/teacher-login';
            let formData = new FormData();
            formData.append(login);
            fetch(url, {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if(response.ok){
                    return response.json()
                }
                alert(response.json()['message'])
            })
        }
    }

  return (
    <div>
        <Navbar />
        <div className='container shadow'>
            <h3 className='cover-image'>Login</h3>
            <form className='form-container'>
                <div className='mb-3'>
                    <input className='form-control' type='text' name='username' placeholder='Username' onChange={handleChange}/>
                </div>
                <div className='mb-3'>
                    <input className='form-control' type='text' name='password' placeholder='Password' onChange={handleChange}/>
                </div>
                <input type='submit' value='Login' className='btn m-1 btn-primary' onClick={handleSubmit}/>
                <p>Do not have an accout, <a to='/teacher-register' className='btn m1 btn-sm btn-warning'>Register</a></p>
            </form>
        </div>
    </div>
  )
}
