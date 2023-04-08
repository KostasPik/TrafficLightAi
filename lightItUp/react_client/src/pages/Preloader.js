import React from 'react'
import './Preloader.css'
import TrafficLightImage from '../assets/traffic.png'
import { Link } from 'react-router-dom'
function Preloader() {
  return (
    <div id='preloader'>    
        <h1 class="title">L<img src={TrafficLightImage}></img>ghtItUp</h1>
        <div class="loading-window">
            <div class="car">
                <div class="strike"></div>
                <div class="strike strike2"></div>
                <div class="strike strike3"></div>
                <div class="strike strike4"></div>
                <div class="strike strike5"></div>
                <div class="car-detail spoiler"></div>
                <div class="car-detail back"></div>
                <div class="car-detail center"></div>
                <div class="car-detail center1"></div>
                <div class="car-detail front"></div>
                <div class="car-detail wheel"></div>
                <div class="car-detail wheel wheel2"></div>
            </div>
        
            {/* <div class="text">
                <span>Loading</span><span class = "dots">...</span>
            </div> */}
        </div>
        <div className='nav-button'>
        <Link id="preloader-button" to='/map/'>View Map</Link>

        </div>
        
    </div>

  )
}

export default Preloader