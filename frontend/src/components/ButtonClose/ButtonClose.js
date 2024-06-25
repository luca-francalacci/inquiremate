import * as React from 'react';
import Button from '@mui/material/Button';
import CloseIcon from '@mui/icons-material/Close';

export default function ButtonClose({ theme_color, onValueChange  }) {

  function handleClickButton(){
    onValueChange(false)
  }

  return (
    <Button
      variant="contained"
      onClick={handleClickButton} // Passa la funzione per gestire il clic
      style={{
        backgroundColor: theme_color.light,
        paddingRight: 0,
        paddingLeft: 0,
      }}
    >
        <CloseIcon />
    </Button>
  )
}
