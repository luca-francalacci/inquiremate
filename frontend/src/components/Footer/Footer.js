import './Footer.css'
import React from 'react'
export default function Footer({theme}){
    console.log("FOOTER")
    
    React.useEffect(()=>{
        
    },[])
    

    return(
        <footer style={{
            backgroundColor:theme.dark,
            zIndex:999
        }}>

        </footer>
    )
}