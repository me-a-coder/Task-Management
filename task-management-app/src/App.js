import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './Sidebar';
import Dashboard from './Dashboard';
import Logout from './Logout';
import Login from './Login'; 

function App() {
  return (
    <Router>
      <div>
        <Sidebar />  
        <div className="main-content">
          <Routes>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<Dashboard />}/>
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
