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
#
# Set the constants
multiplier=25214903917
addend=11
mod=(1 << 48)
seed_0_candidate=[]
# Set the Random_double value here
input=0.40012931887910996


# Multiply value by 2^53 
input_multiplied=input * (1 << 53)
print ("Input Value * 2^53 = " + str(input_multiplied))
input_multiplied=round(input_multiplied)

# Round This value to nearest integer so we can perform bit manipulation
print ("Input Value * 2^53, rounded = " + str(input_multiplied) + "\n(In binary: {0:b})".format(input_multiplied))

# Extract the 26 MBSs of the input (equal to the first, next(26) statement)
high_bits=input_multiplied >> 27
print ("26 High bits = " + str(high_bits) +  "\n(In binary: {0:b})".format(high_bits))
# Extract the 27 LBSs of the input (equal to the second, next(27) statement)
low_bits=input_multiplied % (1<<27)
print ("27 Low bits = " + str(low_bits) + "\n(In binary: {0:b})".format(low_bits))

# Try every combination of 22 LSBs (2^22 iterations)
# combined with the known 26 MSBs to create canditates for seed 0
# and calculate seed 1 based on each seed 0 candiate
n = 0
print ("Trying bits for seed...")
for i in range(1 << 22):
    seed_0_guess = int((high_bits << 22) + i)
    seed_1_guess = int((seed_0_guess * multiplier + addend) % mod)

    # Test if seed 1 candidate generates the expected LSB bits 
    # If match found, store the candiate.
    if  (seed_1_guess >> 21) == low_bits:
        seed_0_candidate.append(seed_0_guess)
        print("Seed found: " + str(seed_0_candidate[n]))
        ++ n
if len(seed_0_candidate) == 0:
    print ("Failed to find a seed candidate from input value")

# Now we hopefully one (possibly more) candidates for seed 0, we can calculate nextDouble() values for each seed candidate.
for n, seed_0 in enumerate(seed_0_candidate, start=1):
    print ("Printing nextDouble() values for candidate " + str(n))
    for i in range(10):
        seed_1 = int((seed_0 * multiplier + addend) % mod)
        
        # python version of: nextDouble()
        next_double=(((seed_0 >> 22) << 27)+(seed_1 >> 21)) / (1 << 53)
        seed_0 = int((seed_1 * multiplier + addend) % mod)
        
        print ("New Random double value " + str(i) + " = " + str(next_double))
        print ("Die Roll= " + str(i) + " = " + str(int(next_double * 6 + 1)))
        
        

