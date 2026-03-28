#Author: Abhivaadya Sharma

# Words Frequency in String - Shorthand
s = input("Enter a string: ")

# Split and count frequency using dictionary comprehension
freq = {word: s.split().count(word) for word in set(s.split())}

print(freq)
