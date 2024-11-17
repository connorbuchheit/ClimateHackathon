import './App.css';
import React, {useState} from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './Login';
import CpuPreference from './CpuPreference';
import SignUp from './SignUp';
import Services from './Services'

const App = () => {
  const [allocation, setAllocation] = useState('')

  return (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/cpu-preference" element={<CpuPreference allocation = {allocation} setAllocation = {setAllocation}/>} />
      <Route path="/services" element={<Services allocation = {allocation} setAllocation = {setAllocation}/>} />
    </Routes>
  </BrowserRouter>
  );
}

export default App;