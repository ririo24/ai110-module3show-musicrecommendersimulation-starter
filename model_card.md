# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**SongSuggester**
---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

Song Suggester is a music recommender that takes a user's preferences and returns a ranked list of songs they might like from a small catalog. It geberates recommendations by scoing each song against the user's target values for each feature and then choses the closest match. The system assumes the user's preferences stay constant during a listening session. The Song Suggester does not learn from listening history or adapt over time. This is definitely solely for classroom exploration because the catalog is why too small to be applied/scaled to real users. This is a classroom simulation designed to explore how reccommendation algorithims work and give me an understanding of how streaming services work.
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The features of each song that were used were: genre, mood, energy, tempo (in bpm),valence, danceability, acousticness, speechiness, and instrumentalness. 
The user preferences that were considered were mood, energy, likes acoustic, target valence, target danceability, target speechiness, target instrumentalness.
The recommender takes the stated preferences and compares them against each song. 
Some changes I made from the starter logic was, adding more song features which gave the system a more complete picture of each song.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

There are 18 songs in the catalog. 
The genres represented are pop, lofi, rock, metal, ambient, jazz, synthwave, indie-pop, hip-hop, classical, r&b, edm, folk, blues, and latin.
I added 8 more songs. 
There are probably parts of musicla taste missing in the dataset like if a user likes to listen to songs they know or are more explorative with their music. Even though there are some categories missing in the dataset, I do think that the dataset is pretty thorough and captures the main features of a song.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for users with clear and consistent preferences. 

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The most significant bias in this system is that most of 18 genres are represented by exactly one song, making the genre bonus pretty unhelpful for scoring purposes for most users. A blues fan will always see Delta Rain Blues ranked first in their recommendations regardless of how poorly it matches their other preferences because no other blues song exists in the songs catalog. This was seen during testing when the "Deep Intense Rock" profile ranked Iron Cathedral below Gym Hero. The fix requires either expanding the dataset with multiple songs per genre, or replacing exact-match scoring with partial credit for adjacent genres.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested all the user profiles. I had 3 standard and 4 adversarial ones. For each profile, I checked if the #1 result matched what a human would intuitively pick. A surprising result was that Gym Hero, a pop song, ranked above Iron Cathedral, a metal song, for a user with an intense rock profile. The mood for the user profile (Deep Intense Rock) was "intense" so it matched the pop but not the metal song of the catalog. This just showed me that the mood bonus was kinda throwing things off and overriding musical common sense. I ran an experiment to disable the mood check entirely. When I did that, Iron Cathedral did end up ranking higher than Gym Hero, which made sense for this user's taste profile. This demonstrated that mood was the category that had caused the unexpected ranking of pop higher than metal for a rock-loving user. 

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Additional features I would include to improve the model would be to have partial mood and genre matching. I would have a similarity table of some sorts that would give partial credit to songs in related cateogries so that issue of the pop song getting reccomended over a metal song to a rock lover, woudn't happen. Additionally, I could attempt to improve diversity among the top results if my catalog got bigger and started recommeding users songs by the same artist or of the same genre. In order to expose the user to more songs, I coud make a diveristy rule that would not let one singluar artist or of a single genre appear multiple times in this user's top 5 recommended songs. To handle more complex user tastes, I could have a context feature where I consider the time of day or the length of the listening sesssion to personalize the recommended songs to the context of the moment.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps
- What was your biggest learning moment during this project?
- How did using AI tools help you, and when did you need to double-check them?
- What surprised you about how simple algorithms can still "feel" like recommendations?
- What would you try next if you extended this project?

Recommender systems work with a lot of data and categories. In order to provide the user with solid recommendations, a recommender system must have a large number of categories assesing the musicality of the song, and it must have a lot of information on the user and their preferences. Something interesting I discovered was the high or low impact/weight of different components of a song into a scoring algorithm. 
This project made me realize how much data music recommendation apps must be collecting on users to provide them services they must be willing to pay for, or at the very least, enjoy, in order for their clients to continue using it. They must have tons of data on user patterns and behaviors, knowing what time of day they are free to listen to music, what kind of music they're into late at night, etc. so they can best cater to them. 
I had to double check Claude a few times. It had tried deleting things I didn't ask it to delete and impliment features I didn't ask for. But beside attempting some unauthorized actions, Claude was pretty helpful in me get a better understanding of how streaming services operate and how to implement music recommender algorithms.
If extending this project, I would add more song data and add a context feature to be mindful of things like time of day, to best understand the listening desires of my users.
