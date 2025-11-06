import React from "react";

function EventCard({ event, onRegister }) {
  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h3 className="text-xl font-bold">{event.title}</h3>
      <p className="text-gray-600 font-semibold italic border-l-4 border-blue-500 pl-4 my-2">
        {event.description}
      </p>
      <p className="text-gray-600">Date: {event.date}</p>
      <p className="text-gray-600">Time: {event.time}</p>
      <p className="text-gray-600">Location: {event.location}</p>
      <p className="text-gray-600">Slots Left: {event.SlotsLeft}</p>
      <p className="text-gray-600">Price: {event.price}</p>
      <button
        onClick={() => onRegister(event._id)}
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Register
      </button>
    </div>
  );
}

export default EventCard;