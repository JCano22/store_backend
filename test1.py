print("Test 1")

# Dictionaries
user = {
    "name": "Jorge",
    "last_name": "Cano",
    "age": 38
}

print(user)
print(type(user))

print(user["name"] + " " + user["last_name"])


# list
numbers = [1, 2, 3]

# add elements to list
numbers.append(4)
numbers.append(5)

print(numbers)

# length
print(len(numbers))  # count items
print(len(user["name"]))  # count chars in string
print(len(user))  # count the keys


# #####################
# age = [32, 74, 20, 69, 52, 26, 31, 77, 43, 73, 51, 57, 19, 79, 40, 34, 27, 23, 21, 44,
#        53, 55, 24, 36, 41, 47, 78, 46, 68, 75, 49, 83, 61, 60, 29, 56, 67, 17, 70, 81, 87, 38]


# def exc1():
#     # print all the numbers
#     total = 0
#     for i in age:
#         total += i
#         # print(i)

#     print(total)

# # count user 21 and greater


# def exc2():
#     # print all numbers greater than 21
#     ctr = 0
#     for i in age:
#         if i >= 21:
#             print(i)
#             ctr += 1
#     print(ctr)


# # count users between 30 and 40 (inclusive)
# def exc3():
#     ctr = 0
#     for i in age:
#         if i >= 30 and i <= 40:
#             ctr += 1
#             print(i)
#     print("There are " + str(ctr) + " users between 30 and 40")


# # call your functions
# exc1()
# exc2()
# exc3()

# name = "jorge"
# print('Hello {}' .format(name))

