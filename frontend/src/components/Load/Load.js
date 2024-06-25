import Typography from '@mui/material/Typography';
import Logo from '../../logo.svg';
import { useMediaQuery } from '@mui/material';
import './Load.css'; 

export default function Load({ theme_color }) {
    const isSmallScreen = useMediaQuery('(max-width:600px)');
    const isMediumScreen = useMediaQuery('(min-width:601px) and (max-width:1200px)');

    return (
        <div className='load_box' style={{
            color: theme_color.contrastText,
            textAlign: 'center'
        }}>
            <img 
                src={Logo} 
                alt='Logo' 
                width={isSmallScreen ? '100px' : isMediumScreen ? '150px' : '200px'} 
                className='rotate'
            />
            
        </div>
    );
}
