import React,{useState, useEffect} from 'react'
import Title from './Title'
import avatar from "./images/avatar.png"
import { Link, useHistory } from 'react-router-dom'

function StudentDashboard() {

    let history = useHistory()

    const [testlist, setTestlist] = useState({})

    useEffect(() => {
        fetch('http://localhost:5000/get-student-enrollments', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': localStorage.getItem('token')
            }
        })
        .then(res => res.json())
        .then(data => {
            setTestlist(data)
            console.log(data)
        })
    }, [])

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
                            <h5 className="card-title">{localStorage.getItem('username')}</h5>
                            <p className="card-text">User_Description</p>
                            <p className="card-text"><small className="text-muted">Branch: CSE</small></p>
                            <p className="card-text"><small className="text-muted">Enrollment Number: {localStorage.getItem('roll_no')}</small></p>
                        </div>
                    </div>
                </div>
            </div>
            <div className="container">
                <button className="btn btn-primary" onClick={handleLogout}>Logout</button>
            </div>
            <div className="container">
                <h2>Enrolled Tests</h2>
                {testlist?.enrollments !== undefined ?
                    (<table className="table table-hover">
                        <thead>
                            <tr>
                                <th scope="col">Test Name</th>
                                <th scope="col"></th>
                            </tr>
                        </thead>
                        <tbody>
                            {testlist?.enrollments.map((test) => (
                                <tr>
                                    <td>{test}</td>
                                    <td><Link to="/start-test/videoRecord" className="btn btn-primary">Start Test</Link></td>
                                </tr>
                            ))}
                        </tbody>
                    </table>): <p>No Enrollments</p>
                }
            </div>
        </div>
    )
}

export default StudentDashboard