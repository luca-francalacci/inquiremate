import * as React from 'react';
import ResponsiveAppBar from "./ResponsiveAppBar";
import SubAppBar from "./SubAppBar"
import {IndexContext} from '../../context'

export default function AppBar({theme_color,menu }){
    const context = React.useContext(IndexContext)

    let ris=<ResponsiveAppBar theme_color={theme_color}  menu={menu}/>

    if(context[0] !== false){
        ris = <>
            {ris}
            <SubAppBar  theme_color={theme_color}/>
        </>
    }
    
    return ris
    
}