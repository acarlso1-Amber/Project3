from tkinter.simpledialog import askfloat
import nn
import numpy as np

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.

        python3.7 autograder.py -q q1

        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)

        Implement the run(self, x) method. This should compute the dot product of the stored weight vector and the given input returning an nn.DotProduct object.
        """
        "*** YOUR CODE HERE ***"
        return nn.DotProduct(x, self.w)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        dot = nn.as_scalar(self.run(x))
        if dot >= 0:
            return 1
        else:
            return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        weights ← weights + direction ⋅ multiplier
        
    
        Write the train(self) method. This should repeatedly loop over the data set and make updates on examples that are misclassified. Use the update method of the nn.Parameter class to update the weights. When an entire pass over the data set is completed without making any mistakes, 100% training accuracy has been achieved, and training can terminate.
        
        
        """
        "*** YOUR CODE HERE ***"
        batchsize = 1
        mismatch = True
        while mismatch: 
            mismatch = False
            for x, y in dataset.iterate_once(batchsize): 
                node = nn.as_scalar(y)
                if (self.get_prediction(x) != node):
                    mismatch = True
                    self.w.update(x, node)


class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    python3.7 autograder.py -q q2
    """


    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.learningRate=0.05

        self.w1 = nn.Parameter(1,80)
        self.b1 = nn.Parameter(1,80)

        self.w2 = nn.Parameter(80,40)
        self.b2 = nn.Parameter(1,40)

        self.w3 = nn.Parameter(40,1)
        self.b3 = nn.Parameter(1,1)

        self.parameters=[self.w1,self.b1,self.w2,self.b2,self.w3,self.b3]

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        layer_01 = nn.AddBias(nn.Linear(x                ,self.w1),self.b1)
        layer_02 = nn.AddBias(nn.Linear(nn.ReLU(layer_01),self.w2),self.b2)
        layer_03 = nn.AddBias(nn.Linear(nn.ReLU(layer_02),self.w3),self.b3)

        return layer_03

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x),y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"

        batchSize=25
        loss=float('inf')
        minLoss=0.005
        
        while loss>=minLoss:
            for x, y in dataset.iterate_once(batchSize):
                loss=self.get_loss(x,y)
                gradiants = nn.gradients(loss,self.parameters)
                loss=nn.as_scalar(loss)
                for i in range(len(self.parameters)):
                    self.parameters[i].update(gradiants[i],-self.learningRate)


        """
        #TODO: Copied from perceptron model
        batchsize = 1
        mismatch = True
        while mismatch: 
            mismatch = False
            for x, y in dataset.iterate_once(batchsize): 
                node = nn.as_scalar(y)
                loss = self.get_loss(x,y)
                gradients = nn.gradients(loss,dataset)
                if (self.get_prediction(x) != node): #TODO change self.getPrediction
                    mismatch = True
                    self.w.update(x, node)
        """
class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    python3.7 autograder.py -q q3
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.learningRate=0.1


        """
        self.w1 = nn.Parameter(1,80)
        self.b1 = nn.Parameter(1,80)

        self.w2 = nn.Parameter(80,40)
        self.b2 = nn.Parameter(1,40)

        self.w3 = nn.Parameter(40,1)
        self.b3 = nn.Parameter(1,1)"""
        l1start=784
        l2start=300
        l3start=150
        l4start=75

        self.w1 = nn.Parameter(l1start,l2start)
        self.b1 = nn.Parameter(1,      l2start)

        self.w2 = nn.Parameter(l2start,l3start)
        self.b2 = nn.Parameter(1,      l3start)

        self.w3 = nn.Parameter(l3start,l4start)
        self.b3 = nn.Parameter(1,      l4start)

        self.w4 = nn.Parameter(l4start,10)
        self.b4 = nn.Parameter(1,      10)

        self.parameters=[self.w1,self.b1,self.w2,self.b2,self.w3,self.b3,self.w4,self.b4]

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        layer_01 = nn.AddBias(nn.Linear(x                ,self.w1),self.b1)
        layer_02 = nn.AddBias(nn.Linear(nn.ReLU(layer_01),self.w2),self.b2)
        layer_03 = nn.AddBias(nn.Linear(nn.ReLU(layer_02),self.w3),self.b3)
        layer_04 = nn.AddBias(nn.Linear(nn.ReLU(layer_03),self.w4),self.b4)

        return layer_04

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(x),y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        #dataset.get_validation_accuracy()
        batchSize=100
        #loss=float('inf')
        #minLoss=0.005
        
        while dataset.get_validation_accuracy()<0.975:
            for x, y in dataset.iterate_once(batchSize):
                loss=self.get_loss(x,y)
                gradiants = nn.gradients(loss,self.parameters)
                #loss=nn.as_scalar(loss)
                for i in range(len(self.parameters)):
                    self.parameters[i].update(gradiants[i],-self.learningRate)

class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"

        #l1start=self.num_chars
        #l2start=236
        #l3start=l2start
        #l4start=5
        self.learningRate = 0.01
        self.w1 = nn.Parameter(47,236)
        self.b1 = nn.Parameter(1,236)

        self.hw = nn.Parameter(236,236)

        self.w2 = nn.Parameter(236,236)
        self.b2 = nn.Parameter(1,236)

        self.w3 = nn.Parameter(236,5)
        self.b3 = nn.Parameter(1,5)

        self.parameters=[self.w1,self.b1,self.w2,self.b2,self.w3,self.b3,self.hw]

    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"
        hidden = 0
        for i in range(0, len(xs)):
            x = xs[i]
            if i == 0:
                # layer_01 = nn.AddBias(nn.Linear(x                ,self.w1),self.b1)
                # layer_02 = nn.AddBias(nn.Linear(nn.ReLU(layer_01),self.w2),self.b2)
                # layer_03 = nn.AddBias(nn.Linear(nn.ReLU(layer_02),self.w3),self.b3)
                # layer_04 = nn.AddBias(nn.Linear(nn.ReLU(layer_03),self.w4),self.b4)
                # h = layer_04
                #z, activation, hidden
                # z = nn.Linear(x, self.w)
                # activation
                hidden =  nn.ReLU(nn.AddBias(nn.Linear(x,self.w1),self.b1))
            else:
                # layer_01 = nn.AddBias(nn.Add(nn.Linear(x, self.w1), nn.Linear(h, self.w1)),self.b1)
                # layer_02 = nn.AddBias(nn.Add(nn.Linear(x, self.w2), nn.Linear(h, self.w2)),self.b2)
                # layer_03 = nn.AddBias(nn.Add(nn.Linear(x, self.w3), nn.Linear(h, self.w3)),self.b3)
                # layer_04 = nn.AddBias(nn.Add(nn.Linear(x, self.w4), nn.Linear(h, self.w4)),self.b4)
                # print("placeholder")
                #z, hidden
                hidden = nn.ReLU(nn.AddBias(nn.Add(nn.Linear(x, self.w1), nn.Linear(hidden, self.hw)),self.b2))
        hidden = nn.AddBias(nn.Linear(hidden, self.w3), self.b3)
        return hidden
                

    def get_loss(self, xs, y):
        """,
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        return nn.SquareLoss(self.run(xs),y)

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        batchSize=100
        while dataset.get_validation_accuracy()<0.85:
            for x, y in dataset.iterate_once(batchSize):
                loss=self.get_loss(x,y)
                gradiants = nn.gradients(loss,self.parameters)
                for i in range(len(self.parameters)):
                    self.parameters[i].update(gradiants[i],-self.learningRate)
