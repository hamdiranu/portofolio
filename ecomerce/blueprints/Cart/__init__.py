##============== Person Class =================##
# import random

# class User():

#     def __init__(self):
#         self.reset()

#     def reset(self):
#         self.id = 0
#         self.name = None
#         self.age = 0
#         self.sex = None
#         self.client_id = 0

#     def serialize(self):
#         return {
#             'id'        :self.id,
#             'name'      :self.name,
#             'age'       :self.age,
#             'sex'       :self.sex,
#             'client_id' :self.client_id
#         }
        
# class Users():

#     users = []

#     def __init__(self):
#         for i in range(1,5):
#             user = User()
#             user.id = i
#             user.name = "user ke %d" %(i)
#             user.age = random.randrange(1,90)
#             user.sex = random.choice(["Male","Female"])
#             user.client_id = random.randrange(1,90)
            
#             self.users.append(user.serialize())

#     def get_list(self):
#         return self.users

#     def add(self, serialized):
#         self.users.append(serialized)

#     def get_one_id(self, id):
#         for i,j in enumerate(self.users):
#             if int(j['id']) == int(id):
#                 return j
#         return None
    
#     def edit_data(self, id, name, age, sex, client_id):
#         for i,j in enumerate(self.users):
#             if int(j['id']) == int(id):
#                 user = User()
#                 user.id        = id
#                 user.name      = name if name != None else j['name']
#                 user.age       = age  if age != None else j['age']
#                 user.sex       = sex  if sex != None else j['sex']
#                 user.client_id = client_id if client_id != None else j['client_id']
#                 self.users[i] = user.serialize()
#                 return user
#         return None

#     def delete(self, id):
#         for i,j in enumerate(self.users):
#             if int(j['id']) == int(id):
#                 self.users.pop(i)

    

            
            