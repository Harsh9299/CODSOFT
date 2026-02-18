# ============================================================================
# recommender.py - Content-Based Recommendation Engine
# ============================================================================
# PURPOSE:
# This file implements the core logic for recommending movies using
# CONTENT-BASED FILTERING - a technique that recommends items similar to
# what the user already likes.
#
# HOW CONTENT-BASED FILTERING WORKS (BEGINNER EXPLANATION):
# -------------------------------------------------------------------------
# Imagine you liked "Inception" (a sci-fi action movie). The system will:
#
# 1. ANALYZE THE CONTENT:
#    - Look at the genre keywords: "science fiction action thriller dreams"
#
# 2. CONVERT WORDS TO NUMBERS:
#    - Computers can't understand words, only numbers
#    - We convert genre text into numerical vectors (lists of numbers)
#    - Similar words create similar numbers
#
# 3. MEASURE SIMILARITY:
#    - Compare the movie you liked with ALL other movies
#    - Calculate how similar each movie is (using cosine similarity)
#    - Movies with similar genres get higher similarity scores
#
# 4. RECOMMEND SIMILAR MOVIES:
#    - Find movies with the highest similarity scores
#    - These are movies with similar content/genres
#    - Example: "The Matrix" (also sci-fi action) would be recommended
#
# WHY IT WORKS:
# If you enjoyed a sci-fi action movie, you'll probably enjoy other
# sci-fi action movies too!
# ============================================================================

# Import necessary libraries from scikit-learn
from sklearn.feature_extraction.text import CountVectorizer  # Converts text to numbers
from sklearn.metrics.pairwise import cosine_similarity  # Measures similarity


def recommend_movies(movie_name, df):
    """
    Finds and recommends movies similar to the given movie.
    
    BEGINNER EXPLANATION:
    This function takes a movie name and finds 3 other movies that are most
    similar to it based on their genres.
    
    HOW IT WORKS STEP-BY-STEP:
    1. Validates that the movie exists in our database
    2. Converts all genre descriptions into numerical vectors
    3. Calculates similarity scores between all movies
    4. Finds the 3 movies most similar to your input movie
    5. Returns their names
    
    Args:
        movie_name (str): The name of the movie you want recommendations for
                         Example: "Inception"
        df (pd.DataFrame): Table containing movie data with 'movie' and 'genre' columns
    
    Returns:
        list: A list of 3 recommended movie names
              Example: ['The Matrix', 'Interstellar', 'The Dark Knight']
    """
    # STEP 0: Validation - Check if the movie exists in our database
    # If not found, return an error message
    if movie_name not in df['movie'].values:
        return [f"Movie '{movie_name}' not found in database"]
    
    # STEP 1: Convert genre text into numerical vectors
    # ------------------------------------------------
    # WHAT IS HAPPENING:
    # CountVectorizer converts text into numbers by counting word occurrences.
    #
    # EXAMPLE:
    # If we have genres:
    # - Movie A: "action thriller"
    # - Movie B: "action comedy"
    # - Movie C: "romance drama"
    #
    # CountVectorizer creates a vocabulary: [action, thriller, comedy, romance, drama]
    # Then converts each genre to a vector:
    # - Movie A: [1, 1, 0, 0, 0]  (has 'action' and 'thriller')
    # - Movie B: [1, 0, 1, 0, 0]  (has 'action' and 'comedy')
    # - Movie C: [0, 0, 0, 1, 1]  (has 'romance' and 'drama')
    #
    # Now movies can be compared numerically!
    count_vectorizer = CountVectorizer()
    genre_vectors = count_vectorizer.fit_transform(df['genre'])
    
    # STEP 2: Calculate cosine similarity between all movies
    # -------------------------------------------------------
    # WHAT IS COSINE SIMILARITY:
    # A measure of how similar two vectors are (scale: 0 to 1)
    # - 1.0 = Perfectly similar (identical)
    # - 0.0 = Completely different
    #
    # EXAMPLE:
    # Movie A: [1, 1, 0, 0, 0]  (action thriller)
    # Movie B: [1, 0, 1, 0, 0]  (action comedy)
    # Movie C: [0, 0, 0, 1, 1]  (romance drama)
    #
    # Similarity scores:
    # - A vs B = 0.5  (both have 'action', somewhat similar)
    # - A vs C = 0.0  (no common words, completely different)
    #
    # The similarity_matrix contains similarity scores for ALL movie pairs
    similarity_matrix = cosine_similarity(genre_vectors)
    
    # STEP 3: Find the position (index) of the input movie in our dataset
    # --------------------------------------------------------------------
    # We need to know which row contains our movie to get its similarity scores
    movie_index = df[df['movie'] == movie_name].index[0]
    
    # STEP 4: Get similarity scores for the input movie with ALL other movies
    # -----------------------------------------------------------------------
    # similarity_matrix[movie_index] gives us one row of similarity scores
    # enumerate() adds position numbers: [(0, score0), (1, score1), ...]
    similarity_scores = list(enumerate(similarity_matrix[movie_index]))
    
    # STEP 5: Sort movies by similarity score (highest first)
    # -------------------------------------------------------
    # We want the most similar movies at the top
    # key=lambda x: x[1] means "sort by the second element" (the score)
    # reverse=True means "highest to lowest"
    sorted_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    
    # STEP 6: Get the top 3 similar movies
    # ------------------------------------
    # sorted_movies[0] is the movie itself (similarity = 1.0)
    # So we take sorted_movies[1:4] to get the next 3 most similar movies
    top_movies = sorted_movies[1:4]
    
    # STEP 7: Extract just the movie names from the results
    # -----------------------------------------------------
    # top_movies contains [(index, score), ...]
    # We only want the movie names, so we look up each index in the DataFrame
    recommended_movie_names = [df.iloc[movie[0]]['movie'] for movie in top_movies]
    
    return recommended_movie_names

