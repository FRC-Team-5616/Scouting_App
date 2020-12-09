import json

"""
1 = Important Information
{"Team Message": {"From": "Ashlen", "Message Header": "Emojis","Message": "Emojis Suck", "Secret?": False}}
2 = Other Team Information
{1234:{"Team Name": "Team Nice", "Robot Specs": "bla bla bla", "Coding Language": "Python", "Extra Information": "yay"}}
3 = Random
["Random information", "bla bla bla", "cool guy lyn is cool"]
4 = Secret Chat
{
1 : Message 1
2 : Message 2
3 : Message 3...
}
"""
temp_data = {
    1: {"Team Message": {"From": "Ashlen", "Message Header": "Emojis", "Message": "Emojis Suck", "Secret?": False}},
    2: {1234: {"Team Name": "Team Nice", "Robot Specs": "bla bla bla", "Coding Language": "Python",
               "Extra Information": "yay"}}, 3: ["Random information", "bla bla bla", "cool guy lyn is cool"],
    4: {1: "Ayo", 2: "Joe", 3: "Mac"}}
data = {1: {}, 2: {}, 3: {}, 4: {}}
data2 = json.dumps(temp_data, indent=4)
print(data2)
with open("data.json", "w") as ham:
    ham.write(data2)
