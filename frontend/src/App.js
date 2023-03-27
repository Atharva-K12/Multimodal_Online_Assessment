import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";
import {
  Copyright, 
  AdminLogin, 
  FrontPage, 
  StudentLogin, 
  StudentRegister, 
  TeacherLogin, 
  TeacherRegister, 
  AdminDashboard, 
  StudentDashboard, 
  VideoRecorder 
} from "./components";

export default function App() {
  const location = 'http://127.0.0.1:5000'

  return (
    <div>
      <Router>
        <Switch>
          <Route path = "/student-login" render={() => <StudentLogin location = {location} />} />
          <Route path = "/teacher-login" render={() => <TeacherLogin location = {location} />}/>
          <Route path = "/admin-login" render={() => <AdminLogin location = {location} />} />
          <Route path = "/student-register" render={() => <StudentRegister location = {location} />} />
          <Route path = "/admin-dashboard" render={() => <AdminDashboard location = {location} />} />
          <Route path = "/teacher-register" render={() => <TeacherRegister location = {location} />} />
          <Route path = "/student-dashboard" render={() => <StudentDashboard location = {location} />} />
          <Route path = "/start-test" render={() => <VideoRecorder location={location} />} />
          <Route path = "/" render={() => <FrontPage />} />
        </Switch>
      </Router>
      <Copyright/>
    </div>
  );
}
