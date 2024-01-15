import csv

class FamilyMember:
    def __init__(self, first_name, last_name, mother=None, father=None, partner=None):
        self.first_name = first_name
        self.last_name = last_name
        self.mother = mother
        self.father = father
        self.children = []
        self.partner = partner

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"

def find_member(family, first_name, last_name):
    for member in family:
        if member.first_name == first_name and member.last_name == last_name:
            return member
    return None

def create_family_tree(csv_file):
    family = []
    csv_data = []

    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_data.append(row)

    for row in csv_data:
        family_member = FamilyMember(row['FirstName'], row['LastName'])
        family.append(family_member)

    for row in csv_data:
        member = find_member(family, row['FirstName'], row['LastName'])
        if member:
            member.mother = find_member(family, *row['Mother'].split()) if row['Mother'] else None
            member.father = find_member(family, *row['Father'].split()) if row['Father'] else None
            member.partner = find_member(family, *row['Partner'].split()) if row['Partner'] else None
            if row['Children']:
                children_names = [child.split() for child in row['Children'].split(';')]
                member.children = [find_member(family, *child) for child in children_names]

    return family

def get_family_details(family, first_name, last_name):
    member = find_member(family, first_name, last_name)
    if not member:
        return "Member not found"

    parents = [parent for parent in [member.mother, member.father] if parent]
    grandmothers = [grandparent for parent in parents for grandparent in [parent.mother] if grandparent]
    grandfathers = [grandparent for parent in parents for grandparent in [parent.father] if grandparent]
    children = member.children
    grandchildren = [grandchild for child in children for grandchild in child.children if grandchild]

    return {
        'Parents': parents,
        'Grandmothers': grandmothers,
        'Grandfathers': grandfathers,
        'Children': children,
        'Grandchildren': grandchildren
    }

csv_file_path = 'family_tree.csv'
def main():
    family = create_family_tree(csv_file_path)

    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")

    family_details = get_family_details(family, first_name, last_name)
    print("\nFamily Details:")
    print(family_details)

if __name__ == "__main__":
    main()
