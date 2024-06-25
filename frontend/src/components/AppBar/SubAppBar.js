import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import {IndexContext} from '../../context'


export default function SubAppBar({ theme_color}) {
  const context = React.useContext(IndexContext)

  return (<>
    <AppBar className='responsive_app_bar' position="static" elevation={0} 
      style={{zIndex:998}}
      sx={{
        backgroundColor: theme_color.main
        }}>
      <Container maxWidth="xl">
        <Toolbar >
          <Box sx={{ 
            flexGrow: 1 
          }}>
          </Box>
          <Typography
            variant="h5"
            noWrap
            sx={{
              mr: 2,
              display: { xs: 'flex', md: 'flex' },
              flexGrow: 1,
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
              textAlign: 'center' 
            }}
          >
            {context[0]}
          </Typography>
        </Toolbar>
      </Container>
    </AppBar>
    </>
  );
}
