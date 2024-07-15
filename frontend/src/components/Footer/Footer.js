import './Footer.css'
import React from 'react'
export default function Footer({theme}){

    return(
        <footer style={{
            backgroundColor:theme.dark,
            zIndex:999
        }}>

        </footer>
    )
}