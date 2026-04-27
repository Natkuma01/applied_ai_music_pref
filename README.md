# 🎵 Music Recommender Simulation

## 📌 About This Project

This project builds an intelligent music recommendation system that uses vector embeddings and cosine similarity to suggest personalized songs based on user preferences. It processes user input and song metadata to intelligently match preferences with available tracks, while a guardrail system ensures recommendation quality and safety. The system applies bonus scoring for matching genres and ranks the top 5 recommendations for delivery to users.

## 🎯 Project Goals

• 🎼 **Convert preferences to vectors** - Transform user preferences into numerical representations for similarity matching

• 🎸 **Match songs with precision** - Use cosine similarity to calculate how well each song matches user tastes

• ✨ **Boost matching genres** - Apply bonus points when song genres align with user preferences for better relevance

• 🏆 **Rank top recommendations** - Deliver a curated list of the top 5 songs ranked by relevance

• 🛡️ **Quality assurance** - Implement guardrail verification to validate results and add warnings when quality thresholds aren't met

## 🏗️ Architecture Overview

The system leverages a **Cosine Similarity Calculation Engine** to compute how well each song matches user preferences by comparing vector representations holistically rather than individual categories. This approach applies a bonus score when genres match perfectly, and a penalty when they diverge, while still being capable of recommending songs from different genres if they align with the user's overall preference vector. We chose cosine similarity because it captures nuanced pattern matching across multiple dimensions simultaneously—meaning a rock song with indie elements might still be recommended to a pop enthusiast if the underlying audio characteristics align.

🎚️ **Trade-off Note:** While cosine similarity doesn't scale efficiently with massive datasets, it's ideal for our use case with just 20 songs, providing fast, accurate, and interpretable recommendations without the overhead of more complex algorithms.

## 💬 Sample Interactions

**Example 1: Pop Enthusiast with Genre Match**
- 🎤 **User Input:** "I love upbeat pop songs with catchy lyrics, energetic rhythm, modern production"
- 🎵 **System Output:** 
  - #1: "Take Me Out" - Pop (98% match, Genre Bonus Applied)
  - #2: "Levitating" - Pop (96% match, Genre Bonus Applied)
  - #3: "Good As Hell" - Pop/Soul (92% match, Minor Genre Variation)
  - #4: "Blinding Lights" - Synthwave/Pop (89% match)
  - #5: "Walking on Sunshine" - Pop/Soul (87% match)

**Example 2: Indie Rock Fan with Genre Diversity**
- 🎤 **User Input:** "Indie rock with introspective lyrics, alternative sound, emotional depth"
- 🎵 **System Output:**
  - #1: "Mr. Brightside" - Indie Rock (97% match, Genre Bonus Applied)
  - #2: "Wonderwall" - Alternative Rock (95% match, Genre Bonus Applied)
  - #3: "Sex on Fire" - Rock (91% match, Similar Vibes)
  - #4: "Creep" - Alternative Rock (88% match)
  - #5: "Use Somebody" - Alternative Rock (86% match)

**Example 3: Cross-Genre Discovery**
- 🎤 **User Input:** "Smooth, mellow vibes with soulful vocals and jazzy elements"
- 🎵 **System Output:**
  - #1: "Thinking Out Loud" - Soul/Pop (96% match)
  - #2: "Adore You" - Pop/Soul (94% match)
  - #3: "Kiss Me" - Alternative/Pop (90% match, Different Genre but Similar Vibe)
  - #4: "Electric Feel" - Funk/Electronic (87% match)
  - #5: "Fluorescent Adolescent" - Indie (85% match, Soulful Quality Detected)

## 🛠️ Design Decisions

**Why Cosine Similarity?**
- **Holistic Matching:** Compares songs across all dimensions simultaneously rather than categorical matching alone, capturing nuanced preferences
- **Genre Flexibility:** Allows cross-genre recommendations when underlying audio characteristics align, preventing "genre silos"
- **Interpretability:** Easy to explain why a song was recommended and debug edge cases

**Key Trade-offs Made:**
- ✅ **Chose:** Fast, interpretable results over perfect accuracy → Better UX for small datasets
- ✅ **Chose:** Simple 5-song ranking over personalized learning → Reduced complexity, easier testing
- ✅ **Chose:** Bonus/penalty system over neural networks → Human-understandable scoring over black-box predictions
- ❌ **Rejected:** Complex deep learning models → Too much overhead for 20 songs and limited user data

**Bonus/Penalty System:**
- Genre match: +15% boost to similarity score
- Genre mismatch: -5% penalty to encourage exploration while honoring preferences
- This creates balanced recommendations that respect genres while allowing cross-genre discovery

## 🧪 Testing Summary

