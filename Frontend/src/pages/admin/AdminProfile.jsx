import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom"; // Import useNavigate for navigation
import { User, LogOut } from "lucide-react"; // Import icons from lucide-react

const Profile = () => {
  const [userDetails, setUserDetails] = useState(null);
  const [techEvents, setTechEvents] = useState([]); // State for Tech events
  const [nonTechEvents, setNonTechEvents] = useState([]); // State for NonTech events
  const [loading, setLoading] = useState(true);
  const [dropdownOpen, setDropdownOpen] = useState(false); // State for dropdown visibility
  const navigate = useNavigate(); // Initialize useNavigate

  useEffect(() => {
    fetchProfileData();
  }, []);

  const fetchProfileData = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get("http://127.0.0.1:5000/auth/admin_user/details", {
        headers: { Authorization: token },
      });
      const { user, created_events } = response.data;

      // Separate Tech and NonTech events
      const tech = created_events.filter((event) => event.EventType === "Tech");
      const nonTech = created_events.filter((event) => event.EventType === "NonTech");

      setUserDetails(user);
      setTechEvents(tech);
      setNonTechEvents(nonTech);
    } catch (error) {
      console.error("Error fetching profile data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token"); // Remove token from localStorage
    navigate("/login"); // Navigate to the login page
  };

  if (loading) {
    return <div className="text-center mt-10 text-blue-600 text-lg">Loading...</div>;
  }

  if (!userDetails) {
    return <div className="text-center mt-10 text-red-600 text-lg">Failed to load profile data.</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-gray-800 p-4 shadow-lg text-white flex justify-between items-center">
        <h1 className="font-semibold text-lg">Profile Dashboard</h1>
        <div className="relative">
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)} // Toggle dropdown visibility
            className="bg-gray-700 hover:bg-gray-600 text-white p-2 rounded-full transition duration-300"
          >
            <User className="h-5 w-5" />
          </button>
          {dropdownOpen && (
            <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg z-10">
              <button
                onClick={() => navigate("/admindashboard")} // Navigate to the homepage
                className="flex items-center w-full text-left px-4 py-2 text-gray-800 hover:bg-gray-100"
              >
                <User className="h-4 w-4 mr-2" />
                Home
              </button>
              <button
                onClick={handleLogout} // Logout functionality
                className="flex items-center w-full text-left px-4 py-2 text-gray-800 hover:bg-gray-100"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </button>
            </div>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto mt-10 p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Profile Card */}
          <div className="col-span-1 bg-white p-6 rounded-lg shadow-md">
            <h1 className="text-3xl font-bold mb-4 text-gray-800">Profile</h1>
            <div className="space-y-4">
              <p>
                <strong className="text-gray-800">Name:</strong> {userDetails.name}
              </p>
              <p>
                <strong className="text-gray-800">Username:</strong> {userDetails.username}
              </p>
              <p>
                <strong className="text-gray-800">Email:</strong> {userDetails.email}
              </p>
              <p>
                <strong className="text-gray-800">Role:</strong> {userDetails.role}
              </p>
            </div>
          </div>

          {/* Tech Events Section */}
          <div className="col-span-2 bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">Tech Events</h2>
            {techEvents.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {techEvents.map((event) => (
                  <div
                    key={event._id}
                    className="bg-gray-200 p-4 rounded-md hover:bg-gray-300 transition duration-300 shadow-sm"
                  >
                    <h3 className="text-lg font-semibold text-gray-800">
                      {event.title || "Untitled Event"}
                    </h3>
                    <p className="text-gray-600">
                      {event.date || "Unknown Date"} at {event.time || "Unknown Time"}
                    </p>
                    <p className="text-gray-600">Location: {event.location || "Unknown"}</p>
                    <p className="text-gray-600">Cost: {event.price ? `$${event.price}` : "Free"}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-600">No Tech events created yet.</p>
            )}
          </div>

          {/* NonTech Events Section */}
          <div className="col-span-2 bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-4 text-gray-800">NonTech Events</h2>
            {nonTechEvents.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {nonTechEvents.map((event) => (
                  <div
                    key={event._id}
                    className="bg-gray-200 p-4 rounded-md hover:bg-gray-300 transition duration-300 shadow-sm"
                  >
                    <h3 className="text-lg font-semibold text-gray-800">
                      {event.title || "Untitled Event"}
                    </h3>
                    <p className="text-gray-600">
                      {event.date || "Unknown Date"} at {event.time || "Unknown Time"}
                    </p>
                    <p className="text-gray-600">Location: {event.location || "Unknown"}</p>
                    <p className="text-gray-600">Cost: {event.price ? `$${event.price}` : "Free"}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-600">No NonTech events created yet.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;