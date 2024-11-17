import './App.css';
import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './Login';
import CpuPreference from './CpuPreference';
import SignUp from './SignUp';

function App() {
  return (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/signup" element={<SignUp />} />
      <Route path="/cpu-preference" element={<CpuPreference />} />
    </Routes>
  </BrowserRouter>
  );
}

export default App;


// function App() {

//   const [page, setPage] = useState('cpuPreference');

//   const renderPage = () => {
//     if (page === 'login'){
//       return <Login goToSignUp = {() => setPage('signUp')} 
//                     goToCpuPreference = {() => setPage('cpuPreference')} />;
//     } else if (page === 'signUp'){
//       return <SignUp goToLogin={() => setPage('login')} />;
//     } else if (page === 'cpuPreference'){
//       return <CpuPreference />;
//     }
//   };

//   return (
//     <div>
//       {renderPage()}
//     </div>
//   );
// }

// export default App;
