##About
Contains tasks that need attention sometime in the future. This is not 
meant to be a document that lists ALL the tasks that need to be done. 
The purpose of the document is simply to help me keep a track of tasks
that should eventually be done (and that are likely to be forgotten by
me if not documented).

###Tasks
- Figure out the relevant parts of jquery.formset.js script and create another 
one with relevant functionality only.
- RecipeIngredientForm: how to inherit the form from Fridge and change 
exclude, etc., so that I do not have to repeat almost all of the code in it?
- Somehow deal with plurals? Have two values for each unit?
- Refactor tests to use RequestFactory for quicker tests. Relevant link:
http://matthewdaly.co.uk/blog/2015/08/02/testing-django-views-in-isolation/
- Change ingredient 'type' to something else.
- Figure out whether Django encodes url string by default.
- Figure out a way to separate multi-word ingredients. Dash does not seem
to be a safe choice. Maybe something else instead of it?
- Figure out why settings cannot be reached when populate.py is called from 
root directory.
- Update mock_db.py to have stuff that is used in other tests, so that code 
duplication can be reduced. 
- Include some kind of config file in which common HTML phrases (e.g., no 
recipes found) could be written down. This way, can import them in views, 
pass on to templates, use in tests, etc., no need to change in multiple places.
- Would be nice to thoroughly test population script. At the moment, it is 
quite fragile.
- On testing population script: see utilities/tests/test_populate.py.
- Also, populate.py uses a lot of if name = main, would be nice to get rid of
 them.
