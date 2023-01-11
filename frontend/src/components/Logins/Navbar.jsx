import React from 'react'
import { Link } from 'react-router-dom';
import "../../css/Logins/Navbar.css";

export default function Navbar() {
  return (
    <div>
        <nav className="navbar navbar-expand-lg navbar-light bg-dark">
            <div className="parent">
                <h2>FYP 2023</h2>
                <div className="child">
                    <div className='links'>
                        <Link href="/">Home</Link>
                    </div>
                    <div className='links'>
                        <Link href="/admin-login">Admin</Link>
                    </div>
                    <div className='links'>
                        <Link href="/teacher-login">Teacher</Link>
                    </div>
                    <div className='links'>
                        <Link href="/student-login">Student</Link>
                    </div>
                </div>
            </div>
        </nav>
    </div>
  )
}
