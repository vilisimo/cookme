##About
Contains tasks that need attention sometime in the future. This is not 
meant to be a document that lists ALL the tasks that need to be done. 
The purpose of the document is simply to help me keep a track of tasks
that should eventually be done (and that are likely to be forgotten by
me if not documented).

###Tasks
- Extract relevant parts of jquery.formset.js script and create another 
one with relevant functionality only.
- RecipeIngredientForm: how to inherit the form from Fridge and change 
exclude, etc., so that I do not have to repeat almost all of the code in it?
- Somehow deal with plurals? Have two values for each unit?
- Different quantities: what if recipe requires 2 cups of sugar, whereas you 
have 500g? Also, what if user has 500g of sugar in a fridge, but decides to 
add another helping of 3 tablespoons? One possible solution: have functions 
that convert various different units to other units. Whichever was first in 
the fridge, stays. All additions are converted to that unit. OR if 500g 
converted to cups is more than 1 cup, everything is converted to grams. 
Multiple ways to do it.
- Refactor tests to use RequestFactory for quicker tests. Relevant link:
http://matthewdaly.co.uk/blog/2015/08/02/testing-django-views-in-isolation/
- Change ingredient 'type' to something else. Now shadows built-in name.
- Figure out a way to separate multi-word ingredients. Dash (current) does 
not seem to be a safe choice. Maybe something else instead of it?
- Update mock_db.py to have stuff that is used in other tests, so that code 
duplication can be reduced. 
- Include some kind of config file in which common HTML phrases (e.g., no 
recipes found) could be written down. This way, can import them in views, 
pass on to templates, use in tests, etc., no need to change in multiple places.
- On testing population script: see utilities/tests/test_populate.py.
- Merge fridge_subset_recipes() with subset_recipes().

JavaScript:
1. Highlight current page in navbar.