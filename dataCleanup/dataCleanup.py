import json
from cleanIngredientsInstructions import CleanIngredientsAndInstructions as cii
from clearDuplicates import ClearDuplicates as cdup

def dataCleanup(data_to_clean):    
    id = 0
    new_data = {}
    for i in range(len(data_to_clean)):
    
        with open(data_to_clean[i], "r") as recipe_file:
            recipes = json.load(recipe_file)
        
 
        for rec in recipes:
            print(id)
            if not recipes[rec]:
                continue
            if recipes[rec]["ingredients"] and recipes[rec]["instructions"]:
                new_ingredient_list = cii.cleanIngredients(recipes[rec]["ingredients"])
                new_instructions_list = cii.cleanInstructions(recipes[rec]["instructions"])
            else: 
                continue

            new_data[id] = {
                "title" : recipes[rec]["title"].rstrip(),
                "ingredients" : new_ingredient_list,
                "instructions" : new_instructions_list,
                "picture_link" : recipes[rec]["picture_link"] 
            }
            
            if id % 5000 == 0:
                try:
                    with open("dataCleanup/combined_and_cleaned_recipes.json", "r") as file:
                        data = json.load(file)
                except FileNotFoundError:
                    data = {}
                data.update(new_data)

                with open("dataCleanup/combined_and_cleaned_recipes.json", "w") as file:
                    json.dump(data, file, indent=4)
                new_data = {}
            id += 1
        
        # # Add any leftover data in new_data
        with open("dataCleanup/combined_and_cleaned_recipes.json", "r") as file:
                data = json.load(file)
        data.update(new_data)

        with open("dataCleanup/combined_and_cleaned_recipes.json", "w") as file:
            json.dump(data, file, indent=4)
        new_data = {}

    # Clear true duplicates
    with open("dataCleanup/combined_and_cleaned_recipes.json", "r") as in_file:
        data = json.load(in_file)
    dup_title_ids = cdup.checkDuplicates(data)
    true_dups = cdup.verifyDuplicateRecipes(dup_title_ids, data)
    cdup.createFileNoDups(true_dups, data)


def main():
    data_to_clean = ['dataCleanup/recipes_raw_nosource_ar.json', 'dataCleanup/recipes_raw_nosource_epi.json', 'dataCleanup/recipes_raw_nosource_fn.json']
    dataCleanup(data_to_clean)

if __name__ == "__main__":
    main()