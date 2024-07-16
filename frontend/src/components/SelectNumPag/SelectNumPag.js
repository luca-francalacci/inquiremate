import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import ArrowDropDownIcon from '@mui/icons-material/ArrowDropDown';


export default function SelectNumPag({ theme_color, data, label, changeValue }) {
  const [valSelect, setValSelect] = React.useState('');

  const handleChange = (event) => {
    setValSelect(event.target.value);
    changeValue(event.target.value)
  };

  return (
    <Box>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label"
          sx={{
            color: theme_color.contrastText,
            '&.Mui-focused': {
              color: theme_color.contrastText
            },
            
          }}>{label}</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={valSelect}
          label={label}
          onChange={handleChange}
          IconComponent={ArrowDropDownIcon}
          sx={{
            backgroundColor: theme_color.main,
            color: theme_color.contrastText,
            borderRadius: theme_color.borderRadius,
            '& .MuiSelect-icon': {
              fill: theme_color.contrastText,
            },
          }}
          MenuProps={{
            PaperProps:{
              style:{

                backgroundColor: theme_color.main,
                color: theme_color.contrastText
              }
            }
          }}

        >
          {
            data.map((item,i) => (
              <MenuItem 
                key={i} 
                value={item}
                sx={{
                  '&:hover':{
                    backgroundColor:theme_color.light,
                  }
                }}
                >{item}</MenuItem>
            ))
          }
        </Select>
      </FormControl>
    </Box>
  );
}
