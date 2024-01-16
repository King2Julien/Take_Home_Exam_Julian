import csv

# Define a class for family members
class FamilyMember:
    def __init__(self, first_name, last_name='', mother=None, father=None):
        # Initialize the FamilyMember object with the provided attributes
        self.first_name = first_name
        self.last_name = last_name
        self.mother = mother
        self.father = father
        self.partner = None
        self.children = []

    def set_partner(self, partner):
        # Set the partner of this family member
        self.partner = partner

    def add_child(self, child):
        # Add a child to the list of children for this family member
        self.children.append(child)

# Function to create a family tree from a CSV file
def create_family_tree(csv_file):
    family = {}  # Dictionary to store family members
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_name = row['FirstName']
            last_name = row['LastName']
            mother_name = row['Mother']
            father_name = row['Father']
            full_name = f"{first_name} {last_name}"

            if full_name not in family:
                # Create a new FamilyMember if not already in the family dictionary
                family[full_name] = FamilyMember(first_name, last_name)

            member = family[full_name]

            if mother_name and mother_name in family:
                # Connect this member to their mother and set the partner if necessary
                mother = family[mother_name]
                member.mother = mother
                mother.add_child(member)
                if member.father:
                    mother.set_partner(member.father)

            if father_name and father_name in family:
                # Connect this member to their father and set the partner if necessary
                father = family[father_name]
                member.father = father
                father.add_child(member)
                if member.mother:
                    father.set_partner(member.mother)

    return family

# Function to find grandparents of a family member
def find_grandparents(family, member):
    grandparents = {
        'Grandmother (Mother Side)': None,
        'Grandfather (Mother Side)': None,
        'Grandmother (Father Side)': None,
        'Grandfather (Father Side)': None
    }

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

# Function to find family information about a member
def find_family_information(family, full_name):
    if full_name in family:
        member = family[full_name]
        grandparents = find_grandparents(family, member)
        return {
            'Grandmother (Mother Side)': grandparents['Grandmother (Mother Side)'],
            'Grandfather (Mother Side)': grandparents['Grandfather (Mother Side)'],
            'Grandmother (Father Side)': grandparents['Grandmother (Father Side)'],
            'Grandfather (Father Side)': grandparents['Grandfather (Father Side)'],
            'Mother': member.mother,
            'Father': member.father,
            'Partner': member.partner
        }
    else:
        return None

# Function to find children of a parent
def find_children(family, parent):
    children = []
    for member in family.values():
        if member.mother == parent or member.father == parent:
            children.append(member)
    return children if children else None

# Function to find grandchildren of a family member
def find_grandchildren(children):
    if children is None:
        return None

    grandchildren = []
    for child in children:
        grandchildren.extend(child.children)
    
    return grandchildren if grandchildren else None

# Function to display family information
def display_family_information(info, children, grandchildren):
    for key, value in info.items():
        if value:
            if isinstance(value, FamilyMember):
                # Display family member's name if it's a FamilyMember object
                print(f'{key}: {value.first_name} {value.last_name}')
            else:
                # Display other family information
                print(f'{key}: {value}')
        else:
            # Display "None" for missing information
            print(f'{key}: None')

    if grandchildren is not None:
        # Display children if they exist
        print("Children:", ', '.join([f"{child.first_name} {child.last_name}" for child in children]))
    else:
        # Display "None" if no children
        print("Children: None")

    if grandchildren is not None:
        # Display grandchildren if they exist
        print("Grandchildren:", ', '.join([f"{grandchild.first_name} {grandchild.last_name}" for grandchild in grandchildren]))
    else:
        # Display "None" if no grandchildren
        print("Grandchildren: None")

# Main function
def main():
    csv_file_path = 'family_tree_zenofcsv.csv'
    family_tree = create_family_tree(csv_file_path)
    
    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")
    full_name = f"{first_name} {last_name}"

    family_information = find_family_information(family_tree, full_name)
    if family_information:
        person = family_tree[full_name]
        children = find_children(family_tree, person)
        grandchildren = find_grandchildren(children)
        display_family_information(family_information, children, grandchildren)
    else:
        print("Member not found")

if __name__ == "__main__":
    main()
