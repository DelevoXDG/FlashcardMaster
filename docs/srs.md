# SRS for Flashcard Management Application

## 1. Introduction
The main purpose of the Flashcard Management App is to facilitate effective and organized learning through the use of digital flashcards. It is a tool designed to enhance the learning experience by helping users effectively manage their flashcard collections, create personalized study playlists, view flashcard data of various types, and track their learning progress through comprehensive statistics. The app leverages unique features such as a spaced repetition algorithm, stats analysis, and intuitive user interfaces to provide an efficient learning environment. It is intended to be implemented as a web application or as an installable application on computers or with additional modifications for smartphones.

## 2. Database Structure
The application relies on the following databases to store and manage flashcard data:

1. `Decks`:
	- stores information about the flashcard decks created, including deck titles, cover images.
2. `Flashcards`:
	- stores information about individual flashcards, including their type, question, answer, difficulty level, and data related to revision intervals.
3. Categorization:
	 - i.e. `Categories`, `Tags`
4. Stats-related:
	- i.e. `FlashcardAnswers` to track the number of flashcards answered correctly, the total number of flashcards attempted, and calculate correctness rates.

## 3. Functionalities
The list of base functionalities that can be expanded in the future. 

### 3.1. Collection Management
The Collection Management module is responsible for managing flashcard decks. It includes the following functionalities:

1. **Deck Listing:**
	- Display a list of decks with their relevant info, including titles, cover images and number of cards discovered or mastered.
	- Allow users to select, add, remove, merge and modify decks.
2. **Import and Export Decks**
	- Enable users to import flashcard decks from external sources and export decks for sharing or backup purposes.
3. **Statistics Button**
4. **Study Playlist Creation:** 
	- Allow users to create study playlists based on one or several selected decks.

### 3.2. Study Playlist Creation
The Playlist Creation module allows users to create study playlists based on selected flashcard decks. It is triggered from the deck listing. It includes the following functionalities:

1. **Flashcard Deck Selection:**
	- Allow users to select one or more flashcard decks to include in the playlist.
2. **Difficulty Selection:**
	- e.g. light, hard or random.
	- Sort the flashcards within the playlist based on the selected difficulty level or order them randomly based on user's preference.
3. **Study Type Customization:**
	- e.g. revision, learning or random.
	- Sort the flashcards within the playlist based on the selected study type or order them randomly based on user's preference.

### 3.3. Flashcard Display
Once the playlist is created the study session can be started. It supports different modes such as:

1. **Quiz Mode:**
	- Present flashcards with predefined answers.
	- Allow users to test their knowledge by selecting the correct answer from multiple choices or providing a typed response.
2. **Flip Mode:**
	- Enable users to answer flashcard questions to themselves (without typing or selecting an answer).
	- Provide a flip option to reveal the correct answer and check their response.

It also supports:

1. **Intelligent Card Sorting:**
	- Smart sorting to prioritize flashcards based on their last review date and preferences selected upon playlist creation.

### 3.4. Card Management
The Card Management module focuses on managing individual flashcards within a deck. It includes the following functionalities:

1. **Flashcard Attributes Modification:**
	- Allow modification of various card attributes.
	- Support different types of answers, including multiple-choice, true/false, or typed text.
2. **Planned Revision:**
	- Provide options for users to set planned revision times for each flashcard, such as immediate revision, short-term revision, and long-term revision.
### 3.5. Stats Viewing
The Stats Viewing module focuses on displaying learning statistics to users. It includes the following functionalities:

1. **Correctness Graph:**
	- Present a graph illustrating the user's correctness rate over time.
	- Provide insights into their learning progress and performance.
2. **Question Count Graph:**
	- Display a graph showing the number of flashcards answered throughout a selected timeframe, such as the current month.
