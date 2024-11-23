from recipes_class import Recipes, clear_console

# initialise Recipes object
recipes = Recipes()

# define the main menu
def main() -> None:
    while True:
        clear_console()
        print("\nRecipe Manager\n")
        print("1. Add a recipe")
        print("2. Edit a recipe")
        print("3. Delete a recipe")
        print("4. View all recipes")
        print("5. Search recipes")
        print("6. Display a Recipe")
        print("7. Exit")
        choice = input("\nEnter your choice (1-7):\n")
        if choice == "1":
            recipes.add_recipe()
        elif choice == "2":
            recipes.edit_recipe()
        elif choice == "3":
            recipes.delete_recipe()
        elif choice == "4":
            recipes.view_recipes()
        elif choice == "5":
            recipes.search_recipes()
        elif choice == "6":
            recipes.display_recipe()
        elif choice == "7":
            break
        else:
            print("\nInvalid choice. Try again.")

# run the main menu
if __name__ == "__main__":
    main()
