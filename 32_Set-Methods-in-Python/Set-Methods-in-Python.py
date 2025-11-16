s={1,2,3,2,}

s.add(7)
s.update([3,4,6])
s.remove(2)
# s.clear()  #clear all the set 
s.discard(5)

# Merge two sets (union)
a = {1, 2}
b = {2, 3}
print(a.union(b))    # {1, 2, 3}

# Return common elements
a = {1, 2, 3}
b = {2, 3, 4}
print(a.intersection(b))   # {2, 3}

# difference() -- Elements in A but not in B
print(a.difference(b))     # {1}

# symmetric_difference() → Elements not common
print(a.symmetric_difference(b))   # {1, 4}

# issubset()
{1, 2}.issubset({1, 2, 3})     # True

# issuperset()
{1, 2, 3}.issuperset({1, 2})   # True

# isdisjoint()
{1, 2}.isdisjoint({3, 4})      # True

# delete a full set
# del setname