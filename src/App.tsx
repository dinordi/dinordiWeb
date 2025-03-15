import { useState } from "react";
import axios from "axios";
import "./App.css";

const services = ["pikaraoke-ledfx", "spotify-ledfx"];

function App() {
  const [status, setStatus] = useState<{ [key: string]: string }>({});

  const handleAction = async (service: string, action: string) => {
    try {
      await axios.post(`http://localhost:5000/${action}/${service}`);
      checkStatus(service);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const checkStatus = async (service: string) => {
    try {
      const response = await axios.get(`http://localhost:5000/status/${service}`);
      console.log("Status:", response.data.service);
      setStatus((prev) => ({ ...prev, [service]: response.data.status }));
    } catch (error) {
      console.error("Error fetching status:", error);
    }
  };

  return (
    <div>
      <h1>Service Controller</h1>
      {services.map((service) => (
        <div key={service}>
          <h3>{service}: {status[service] || "Unknown"}</h3>
          <button onClick={() => handleAction(service, "start")}>Start</button>
          <button onClick={() => handleAction(service, "stop")}>Stop</button>
          <button onClick={() => checkStatus(service)}>Check Status</button>
        </div>
      ))}
    </div>
  );
}

export default App;