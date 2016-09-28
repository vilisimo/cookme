##About
Contains tasks that need attention as soon as possible. This is not 
meant to be a document that lists ALL the tasks that need to be done. 
The purpose of the document is simply to help me keep a track of tasks
that should eventually be done (and that are likely to be forgotten by
me).

###Tasks
- Make sure that a user can delete a recipe from his/her fridge.
- Figure out settings stuff.
- Figure out what the jquery.formset.js script does and create another one 
with relevant functionality only.
- Test ListView.
http://stackoverflow.com/documentation/django/1220/class-based-views#t=201609191926080087478
- RecipeIngredientForm: how to inherit the form from Fridge and change 
exclude, etc., so that I do not have to repeat almost all of the code in it?
- Somehow deal with plurals? Have two values for each unit?
- Refactor tests cases: almost all use the same URLs, etc. Can be put in 
setUp. Last: test_forms in recipes
- Refactor tests to use RequestFactory for quicker tests. Relevant link:
http://matthewdaly.co.uk/blog/2015/08/02/testing-django-views-in-isolation/