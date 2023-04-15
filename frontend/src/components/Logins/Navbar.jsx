import React from 'react'
import {Link} from 'react-router-dom'
import "../../css/Logins/Navbar.css";

export default function Navbar() {
  return (
    <div>
        <nav className="navbar navbar-expand-lg navbar-light bg-dark">
            <div className="parent">
                <h2>FYP 2023</h2>
                <div className="child">
                    <div className='links'>
                        <Link to="/">Home</Link>
                    </div>
                    <div className='links'>
                        <Link to="/admin-login/">Admin</Link>
                    </div>
                    <div className='links'>
                        <Link to="/teacher-login/">Teacher</Link>
                    </div>
                    <div className='links'>
                        <Link to="/student-login/">Student</Link>
                    </div>
                </div>
            </div>
        </nav>
    </div>
  )
}
