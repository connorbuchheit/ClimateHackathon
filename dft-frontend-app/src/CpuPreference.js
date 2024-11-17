import './CpuPreference.css'
import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom';

const CpuPreference = ({allocation, setAllocation}) => {

  const navigate = useNavigate();

  const handlePreference = (pref) => {
    setAllocation(pref);
    navigate('/services');
  }; 

  return (
    <div>
        <h2 class = 'container'>What is your CPU allocation preference?</h2>
        <div class = 'container'>
            <button class = 'expand-button' onClick = {() => handlePreference('low')}>
                <span class = 'button-text'>Low allocation</span>
                <span class = 'hover-text'>You'll allocate lower CPU, <br /> get into some learning modules!</span>
            </button>
            <button class = 'expand-button' onClick = {() => handlePreference('high')}>
                <span class = 'button-text'>High allocation</span>
                <span class = 'hover-text'>You'll allocate higher CPU, <br /> take some time to do some chill reading!</span>
            </button>
        </div>
    </div>
  );

}

export default CpuPreference;
