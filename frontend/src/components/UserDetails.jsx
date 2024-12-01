import React from "react";

const UserDetails = ({ userDetails, setUserDetails }) => {
  const handleChange = (e) => {
    setUserDetails({ ...userDetails, [e.target.name]: e.target.value });
  };

  return (
    <div className="p-4 border rounded shadow">
      <h2 className="font-bold text-lg">User Details</h2>
      <div className="mt-4 space-y-2">
        <input
          type="text"
          name="name"
          placeholder="Name"
          className="border p-2 w-full"
          value={userDetails.name}
          onChange={handleChange}
        />
        <input
          type="number"
          name="age"
          placeholder="Age"
          className="border p-2 w-full"
          value={userDetails.age}
          onChange={handleChange}
        />
        <select
          name="gender"
          className="border p-2 w-full"
          value={userDetails.gender}
          onChange={handleChange}
        >
          <option value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select>
      </div>
    </div>
  );
};

export default UserDetails;
