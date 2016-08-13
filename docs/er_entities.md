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
| *name* | Name of the recipe. |
| *description* | Description of the recipe (instructions). |
| *author (FK)* | User that has created the recipe. |
| *date* | When the recipe was added. |
| *views* | How many times the recipe has been viewed. |

###Fridge
| Field | Description |
| --- | --- |
| *owner (FK)* | Fridge's owner (user). |

###Ingredient
| Field | Description |
| --- | --- |
| *name* | Name of the ingredient |
| *description* | Description of the ingredient. |

###FridgeRecipe
| Field | Description |
| --- | --- |
| *fridge (FK)* | Fridge the recipe belongs to. |
| *recipe (FK)* | Recipe that belongs to the fridge. |

###FridgeIngredient
| Field | Description |
| --- | --- |
| *fridge (FK)* | Fridge the ingredient belongs to. |
| *ingredient (FK)* | Recipe that belongs to the fridge. |

###RecipeIngredient
| Field | Description |
| --- | --- |
| *recipe (FK)* | Recipe that the ingredient is part of. |
| *ingredient (FK)* | Ingredient that makes up the recipe. |

###Quantity
| Field | Description |
| --- | --- |
| *measurement* | Name of the measurement (oz/ml/etc). |
| *description* | Description of the measurement. |

###User
| Field | Description |
| --- | --- |