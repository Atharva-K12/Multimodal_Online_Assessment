import React from 'react'
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import Navbar from './Navbar'
import FrontPage from './FrontPage'
import StudentLogin from './StudentLogin'
import TeacherLogin from './TeacherLogin'
import StudentRegister from './StudentRegister'
import TeacherRegister from './TeacherRegister'
import AdminLogin from './AdminLogin'

export default function login(props) {
  const location = props.location
  return (
    <div>
      <Navbar/>
      <Router>
        <Switch>
          <Route path="/" component={FrontPage}/>
          <Route path="student-login" location = {location} component={StudentLogin}/>
          <Route path="teacher-login" location = {location} component={TeacherLogin}/>
          <Route path="student-register" location = {location} component={StudentRegister}/>
          <Route path="teacher-register" location = {location} component={TeacherRegister}/>
          <Route path="admin-login" location = {location} component={AdminLogin}/>
        </Switch>
      </Router>
    </div>
  )
}
