import React, {useState} from 'react'
import '../../css/Logins/Register.css'
import Navbar from './Navbar'
import {Link} from 'react-router-dom'

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
        e.preventDefault()
        if(student === {}){
            alert('Please fill in the form')
        }else{
            let url = location + '/student-register'
            fetch(url, {
                method:'POST',
                headers:{ 
                    'Content-type':'application/json',
                },
                body:JSON.stringify(student)
            })
            .then(response => {
                if(response.ok){
                    return response.json()
                }
                alert(response.json()['message'])
            })
            .catch((e)=>console.log(e))
        }
    }

  return (
    <div>
        <Navbar />
        <div className='container shadow'>
            <h3 className='cover-image'>Register</h3>
            <form className='form-container'>
                <div className='mb-3'>
                    <input className='form-control' type='text' name='username' placeholder='Username' onChange = {handleChange}/>
                </div>
                <div className='mb-3'>
                    <input className='form-control' type='text' name='password' placeholder='Password' onChange = {handleChange}/>
                </div>
                <div className='mb-3'>
                    <input className='form-control' type='text' name='email' placeholder='Email' onChange = {handleChange}/>
                </div>
                <div className='mb-3'>
                    <input className='form-control' type='text' name='name' placeholder='Name' onChange = {handleChange}/>
                </div>
                <input type='submit' value='Register' className='btn m-1 btn-primary' onClick = {handleSubmit}/>
                <p>Already have an account, <Link to = "/student-login" className = 'btn m-1 btn-sm btn-warning'>Login</Link></p>
            </form>
        </div>
    </div>
  )
}
