import logo from './logo.svg';
import './App.css';
import Map from './pages/Map';
import Preloader from './pages/Preloader';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

function App() {
  return (
    <div className="App">
     <Router>
        <Routes>

          <Route path='/' exact element={<Preloader/>} />
          <Route path='/map' exact element={<Map />} />
            <Route path='*' element={<Preloader />} /> 
        </Routes>
     </Router>
     
    </div>
  );
}

export default App;
