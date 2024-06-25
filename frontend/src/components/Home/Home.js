import Typography from '@mui/material/Typography';
import Logo from '../../logo.svg';
import { useMediaQuery } from '@mui/material';
import Load from '../Load/Load';

export default function Home({ theme_color }) {
    const isSmallScreen = useMediaQuery('(max-width:600px)');
    const isMediumScreen = useMediaQuery('(min-width:601px) and (max-width:1200px)');

    return (
        <div className='home_box' style={{
            color: theme_color.contrastText,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            padding: '20px',
            textAlign: 'center'
        }}>
            <img 
                src={Logo} 
                alt='Logo' 
                width={isSmallScreen ? '100px' : isMediumScreen ? '150px' : '200px'} 
            />
            <Typography
                noWrap
                sx={{
                    fontSize: isSmallScreen ? 30 : isMediumScreen ? 40 : 50,
                    mr: 2,
                    fontFamily: 'monospace',
                    fontWeight: 700,
                    letterSpacing: '.3rem',
                    textDecoration: 'none',
                    textAlign: 'center',
                }}
            >
                InquireMate
            </Typography>
            <div>v. <i>alpha</i></div>
        </div>
    );
}
