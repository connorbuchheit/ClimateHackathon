import React from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    // Logic for login, then redirect to the next page
    navigate('/cpu-preference'); // Redirect to CpuPreference page
  };

  const handleSignUp = () => {
    // Redirect to the sign-up page
    navigate('/signup');
  };

  return (
    <div>
      <h2>Login</h2>
      <button onClick={handleLogin}>Login</button>
      <button onClick={handleSignUp}>Sign Up</button>
    </div>
  );
};

export default Login;
