import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';


export default function InputText({ theme_color, label, setInput, type='text' }) {

  function handleInputChange (event){
    setInput(event.target.value)
  }

  return (
    <Box sx={{ 
        '& > :not(style)': {width:'100%', borderColor:'transparent' }
    }}>
    <TextField
        id="outlined-controlled"
        label={label}
        type={type}
        onChange={handleInputChange}
        sx={{ 
            backgroundColor: theme_color.main, 
            color: theme_color.contrastText, 
            borderRadius: '5px',
            '& .MuiSelect-icon': {
              fill: theme_color.contrastText, 
            },        
        }}
        
        InputProps={{ 
          style: { 
            color: theme_color.contrastText 
          } 
        }}
        
        InputLabelProps={{
            style: { 
                color: theme_color.contrastText, 
            } 
        }}
    />

    </Box>
  );
}
