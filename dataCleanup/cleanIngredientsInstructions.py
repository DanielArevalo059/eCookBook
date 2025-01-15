class CleanIngredientsAndInstructions():

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