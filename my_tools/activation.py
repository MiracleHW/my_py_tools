import numpy as np
import matplotlib.pyplot as plt 

class Activation():
    def forward(self):
        raise NotImplementedError
    def backward(self):
        raise NotImplementedError

class Sigmoid(Activation):
    def forward(self,x):
        return 1/(1+np.exp(-x))
    def backward(self,x):
        return np.exp(-x)/((1+np.exp(-x))**2)

class ReLU(Activation):
    def forward(self,x):
        return np.where(x>=0,x,0)
    def backward(self,x):
        return np.where(x>=0,1,0)

class Softplus(Activation):
    def forward(self,x):
        return np.log(1+np.exp(x))
    def backward(self,x):
        return np.exp(x) / (1+np.exp(x))

class Tanh(Activation):
    def forward(self,x):
        return np.tanh(x)
    def backward(self,x):
        return 1/(np.cosh(x)**2)

class LeakyReLU(Activation):
    def __init__(self,alpha) -> None:
        self.alpha = alpha
    def forward(self,x):
        return np.where(x>=0,x,x*self.alpha)
    def backward(self,x):
        return np.where(x>=0,1,self.alpha)

class ELU(Activation):
    def __init__(self,alpha) -> None:
        self.alpha = alpha
    def forward(self,x):
        return np.where(x>=0,x,self.alpha*(np.exp(x)-1))
    def backward(self,x):
        return np.where(x>=0,1,self.alpha*np.exp(x))

class Mish(Activation):
    def __init__(self) -> None:
        self.m = Softplus()
    def forward(self,x):
        return x*np.tanh(self.m.forward(x))
    def backward(self,x):
        return np.tanh(self.m.forward(x)) + x/(np.cosh(self.m.forward(x))**2)*self.m.backward(x)

class SiLU(Activation):
    def __init__(self) -> None:
        self.sig = Sigmoid()
    def forward(self,x):
        return x*self.sig.forward(x)
    def backward(self,x):
        return self.sig.forward(x)+x*self.sig.backward(x)

class GELU(Activation):
    def inner(self,x):
        return np.sqrt(2/np.pi)*(x+0.047715*(x**3))
    def forward(self,x):
        return 0.5*x*(1+np.tanh(self.inner(x)))
    def backward(self,x):
        return 0.5*(1+np.tanh(self.inner(x))) + 0.5*x*(1/(np.cosh(self.inner(x))**2))*(1+3*0.047715*(x**2))


def plot():
    plot_func = [
        # Sigmoid(),
        # Tanh(),
        # ReLU(),
        # LeakyReLU(0.1),
        # ELU(0.1),
        Mish(),
        SiLU(),
        # GELU(),
    ]
    x = np.arange(-5,5,step=0.01)

    fig = plt.figure(figsize=(10,4))

    ax = fig.add_subplot(121)
    ax.spines["left"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_color("none")

    for func in plot_func:
        y = func.forward(x)
        ax.plot(x,y,label=func.__class__.__name__)
    ax.legend()

    ax = fig.add_subplot(122)
    ax.spines["left"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["bottom"].set_position("zero")
    ax.spines["top"].set_color("none")

    for func in plot_func:
        y = func.backward(x)
        ax.plot(x,y,label=func.__class__.__name__)
    ax.legend()

    plt.show()

if __name__=="__main__":
    plot()
