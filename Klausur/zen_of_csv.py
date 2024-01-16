import csv

class FamilyMember:
    # Constructor for FamilyMember class
    def __init__(self, first_name, last_name='', mother=None, father=None):
        self.first_name = first_name
        self.last_name = last_name
        self.mother = mother
        self.father = father
        self.partner = None
        self.children = []

    # Sets the partner of the family member
    def set_partner(self, partner):
        self.partner = partner

    # Adds a child to the family member's list of children
    def add_child(self, child):
        self.children.append(child)

# Creates a family tree from a CSV file
def create_family_tree(csv_file):
    family = {}
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Extracting member information from each row
            first_name = row['FirstName']
            last_name = row['LastName']
            mother_name = row['Mother']
            father_name = row['Father']
            full_name = f"{first_name} {last_name}"

            # If the member is not already in the family, add them
            if full_name not in family:
                family[full_name] = FamilyMember(first_name, last_name)

            member = family[full_name]

            # Linking the member to their mother if she exists in the family tree
            if mother_name and mother_name in family:
                mother = family[mother_name]
                member.mother = mother
                mother.add_child(member)
                if member.father:
                    mother.set_partner(member.father)

            # Linking the member to their father if he exists in the family tree
            if father_name and father_name in family:
                father = family[father_name]
                member.father = father
                father.add_child(member)
                if member.mother:
                    father.set_partner(member.mother)

    return family

# Finds grandparents of a given family member
def find_grandparents(family, member):
    grandparents = {
        'Grandmother (Mother Side)': None,
        'Grandfather (Mother Side)': None,
        'Grandmother (Father Side)': None,
        'Grandfather (Father Side)': None
    }

    # Identifying and assigning grandparents from both mother's and father's side
    if member.mother:
        if member.mother.mother:
            grandparents['Grandmother (Mother Side)'] = member.mother.mother
        if member.mother.father:
            grandparents['Grandfather (Mother Side)'] = member.mother.father

    if member.father:
        if member.father.mother:
            grandparents['Grandmother (Father Side)'] = member.father.mother
        if member.father.father:
            grandparents['Grandfather (Father Side)'] = member.father.father

    return grandparents

# Retrieves family information for a given member
def find_family_information(family, full_name):
    if full_name in family:
        member = family[full_name]
        grandparents = find_grandparents(family, member)
        return {
            'Grandparents': grandparents,
            'Mother': member.mother,
            'Father': member.father,
            'Partner': member.partner
        }
    else:
        return None

# Finds children of a given parent
def find_children(family, parent):
    children = []
    for member in family.values():
        if member.mother == parent or member.father == parent:
            children.append(member)
    return children

# Finds grandchildren given a list of children
def find_grandchildren(children):
    grandchildren = []
    for child in children:
        grandchildren.extend(child.children)
    return grandchildren

# Displays family information including children and grandchildren

def display_family_information(info, children, grandchildren):
    # Displaying each key-value pair in the info dictionary
    for key, value in info.items():
        if value:
            # If the value is a FamilyMember object, display full name
            if isinstance(value, FamilyMember):
                print(f'{key}: {value.first_name} {value.last_name}')
            else:
                print(f'{key}: {value}')
        else:
            print(f'{key}: None')

    # Displaying the names of children and grandchildren
    print("Children:", ', '.join([f"{child.first_name} {child.last_name}" for child in children]))
    print("Grandchildren:", ', '.join([f"{grandchild.first_name} {grandchild.last_name}" for grandchild in grandchildren]))

# Main function to run the program
def main():
    csv_file_path = 'family_tree_zenofcsv.csv'
    # Creating the family tree from the CSV file
    family_tree = create_family_tree(csv_file_path)
    
    # Prompting user to enter the name of the family member
    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")
    full_name = f"{first_name} {last_name}"

    # Finding and displaying family information for the entered name
    family_information = find_family_information(family_tree, full_name)
    if family_information:
        person = family_tree[full_name]
        children = find_children(family_tree, person)
        grandchildren = find_grandchildren(children)
        display_family_information(family_information, children, grandchildren)
    else:
        print("Member not found")

# Ensuring the main function is called when the script is executed directly
if __name__ == "__main__":
    main()