#!/usr/bin/env python3
"""
part1.py

UNSW COMP9444 Neural Networks and Deep Learning

ONLY COMPLETE METHODS AND CLASSES MARKED "TODO".

DO NOT MODIFY IMPORTS. DO NOT ADD EXTRA FUNCTIONS.
DO NOT MODIFY EXISTING FUNCTION SIGNATURES.
DO NOT IMPORT ADDITIONAL LIBRARIES.
DOING SO MAY CAUSE YOUR CODE TO FAIL AUTOMATED TESTING.
"""

import torch

class rnn(torch.nn.Module):

    def __init__(self):
        super(rnn, self).__init__()

        self.ih = torch.nn.Linear(64, 128)
        self.hh = torch.nn.Linear(128, 128)

    def rnnCell(self, input, hidden):
        """
        TODO: Using only the above defined linear layers and a tanh
              activation, create an Elman RNN cell.  You do not need
              to include an output layer.  The network should take
              some input (inputDim = 64) and the current hidden state
              (hiddenDim = 128), and return the new hidden state.
        """
        input = self.ih(input)
        hidden = self.hh(hidden)
        tanh = torch.nn.Tanh()
        return tanh(torch.add(input, hidden))


    def forward(self, input):
        hidden = torch.zeros(128)
        times = input.size()
        for i in range(times[0]):
            hidden = self.rnnCell(input[i,:,:], hidden)
        """
        TODO: Using self.rnnCell, create a model that takes as input
              a sequence of size [seqLength, batchSize, inputDim]
              and passes each input through the rnn sequentially,
              updating the (initally zero) hidden state.
              Return the final hidden state after the
              last input in the sequence has been processed.
        """
        return hidden

class rnnSimplified(torch.nn.Module):

    def __init__(self):
        super(rnnSimplified, self).__init__()
        """
        TODO: Define self.net using a single PyTorch module such that
              the network defined by this class is equivalent to the
              one defined in class "rnn".
        """
        self.net = torch.nn.RNN(64, 128, 1)

    def forward(self, input):
        _, hidden = self.net(input)

        return hidden

def lstm(input, hiddenSize):
    """
    TODO: Let variable lstm be an instance of torch.nn.LSTM.
          Variable input is of size [batchSize, seqLength, inputDim]
    """
    lstm = torch.nn.LSTM(
        input_size = input.size()[2],
        hidden_size = hiddenSize,
        batch_first = True,
    )
    return lstm(input)

def conv(input, weight):
    """
    TODO: Return the convolution of input and weight tensors,
          where input contains sequential data.
          The convolution should be along the sequence axis.
          input is of size [batchSize, inputDim, seqLength]
    """
    '''
    conv = torch.nn.functional.conv1d(
        in_channels = input.size()[0],
        out_channels = weight.size()[0],
        kernel_size = (weight.size()[1], weight.size()[2]),
    )
    '''
    reuslt = torch.nn.functional.conv1d(
        input,
        weight
    )
    return reuslt
   
    '''
    print(input.size())
    print(weight.size())
    print(weight)
    '''
