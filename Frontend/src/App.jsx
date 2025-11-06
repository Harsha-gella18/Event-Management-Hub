import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from "./pages/main/Home.jsx";
import Signup from './pages/main/Signup.jsx';
import UserDashboard from './pages/users/UserDashboard.jsx';
import AdminDashboard from './pages/admin/AdminDashboard.jsx';
import ProtectedRoute from './Components/main/ProtectedRoute.jsx';
import Profile from './pages/admin/AdminProfile.jsx';
import UserProfile from './pages/users/UserProfile.jsx'; // Import UserProfile

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Home />} />
        <Route path="/signup" element={<Signup />} />

        {/* Protected Routes */}
        <Route
          path="/user-dashboard"
          element={
            <ProtectedRoute allowedRoles={['USER', 'ADMIN']}>
              <UserDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admindashboard"
          element={
            <ProtectedRoute allowedRoles={['ADMIN']}>
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/adminprofile"
          element={
            <ProtectedRoute allowedRoles={['ADMIN']}>
              <Profile />
            </ProtectedRoute>
          }
        />
        <Route
          path="/userprofile"
          element={
            <ProtectedRoute allowedRoles={['USER']}>
              <UserProfile />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;