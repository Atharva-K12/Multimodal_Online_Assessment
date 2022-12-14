import React,{useState} from 'react'
import {Link} from 'react-router-dom'

function Register() {
    const [student,setStudent] = useState({})

    const handleChange=(e)=>{
        const {name,value} = e.target
        setStudent({
            ...student,
            [name]:value
        })

    }

    const handleSubmit = (e) => {
        e.preventDefault();

    }

    return (
        <div className="container shadow">
            <h3 className="cover-image">Register</h3>
            <form className="form container">
                <div className="mb-3">
                    <input className="form-control" type="text" name="username" placeholder="Username" onChange={handleChange}/>
                </div>
                <div className="mb=3">
                    <input className="form-control" type="password" name="password" placeholder="Password" onChange={handleChange}/>
                </div>
                <input type="submit" value="Register" className="btn m-1 btn-primary" onClick={handleSubmit}/>
                <p>Already have an account,<Link to="login" className="btn m-1 btn-sm btn-warning">Login</Link></p>
            </form> 
        </div>
    )
}

export default Register