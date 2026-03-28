# Author: Abhivaadya Sharma

def count_matching_chars(s1, s2):
    return len(set(s1) & set(s2))

# Example
str1 =input("Enter string-1")
str2 =input("Enter string-2")

print("Matching characters count:", count_matching_chars(str1, str2))
