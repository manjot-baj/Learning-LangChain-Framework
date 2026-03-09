nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# ----------------------------------
"""
Filter Functions
--> SELECT ELEMENT

filter(function, iterable)
Applies a function to each element
Keeps elements where the function returns True
"""

evens = list(filter(lambda n: n % 2 == 0, nums))
print(evens)

# -----------------------------------

"""
Map Functions
--> TRANSFORM/MODIFY ELEMENT
map(function, iterable)
Applies a function to every element
Returns transformed values
"""

doubles = list(map(lambda n: n * 2, evens))
print(doubles)

# ------------------------------------
"""
Reduce Function
--> COMBINE ELEMENT, Return a Combine single value

reduce(function, iterable)
Combines elements pair by pair
Produces one final value
"""

from functools import reduce

sum = reduce(lambda a, b: a + b, doubles)
print(sum)
