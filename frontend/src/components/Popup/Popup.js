import * as React from 'react';
import Modal from '@mui/material/Modal';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import ButtonSendMsg from '../ButtonSendMsg/ButtonSendMsg';
import ButtonClose from '../ButtonClose/ButtonClose';
import './Popup.css'
import loadSVG from '../../img/load.svg';
import InputText from '../InputText/InputText';
import { Checkbox } from '@mui/material';

import Load from '../Load/Load';

export default function Popup({ theme_color, changeButtonClose, list_link ,setRequestOkay}) {

    const rootRef = React.useRef(null);
    const [selectedLink, setSelectedLink] = React.useState(null);
    const [selectionDepth,setSelectionDepth] = React.useState(null)
    const [load, setLoad] = React.useState(false)
    const [depthError, setDepthError] = React.useState('')
    const [linkError, setLinkError] = React.useState('')
    const [isChecked, setIsChecked] = React.useState(false);

    // const list_metadata = ['Arte', 'Cucina', 'Cultura', 'Narrativa', 'Natura', 'Scienza', 'Sport', 'Hobby']
    // const [selectedDate, setSelectedDate] = React.useState( Array.from({ length: list_metadata.length }, _ => false)) 


    const customStyles = {
        radio: {
            color: theme_color.light, // colore del selettore
            '&.Mui-checked': {
                color: theme_color.contrastText, // colore elemento selezionato
            },
        },
    };

    function changeSelectedLink(event) {
        setSelectedLink(event.target.value);
        setLinkError(null)
    }

    function changeSelectionDepth(event){
        setSelectionDepth(parseInt(event));
        setDepthError(null)
    }

    React.useEffect(() => {
    },[depthError,linkError])

    function sendMsg() {
        console.log("selectedLink: "+selectedLink) 
        console.log("selectedLink: "+isNaN(selectedLink)) 

        if((selectionDepth!=null && selectionDepth > -1 && !isNaN(selectionDepth)) && 
            selectedLink!=null){
                setLoad(true)

                // CHIAMATA API PER LO SCRAPING
                let post_data = {
                    'http': selectedLink,
                    'd': selectionDepth,
                    'summary': isChecked
                }
                console.log(post_data)

                let fetch_api = 'http://127.0.0.1:8000/inquireMate/scraping_embedding'

                fetch(fetch_api, {
                    method: 'POST',
                    headers:{
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(post_data)
                })
                .then(response => response.json())
                .then(data => {
                    if(data==false){
                        setRequestOkay("Riprovare")
                    } else{
                        const url = window.URL.createObjectURL(new Blob([JSON.stringify(data)]))
                        const link = document.createElement('a')
                        link.href = url
                        link.setAttribute('download', 'file.json')
                        document.body.appendChild(link)
                        link.click()
                        setRequestOkay("Eseguita con successo!")
                    }
                    setLoad(false)
                    changeButtonClose(false)
                    
                })
                .catch(error => {
                    console.log("C'è stato un errore")
                // Imposta load su false in caso di errore
                    setLoad(false)
                    changeButtonClose(false)
                    setRequestOkay("Riprovare")

                })
        } else {
            if(selectedLink == null){
                setLinkError('* selezionare un url')
            }
            if(selectionDepth < 0 || selectionDepth == null || isNaN(selectionDepth)){
                setDepthError('* inserire una profondità valida')
            }
        }
    }

    return (
        <Box ref={rootRef}>
            <Modal
                disablePortal
                disableEnforceFocus
                disableAutoFocus
                open
                aria-labelledby="server-modal-title"
                aria-describedby="server-modal-description"
                sx={{
                    display: 'flex',
                    p: 1,
                    alignItems: 'center',
                    justifyContent: 'center',
                    rowGap: '100px'

                    
                }}
                container={() => rootRef.current}
            >
                <Box
                    sx={{
                        position: 'relative',
                        width: 300,
                        bgcolor: theme_color.dark,
                        color: theme_color.contrastText,
                        borderRadius: 2,
                        boxShadow: (theme) => theme.shadows[5],
                        p: 2,
                    }}
                    >
                    {load ? 
                        <div className='load_box'>
                            <div className='load'>
                                <Load theme_color={{theme_color}}/>
                                
                            </div>
                        </div>: 
                    null}
                    <Box sx={{ 
                        display: 'flex', 
                        justifyContent: 'space-between', 
                        paddingLeft:'10px', 
                        paddingRight:'10px', 
                        paddingBottom:'10px', 
                        alignItems:'center' 
                        }}>
                        <Typography id="server-modal-title" variant="h6" component="h2">
                            Selezionare l'url
                        </Typography>
                        <Box sx={{ 
                                display: 'flex', 
                                justifyContent: 'flex-end'
                            }}>
                            <ButtonClose
                                theme_color={theme_color}
                                onValueChange={changeButtonClose}
                            />
                        </Box>
                    </Box>
                    <div className='popup_box'>
                    
                        <RadioGroup onChange={changeSelectedLink}>
                            {list_link.map(url => (
                                <FormControlLabel
                                    key={url}
                                    value={url}
                                    control={<Radio sx={customStyles.radio} />}
                                    label={url.split('/')[2]}
                                />
                            ))}
                        </RadioGroup>
                        <div id='div_error'>{linkError}</div>

                        <Box sx={{
                            display: 'flex',
                            flexDirection: 'row',
                            alignItems: 'center',
                            justifyContent: 'space-between',
                            gap: '30px'
                        }}>
                            <Typography id="server-modal-title" variant="h6" component="h2">
                                Profondità
                            </Typography>
                            <div style={{
                                width: '100px', 
                                textAlign: 'center'
                                }}>
                                    <InputText theme_color={theme_color} label={""} setInput={changeSelectionDepth} type='number' />
                            </div>
                        </Box>
                        <div id='div_error'>
                            {depthError}
                        </div>
                        
                        <ButtonSendMsg 
                            theme_color={theme_color} 
                            onValueChange={sendMsg} 
                        />
                    </div>
                </Box>
            </Modal>
        </Box>
    );
}
