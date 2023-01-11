import React, {useState} from 'react'
import '../../css/Logins/Register.css'
import { Link } from 'react-router-dom'

export default function StudentRegister(props) {
    const location = props.location

    const [teacher, setTeacher] = useState({})

    const handleChange = (e) => {
        const {name,value} = e.target
        setTeacher({
            ...teacher,
            [name]:value
        })
    }

    const handleSubmit = (e) => {
        if(teacher === {}){
            alert('Please fill in the form')
        }else{
            let url = location + '/teacher-register'
            let formData = new FormData();
            formData.append(teacher);
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
                <input className='form-control' type='text' name='phone' placeholder='Phone' onChnage = {handleChange}/>
            </div>
            <input type='submit' value='Register' className='btn m-1 btn-primary' onClick = {handleSubmit}/>
            <p>Already have an account, <Link to = "/teacher-login" className = 'btn m-1 btn-sm btn-warning'>Login</Link></p>
        </form>
    </div>
  )
}
