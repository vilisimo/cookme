##About
The document contains extension of ER diagram: fields that belong to models/entities.

###Rating
| Field | Description |
| --- | --- |
| *stars* | How many stars user has given the recipe. |
| *user (FK)* | Which user created the rating.
| *recipe (FK)* | Which recipe was rated.
| *date* | When the rating was created.

###Recipe
| Field | Description |
| --- | --- |
| *author (FK)* | User that has created the recipe. |
| *title* | Name of the recipe. |
| *description* | Description of the recipe (instructions). |
| *ingredients (m2m)* | Ingredients that make up the recipe. |
| *date* | When the recipe was added. |
| *views* | How many times the recipe has been viewed. |
| *image* | Image representing the recipe |

###Fridge
| Field | Description |
| --- | --- |
| *owner (FK)* | Fridge's owner (user). |
| *recipes (m2m)* | Recipes that belong to the fridge. |
| *ingredients (m2m)* | Ingredients that belong to the fridge. |

###Ingredient
| Field | Description |
| --- | --- |
| *name* | Name of the ingredient |
| *description* | Description of the ingredient. |

###Quantity
| Field | Description |
| --- | --- |
| *measurement* | Name of the measurement (oz/ml/etc). |
| *description* | Description of the measurement. |

###RecipeIngredientQuantity (tentative)
| Field | Description |
| --- | --- |
| *recipe (FK)* | Recipe that has ingredient. |
| *ingredient (FK)* | Ingredient that has quantity. |
| *quantity (FK)* | Quantity that has amount. |
| *amount* | Amount of the ingredient (float). |

###FridgeIngredientQuantity (tentative)
| Field | Description |
| --- | --- |
| *fridge (FK)* | Fridge that has ingredient. |
| *ingredient (FK)* | Ingredient that has quantity. |
| *quantity (FK)* | Quantity that has amount. |
| *amount* | Amount of the ingredient (float). |

###User
| Field | Description |
| --- | --- |