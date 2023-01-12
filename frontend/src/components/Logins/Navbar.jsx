import React from 'react'
import "../../css/Logins/Navbar.css";

export default function Navbar() {
  return (
    <div>
        <nav className="navbar navbar-expand-lg navbar-light bg-dark">
            <div className="parent">
                <h2>FYP 2023</h2>
                <div className="child">
                    <div className='links'>
                        <a href="/">Home</a>
                    </div>
                    <div className='links'>
                        <a href="/admin-login">Admin</a>
                    </div>
                    <div className='links'>
                        <a href="/teacher-login">Teacher</a>
                    </div>
                    <div className='links'>
                        <a href="/student-login">Student</a>
                    </div>
                </div>
            </div>
        </nav>
    </div>
  )
}
