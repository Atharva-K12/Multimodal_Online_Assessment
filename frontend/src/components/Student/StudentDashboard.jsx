import React from 'react'
import Title from './Title'
import avatar from "./images/avatar.png"
import { Link, useHistory } from 'react-router-dom'

function StudentDashboard() {

    let history = useHistory()

    const handleLogout = () => {
        localStorage.removeItem('token')
        localStorage.removeItem('username')
        localStorage.removeItem('roll_no')
        history.push('/student-login')
    }

    const mystyle={
        maxWidth: "540px",
    }

    // if(!login){
    //     return <Redirect to="/student-login"/>
    // }

    return (
        <div>
            <Title/>
            <div className="card mb-3 container" style={{ mystyle }}>
                <div className="row g-0">
                    <div className="col-md-3">
                        <img width="250" height="250" src={avatar} alt="..." />
                    </div>
                    <div className="col-md-8">
                        <div className="card-body">
                            <h5 className="card-title">Test</h5>
                            <p className="card-text">User_Description</p>
                            <p className="card-text"><small className="text-muted">Branch: CSE</small></p>
                            <p className="card-text"><small className="text-muted">CGPA: 9.0</small></p>
                        </div>
                    </div>
                </div>
            </div>
            <div className="container">
                <button className="btn btn-primary" onClick={handleLogout}>Logout</button>
            </div>
        </div>
    )
}

export default StudentDashboard