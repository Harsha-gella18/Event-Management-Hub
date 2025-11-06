import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import EventCard from "../../Components/admin/admindashboard/eventcard";
import AddEventModal from "../../Components/admin/admindashboard/AddEventModel";
import EditEventModal from "../../Components/admin/admindashboard/EditEventModel";
import TakeAttendanceModal from "../../Components/admin/admindashboard/TakeAttendance";
import { User } from "lucide-react";

function AdminDashboard() {
  const [events, setEvents] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [currentEventId, setCurrentEventId] = useState(null);
  const [isAttendanceModalOpen, setIsAttendanceModalOpen] = useState(false);
  const [newEvent, setNewEvent] = useState({
    title: "",
    date: "",
    time: "",
    location: "",
    description: "",
    price: 0,
    TotalCount: 0,
    EventType: "",
    Points: 0,
  });
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [username, setUsername] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    fetchEvents();
    fetchUserDetails();
  }, []);

  const fetchEvents = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get("http://127.0.0.1:5000/events/admin/get_events", {
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
      setUsername(response.data.user.username);
    } catch (error) {
      console.error("Error fetching user details:", error);
      alert("Failed to fetch user details. Please try again.");
    }
  };

  const handleAddEvent = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      if (isEditing) {
        await axios.put(
          `http://127.0.0.1:5000/events/edit_event/${currentEventId}`,
          newEvent,
          { headers: { Authorization: token } }
        );
        alert("Event updated successfully!");
      } else {
        await axios.post("http://127.0.0.1:5000/events/add_event", newEvent, {
          headers: { Authorization: token },
        });
        alert("Event added successfully!");
      }
      setIsModalOpen(false);
      setIsEditing(false);
      setCurrentEventId(null);
      fetchEvents();
    } catch (error) {
      console.error("Error saving event:", error);
      alert("Failed to save the event. Please try again.");
    }
  };

  const handleEditEvent = (event) => {
    setNewEvent({
      title: event.title,
      date: event.date,
      time: event.time,
      location: event.location,
      description: event.description,
      price: event.price,
      TotalCount: event.TotalCount,
      Points: event.Points,
      EventType: event.EventType,
    });
    setCurrentEventId(event._id);
    setIsEditing(true);
    setIsModalOpen(true);
  };

  const handleDeleteEvent = async (eventId) => {
    if (window.confirm("Are you sure you want to delete this event?")) {
      try {
        const token = localStorage.getItem("token");
        await axios.delete(`http://127.0.0.1:5000/events/delete_event/${eventId}`, {
          headers: { Authorization: token },
        });
        alert("Event deleted successfully!");
        fetchEvents();
      } catch (error) {
        console.error("Error deleting event:", error);
        alert("Failed to delete the event. Please try again.");
      }
    }
  };

  const handleTakeAttendance = (eventId) => {
    setCurrentEventId(eventId);
    setIsAttendanceModalOpen(true);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/");
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setIsEditing(false);
    setNewEvent({
      title: "",
      date: "",
      time: "",
      location: "",
      description: "",
      price: 0,
      Points: 0,
      EventType: "",
      TotalCount: 0,
    });
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
                onClick={() => navigate("/adminprofile")}
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

      <div className="py-10 px-10">
        <h1 className="text-3xl font-bold text-center mb-6">Admin Dashboard</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {events.map((event) => (
            <EventCard
              key={event._id}
              event={event}
              onEdit={() => handleEditEvent(event)}
              onDelete={() => handleDeleteEvent(event._id)}
              onTakeAttendance={() => handleTakeAttendance(event._id)}
            />
          ))}
        </div>
      </div>

      <button
        onClick={() => {
          setIsModalOpen(true);
          setIsEditing(false);
        }}
        className="fixed bottom-4 right-4 bg-blue-500 text-white font-semibold py-3 px-5 rounded-lg shadow-lg hover:bg-blue-700"
      >
        Add New Event
      </button>

      {isModalOpen && (
        isEditing ? (
          <EditEventModal
            newEvent={newEvent}
            setNewEvent={setNewEvent}
            handleAddEvent={handleAddEvent}
            onClose={handleCloseModal}
          />
        ) : (
          <AddEventModal
            newEvent={newEvent}
            setNewEvent={setNewEvent}
            handleAddEvent={handleAddEvent}
            onClose={handleCloseModal}
          />
        )
      )}

      {isAttendanceModalOpen && (
        <TakeAttendanceModal
          eventId={currentEventId}
          onClose={() => setIsAttendanceModalOpen(false)}
          fetchEvents={fetchEvents}
        />
      )}
    </div>
  );
}

export default AdminDashboard;