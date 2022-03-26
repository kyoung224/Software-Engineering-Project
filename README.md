# Heroku deployment
https://software-project1-gkim70.herokuapp.com/

# General Info: Library
For this project, I used many different libraries contatining
- os
- flask
- random
- requests
- dotenv
- SQLAlchemy
- flask_sqlalchemy
- json

# General Info: API
The APIs I used were
- Get an Artist's Top Tracks API from Spotify: https://api.spotify.com/v1/artists/{id}/top-tracks
- Get an Artist API from Spotify: https://api.spotify.com/v1/artists/{id}
- Search API from Genius: http://api.genius.com/search
- Search API from Spotify: https://api.spotify.com/v1/search

# General Info: Setup
In order to run this program, there is a filie named .env, hidden by gitignore. This .env file contains 3 informations that are very critical in order to run the program: Spotify Client ID, Spotify Client Secret ID, Genius Access Token, Database URL.
After these keys are defined, a user will be first directed to login / signup page where each users will have to enter a valid username into the login input box in order to be directed to the main page. If the user does not have an username assigned, they can create one by using the sign up input box.
When authenticated, users will be directed to react page in App.js which will show artists track and informations according to the database. If the user is new and have not added any artists, the page will tell users to add an artist. 
There will be three buttons each used for adding, deleting, and saving. When add button is pressed, the input will be saved to the add queue list and for the delete button, the input will be saved to the delete queue. These don't have anything to do with the actual database untill the save button is pressed. When save button is pressed, it will then send those datas in queue to app.py and deal with database related stuff.
If the artist name that user entered does not COMPLETELY match up with what is stored in the Spotify API, it will return an error message saying that it was a invalid artist name so it is important for users to use 100% matching artist name.
When a correct artist name was submitted, the name will be submitted to app.py to look up the artistID based from the input artist name and store it in a database. 
Then an artist will be chosen randomly among the ones stored in the database, and in order to fetch other necessary informations from spotify, it will go through the get_data function which is imported from the spotify.py.
In this spotify.py file, there exists API that can fetch the artist's top 10 tracks at the most and also another API that fetches the artist's information. 
By chaning the json values in the functions starting from line 81, users will be able to get different outputs from what I had.
Then, a title fetched from this spotify.py will be loaded into the function get_lyrics imported by genius.py in the app.py to fetch the url link for the song, which isn't completely accurate at the moment, in the app.py.
Finally in app.py, it will render the values fetched from the APIs and load them to the react, displaying the informations. 

# Technical Issuses
The technical issues I encountered with my project is 
1. Css not being applied to the login.html
2. Unable to run unittest on react due to assignment to const args is being null
3. Dealing with adding and deleting artist

The way I fixed the first problem is by coding in the css as internal css for login.html. The reason why it did not work with App.css is due to the static folder relocating due to blueprint, but I could not find a way to work around with it except for using an internal css.
For the second problem, I looked at discord and found someone else also having a similar problem, but they found the solution so I followed it by creating another javascript file named Test.js, and remove the args when used and copied over the function that I wanted to test about and it did the trick.
Finally for the third problem, I decided to have a different state hook per button so when I press the save button, it will handle each case depending on what state was changed.
# Known Problems
The known problems of my project would be that the lyrics from Genius API does not completely match up with the song fecthed from Spotify API. 
In order to fix this problem, it will be good to set up some kind of a loop checking if the song that was fetched using Genius's search API completely matches up the song from Spotify by not only checking the title, but also the artist.
Second problem that I can sense is there will be a conflict between add and delete I believe since I am allowing the same input to exist by having a different queue for add and delete.
Third problem is that in order to add an artist to the database, user has to input the EXACT name that will match up with the one spotify has, which will be bit hard because some artists use foreign alphabets that some users won't know about.
In order to fix this problem, I could do some deep checking through many loops and conditions in the future to make this app more user friendly.


# To Improve
In order to improve my project for the future, I would like to to solve the problems where the user will have to input the artist even when they want to delete. If I can, I would like to have a delete button right next to each artist names so by just clicking on that button, users will be able to remove them.
