import React, {useState} from 'react'
import '../../css/Logins/Register.css'
import Navbar from './Navbar'

export default function StudentRegister(props) {
    const location = props.location

    const [student, setStudent] = useState({})

    const handleChange = (e) => {
        const {name,value} = e.target
        setStudent({
            ...student,
            [name]:value
        })
    }

    const handleSubmit = (e) => {
        if(student === {}){
            alert('Please fill in the form')
        }else{
            let url = location + '/student-register'
            let formData = new FormData();
            formData.append(student);
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
            <h3 className='cover-image'>Register</h3>
            <form className='form-container'>
                <div className='mb-3'>
                    <input className='form-control' type='text' name='username' placeholder='Username' onChnage = {handleChange}/>
                </div>
                <div className='mb-3'>
                    <input className='form-control' type='text' name='password' placeholder='Password' onChnage = {handleChange}/>
                </div>
                <div className='mb-3'>
                    <input className='form-control' type='text' name='email' placeholder='Email' onChnage = {handleChange}/>
                </div>
                <div className='mb-3'>
                    <input className='form-control' type='text' name='name' placeholder='Name' onChnage = {handleChange}/>
                </div>
                <input type='submit' value='Register' className='btn m-1 btn-primary' onClick = {handleSubmit}/>
                <p>Already have an account, <a to = "/student-login" className = 'btn m-1 btn-sm btn-warning'>Login</a></p>
            </form>
        </div>
    </div>
  )
}