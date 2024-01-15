# Define the family tree
family_tree = {
    'person1': {'parents': ['parent1', 'parent2'], 'children': ['child1', 'child2']},
    'parent1': {'parents': ['grandparent1', 'grandparent2'], 'children': ['person1', 'uncle1']},
    # ... more family members ...
}

def get_family_info(person_id):
    # Get parents and grandparents
    parents = family_tree.get(person_id, {}).get('parents', None)
    grandparents = []
    if parents:
        for parent in parents:
            grandparents.extend(family_tree.get(parent, {}).get('parents', []))
    else:
        grandparents = None

    # Get children and grandchildren
    children = family_tree.get(person_id, {}).get('children', None)
    grandchildren = []
    if children:
        for child in children:
            grandchildren.extend(family_tree.get(child, {}).get('children', []))
    else:
        grandchildren = None

    return {
        'parents': parents,
        'grandparents': grandparents,
        'children': children,
        'grandchildren': grandchildren
    }

# Example usage
person_info = get_family_info('person1')
print(person_info)
