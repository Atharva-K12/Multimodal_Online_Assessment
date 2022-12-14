import React from 'react'
import { Link } from 'react-router-dom'
import './score.css'

function Score() {
  return (
    <div className='m-3'>
        <h1>Score Obtained</h1>
        <table className='scoreTable'>
            <tr>
                <th>Similarity Score</th>
                <th>Plagiarism Percentage Score</th>
                <th>Aggregate Score</th>
            </tr>
            <tr>
                <td>1</td>
                <td>0.5</td>
                <td>0.5</td>
            </tr>
        </table>
        <Link className="btn m-3 btn-sm btn-primary" to='/VideoRecord'>Next Question</Link>
    </div>
  )
}

export default Score