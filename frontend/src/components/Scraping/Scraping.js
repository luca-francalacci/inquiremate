import * as React from 'react' 
import Typography from '@mui/material/Typography';
import ButtonSendMsg from '../ButtonSendMsg/ButtonSendMsg'
import SelectNumPag from '../SelectNumPag/SelectNumPag'
import InputText from '../InputText/InputText' 
import loadSVG from '../../img/load.svg'
import Popup from '../Popup/Popup' 
import './Scraping.css'
import Load from '../Load/Load';

export default function Scraping({theme_color}){
    
    const list_n_query = [3, 5, 7]
    const [newQuery, setNewQuery] = React.useState('') 
    const [numUrl, setNumUrl] = React.useState(null)
    const [load, setLoad] = React.useState(false) 
    const [apiResult, setApiResult] = React.useState(
      "In attesa: di una domanda o di un url. \n Scraping delle pagine web attraverso la ricerca su Google oppure attraverso l'utilizzo di un url specifico."
    )
    const [buttonClose, setButtonClose] = React.useState(false)
    const [listLink, setListLink] = React.useState([])
    const [queryError,setQueryError] = React.useState('')
    const [urlError,setUrlError] = React.useState(null)


    function changeQuery(event){
      setNewQuery(event)
      setQueryError('')
    }

    function changeUrl(event){
      setNumUrl(event)
      setUrlError('')
    }
    

    function onValueChange() {
      console.log('newQuery: '+newQuery.length)
      console.log('numUrl: '+numUrl)

      if(newQuery.length>0 && numUrl!=null){
        setLoad(true)
        
        // CHIAMATA API PER OTTENERE I LINK
        let fetch_api="http://127.0.0.1:8000/inquireMate/web_search"

        let postData = {
          "query": newQuery,
          "n": numUrl
        }

        fetch(fetch_api, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
          setListLink(data)
          setButtonClose(true)
          listLink.forEach(element => {
            console.log(element)
          });
          setLoad(false)
        })
        .catch(error => {
          console.error('Errore nella richiesta fetch:', error)
          setLoad(false)
        })
        
      } else {
        if(newQuery.length<1){
          console.log(newQuery==null)
          console.log(isNaN(newQuery))
          setQueryError('* digitare una domanda')
        }
        if(numUrl==null){
          setUrlError('* selezionare un numero')
        }
      }
    }
    
    function changeButtonClose(event){
      console.log("[InquireMate] changeButtonClose: "+event)
      setButtonClose(event)
      console.log(buttonClose)
    }
      
    return (<>
      <div className='box_di_prova'>

        {buttonClose?(
          <Popup 
            theme_color={theme_color} 
            changeButtonClose={changeButtonClose} 
            list_link={listLink}
          />):(<></>)}
          
          <div className='InquireMate_query'
            style={{
              backgroundColor: theme_color.dark,
              color: theme_color.contrastText,
              elevation: 3,
            }}>
            <InputText theme_color={theme_color} label={"Chiedimi qualcosa"} setInput={changeQuery} />
          
            <div id='div_error'>{queryError}</div>
            <div className='div_num_res'>
                <div style={{
                  display: 'flex',
                  width: '50%',
                  justifyContent: 'right'
                }}>
                  <Typography>Numero di risultati</Typography>
                </div>
              <div style={{
                width: '50%', 
                textAlign: 'center'
                }}>
                  <div style={{
                      width:'100px'
                    }}>
                    <SelectNumPag theme_color={theme_color} data={list_n_query} changeValue={changeUrl} />
                  </div>
                
              </div>
            </div>
          
            
            <div id='div_error'>{urlError}</div>
            <ButtonSendMsg theme_color={theme_color} onValueChange={onValueChange} />
          </div>
          {/* Mostra l'immagine di caricamento solo quando load è true */}
          {load ?  
            <div className='load_box'>
              <div className='load'>
                <Load theme_color={{theme_color}}/>
              </div>
            </div>: 
          null}
        </div>
    </>) 
  }