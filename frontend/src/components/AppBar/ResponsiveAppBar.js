import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import Logo from '../../logo.svg';

import {IndexContext} from '../../context'

export default function ResponsiveAppBar({ theme_color, menu }) {
  const context = React.useContext(IndexContext)
  const pages = [];
  
  for (let key in menu) {
    pages.push(key);
  }

  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [currentPage, setCurrentPage] = React.useState(false);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  function handleSetPage(page) {
    setCurrentPage(page);
    context[1](page);
    // onIndexPageChange(page);
  }

  return (
    <AppBar position="static"
      style={{zIndex:1000}}
      sx={{
        backgroundColor: theme_color.dark
      }}>
      <Container maxWidth="xl">
        <Toolbar disableGutters>

          {/*----- SCHERMO INTERO -----*/}
          <Box
            component="img"
            src={Logo}
            alt="Logo"
            sx={{ display: { xs: 'none', md: 'flex' }, width: '50px', marginRight: '10px' }}
          />

          <Typography
            variant="h6"
            noWrap
            component="a"
            href=""
            sx={{
              mr: 2,
              display: { xs: 'none', md: 'flex' },
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            InquireMate
          </Typography>

          {/*----- SCHERMO RIDOTTO -----*/}
          {/* menù quando riduco lo schermo */}
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
                '& .MuiPaper-root': {
                  backgroundColor: theme_color.main, // Aggiungi questa linea
                },
              }}
            >
              {pages.map((page) => (
                <MenuItem
                  style={{
                    backgroundColor: theme_color.main,
                    color: theme_color.contrastText,
                  }}
                  key={page}
                  onClick={() => { handleSetPage(page); handleCloseNavMenu(); }} >
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>

          <Typography
            variant="h5"
            noWrap
            component="a"
            href=""
            sx={{
              mr: 2,
              display: { xs: 'flex', md: 'none' },
              flexGrow: 1,
              fontFamily: 'monospace',
              fontWeight: 700,
              letterSpacing: '.3rem',
              color: 'inherit',
              textDecoration: 'none',
            }}
          >
            InquireMate
          </Typography>

          {/* menù schermo intero */}
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {pages.map((page) => (
              <Button
                key={page}
                onClick={() => { handleSetPage(page); handleCloseNavMenu(); }}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                {page}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
}
