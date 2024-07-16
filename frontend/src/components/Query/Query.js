import InputText from '../InputText/InputText' 
import ButtonSendMsg from '../ButtonSendMsg/ButtonSendMsg'
import * as React from 'react'
import './Query.css'
import Load from '../Load/Load'


export default function Query({theme_color}){

    const [question, setQuestion] = React.useState('') 
    const [queryResult, setQueryResult] = React.useState('In attesa')
    const [load, setLoad] = React.useState(false) 
    const [queryError,setQueryError] = React.useState('')
    
    function changeQuery(event){
        setQuestion(event)
        setQueryError('')
    }
    function submit_query(){
        setLoad(true)
        if(question.length>0){
            let postData = {
                'query': question
            }
            let fetch_api = 'http://127.0.0.1:8000/query'
            setLoad(true)
            fetch(fetch_api, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(postData)
            })
            .then(response => response.json())
            .then(data => {
                setLoad(false)
                let txt = "<ul>"
                data[0].forEach(element => {
                    if(element[0]==='.'){
                        element=element.slice(1)
                    }
                    if(element.length!=0){
                        txt = txt+"<li>"+element+"</li>"+"<br/>"    
                    }
                    
                });
                txt = txt+"</ul>"
                setQueryResult(txt)
            })
            .catch(error => {
                setLoad(false)
                console.error(error);
            })
        } else {
            setQueryError('* digitare una domanda')
        }
        
    }
  
    return(
        <div  className='query-box'>
            <div className='body_of_the_query'
                style={{
                    backgroundColor: theme_color.dark,
                    color: theme_color.contrastText,
                    elevation: 3,
                }}>
                <InputText theme_color={theme_color} label={"Chiedimi qualcosa"} setInput={changeQuery} />          
                <div id='div_error'>{queryError}</div>
                <ButtonSendMsg theme_color={theme_color} onValueChange={submit_query}  />
            </div>
            {load ?  
                <div className='load_box'>
                <div className='load'>
                    <Load theme_color={{theme_color}}/>
                </div>
                </div>: 
            null}
            <div className="query_span"
                style={{
                    backgroundColor: theme_color.main,
                    position: 'relative',
                    overflow: 'auto',
                    fontSize:'12pt',
                }}>
                <span style={{ position: 'absolute', margin: '0px', color: theme_color.contrastText}}>
                <div style={{
                    textAlign: 'justify', 
                    margin:'15px',}} dangerouslySetInnerHTML={{ __html: queryResult }}></div>
                </span>
            </div>
        </div>
    )
}