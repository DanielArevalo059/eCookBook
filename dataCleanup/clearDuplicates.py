import json

def checkDuplicates(data):
    title_dict = {}
    duplicates = {} #duplicate objects; "title" : [ids]
    
    # Track duplicate titles, save id of duplicate titles in duplicates dict
    for r in data:
        rec_title = data[r]["title"].lower()
        if rec_title in title_dict:
            duplicates.setdefault(rec_title, [title_dict[rec_title]]).append(r)
        else:
            title_dict[rec_title] = r

    # Create list of lists of duplicate title ids
    dup_title_ids = []
    for dup in duplicates.values():
        dup_title_ids.append(dup)

    return dup_title_ids
    
def verifyDuplicateRecipes(dup_data, data):
    """
    Loop through all duplicate ids and compare the object of each id to all objects ahead of it in the list
    Create and return a set of one id of true duplicates
    """
    true_dups = set()
    for i in range(len(dup_data)):
        id_list = dup_data[i]
        for j in range(len(id_list)):
            rec_id_1 = id_list[j]
            rec_obj_1 = data[rec_id_1]
            for k in range(j+1, len(id_list)):
                rec_id_2 = id_list[k]
                rec_obj_2 = data[rec_id_2]
                if rec_obj_1 == rec_obj_2:
                    true_dups.add(rec_id_1)
    return true_dups
    


def createFileNoDups(true_dups, data):
    """
    Loop through original data, create new data excluding the ids of duplicates
    Dump new data
    """
    id = 0
    new_data = {}
    for recipe in data:
        
        if recipe in true_dups:
            continue
        new_data[id] = data[recipe]
        id += 1
    with open("combined_cleaned_nodups_recipes.json", "w") as out:
        json.dump(new_data, out, indent=4)
    

def main(data):
    dup_title_ids = checkDuplicates(data)
    true_dups = verifyDuplicateRecipes(dup_title_ids, data)
    createFileNoDups(true_dups, data)


if __name__ == "__main__":
    with open("combined_and_cleaned_recipes.json", "r") as in_file:
        data = json.load(in_file)
    main(data)
