import './CpuPreference.css'
import React, { useState } from 'react'
import App, { setPage, renderPage } from './App.js'
import Login from './Login.js'
import SignUp from './SignUp.js'

function CpuPreference() {

  const [allocation, setAllocation] = useState('')

  return (
    <div>
        <h2 class = 'container'>What is your CPU allocation preference?</h2>
        <div class = 'container'>
            <button class = 'expand-button' onClick = {() => {setAllocation('low')}}>
                <span class = 'button-text'>Low allocation</span>
                <span class = 'hover-text'>You'll allocate lower CPU, <br /> get into some learning modules!</span>
            </button>
            <button class = 'expand-button' onClick = {() => setAllocation('high')}>
                <span class = 'button-text'>High allocation</span>
                <span class = 'hover-text'>You'll allocate higher CPU, <br /> take some time to do some chill reading!</span>
            </button>
        </div>
    </div>
  );

}

export default CpuPreference;
