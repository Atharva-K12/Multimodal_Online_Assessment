import React, { useState } from "react";

export const EditableRow = ({ data, onUpdate }) => {
  const [isEditing, setEditing] = useState(false);
  const [rowData, setRowData] = useState(data);

  const handleChange = (event) => {
    setRowData({ ...rowData, [event.target.name]: event.target.value });
  };

  const toggleEdit = () => {
    setEditing(!isEditing);
  };

  const handleSave = () => {
    onUpdate(rowData);
    toggleEdit();
  };

  return (
    <tr>
      {Object.values(rowData).map((value, index) => (
        <td key={index}>
          {isEditing ? (
            <input
              name={Object.keys(rowData)[index]}
              value={value}
              onChange={handleChange}
            />
          ) : (
            value
          )}
        </td>
      ))}
      <td>
        {isEditing ? (
          <button onClick={handleSave}>Save</button>
        ) : (
          <button onClick={toggleEdit}>Edit</button>
        )}
      </td>
    </tr>
  );
};
