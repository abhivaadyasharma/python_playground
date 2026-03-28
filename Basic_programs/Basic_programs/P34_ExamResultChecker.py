#Author: Abhivaadya Sharma

marks1=int(input("Enter marks of 1st subject: "))
marks2=int(input("Enter marks of 2nd subject: "))
marks3=int(input("Enter marks of 3rd subject: "))

#Check for total percentege

Total_Marks_Achieved= marks1+marks2+marks3
Total_Marks=300
percentage=Total_Marks_Achieved/Total_Marks*100
print(f"Your percentage is = {percentage}")

if(percentage>33 and marks1>33 and marks2>33 and marks3>33):
    print("Congratulation! you passed 🎉")

elif(percentage==33 and marks1>33 and marks2>33 and marks3>33):
    print("You were saved by god to fail(33😂)")

elif (percentage==33 and marks1<33 or marks2>33 or marks3>33) :
    print("You fail as you got marks less than 33 in one subject! Try next year")

elif (percentage<33):
    print("You fail as your percentage is less than 33!Try again next year")