# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  
MusicPro 1.0

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 
User can set their own preference base on Genre, mood, energy, danceability, valence.
It is designed to transform a set of playlist into a personalized musical experience.
It is built for music platfor mstartups and developers who want to understand the 
constent-based recommendation systems.

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.
The system acts reward points based on how well a song fits a user's request.
Originally we prioritized the Genre but then we shifted the system to focus more
on the energy of the music. This change was made to see if the recommender could
learn to suggest songs that sound right even if they belong to a different 
category, moving away from strict labels toward a more vibe-based ranking. 

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  
The dataset began with 10 songs, then I expanded to 20 songs using Claude code to generate it. While the expansion added diversity, such as genres like Metal, Blues, and Classical, the dataset remain unfair toward certain tastes. Specifically, it heavily favors on high engergy music, which means user who prefer chill or low energy vibes have significantly fewer options to choose from. This can lead to repetitive or less accurate recommendations.
Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  
- build for high energy fans
- the system does not just looking at label, it focus on vibe (because 
energy weight more than genre)
- transparent: it clearly show how the points system works, user can see
why the song is recommended.
Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 
- the data has biased, for instance, there maybe only one song is metal or ong song that is low energy
- the scoring is not fair, the score is always increment, so even the song is not a good match, it still get points
- the logic is exteme, the code see the world only two side. For instance, Rock and Metal can be similar genre. However, the code treat the two as distinct. It prevents users from discovering music that is close enough or similar to what they like

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 
I was surprised at how quickly the system ran out of relevant songs. For niche genres like Blues or Metal, 
the user got their #1 match, but picks #2 through #5 felt random. This is because once the "Genre Match" 
points were off the table, the system just picked whatever was closest in energy, even if it was a 
totally different vibe (like Hip-Hop for a Blues fan).

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  
- expend dataset, have more variety of song. It should included low-energy songs, and each genre should have the same amount of songs
- for the point system, I would also reduce points when songs are not
matched with the user's preference. I think this can make a clear distinction between the songs that user's prefer or not.

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  
Through this project, I learned that a recommender is only as good as its underlying data. If the dataset is not diverse and balanced, the predictions will naturally lean toward the most common categories. I also discovered that fine-tuning a scoring system is an iterative process. Small shifts in weights can lead to unexpected results. This really highlighted that building a fair system takes a lot of trial and error and avery balanced dataset.
Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
