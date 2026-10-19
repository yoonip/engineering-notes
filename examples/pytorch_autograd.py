import torch

x = torch.tensor(3.0, requires_grad=True)
y = x.square()
y.backward()
print(x.grad.item())  # dy/dx = 6.0
