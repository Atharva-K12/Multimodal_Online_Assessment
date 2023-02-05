import React,{useState} from 'react'
import { EditableRow } from './EditableRow'

export default function AdminDashboard() {

  const [data, setData] = useState([
    { ID: 1, Name: "John", Approval_Status: "Pending" },
    { ID: 2, Name: "Mary", Approval_Status: "Pending" },
    { ID: 3, Name: "Peter", Approval_Status: "Pending" },
  ])


  const onUpdate = (updated_row) => {  
    console.log(updated_row);
    // make an API call to update on the server

    // update the state
    // remove the row which was approved from data
    const updatedData = data.filter(obj => obj.ID !== updated_row.ID);

    setData(updatedData)
    console.log(data);
  }

  return (
    <div className='admin-dashboard container'>
        <table class = 'table table-hover table-bordered'>
        <thead>
          <tr>
            {Object.keys(data[0]).map((header, index) => (
              <th key={index}>{header}</th>
            ))}
            <th>Actions</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          {data.map((row, index) => (
            <EditableRow
              key={index}
              data={row}
              onUpdate={onUpdate}
            />
          ))}
        </tbody>
      </table>
    </div>
  )
}
