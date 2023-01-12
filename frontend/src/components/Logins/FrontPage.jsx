import React from 'react'
import "../../css/Logins/FrontPage.css"
import Navbar from './Navbar'

export default function FrontPage() {
  return (
    <div>
      <Navbar/>
      <div className='frontpage'>
          <h1>
              Let's Quiz
          </h1>
          <h2>
              Test your techical skills and knowledge
          </h2>
          <h6>
              We organize vivas with video proctoring and voice analysis techniques.
          </h6>
          <h6>
          Visit the respective links to register and login according to your role as a student or a teacher.
          </h6>
      </div>
    </div>
  )
}
