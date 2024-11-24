# README

The user interface only seems to display properly when run in a linux terminal, when I run it in the pycharm console, 
the clear_console function doesn't do anything. I couldn't work out how to fix this but I guess the ANSI escape 
characters just aren't supported by the console in pycharm.

## Features
When you first run the program, you are presented with the main menu. Choose an option by typing the number and pressing 
enter.

You can add a new recipe, edit an existing one, or delete one that isn't needed. Each of these options will lead you 
through the process with prompts, and the last option in every menu is to go back to the previous menu.

You can also see a list of all recipes, or filter that list by searching for keywords in the titles, tags and 
ingredients of all recipes. Both of these options will lead onto displaying the details of a recipe, or you can go 
straight to displaying a recipe from the main menu if you know the recipe's name.

Each recipe contains the following details:
- author
- a rating out of 5
- a list of tags for easy searching
- a dictionary of ingredients with their quantities
- a list of instructions

## Implementation Decisions and Challenges
I decided to store each recipe as a dictionary, and keep all the recipes together in another dictionary, but since all 
the functions are working on the same recipe data, it made more sense to me to put it all in a class. I didn't implement 
anything for multiple users, but if I had done, each user could have a separate Recipes object and the filepath for the 
recipes.json file could include the username so each one could have a different recipes file.

I decided to move the Recipes class definition to a separate module because it was getting so long that I couldn't find 
things easily. But then I had two different modules both using the clear_console function, and if I left that in the 
main module, I would have to import it into the recipes_class module and then I would have circular imports, so I put 
clear_console in the recipes_class module and imported both in the same direction.

When I wrote the edit_name method which can be called inside the edit_recipe method, it created a problem. when the user 
called edit_recipe, it would ask for a recipe name to use for looking up the recipe in the dictionary. if the user then 
called edit name, it would change the dictionary key of the recipe and then execution would go back to the edit_recipe 
method which was still using the old recipe name. So I had to write the edit_name method slightly differently to all the 
others and make it return the new name, so that edit_recipe could use that return value to update the name variable.

I was pleased with how the clear_console function worked in the linux cli, but I couldn't work out why it didn't work 
inside pycharm. The program is still perfectly usable in pycharm, but it looks much better when the console clears for 
each new menu.

When I wrote the find_valid_name method, I realised that if the user gets to that point and doesn't know the name of any 
recipe (or if there aren't any recipes in the record), it will just keep asking for another attempt and there is no way 
out of that loop. So I added the 'back' option so there will always be a way to exit that function that is clearly 
presented to the user.