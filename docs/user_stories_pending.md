## About
The file contains user stories for the project.


## User stories

User can add a recipe to his/her fridge.
  - attempt to add a recipe with title, description and ingredients (PASS)
  - attempt to add a recipe without title (FAIL)
  - attempt to add a recipe without description (FAIL)
  - attempt to add recipe without ingredients (FAIL)
  - attempt to access the page without logging in (FAIL)
Priority: MUST HAVE
Status: NOT STARTED


User can save recipes from global recipe book to his fridge.
  - attempt to save a recipe from global recipe book (PASS)
  - attempt to save a recipe that is already saved (FAIL)
Priority: MUST HAVE
Status: NOT STARTED


User can add a recipe to a global recipe book.
  - attempt to add a recipe with title, description and ingredients (PASS)
  - attempt to add a recipe without title (FAIL)
  - attempt to add a recipe without description (FAIL)
  - attempt to add recipe without ingredients (FAIL)
  - attempt to access the page without logging in (FAIL)
Priority: MUST HAVE
Status: NOT STARTED


User can log in to the website using his/her ID and password combination.
  - attempt to log in with correct id & password combination (PASS)
  - attempt to log in with incorrect id & password combination (FAIL)
  - attempt to log in without password (FAIL)
  - attempt to log in without username (FAIL)
  - attempt to log in without either password or username (FAIL)
Priority: MUST HAVE
Status: NOT STARTED

User can register on the website.
  - attempt to register with unique username & password combination (PASS)
  - attempt to register with a username that already exists in the database (FAIL)
  - attempt to register with a password that already exists in the database (FAIL)
  - attempt to register without a username (FAIL)
  - attempt to register without a password (FAIL)
Priority: MUST HAVE
Status: NOT STARTED


User can edit the recipes he/she has uploaded.
  - attempt to edit his/her own recipe (PASS)
  - attempt to edit others' recipes (FAIL)
Priority: SHOULD HAVE
Status: NOT STARTED


User can choose from what category he/she should be shown the recipes.
  - attempt to pick a category that has recipes available (PASS)
  - attempt to pick a category that has no recipes available (should not be shown at all) (FAIL)
  - attempt to access the non-existent category and suggested recipes (FAIL)
Priority: COULD HAVE
Status: NOT STARTED


User can enter an ingredient in a search bar to see information about it or add it if it is not existent.
  - entering ingredient's title in a search will bring up information about it (PASS)
  - not entering anything will not do anything (PASS)
  - entering non-existent ingredient will show any results (PASS)
  - entering non-existent ingredient will offer the user to add it (PASS)
Priority: SHOULD HAVE
Status: NOT STARTED


User can enter an ingredient in a search bar to search for the recipes containing that ingredient.
  - searching for ingredient will show recipes containing it (PASS)
  - searching for non-existent ingredient will not show any results (PASS)
Priority: SHOULD HAVE
Status: NOT STARTED


User can add/edit the photo associated with recipe.
  - attempt to add a valid-sized photo (300x300?) (PASS)
  - attempt to add an over-sized photo (FAIL)
    - photo should be re-sized
  - attempt to add an undersized photo (FAIL)
  - attempt to add a photo that is not a JPG (FAIL)
Priority: SHOULD HAVE
Status: NOT STARTED


User can see recipes added by others.
  - attempt to access the global recipe book (PASS)
  - attempt to access a recipe that does not exist (FAIL)
    - redirect or error 404
Priority: SHOULD HAVE
Status: NOT STARTED


User can rate his/her recipes, as well as others.
  - attempt to rate his/her own recipe (PASS)
  - attempt to rate others' recipes (PASS)
  - attempt to rate recipes without logging in (FAIL)
Priority: SHOULD HAVE
Status: NOT STARTED


User can see a recipe rating. 
  - attempt to access the recipe's rating when there is one (PASS)
  - attempt to access the recipe's rating when there is none (FAIL)
Priority: SHOULD HAVE
Status: NOT STARTED


User receives an email upon registration.
  - register a user with existing email (FAIL)
  - register a user with non-existent email provider (FAIL)
  - register a user with an existing email (FAIL)
Priority: COULD HAVE
Status: NOT STARTED


User can share his/her fridge's recipe book (as a list of recipes).
  - attempt to share his/her fridge's recipe book with others (make it publicly available) (PASS)
  - attempt to share other's recipe book (FAIL)
  - attempt to access fridge that was not shared
Priority: COULD HAVE
Status: NOT STARTED


