import json

def clear_console():
    """this function uses ANSI escape codes to clear previous responses from the console"""
    print("\033[H\033[J", end="")

class Recipes:
    def __init__(self):
        # using a try except block means it will work even if there is no file or the file doesn't load
        try:
            # using a with statement to open the file safely, ensuring it will be closed properly, even if there is a problem
            with open('./recipes.json', 'r') as recipes_file:
                self.recipes: dict = json.load(recipes_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.recipes: dict = {}

    def find_valid_name(self):
        """this function takes an input and checks whether it appears in the keys of the recipes dictionary (using the
        lower method to ignore capitalisation. If a case-insensitive match is found, the input string is replaced by the
        matching key to ensure an exact match, so it can be used for dictionary lookups."""
        while True:
            name = input("Enter a recipe name ('back' to go back):\n")

            # because i need to iterate over all names separately rather than a concatenated string of names, the
            # quickest way to make this comparison case-insensitive is to make a new list with the keys in lower case
            lower_recipes = [name.lower() for name in self.recipes]
            if name.lower() in lower_recipes:
                # this ensures that the 'name' variable exactly matches the dictionary key
                for r in self.recipes:
                    if name.lower() == r.lower():
                        name = r
                break
            elif name.lower() == "back": # needed a way to escape if there aren't any recipes to choose
                break
            else:
                print("\nRecipe not found, please try again.\n")

        return name

    def move_to_display_menu(self):
        """there are two different places that I wanted to lead to the same 'display recipe' options menu, so I wrote
        that functionality into a method to avoid repeating it in two places"""
        while True:
            print("\nPlease choose an option:")
            print("1. Display a recipe")
            print("2. Return to main menu.")

            choice = input("\nEnter your choice 1 - 2:\n")

            if choice == "1":
                self.display_recipe()
            elif choice == "2":
                return
            else:
                print("Invalid choice, please try again.")
                continue

    def save_recipes(self):
        """this method is automatically called at the end of any other method that changes the recipes dictionary"""
        with open('recipes.json', 'w') as recipes_file:
            json.dump(self.recipes, recipes_file)

    def add_recipe(self):
        # initialise dictionary object to store recipe data
        new_recipe = {}

        # input ingredients
        ingredients = {}
        while True:
            next_ingredient = input("Enter an ingredient, leave blank when finished:\n")
            if not next_ingredient:
                break
            next_quantity = input("Enter a quantity:\n")
            ingredients[next_ingredient] = next_quantity
        new_recipe['ingredients'] = ingredients

        # input instructions
        instructions = []
        while True:
            next_instruction = input("Enter an instruction, leave blank when finished:\n")
            if not next_instruction:
                break
            instructions.append(next_instruction)
        new_recipe['instructions'] = instructions

        # input tags
        new_recipe['tags'] = []
        while True:
            new_tag = input("Enter a tag, leave blank to finish:\n")
            if not new_tag:
                break
            new_recipe['tags'].append(new_tag)

        # input author
        new_recipe['author'] = input("Enter the author:\n")

        # input rating
        new_recipe = self.add_rating(new_recipe)

        # add recipe to recipes dictionary
        name = input("Enter a recipe name:\n")
        self.recipes[name] = new_recipe
        self.save_recipes()

    def add_rating(self, recipe: dict):
        """this method is called during the add_recipe method, not from an options menu"""
        while True:
            # catch non-numerical inputs
            try:
                rating = int(input("Enter a rating (1-5):\n"))
                # validate input in correct range
                if rating > 5 or rating < 1:
                    print("Invalid rating entered, please use a number from 1 to 5.")
                    continue
                recipe['rating'] = rating
                break
            except ValueError:
                print("Invalid rating entered, please use a number from 1 to 5.")

        return recipe

    def delete_recipe(self):
        clear_console()
        print("Delete Recipe")

        # get a valid recipe name or go back to previous menu
        name = self.find_valid_name()
        if name == "back":
            return

        # verify user's intention
        answer = input("Are you sure you want to delete this recipe? (y/n): ")
        if answer in ["y", "Y", "yes", "YES", "Yes"]:
            del self.recipes[name]
            self.save_recipes()
            print(f"{name} removed")
        else:
            input("Recipe not deleted, press enter to return to main menu.")

    def view_recipes(self):
        """this method prints the name of every recipe in the system"""
        clear_console()
        print("\nView All Recipes")
        print("\nRecipe Titles:")

        # iterate through recipes dictionary and print each key
        for recipe in self.recipes.keys():
            print(f"- {recipe}")

        self.move_to_display_menu()

    def search_recipes(self):
        """takes a user's search query and prints a list of any recipes that have that search term in the title,
        ingredients or tags"""
        clear_console()

        # get a search query
        query = input("\nSearch for a recipe name, category, or ingredient:\n")

        # initialise list for search results
        filtered_recipes = []

        # join all strings in ingredients and tags lists to make them quicker to search
        # use the .lower string method in the comparisons to make them case-insensitive
        for title, recipe in self.recipes.items():
            if query.lower() in title.lower():
                filtered_recipes.append(title)
            elif query.lower() in ' '.join(recipe['ingredients']).lower():
                filtered_recipes.append(title)
            elif query.lower() in ' '.join(recipe['tags']).lower():
                filtered_recipes.append(title)

        # print the list items if there are any
        if not filtered_recipes:
            print("No recipes found")
        else:
            print("\nRecipes matching search:")
            for recipe in filtered_recipes:
                print(f"- {recipe}")

        # show option to display a recipe
        self.move_to_display_menu()

    def edit_recipe(self):
        """takes user input and calls the relevant editing function"""

        # get a valid recipe name or go back to previous menu
        name = self.find_valid_name()
        if name == "back":
            return

        while True:
            clear_console()
            print(f"Editing Recipe: {name}")
            print("\nPlease choose an option:")
            print("1. Change Name")
            print("2. Edit Tags")
            print("3. Edit Ingredients")
            print("4. Edit Instructions")
            print("5. Edit Rating")
            print("6. Save recipe and exit editing")
            print("7. Exit without saving")

            choice = input("\nEnter your choice (1-7):\n")

            if choice == '1':
                name = self.edit_name(name)
            elif choice == '2':
                self.edit_tags(name)
            elif choice == '3':
                self.edit_ingredients(name)
            elif choice == '4':
                self.edit_instructions(name)
            elif choice == '5':
                self.recipes[name] = self.add_rating(self.recipes[name])
            elif choice == '6':
                self.save_recipes()
                break
            elif choice == "7":
                break
            else:
                print("\nInvalid choice")
                continue

    def edit_name(self, name: str):

        clear_console()
        while True:
            # get user input
            new_name = input("\nEnter new recipe name:")

            # check for collisions
            if new_name in self.recipes:
                print("\nPlease use a name that hasn't been used already")
                continue

            # replace recipe name
            self.recipes[new_name] = self.recipes[name]
            del self.recipes[name]

            # confirm name change
            print(f"\n{name} succesfuly changed to {new_name}")
            input("\nPress enter to return to Edit Recipe menu.")

            # output new name to update other parts of the program
            return new_name

    def edit_tags(self, name: str):
        while True:
            clear_console()

            # display options
            print(f"Editing {name} tags")
            print("\nPlease choose an option:")
            print("1. Add new tag")
            print("2. Remove existing tag")
            print("3. Go back")

            # take user input
            choice = input("\nEnter your choice (1-3):\n")

            # call functions
            if choice == '1':
                self.add_tag(name)
            elif choice == "2":
                self.delete_tag(name)
            elif choice == "3":
                break
            else:
                print("\nInvalid choice")
                continue

    def add_tag(self, name: str):
        """appends new tag to the list of tags"""

        print(f"Existing tags: {self.recipes[name]["tags"]}")
        self.recipes[name]["tags"].append(input("Enter new tag: "))
        print(f"Updated tags: {self.recipes[name]['tags']}")
        input("\nPress enter to return to Edit Tags menu.")

    def delete_tag(self, name: str):
        """removes a specified tag from the list"""

        print(f"Existing tags: {self.recipes[name]["tags"]}")

        # keep asking for input until valid tag is entered
        while True:
            unwanted = input("Enter tag to remove: ")
            if unwanted in self.recipes[name]["tags"]:
                break
            print("Invalid tag entered, please try again.")

        # remove tag
        self.recipes[name]["tags"].remove(unwanted)
        print(f"Updated tags: {self.recipes[name]['tags']}")

        input("\nPress enter to return to Edit Tags menu.")

    def edit_ingredients(self, name: str):
        """calls the relevant editing function for ingredients"""

        while True:
            clear_console()

            # display options
            print(f"Editing {name} ingredients")
            print("\nPlease choose an option:")
            print("1. Add new ingredient")
            print("2. Remove existing ingredient")
            print("3. Edit quantity of existing ingredient")
            print("4. Go back")

            choice = input("\nEnter your choice (1-4):\n")

            if choice == '1':
                self.add_ingredient(name)
            elif choice == "2":
                self.delete_ingredient(name)
            elif choice == "3":
                self.edit_quantity(name)
            elif choice == "4":
                break
            else:
                print("\nInvalid choice")
                continue

    def add_ingredient(self, name: str):
        title = "existing ingredients:"
        while True:
            clear_console()

            # display current ingredients
            print(f"{name} {title}")
            for k, v in self.recipes[name]['ingredients'].items():
                print(f"{v:<10}{k}")

            # display options
            print("\nPlease choose an option:")
            print("1. Add new ingredient")
            print("2. Go back")

            choice = input("\nEnter your choice (1-2):\n")
            if choice == "1":
                new_ingredient = input("Enter a new ingredient: ")
                new_quantity = input("Enter a quantity: ")
                self.recipes[name]['ingredients'][new_ingredient] = new_quantity
                title = "updated ingredients:"
                continue
            elif choice == "2":
                break
            else:
                print("\nInvalid choice")
                continue

    def delete_ingredient(self, name: str):
        """deletes an item from the ingredients dictionary"""
        title = "existing ingredients:"
        while True:
            # display existing ingredients
            clear_console()
            print(f"{name} {title}")
            for k, v in self.recipes[name]['ingredients'].items():
                print(f"{v:<10}{k}")

            # display options
            print("\nPlease choose an option:")
            print("1. Remove an ingredient")
            print("2. Go back")

            # make choice
            choice = input("\nEnter your choice (1-2):\n")
            if choice == "1":
                # keep trying to remove specified ingredient until a valid key is used
                while True:
                    ingredient = input("Enter the ingredient to remove: ")
                    try:
                        del self.recipes[name]['ingredients'][ingredient]
                        title = "updated ingredients:"
                        break
                    except KeyError:
                        print("Invalid ingredient, please type the ingredient exactly as it appears")
                        continue
            # this will break out of the while loop and the whole function
            elif choice == "2":
                break
            # this will go back to the start of the while loop to try again
            else:
                print("\nInvalid choice")
                continue

    def edit_quantity(self, name: str):
        """updates the quantity of existing ingredients"""
        title = "existing ingredients:" # this will change to 'updated ingredients' once updated
        while True:
            # display current ingredients
            clear_console()
            print(f"{name} {title}")
            for k, v in self.recipes[name]['ingredients'].items():
                print(f"{v:<10}{k}")

            # display options
            print("\nPlease choose an option:")
            print("1. Edit an ingredient quantity")
            print("2. Go back")

            # make choice
            choice = input("\nEnter your choice (1-2):\n")
            if choice == "1":
                # keep asking for an ingredient to edit until a valid one is entered
                while True:
                    ingredient = input("Enter the ingredient to edit: ")
                    try:
                        new_quantity = input("Enter a new quantity: ")
                        self.recipes[name]['ingredients'][ingredient] = new_quantity
                        title = "updated ingredients:"
                        break
                    except KeyError:
                        print("Invalid ingredient, please type the ingredient exactly as it appears")
                        continue
            # this breaks out of the while loop and ends the whole function
            elif choice == "2":
                break
            # this goes back to the start of the while loop
            else:
                print("\nInvalid choice")
                continue

    def edit_instructions(self, name: str):
        """provides options to call the methods that add new instructions and delete existing instructions"""
        while True:
            # display options
            clear_console()
            print(f"Edit {name} instructions")
            print("\nChoose an option:")
            print("1. Add new instruction")
            print("2. Remove existing instruction")
            print("3. Go back")

            # make choice
            choice = input("\nEnter your choice 1 - 3:\n")
            if choice == '1':
                self.add_instruction(name)
            elif choice == "2":
                self.delete_instruction(name)
            elif choice == "3":
                break
            else:
                print("\nInvalid choice")
                continue

    def add_instruction(self, name: str):
        """adds a new instruction at a specified position in the list"""
        title = "existing instructions:"
        while True:
            # display current instructions
            clear_console()
            print(f"{name} {title}")
            for n, inst in enumerate(self.recipes[name]['instructions']):
                print(f"{n+1}. {inst}")

            # display options
            print("\nPlease choose an option:")
            print("1. Add new instruction")
            print("2. Go back")

            # make choice
            choice = input("\nEnter your choice (1-2):\n")
            if choice == "1":
                new_inst = input("Enter new instruction: ")
                new_index = int(input("Enter position to insert new instruction: "))
                self.recipes[name]['instructions'].insert(new_index-1, new_inst)
                title = "updated instructions:"
                continue
            elif choice == "2":
                break
            else:
                input("\nInvalid choice, press enter to try again.")
                continue

    def delete_instruction(self, name: str):
        """deletes existing instruction from specified position in the list"""
        title = "existing instructions:" # when updated, this will change to 'updated instructions'
        while True:
            # display existing instructions
            clear_console()
            print(f"{name} {title}\n")
            for n, inst in enumerate(self.recipes[name]['instructions']):
                print(f"{n+1}. {inst}")

            # display options
            print("\nPlease choose an option:")
            print("1. Delete an instruction")
            print("2. Go back")

            # make choice
            choice = input("\nEnter your choice (1-2):\n")
            if choice == "1":
                # find the range of valid indices
                max_num = len(self.recipes[name]['instructions'])
                # keep asking for an index until a valid one is entered
                while True:
                    index = int(input(f"Enter position of unwanted instruction (1-{max_num}): "))
                    try:
                        self.recipes[name]['instructions'].pop(index-1)
                        title = "updated instructions:"
                        break
                    except IndexError:
                        print("Invalid position, try again.")
                continue
            elif choice == "2":
                break
            else:
                print("\nInvalid choice")
                continue

    def edit_rating(self, name: str):
        """updates an existing rating"""
        # keep asking for input until a valid rating is entered
        while True:
            clear_console()
            print(f"Edit {name} rating\n")
            try:
                new_rating = int(input("Enter a rating (1-5):\n"))
                self.recipes[name]['rating'] = new_rating
                break
            except ValueError:
                print("Invalid rating entered, please use a number from 1 to 5.")

    def display_recipe(self):
        # get a valid recipe name or go back to previous menu
        title = self.find_valid_name()
        if title == "back":
            return

        # display recipe details
        clear_console()
        print(f"{title} by {self.recipes[title]['author']}")
        print(f"\nRating: {self.recipes[title]['rating']} / 5")
        print(f"Tags: {', '.join(self.recipes[title]['tags'])}")
        print("\nIngredients")
        for k, v in self.recipes[title]['ingredients'].items():
            print(f"{v:<10}{k}")
        print("\nInstructions")
        for i in self.recipes[title]['instructions']:
            print(f"- {i}")
        input("\nPress enter to return to previous menu.")
