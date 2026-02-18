# ============================================================================
# data.py - Movie Dataset Module
# ============================================================================
# PURPOSE:
# This file manages the movie dataset for our recommendation system.
# It contains the movie database with movie names and their genre descriptions.
#
# WHAT IT DOES:
# - Stores information about different movies
# - Each movie has a name and genre keywords (like 'action', 'drama', etc.)
# - Provides a function to load this data into a pandas DataFrame
#
# WHY WE NEED THIS:
# The recommendation system needs movie data to compare and find similarities.
# By keeping the data separate, we can easily update or expand our movie list.
# ============================================================================

import pandas as pd  # Library for working with data in table format


def get_movie_data():
    """
    Creates and returns a DataFrame with movie information.
    
    BEGINNER EXPLANATION:
    This function creates a table (DataFrame) with two columns:
    1. 'movie': The name of each movie
    2. 'genre': Keywords describing what the movie is about
    
    The genre keywords help us understand movie content. For example:
    - "action thriller" means the movie has action scenes and suspense
    - "animation family" means it's a cartoon suitable for families
    
    Returns:
        pd.DataFrame: A table with 10 movies and their genre descriptions
    """
    # Create a dictionary with movie data
    # Each key ('movie' and 'genre') represents a column in our table
    data = {
        # Column 1: Movie names
        'movie': [
            'The Shawshank Redemption',
            'Inception',
            'The Lion King',
            'The Dark Knight',
            'Toy Story',
            'Titanic',
            'The Matrix',
            'Finding Nemo',
            'Pulp Fiction',
            'Interstellar'
        ],
        # Column 2: Genre keywords for each movie
        # These words describe the movie's theme, style, and content
        'genre': [
            'drama prison friendship redemption',
            'science fiction action thriller dreams',
            'animation family adventure music',
            'action crime superhero thriller',
            'animation comedy family adventure',
            'romance drama disaster epic',
            'science fiction action cyberpunk',
            'animation family ocean adventure',
            'crime drama dark comedy',
            'science fiction drama space adventure'
        ]
    }
    
    # Convert the dictionary into a pandas DataFrame (table structure)
    # This makes it easy to search, filter, and analyze the data
    return pd.DataFrame(data)

