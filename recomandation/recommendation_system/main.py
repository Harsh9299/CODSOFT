# ============================================================================
# main.py - Movie Recommendation System Interface
# ============================================================================
# PURPOSE:
# This is the main program that runs the movie recommendation system.
# It provides a user-friendly interface for getting movie recommendations.
#
# WHAT IT DOES:
# 1. Displays available movies to the user
# 2. Asks the user to enter a movie they like
# 3. Uses content-based filtering to find similar movies
# 4. Shows the top 3 recommendations
#
# HOW TO RUN:
# Simply execute this file: python main.py
# ============================================================================

# Import functions from other files in our project
from data import get_movie_data          # Gets the movie dataset
from recommender import recommend_movies  # Finds similar movies


def run_demo():
    """
    Demo function for teachers/interviewers to quickly evaluate the system.
    
    EXPLANATION:
    This function automatically demonstrates the recommendation system
    without requiring user input. Perfect for quick evaluation!
    """
    print("=" * 70)
    print("DEMO MODE - Automatic Recommendation System Demonstration")
    print("=" * 70)
    print()
    
    # Load the movie dataset
    df = get_movie_data()
    
    print("📊 DATASET LOADED:")
    print(f"Total movies in database: {len(df)}")
    print()
    
    # Test movies to demonstrate different genres
    test_movies = ["Inception", "The Lion King", "Titanic"]
    
    print("🎬 DEMONSTRATION - Testing Content-Based Filtering:\n")
    print("=" * 70)
    
    # Run recommendations for each test movie
    for i, test_movie in enumerate(test_movies, 1):
        print(f"\n[Test {i}]")
        print("-" * 70)
        print(f"🎥 SELECTED MOVIE: '{test_movie}'")
        
        # Get the genre of the test movie
        genre = df[df['movie'] == test_movie]['genre'].values[0]
        print(f"   Genre: {genre}")
        print()
        
        # Get recommendations
        recommendations = recommend_movies(test_movie, df)
        
        # Display results
        print(f"✨ RECOMMENDED MOVIES (Based on genre similarity):")
        print()
        for idx, movie in enumerate(recommendations, 1):
            # Show genre of recommended movie
            rec_genre = df[df['movie'] == movie]['genre'].values[0]
            print(f"   {idx}. {movie}")
            print(f"      └─ Genre: {rec_genre}")
            print()
        
        print("=" * 70)
    
    print("\n✅ DEMO COMPLETE - System is working correctly!")
    print("\nYou can now run the interactive mode to try it yourself.\n")


def main():
    """
    Main function that runs the entire recommendation system.
    
    BEGINNER EXPLANATION:
    This function controls the flow of the program:
    - Shows welcome message
    - Loads movie data
    - Gets user input
    - Generates recommendations
    - Displays results
    """
    # Display welcome banner
    print("=" * 60)
    print("        🎬 Movie Recommendation System 🎬")
    print("=" * 60)
    print("\nWelcome! Let's find movies you'll love! 😊")
    print()
    
    # STEP 1: Load the movie dataset from data.py
    # --------------------------------------------
    # This gets our table of movies with their genre information
    df = get_movie_data()
    
    # Display all available movies to help the user choose
    print("📚 AVAILABLE MOVIES IN OUR DATABASE:")
    print("-" * 60)
    for idx, movie in enumerate(df['movie'], 1):
        print(f"   {idx}. {movie}")
    print("-" * 60)
    print()
    
    # STEP 2: Get user input
    # ----------------------
    # Ask the user to type a movie name
    # .strip() removes extra spaces from the beginning and end
    print("💬 Please tell us which movie you enjoyed:")
    movie_name = input("   Enter movie name: ").strip()
    print()
    
    # STEP 3: Get recommendations using content-based filtering
    # ---------------------------------------------------------
    # This calls our recommendation function from recommender.py
    # It will return a list of 3 similar movies
    recommendations = recommend_movies(movie_name, df)
    
    # STEP 4: Display results to the user
    # ------------------------------------
    # Check if the movie was found or not
    if recommendations and "not found" in recommendations[0]:
        # Movie doesn't exist in our database - show error message
        print("=" * 60)
        print("❌ " + recommendations[0])
        print("\n💡 Tip: Please choose from the available movies listed above.")
        print("=" * 60)
    else:
        # Movie found! Show the recommendations in a nice format
        print("=" * 60)
        print(f"🎥 SELECTED MOVIE: '{movie_name}'")
        print("=" * 60)
        print()
        print("✨ RECOMMENDED MOVIES FOR YOU:")
        print("-" * 60)
        # Display each recommended movie with a number
        for idx, movie in enumerate(recommendations, 1):
            print(f"   {idx}. {movie}")
        print("-" * 60)
        print("\n💡 These movies have similar genres to your selection!")
    
    # Thank you message
    print("\n🙏 Thank you for using our recommendation system!")
    print("   We hope you enjoy watching! 🍿")


# This special code runs the main() function when the file is executed
# It won't run if this file is imported by another file
if __name__ == "__main__":
    # EVALUATION MODE: Run demo first for teachers/interviewers
    # ----------------------------------------------------------
    # This automatically demonstrates the system working
    # Comment out the next line if you want to skip the demo
    run_demo()
    
    # Ask if user wants to try interactive mode
    print("\n" + "=" * 70)
    choice = input("Would you like to try the interactive mode? (yes/no): ").strip().lower()
    
    if choice in ['yes', 'y']:
        print()
        main()  # Run the interactive version
    else:
        print("\nThank you for evaluating our recommendation system! 👋")

