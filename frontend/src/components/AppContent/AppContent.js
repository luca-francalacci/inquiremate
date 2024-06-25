import React from 'react';
import Home from '../Home/Home'
import {IndexContext} from '../../context'

export default function AppContent({theme_color,menu}){
    const context = React.useContext(IndexContext)
    let index=context[0]
    
    if (index in menu){
        return(menu[index])
    } else {
        return(<Home theme_color={theme_color}/>)
    }
}