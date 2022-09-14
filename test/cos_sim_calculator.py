import torch
import math 

cos_sim = torch.nn.CosineSimilarity(dim=0)


user = torch.tensor([19.0, 18.0, 17.0, 16.0])
critic = torch.tensor([16.0, -5.0, 18.0, 14.0])

a = torch.tensor([19.0, 18.0, 17.0, 16.0])
b = torch.tensor([0.0, 0.0, 0.0, 0.0])

x = torch.tensor([10.0, 19.0, 10.0, 19.0, 10.0, 19.0, 10.0, 19.0, 10.0, 19.0])
y = torch.tensor([19.0, 10.0, 19.0, 10.0, 19.0, 10.0, 19.0, 10.0, 19.0, 10.0])


u = torch.tensor([10.0, 1.0])
t = torch.tensor([1.0, 10.0])
output = cos_sim(u, t)
eucld_dist = sum((u-t)**2).sqrt()

addition = sum(x * y)
'''print('rank 10 eucl dist = ')
print(eucld_dist)
print('rank 10 cos sim = ')'''
print(addition.item())
#print(eucld_dist)