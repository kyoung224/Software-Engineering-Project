
import './App.css';
import { useState, useRef } from 'react';

function Test() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"

  const [addQueue, setAddQueue] = useState([]);
  const [deleteQueue, setDeleteQueue] = useState([]);
  const [showList, setShowList] = useState([]);
  const textInput = useRef(null);

  function AddArtist(){
    let newArtist = textInput.current.value;
    let newArtistList = [...addQueue, newArtist];
    setAddQueue(newArtistList);
    textInput.current.value = "";
  }

  function DeleteArtist(){
    let deleteArtist = textInput.current.value;
    let newArtistList = [...deleteQueue, deleteArtist];
    setDeleteQueue(newArtistList);
    textInput.current.value = "";
  }

  function SaveArtist(){
    if (addQueue.length > 0){
      fetch('/addArtist', {
        method: 'POST',
        headers:{
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"artist_input": addQueue}),
      }).then(response => response.json()).then(data => {
        if (data.input_server == false){
          alert("Invalid artist! Please try again");
          let resetAddQueue = addQueue.filter( addQueue => addQueue !== addQueue);
          setAddQueue(resetAddQueue);
        } else{
          let newArtist = data.input_server;
          let newArtistList = [...showList, newArtist];
          setShowList(newArtistList);
          let resetAddQueue = addQueue.filter( addQueue => addQueue !== addQueue);
          setAddQueue(resetAddQueue);
          window.location.reload(true);
        }
      });
    }
    
    if (deleteQueue.length > 0){
      fetch('/deleteArtist', {
        method: 'POST',
        headers:{
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"artist_input": deleteQueue}),
      }).then(response => response.json()).then(data => {
        if (data.input_server == false){
          alert("No such artist on list! Please try again");
          let resetDeleteQueue = deleteQueue.filter( deleteQueue => deleteQueue !== deleteQueue);
          setDeleteQueue(resetDeleteQueue);
        } else{
          let newArtist = data.input_server;
          let newArtistList = [...showList, newArtist];
          setShowList(newArtistList);
          let resetDeleteQueue = deleteQueue.filter( deleteQueue => deleteQueue !== deleteQueue);
          setDeleteQueue(resetDeleteQueue);
          window.location.reload(true);
        }
      });
    }
  }
  
  // TODO: Implement your main page as a React component.
  return (
    <>
    <form method = "POST" action = "/main"> 
        <label for = "artist_input"> Type in artist to add! </label><br/>
        <input ref = {textInput} type = "text" name = "artist_input" placeholder = "Type Artist" data-testid = "text-input"/>
    </form>
    <button onClick={AddArtist}>Add an artist</button>
    <button onClick={DeleteArtist}>Delete an artist</button>
    <button onClick={SaveArtist}>Save! </button>
    <h3> List of Artists to be Added</h3>
    <ul>
      {addQueue.map((artist, index) => (
        <> <li key = {index}> {artist} </li> <br/> </> 
      ))}
    </ul>

    <h3> List of Artists to be Deleted</h3>
    <ul>
      {deleteQueue.map((artist, index) => (
        <> <li key = {index}> {artist} </li> <br/> </> 
      ))}
    </ul>
    </>
  );
}

export default Test;