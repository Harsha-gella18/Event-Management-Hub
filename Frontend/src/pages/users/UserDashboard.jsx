import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { User } from "lucide-react";
import EventCard from "../../Components/users/EventCard";

function UserDashboard() {
  const [events, setEvents] = useState([]);
  const [username, setUsername] = useState("");
  const [techPoints, setTechPoints] = useState(0);
  const [nonTechPoints, setNonTechPoints] = useState(0);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchEvents();
    fetchUserDetails();
  }, []);

  const fetchEvents = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get("http://127.0.0.1:5000/events/user/unregistered_events", {
        headers: { Authorization: token },
      });
      setEvents(response.data.events);
    } catch (error) {
      console.error("Error fetching events:", error);
      alert("Failed to fetch events. Please try again.");
    }
  };

  const fetchUserDetails = async () => {  
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get("http://127.0.0.1:5000/auth/user", {
        headers: { Authorization: token },
      });
      const user = response.data.user;
      setUsername(user.username);
      setTechPoints(user.Tech_points || 0);
      setNonTechPoints(user.NonTech_Points || 0);
    } catch (error) {
      console.error("Error fetching user details:", error);
    }
  };

  const handleRegister = async (eventId) => {
    const confirmRegistration = window.confirm("Are you sure you want to register for this event?");
    if (!confirmRegistration) {
      return;
    }

    try {
      const token = localStorage.getItem("token");
      const response = await axios.post(
        `http://127.0.0.1:5000/events/user/register/${eventId}`,
        {},
        { headers: { Authorization: token } }
      );
      alert(response.data.message);
      fetchEvents();
    } catch (error) {
      console.error("Error registering for event:", error);
      alert("Failed to register for the event. Please try again.");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  };

  const handleProfile = () => {
    navigate("/userprofile");
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-gray-800 text-white py-4 px-6 flex items-center justify-between">
        <h2 className="text-xl font-semibold">Event Management System</h2>
        <div className="relative">
          <button
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
            className="text-sm font-medium flex items-center"
          >
            <User className="h-4 w-4 mr-1" />
            {username}
          </button>
          {isDropdownOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white border rounded shadow-lg">
              <button
                onClick={handleProfile}
                className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100"
              >
                Profile
              </button>
              <button
                onClick={handleLogout}
                className="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100"
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </nav>

      <div className="bg-white shadow-md rounded-lg p-6 mx-4 mt-6 flex justify-between items-center text-center md:mx-10 lg:mx-20">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-700">Technical Points</h3>
          <p className="text-2xl font-bold text-blue-600">{techPoints}</p>
        </div>
        <div className="border-l border-gray-300 h-12 mx-4"></div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-700">Non-Technical Points</h3>
          <p className="text-2xl font-bold text-green-600">{nonTechPoints}</p>
        </div>
      </div>

      <div className="py-10 px-10">
        <h1 className="text-3xl font-bold text-center mb-6">Available Events</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {events.map((event) => (
            <EventCard key={event._id} event={event} onRegister={handleRegister} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default UserDashboard;