**What Worked:**
- ✅ Vector conversion successfully captured preference characteristics
- ✅ Genre bonus system accurately boosted relevant matches
- ✅ Top 5 ranking provided clean, actionable recommendations
- ✅ Guardrail system detected and flagged low-confidence recommendations
- ✅ Cross-genre recommendations discovered surprising but relevant matches

**What Didn't Work Initially:**
- ❌ Raw cosine similarity alone produced too many genre mismatches before bonus/penalty system
- ❌ No filtering led to irrelevant edge-case recommendations
- ❌ Guardrail lacked clear thresholds—refined to 70% confidence minimum
- ❌ Single pass without re-ranking allowed lower-quality songs to slip through

**Key Learnings:**
- 📚 Domain knowledge (genre context) is as important as mathematical similarity
- 📚 Human-in-the-loop feedback would drastically improve accuracy
- 📚 Small datasets benefit from hybrid rule-based + ML approaches
- 📚 Clear confidence thresholds and guardrails are essential for user trust

## 💭 Reflection

Working on this music recommendation project taught me that **AI isn't just about algorithms—it's about understanding the problem domain.** Initially, I focused purely on the math of cosine similarity, but I quickly realized that recommendation quality comes from combining mathematical precision with domain knowledge (genre context, mood indicators, etc.).

I learned that **vectors are a powerful abstraction** for comparing complex preferences without rigid categorical thinking. A song from a "different genre" can still be perfect because similarities exist in dimensions beyond just the genre label. This mirrors real human taste—we don't think in strict categories; we feel patterns and moods.

Most importantly, this project highlighted the **responsibility that comes with AI systems.** The guardrail system isn't just a feature; it's essential for user trust. AI systems must be transparent about confidence levels and fail gracefully rather than silently delivering poor recommendations. Building AI isn't just about high accuracy—it's about high reliability and user confidence.

## 📏 Reliability and Evaluation
To ensure the system provides trustworthy recommendations, I implemented a Confidence Scoring system based on Cosine Similarity and automated Logging to track match quality. During testing, I discovered that balancing the Genre Bonus with Vector Similarity was challenging; initially, high vibe-scores for mismatched genres prevented the Guardrail from triggering. I refined the evaluation logic to check both the genre match and a similarity threshold simultaneously, ensuring that "best of a bad bunch" results are flagged with a warning. This hybrid approach prevents the system from over-relying on a single category, creating a more balanced recommendation. Finally, I used Human Evaluation with extreme "Edge Case" profiles to verify that the AI correctly identifies gaps in the dataset and suggests improvements to the user.

## 🔮 Reflection
1. By giving a +0.2 bonus to Genre, it is a "label bias." If the user chooses a genre but the vectors suggest a different song is a better "vibe" match, the code might still prioritize the genre label even if that specific song is an outlier in the category.
2. Fine-tuning an AI system is a constant trade-off between different priorities. Even after many iterations, it was nearly impossible to find a perfect balance where the system was strict enough to flag missing data but flexible enough to recognize similar "vibes." This taught me that as a developer, I have to make a choice: do I want the AI to be more "creative" or more "accurate"?

## 🚀 Setup & Installation

### Prerequisites
- **Python 3.8+** installed on your system
- **pip** (Python package manager)
- **Git** (to clone the repository)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd applied_ai_music_pref
```

### Step 2: Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# From the project root directory
pip install -r requirements.txt
```

### Step 4: Verify the Data

```bash
# Check that the songs dataset exists
ls -la data/songs.csv
```

### Step 5: Run the Music Recommender

```bash
# From the project root directory
python -m src.main
```

The system will prompt you to enter your music preferences, then output the top 5 personalized recommendations with confidence scores and any guardrail warnings.

### Step 6: Run Tests (Optional)

```bash
# From the project root directory
python -m pytest tests/ -v
```

This runs all unit tests to verify the recommender and guardrail systems are working correctly.

### 📁 Project Structure

```
applied_ai_music_pref/
├── src/
│   ├── main.py              # Entry point - run this to use the recommender
│   └── recommender.py       # Core recommendation engine logic
├── data/
│   └── songs.csv            # Dataset of 20 songs with metadata
├── tests/
│   └── test_recommender.py  # Unit tests for the system
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── model_card.md            # Model documentation
├── reflection.md            # Detailed project reflection
└── DataFlow_Diagram.pdf     # Visual system architecture

```

### ⚙️ Running Different Scenarios

**Interactive Mode (Default):**
```bash
python -m src.main
# Follow the prompts to enter your music preferences
```

**Example: Testing with a Specific Preference**
You can modify `src/main.py` to test different preference scenarios directly without prompts.

### 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'src'` | Make sure you're running from the project root directory and the `.venv` is activated |
| `FileNotFoundError: songs.csv` | Verify `data/songs.csv` exists in the project directory |
| `No such file or directory: requirements.txt` | Ensure you're in the project root when running `pip install` |
| Tests fail | Try reinstalling dependencies: `pip install -r requirements.txt --force-reinstall` |

