# rand.nextDouble
Java rand.nextDouble prediction - in Python.
```
# Java rand.nextDouble prediction
# for java.util.Random
# In Python
# By George Mortimer
#
# From Java docs, the rand.nextDouble function generates a number as follows:
#---------------
#  public double nextDouble() {
#    return (((long)(next(26)) << 27) + next(27))
#     / (double)(1L << 53);
#  }
#---------------
# The next(x) function gets x bits of random data from the 48 bit seed
# It does this by taking the seed and bit shifting right by 48 - x 
# After every call to next(), the seed is recalculated as follows:
#---------------
#  next_seed = (seed * multiplier + addend) % mod)
#---------------
# Where: multiplier = 25214903917
#        addend     = 11
#        mod        = 2 ^ 48 (or 1 << 48)
# Note: the mod function basically bitmasks the seed to 48 bits in total
#
# So, If we can guess the original seed, we can predict all the future nextDouble values.
# If we know a single nextDouble() value, Reversing the rand.nextDouble function we can calculate:
#  - the 26 most significant bits of seed
#  - the 27 most significant bits of next_seed
# Now all we need to do is guess the remaining 22 bits of seed by brute force,
# calculating next_seed for each, and testing to see if we get the correct
# 27 bits of next_seed that we already know.
# We also hope that we only get a single match!
```
