import requests

BASE = "http://127.0.0.1:5000/"

# data = [
#     {"name": "My first video", "views": 420, "likes": 10},
#     {"name": "Cooking Stream", "views": 69, "likes": 20},
#     {"name": "Homicidal Tendancies", "views": 42069, "likes": 30},
# ]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())  

# input()

# response = requests.get(BASE + "video/3")


response = requests.patch(BASE + "video/0", {"name": "Simping for Amouranth"})

print(response.json())
