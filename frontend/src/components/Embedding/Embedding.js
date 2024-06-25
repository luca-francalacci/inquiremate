import * as React from 'react' 
import ButtonSendMsg from '../ButtonSendMsg/ButtonSendMsg'
// import './Scraping.css'
import SelectNumPag from '../SelectNumPag/SelectNumPag'
import InputText from '../InputText/InputText' 
import loadSVG from '../../img/load.svg' 
import { Checkbox } from '@mui/material' 
import CustomizedSwitches from '../CustomizedSwitches/CustomizedSwitches' 

import Checklist from '../Checklist/Checklist' 



export default function Embedding({theme_color}){
    
  const list_of_models = ["BAAI/bge-small-en-v1.5"]
  const list_metadata = ['arte', 'cucina', 'cultura', 'narrativa', 'natura', 'scienza', 'sport', 'storia']
  const [selectedDate, setSelectedDate] = React.useState( Array.from({ length: list_metadata.length }, _ => false)) 
  const [newCollection, setNewCollection] = React.useState(null) 
  const [model, setModel] = React.useState(null) 



  const [newDeep, setNewDeep] = React.useState(null) 
  const [load, setLoad] = React.useState(false)  // Imposta load su false all'inizio
  const [isChecked, setIsChecked] = React.useState(false) 
  const [scraping, setScraping] = React.useState(0)
  const [apiResult, setApiResult] = React.useState(
    "In attesa: di una domanda o di un url. \n Scraping delle pagine web attraverso la ricerca su Google oppure attraverso l'utilizzo di un url specifico."
  )
  
  
  function updateSelectedDate(index){
    selectedDate[index] = !selectedDate[index]
  }

  
  function onValueChange() {

    if (model !== null && newCollection !== null) {
      console.log("valori pronti per esser inviati") 

      // Imposta load su true quando i valori sono pronti per l'invio
      // setLoad(true) 

      let fetch_api=""
      let postData={}
      let metadata = {}
      let theme = []
      let delete_collection = false
      let path = "percorso/questo"

      for(let i=0; i<list_metadata.length; i++){
        if(selectedDate[i]){
          theme.push(list_metadata[i])
        }
      }
      metadata['user'] = 'admin'
      metadata['theme'] = theme
      console.log(metadata)

      if(scraping===0){
        fetch_api="http://127.0.0.1:8000/embedding"

        postData = {
          "model": model,
          "collection": newCollection,
          "metadata": metadata,
          "path": path,
          "delete": delete_collection
        }

      }

      fetch(fetch_api, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(postData)
      })
        .then(response => {
          if (!response.ok) {
            setApiResult("C'è stato un errore")
            throw new Error('Errore nella richiesta')
          }
          return response.json()
        })
        .then(data => {
          console.log('data: ',data)
          const url = window.URL.createObjectURL(new Blob([JSON.stringify(data)]))
          const link = document.createElement('a')
          link.href = url
          link.setAttribute('download', 'file.json')
          document.body.appendChild(link)
          link.click()
      
          console.log(data)
          setLoad(false)
          setApiResult("File scaricato")
        })
        .catch(error => {
          console.log("Errore")
          // Imposta load su false in caso di errore
          setApiResult("C'è stato un errore")
          setLoad(false)
        })
    } else {
      console.log("none")
    }
  }

  React.useEffect(()=>{
    return
    console.log("---SCRAPING:"+scraping)
    setNewDeep(null)
    setModel(null)
  },[scraping])

    
  return (
    <div className='state_text_field-box'>
        
        <div className='query'
          style={{
            backgroundColor: theme_color.dark,
            color: theme_color.contrastText,
            elevation: 3,
          }}>
          {/* 
          --------SWITCH
          <div style={{
            display:'flex',
            justifyContent:'flex-end'
          }}><CustomizedSwitches theme_color={theme_color} txt={["ricerca","http"]} setScraping={setScraping} /></div> */}
          
          {scraping === 0 ?(<>
              <InputText theme_color={theme_color} label={"Nome della collezione"} setInput={setNewCollection} />
              <SelectNumPag theme_color={theme_color} data={list_of_models} label={"Modello"} changeValue={setModel} />
            </>):(<>
              <InputText theme_color={theme_color} label={"Link"} setInput={setNewCollection} />
              {/* <SelectNumPag theme_color={theme_color} data={depth} label={"Profondità"} changeValue={setNewDeep} /> */}
            </>)}
            <Checklist theme_color={theme_color} data={list_metadata} selectedDate={selectedDate} updateData={updateSelectedDate}/>
          
          <ButtonSendMsg theme_color={theme_color} onValueChange={onValueChange} />
        </div>
        
        {/* Mostra l'immagine di caricamento solo quando load è true */}
        {load ?  
          <div className='load_box'>
            <div className='load'><img src={loadSVG} alt="Loading" /></div>
          </div>: 
        null}
      <div className="scraping_response"
        style={{
          backgroundColor: theme_color.main,
          position: 'relative',
          overflow: 'auto', // Nasconde il testo che supera i limiti della div
          fontSize:'12pt',
        }}
      >
      <span style={{ position: 'absolute', margin: '10px', color: theme_color.contrastText}}>
        
        {apiResult}

      </span>

    </div>
    </div>
  ) 
}