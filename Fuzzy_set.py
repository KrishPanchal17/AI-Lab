def fuzzy_union(A, B):
    return {x: max(A.get(x, 0), B.get(x, 0)) for x in set(A) | set(B)}

def fuzzy_intersection(A, B):
    return {x: min(A.get(x, 0), B.get(x, 0)) for x in set(A) & set(B)}

def fuzzy_complement(A):
    return {x: 1 - A[x] for x in A}

def is_subset(A, B):
    return all(A.get(x, 0) <= B.get(x, 0) for x in A)

def de_morgan_law(A, B):
    left1 = fuzzy_complement(fuzzy_union(A, B))
    right1 = fuzzy_intersection(fuzzy_complement(A), fuzzy_complement(B))
    
    left2 = fuzzy_complement(fuzzy_intersection(A, B))
    right2 = fuzzy_union(fuzzy_complement(A), fuzzy_complement(B))
    
    return left1 == right1, left2 == right2

def read_fuzzy_set(name):
    n = int(input(f"Enter the number of elements in fuzzy set {name}: "))
    fuzzy_set = {}
    for _ in range(n):
        x, mu = input("Enter element and its membership value (0 to 1): ").split()
        fuzzy_set[x] = float(mu)
    return fuzzy_set


print("Enter Fuzzy Set A:")
A = read_fuzzy_set("A")
print("Enter Fuzzy Set B:")
B = read_fuzzy_set("B")

union_result = fuzzy_union(A, B)
intersection_result = fuzzy_intersection(A, B)
complement_A = fuzzy_complement(A)
complement_B = fuzzy_complement(B)
subset_result = is_subset(A, B)

dm1, dm2 = de_morgan_law(A, B)

print("\nFuzzy Set A:", A)
print("Fuzzy Set B:", B)
print("Union (A ∪ B):", union_result)
print("Intersection (A ∩ B):", intersection_result)
print("Complement of A:", complement_A)
print("Complement of B:", complement_B)
print(f"Is A ⊆ B?: {'Yes' if subset_result else 'No'}")
print(f"De Morgan's Law 1 ((A ∪ B)^C == A^C ∩ B^C): {'Holds' if dm1 else 'Fails'}")
print(f"De Morgan's Law 2 ((A ∩ B)^C == A^C ∪ B^C): {'Holds' if dm2 else 'Fails'}")
