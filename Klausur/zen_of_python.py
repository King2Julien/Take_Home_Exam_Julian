import csv

class FamilyMember:
    def __init__(self, first_name, last_name='', mother=None, father=None):
        self.first_name = first_name
        self.last_name = last_name
        self.mother = mother
        self.father = father
        self.partner = None
        self.children = []

    def set_partner(self, partner):
        self.partner = partner

    def add_child(self, child):
        self.children.append(child)

def create_family_tree(csv_file):
    family = {}
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            first_name = row['FirstName']
            last_name = row['LastName']
            mother_name = row['Mother']
            father_name = row['Father']
            full_name = f"{first_name} {last_name}"

            if full_name not in family:
                family[full_name] = FamilyMember(first_name, last_name)

            member = family[full_name]

            if mother_name and mother_name in family:
                mother = family[mother_name]
                member.mother = mother
                mother.add_child(member)
                if member.father:
                    mother.set_partner(member.father)

            if father_name and father_name in family:
                father = family[father_name]
                member.father = father
                father.add_child(member)
                if member.mother:
                    father.set_partner(member.mother)

    return family

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
            'Partner': member.partner,
            'Children': member.children,
            'Grandchildren from Children': [child.children for child in member.children]
        }
    else:
        return None

def display_family_information(info):
    for key, value in info.items():
        if value:
            if key == 'Grandchildren from Children':
                grandchildren_info = {}
                for child in value:
                    if child:
                        grandchildren_info[child[0].first_name] = [gc.first_name for gc in child]
                print(f'{key}: {grandchildren_info}')
            elif isinstance(value, FamilyMember):
                print(f'{key}: {value.first_name} {value.last_name}')
            else:
                print(f'{key}: {value}')
        else:
            print(f'{key}: None')

def main():
    csv_file_path = 'family_tree_zenofpython.csv'
    family_tree = create_family_tree(csv_file_path)
    first_name = input("Enter the first name: ")
    last_name = input("Enter the last name: ")
    full_name = f"{first_name} {last_name}"

    family_information = find_family_information(family_tree, full_name)
    if family_information:
        display_family_information(family_information)
    else:
        print("Member not found")

if __name__ == "__main__":
    main()






# Create a family-tree function in python that takes an input of a name and surname and returns:
# Grandmother from the mother side.
# Grandfather from the mother side.
# Grandmother from the father side.
# Grandfather from the father side.
#Mother.
#Father.
#Partner.
#Children.
#Grandchildren from which children.
#
#Or print None if they don't exist.
#All the information is stored in a family_tree.csv file. The information is stored like this:
#Firstname,Lastname,Mother,Father
#Hans,Schmidt,Elisabeth Weber,Karl Schmidt
#Maximilian,Schmidt,Anna Bauer,Hans Schmidt
#Michael,Schmidt,Anna Bauer,Hans Schmidt
#
# The program should read all the information and should read that Michael Schmidt's Father, Hans Schmidt,
# his father Karl Schmidt is Michael Schmidt's Grandfather father side.
#And only with that little information the program should be able to recognize that Michael Schmidt's 
# grandparents are Elisabeth Weber and Karl Schmidt, Hans Schmidt's partner is Anna Bauer or Karl 
# Schmidt's grandchildren are Maximilian Schmidt and Michael Schmidt.
#The program should then print the family information.
    
# 
# if the program gets the input Maximilian Schmidt it should look who his parents are. In that 
# case his parents are Anna Bauer and Hans Schmidt. Then the program searches for Anna Bauer and
# looks for her parents. If the information about her parents are provided the the father of Anna Bauer 
# is === Grandfather mother side of Maximilian Schmidt and the father of Anna Bauer is the Grandmother 
# mother side of Maximilian Schmidt. Then the program searches for the father of Maximilian Schmidt 
# who is Hans Schmidt and looks at Hans Schmidt's parents. The father of Hans Schmidt === Grandfather 
# father side of Maximilian Schmidt and the mother of Hans Schmidt === Grandmother father side of
# Maximilian Schmidt.