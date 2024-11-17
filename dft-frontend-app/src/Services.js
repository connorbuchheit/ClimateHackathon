import React, { useState, useEffect } from "react";
import "./Services.css"; // Move the CSS here for modularity
import { useNavigate } from 'react-router-dom';

const Services = ({allocation, setAllocation}) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [services, setServices] = useState([])
  const navigate = useNavigate();

  // Sample service data

  useEffect(() => {
    if (allocation === "high") {
      setServices([
        { id: 1, name: "Service 1" },
        { id: 2, name: "Service 2" },
        { id: 3, name: "Service 3" },
        { id: 4, name: "Service 4" },
        { id: 5, name: "Service 5" },
        { id: 6, name: "Service 6" },
        { id: 7, name: "Log Out"}]
       );
    } else {
      setServices([{ id: 1, name: "Service 1" },
        { id: 2, name: "Service 2" },
        { id: 3, name: "Service 3" },
        { id: 7, name: "Log Out"}]);
    }
  }, [allocation]);
  
  // Filtered services based on the search term
  const filteredServices = services.filter((service) =>
    service.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Handle service click
  const handleServiceClick = (serviceName) => {
    if(serviceName === 'Log Out'){
        navigate("/");
    }
    alert(`You clicked on ${serviceName}`);
  };

  return (
    <div className="services">
      <h1>SES AI Services</h1>

      {/* Search Bar */}
      <input
        type="text"
        placeholder="Search services..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="search-bar"
      />

      {/* Services Grid */}
      <div className="grid">
        {filteredServices.map((service) => (
          <div
            key={service.id}
            className="grid-item"
            onClick={() => handleServiceClick(service.name)}
          >
            {service.name}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Services;
