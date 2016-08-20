##About
The document contains extension of ER diagram: fields that belong to 
models/entities.

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
| *date* | When the recipe was added. |
| *views* | How many times the recipe has been viewed. |
| *slug* | Field that is used to compute URL. |
| *image* | Image representing the recipe |

###Fridge
Note: it is possible to model database in such a way, that there is no 
need for fridges. That is, all recipes and ingredients would have a FK
to User, and only an illusion of the fridge would be created in the 
front end. However, Fridge entity allows for multiple fridges in the 
future. Also, it improves clarity somewhat (at least for me).
| Field | Description |
| --- | --- |
| *owner (FK)* | Fridge's owner (User). |
| *visible * | Whether the fridge is visible to others. |

###Ingredient
| Field | Description |
| --- | --- |
| *name* | Name of the ingredient |
| *description* | Description of the ingredient. |

###Unit
| Field | Description |
| --- | --- |
| *unit* | Full name of the measurement unit (ounce/kilogram/etc.). |
| *abbrev* | Abbreviation of the measurement unit (oz/kg/ml/etc.) |
| *description* | Description of the measurement. |

###FridgeIngredient
| Field | Description |
| --- | --- |
| *fridge (FK)* | Fridge that has ingredient. |
| *ingredient (FK)* | Ingredient that has quantity. |
| *unit (FK)* | Quantity that has amount. |
| *quantity* | Amount of the ingredient (float). |

###RecipeIngredient
| Field | Description |
| --- | --- |
| *recipe (FK)* | Recipe that has ingredient. |
| *ingredient (FK)* | Ingredient that has quantity. |
| *unit (FK)* | Quantity that has amount. |
| *quantity* | Amount of the ingredient (float). |

###User
| Field | Description |
| --- | --- |