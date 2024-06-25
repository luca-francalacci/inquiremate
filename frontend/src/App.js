import './App.css';
import { createTheme } from '@mui/material/styles';
import { useState } from "react";
import { IndexContext } from './context';
import Footer from './components/Footer/Footer'
import AppBar from './components/AppBar/AppBar';
import AppContent from './components/AppContent/AppContent';
import Scraping from './components/Scraping/Scraping'
import Query from './components/Query/Query'


const primary = {
  main: '#673ab7',
  light: '#8561c5',
  dark: '#482880',
  contrastText: 'white'
}


let select_color = primary

export const theme = createTheme({
  palette: {
    select_color,
    border:{
      borderRadius: 1
    }
  },
  components: {
    MuiSwitch: {
      styleOverrides: {
        switchBase: {
          color: select_color.contrastText // Controls default (unchecked) color for the thumb
        },
        colorPrimary: {
          "&.Mui-checked": {
            color: select_color.contrastText // Controls checked color for the thumb
          }
        },
        track: {
          opacity: 0.7, // Controls default (unchecked) opacity for the track
          backgroundColor: select_color.light, // Controls default (unchecked) color for the track
          ".Mui-checked.Mui-checked + &": {
            opacity: 0.7, // Controls checked opacity for the track
            backgroundColor: select_color.light // Controls checked color for the track
          }
        }
      }
    }
  }
});

let theme_color=theme.palette.select_color


function App() {
  const [indexPage, setIndexPage] = useState(false)
  let menu = {
    'Scraping': <Scraping theme_color={theme_color}/>,
    'Query': <Query theme_color={theme_color}/>
  }
  
  
  return (
  <IndexContext.Provider value={[indexPage, setIndexPage]}>
    
    <div className="App" style={{
          backgroundColor:theme_color.light
        }}>
          {/* menù */}
          <AppBar theme_color={theme_color} menu={menu}/>
          {/* resto */}
          <div  className="box_app">
            <AppContent theme_color={theme_color} menu={menu}/>
          </div>
          <Footer className="footer" theme={theme_color}/>
    </div>
  </IndexContext.Provider>
  )
}
export default App;
