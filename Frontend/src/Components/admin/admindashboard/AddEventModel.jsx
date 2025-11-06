import React from "react";

function AddEventModal({ newEvent, setNewEvent, handleAddEvent, onClose }) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">Add New Event</h2>
        <form onSubmit={handleAddEvent} className="space-y-4">
          {[
            { name: "title", type: "text", label: "Title" },
            { name: "date", type: "date", label: "Date" },
            { name: "time", type: "time", label: "Time" },
            { name: "location", type: "text", label: "Location" },
            { name: "description", type: "textarea", label: "Description" },
            { name: "price", type: "number", label: "Price" },
            { name: "TotalCount", type: "number", label: "Total Count" },
            { name: "Points", type: "number", label: "Points" },
          ].map(({ name, type, label }) => (
            <div key={name}>
              <label className="block text-gray-700 font-bold mb-2">{label}:</label>
              {type === "textarea" ? (
                <textarea
                  name={name}
                  rows="3"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  value={newEvent[name]}
                  onChange={(e) => setNewEvent({ ...newEvent, [name]: e.target.value })}
                  required
                />
              ) : (
                <input
                  type={type}
                  name={name}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  value={newEvent[name]}
                  onChange={(e) =>
                    setNewEvent({
                      ...newEvent,
                      [name]: type === "number" ? Number(e.target.value) : e.target.value,
                    })
                  }
                  required
                />
              )}
            </div>
          ))}

          {/* Dropdown for EventType */}
          <div>
            <label className="block text-gray-700 font-bold mb-2">Event Type:</label>
            <select
              name="EventType"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              value={newEvent.EventType}
              onChange={(e) => setNewEvent({ ...newEvent, EventType: e.target.value })}
              required
            >
              <option value="">Select Event Type</option>
              <option value="Tech">Tech</option>
              <option value="NonTech">NonTech</option>
            </select>
          </div>

          <div className="flex space-x-4 mt-6">
            <button type="submit" className="bg-blue-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700">
              Add Event
            </button>
            <button
              type="button"
              onClick={onClose}
              className="bg-gray-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-gray-700"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddEventModal;