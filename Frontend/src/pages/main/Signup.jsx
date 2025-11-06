import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Header from "../../Components/main/Header.jsx"; // Corrected path
import Footer from "../../Components/main/Footer.jsx"; // Corrected path
import axios from 'axios';

export default function Signup() {
  const [username, setUsername] = useState('');
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState('USER');

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    const userData = {
      username,
      full_name: fullName,
      email,
      phone_number: phoneNumber,
      password,
      confirm_password: confirmPassword, // Ensure this matches the server-side key
      role,
    };

    try {
      const response = await axios.post('http://127.0.0.1:5000/auth/register', userData);
      alert(response.data.message);
      navigate('/login');
    } catch (error) {
      alert('Signup failed: ' + error.response.data.message);
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Header />
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32">
          <div className="container mx-auto px-4 md:px-6">
            <div className="flex flex-col items-center space-y-4 text-center">
              <h1 className="text-3xl font-bold tracking-tighter md:text-4xl">
                Create Your Account
              </h1>
              <form onSubmit={handleSubmit} className="w-full max-w-sm space-y-4">
                <input
                  type="text"
                  placeholder="Username"
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
                <input
                  type="text"
                  placeholder="Full Name"
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  required
                />
                <input
                  type="email"
                  placeholder="Email"
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <input
                  type="text"
                  placeholder="Phone Number"
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Password"
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <input
                  type="password"
                  placeholder="Confirm Password"
                  className="w-full px-3 py-2 border border-gray-300 rounded"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
                <div className="flex space-x-4">
                  <label>
                    <input
                      type="radio"
                      name="role"
                      value="USER"
                      checked={role === 'USER'}
                      onChange={() => setRole('USER')}
                      className="mr-2"
                    />
                    User
                  </label>
                  <label>
                    <input
                      type="radio"
                      name="role"
                      value="ADMIN"
                      checked={role === 'ADMIN'}
                      onChange={() => setRole('ADMIN')}
                      className="mr-2"
                    />
                    Admin
                  </label>
                </div>

                <button
                  type="submit"
                  className="w-full px-4 py-2 bg-black text-white rounded hover:bg-gray-800"
                >
                  Sign Up
                </button>
              </form>
              <p className="text-gray-500">
                Already have an account? <Link to="/login" className="underline">Login</Link>
              </p>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}