import json

def cleanIngredients(ingredients):
    """
    Deletes 'ADVERTISEMENT' in ingredient, if applicable.
    """
    new_ingredient_list = []
    for ingredient in ingredients:
        ingredient_list = ingredient.split()
        ingredient_list = [item for item in ingredient_list if item != "ADVERTISEMENT"]
        new_ingredient_string = " ".join(ingredient_list)
        if new_ingredient_string:
            new_ingredient_list.append(new_ingredient_string)
    return new_ingredient_list

def cleanInstructions(instructions):
    """
    Handles issue where first step in instructions is a string of all instructions, leading to duplicates
    Converts the string of instructions to a numbered list of instructions.
    """
    new_instructions_list = []
    step_num = 1
    instructions_list = instructions.split("\n")
    if len(instructions_list) > 1 and instructions_list[1] in instructions_list[0]:
        instructions_list = instructions_list[1:]
    for i in instructions_list: 
        if i:
            inst_str = f'{str(step_num)}. {i}'
            new_instructions_list.append(inst_str)
            step_num += 1
    return new_instructions_list
    

def main():
    id = 0
    new_data = {}
    data_to_clean = ['dataCleanup/recipes_raw_nosource_ar.json', 'dataCleanup/recipes_raw_nosource_epi.json', 'dataCleanup/recipes_raw_nosource_fn.json']
    for i in range(len(data_to_clean)):
    
        with open(data_to_clean[i], "r") as recipe_file:
            recipes = json.load(recipe_file)
        
 
        for rec in recipes:
            print(id)
            if not recipes[rec]:
                continue
            if recipes[rec]["ingredients"] and recipes[rec]["instructions"]:
                new_ingredient_list = cleanIngredients(recipes[rec]["ingredients"])
                new_instructions_list = cleanInstructions(recipes[rec]["instructions"])
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



if __name__ == "__main__":
    main()