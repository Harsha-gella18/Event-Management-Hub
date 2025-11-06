import React, { useState, useEffect } from "react";
import axios from "axios";
import { motion } from "framer-motion";

function TakeAttendanceModal({ eventId, onClose, fetchEvents }) {
  const [registeredUsers, setRegisteredUsers] = useState([]);
  const [attendance, setAttendance] = useState({});
  const [isAttendanceTaken, setIsAttendanceTaken] = useState(false);

  useEffect(() => {
    fetchRegisteredUsers();
  }, []);

  const fetchRegisteredUsers = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get(`http://127.0.0.1:5000/events/${eventId}/registered_users`, {
        headers: { Authorization: token },
      });
      setRegisteredUsers(response.data.users);
      setIsAttendanceTaken(response.data.isAttendanceTaken);

      const initialAttendance = {};
      response.data.users.forEach((user) => {
        initialAttendance[user._id] = false;
      });
      setAttendance(initialAttendance);
    } catch (error) {
      console.error("Error fetching registered users:", error);
    }
  };

  const handleAttendanceChange = (userId) => {
    setAttendance((prev) => ({
      ...prev,
      [userId]: !prev[userId],
    }));
  };

  const handleSaveAttendance = async () => {
    try {
      const token = localStorage.getItem("token");
      await axios.post(
        `http://127.0.0.1:5000/events/${eventId}/take_attendance`,
        { attendance },
        { headers: { Authorization: token } }
      );
      alert("Attendance saved successfully!");
      fetchEvents();
      onClose();
    } catch (error) {
      console.error("Error saving attendance:", error);
      alert("Failed to save attendance. Please try again.");
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <motion.div 
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-2xl"
      >
        <h2 className="text-3xl font-bold mb-6 text-gray-800">Take Attendance</h2>
        {isAttendanceTaken ? (
          <div className="text-center">
            <p className="text-red-600 font-semibold mb-4">Attendance Already Taken</p>
            <button
              onClick={onClose}
              className="bg-gray-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-gray-700"
            >
              Close
            </button>
          </div>
        ) : (
          <div>
            <div className="space-y-4 h-80 overflow-y-auto">
              {registeredUsers.map((user) => (
                <div key={user._id} className="flex items-center justify-between bg-gray-100 p-3 rounded-lg">
                  <div className="text-gray-700">
                    <span className="font-medium">{user.username}</span> ({user.email})
                  </div>
                  <input
                    type="checkbox"
                    id={user._id}
                    checked={attendance[user._id] || false}
                    onChange={() => handleAttendanceChange(user._id)}
                    className="h-5 w-5 rounded-full text-blue-600 focus:ring-blue-500"
                  />
                </div>
              ))}
            </div>
            <div className="flex justify-end space-x-4 mt-6">
              <button
                onClick={handleSaveAttendance}
                className="bg-blue-500 text-white font-bold py-2 px-6 rounded-lg hover:bg-blue-700 transition duration-200"
              >
                Save Attendance
              </button>
              <button
                onClick={onClose}
                className="bg-gray-500 text-white font-bold py-2 px-6 rounded-lg hover:bg-gray-700 transition duration-200"
              >
                Cancel
              </button>
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}

export default TakeAttendanceModal;
