#Author: Abhivaadya Sharma

# Take input string
sentence=input("Enter a sentence: ")

# Split strings
words=sentence.split()

found = False

# print words of even length
for word in words:
    if len(word)%2==0:
        print(word)
        found=True

if not found:
    print(f"There is no word with even length in the sentence: {sentence}")
