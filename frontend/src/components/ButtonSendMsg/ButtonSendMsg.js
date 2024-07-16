import * as React from 'react';
import Button from '@mui/material/Button';
import SendIcon from '@mui/icons-material/Send';

export default function ButtonSendMsg({ theme_color, onValueChange  }) {
  function handleClickButton(){
    onValueChange("ciao")
  }

  return (
    <Button
      variant="contained"
      endIcon={<SendIcon />}
      onClick={handleClickButton}
      style={{
        backgroundColor: theme_color.light
      }}
    >
      Invia
    </Button>
  )
}
