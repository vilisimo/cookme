## About
The document contains extension of ER diagram: fields that belong to 
models/entities.

### Ingredient
| Field | Description |
| --- | --- |
| *name* | Name of the ingredient |
| *type* | Type of the ingredient |
| *description* | Description of the ingredient. |
| *slug* | Ingredient's slug, derived from its name. |

### Unit
| Field | Description |
| --- | --- |
| *name* | Full name of the measurement unit (ounce/kilogram/etc.). |
| *abbrev* | Abbreviation of the measurement unit (oz/kg/ml/etc.). |
| *plural* | Plural form of unit name. |
| *description* | Description of the measurement. |

### Recipe
| Field | Description |
| --- | --- |
| *author (FK)* | User that has created the recipe. |
| *title* | Name of the recipe. |
| *description* | Short description of the recipe. |
| *steps* | Steps detailing how to cook the dish. |
| *cuisine* | Cuisine the dish belongs to.
| *ingredients* | Ingredients that make up a recipe. |
| *date* | When the recipe was added. |
| *views* | How many times the recipe has been viewed. |
| *slug* | Field that is used to compute URL. |
| *image* | Image representing the recipe |

### RecipeIngredient
| Field | Description |
| --- | --- |
| *recipe (FK)* | Recipe that has ingredient. |
| *ingredient (FK)* | Ingredient that has quantity. |
| *unit (FK)* | Quantity that has amount. |
| *quantity* | Amount of the ingredient (float). |

### Rating (currently not used)
| Field | Description |
| --- | --- |
| *stars* | How many stars user has given the recipe. |
| *user (FK)* | Which user created the rating.
| *recipe (FK)* | Which recipe was rated.
| *date* | When the rating was created.

### Fridge
| Field | Description |
| --- | --- |
| *owner (FK)* | Fridge's owner (User). |
| *visible* | Whether the fridge is visible to others. |
| *ingredients* | Ingredients in a fridge. |
| *recipes (M2M)* | Recipes in a fridge. |

### FridgeIngredient
| Field | Description |
| --- | --- |
| *fridge (FK)* | Fridge that has ingredient. |
| *ingredient (FK)* | Ingredient that has quantity. |
| *unit (FK)* | Quantity that has amount. |
| *quantity* | Amount of the ingredient (float). |

### User
| Field | Description |
| --- | --- |