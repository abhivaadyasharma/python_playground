# Author: Abhivaadya Sharma

word = input("Enter word: ")
vowels = set("aeiou")

letters = set(filter(str.isalpha, word.lower()))

if vowels.issubset(letters):
    print(f"All vowels are present in {word}")
else:
    print(f"All vowels are not present in {word}")
