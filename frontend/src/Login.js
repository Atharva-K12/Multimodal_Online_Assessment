import React, {useState} from 'react'
import {Link} from 'react-router-dom'

function Login() {

    const [login,setLogin] = useState({})

    const handleChange = (e)=>{
        const {name,value} = e.target
        setLogin({
            ...login,
            [name]:value
        })
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        
    }

    return (
        <div className="container shadow">
            <h3 className="cover-image">Login</h3>
            <form className="form container">
                <div className="mb-3">
                    <input className="form-control" type="text" name="username" placeholder="Username" onChange={handleChange}/>
                </div>
                <div className="mb-3">
                    <input className="form-control" type="password" name="password" placeholder="Password" onChange={handleChange}/>
                </div>
                <input type="submit" value="Login" className="btn m-1 btn-primary" onClick={handleSubmit}/>
                <p>Do not have an account,<Link to="register" className="btn m-1 btn-sm btn-warning">Register</Link></p>
            </form>
        </div>
    )
}

export default Login