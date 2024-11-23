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