User can access the 5 best rated recipes from the home page (should it be on front page?).
  - attempt to access best rated recipes (PASS)
  - ensure that the recipes shown are really the most popular ones (TRUE)
Priority: COULD HAVE
Status: NOT STARTED


User can see the 5 most popular (global) recipes from the home page (should it be on front page?).
  - attempt to access 5 most popular recipes on the site (PASS)
  - ensure that the top 5 most popular recipes are the ones that have the most views (PASS)
Priority: COULD HAVE
Status: NOT STARTED


User can access his/her 5 most recently viewed recipes (should it be on front page?)
  - attempt to access recently viewed recipes (PASS)
  - ensure that the recipes shown are the ones that were accessed most recently (PASS)
Priority: COULD HAVE
Status: NOT STARTED


User can view the recipes that he/she created.
  - there is a separate tab for user to view his/her original recipes (PASS)
  - the tab contains only recipes that the user himself/herself created (PASS)
  - statistics are shown below each recipe (avg rating, times viewed) (PASS)
Priority: COULD HAVE
Status: NOT STARTED


User can request recipes that can be made from the ingredients in the fridge.
  - attempt to request possible recipes from the ingredients in a fridge (PASS)
  - attempt to request recipes with the fridge empty - should not show any recipes (PASS)
  - attempt to request possible recipes with specific combination of ingredients that should bring up a known recipe (PASS)
  - attempt to request suggestions with ingredients that are not sufficient to make anything - should not bring any suggestions (but see below) (PASS)
Priority: COULD HAVE
Status: NOT STARTED


User can choose whether recipes are shown on the home page or not.
  - enable the 'show recipes' option and ensure that it is shown (PASS)
  - disable the 'show recipes' option and ensure that it is not shown (PASS)
Priority: WOULD LIKE TO HAVE
Status: NOT STARTED


Upon entering part of the ingredient's name, drop-down appears to shown autocomplete options.
  - entering an existing ingredient shows a drop-down with its name (PASS)
  - entering non-existent ingredient does not show a drop-down (PASS)
  - entering combination that has more than one option shows all of them, or at least 5 of them (PASS)
  - clicking on autocomplete option sends the correct data (the one shown in autocomplete) (PASS)
Priority: WOULD LIKE TO HAVE
Status: NOT STARTED


User can enter more than one ingredient in a search bar to search recipes containing all of the entered ingredients.
  - entering one ingredient shows all recipes containing it (PASS)
  - entering more than one ingredient shows all recipes that contain them (PASS)
  - entering nothing does nothing (PASS)
  - entering half phrases does not match with anything (PASS)
Priority: WOULD LIKE TO HAVE
Status: NOT STARTED


User can search for a recipe through a search bar.
  - entering recipe's title brings up the information about the recipe (PASS)
  - entering non-existent recipe will not show any results (PASS)
  - entering non-existent recipe will offer user to add it (PASS)


User can enter more than one recipe in a search bar to search common ingredients.
  - entering a recipe will show its description and ingredients (PASS)
  - entering more than one recipe will show common ingredient list (PASS)
  - leaving the field blank will do nothing (PASS)
Priority: WOULD LIKE TO HAVE
Status: NOT STARTED


User can request recipes that he/she can make from ingredients with n ingredients missing in the fridge.
  - attempt to request a recipe for which 1 ingredient is missing (PASS)
  - attempt to request a recipe for which n-1 ingredients are missing (PASS)
  - attempt to request a recipe for which n ingredients are missing (PASS)
  - attempt to request a recipe for which n+1 ingredients are missing (PASS)
Priority: WOULD LIKE TO HAVE
Status: NOT STARTED


User can edit ingredients to the fridge.
  - attempt to add an ingredient to the fridge (PASS)
  - attempt to remove ingredient from the fridge (PASS)
  - attempt to change the quantity of an ingredient (PASS)
Priority: WOULD LIKE TO HAVE
Status: NOT STARTED


User can ask for a shop list for specified recipes.
  - attempt to make up a shopping list for a specified recipe (PASS)
  - attempt to add recipes to a shopping list (PASS)
  - attempt to make up a shopping list for multiple recipes (PASS)
  - attempt to request ingredients for an empty basket - should show no ingredients (PASS)
Priority: WOULD LIKE TO HAVE
Status: NOT STARTED


User can hover on the unit of measurement to get its description and conversions.
  - hover on unit of measurement to see description (PASS)
Priority: WOULD LIKE TO HAVE
Status: NOT STARTED
