
import './App.css';
import { useState, useRef } from 'react';

function App() {
  // fetches JSON data passed in by flask.render_template and loaded
  // in public/index.html in the script with id "data"

  const args = JSON.parse(document.getElementById("data").text);
  const [addQueue, setAddQueue] = useState([]);
  const [deleteQueue, setDeleteQueue] = useState([]);
  const [showList, setShowList] = useState([args.artistName_list]);
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
    <h1> Welcome {args.current_user}! </h1> 
    {args.length <= 0 ? ( 
      <>
        <p> Please add an artist</p> 
    </>):
    (
    <>
    <div class = "artist_info_box">
      <h1> About the Artist </h1>
      <div>
        <img src = {args.artist_img} class = "artist_img"/> <br/> 
        Followers: {args.artist_follower} <br/>
        Genres: {args.artist_genre} <br/>
      </div>
      <a href = {args.artist_page}> Link to artist page </a>
    </div>

    <div class = "track_info_box">
      <h1>About the Track </h1>
      <div> 
        Album Name: {args.album_name} <br/>
        Release Date: {args.release_date} <br/>
        Popularity: {args.popularity} <br/>
        Track Number: {args.track_number} <br/>
      </div>

      <h1>List of Artists in the Database </h1>
      
      <ul>
        {showList.map((artist, index) => (
          <> <li key = {index}> {artist} </li><br/> </> 
        ))}
      </ul>

    </div>

    <div class = "musicbox">
      <ul>
          <li> <img src = {args.image} class = "music_bg_img"/> </li>
          <li> <img src = {args.image} class = "music_img"/> </li>
      </ul>

      <div class = "audio_box">
          <audio controls src = {args.url}> </audio> <br/>
          <h2> {args.title} </h2>
          <h3> {args.artist} </h3>
          <p> <a href = {args.lyrics}> Link to Lyrics </a> <br/>
          <a href = {args.spotify_url}> Listen on Spotify </a> </p>
      </div>     
    </div>
    </>
    )
    }
    
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

export default App;