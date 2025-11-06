import React from "react";

function EventCard({ event, onEdit, onDelete, onTakeAttendance }) {
  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h3 className="text-xl font-bold">{event.title}</h3>
      <p className="text-gray-600 font-semibold italic border-l-4 border-blue-500 pl-4 my-2">
        {event.description}
      </p>
      <p className="text-gray-600">Date: {event.date}</p>
      <p className="text-gray-600">Time: {event.time}</p>
      <p className="text-gray-600">Location: {event.location}</p>
      <p className="text-gray-600">Type: {event.EventType}</p>
      <p className="text-gray-600">Points: {event.Points}</p>
      <p className="text-gray-600">Slots Left: {event.SlotsLeft}</p>
      <div className="flex space-x-4 mt-4">
        <button
          onClick={onEdit}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Edit
        </button>
        <button
          onClick={onDelete}
          className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Delete
        </button>
        <button
          onClick={onTakeAttendance} // Trigger the onTakeAttendance function
          className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Take Attendance
        </button>
      </div>
    </div>
  );
}

export default EventCard;