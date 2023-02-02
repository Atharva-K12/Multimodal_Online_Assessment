import React, {useState} from 'react'
import { Link } from 'react-router-dom'
import '../../css/Logins/Login.css'
import Navbar from './Navbar'

export default function StudentLogin(props) {
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
        e.preventDefault()
        if(login === {}){
            alert('Please fill in the form')
        }else{
            let url = location + '/student-login';
            fetch(url, {
                method:'POST',
                headers:{ 
                    'Content-type':'application/json',
                },
                body:JSON.stringify(login)
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
                <p>Do not have an accout, <Link to='/student-register' className='btn m1 btn-sm btn-warning'>Register</Link></p>
            </form>
        </div>
    </div>
  )
}
