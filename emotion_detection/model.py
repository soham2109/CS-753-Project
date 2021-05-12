import os
import sys

import torch
import torchaudio
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class EmotionRecognizer(nn.Module):

	def __init__(self,
				 input_dims=128,
				 hidden_dims=256,
				 num_classes=8,
				 stride=1,
				 dropout=0.2,
				 kernel_size=5):
		super.__init__(self)
		self.conv1 = nn.Conv2d(input_dims, 32,
							   kernel_size= kernel_size,
							   stride=stride,
							   padding= kernel_size//2)
		self.dropout = nn.Dropout(dropout)
		self.relu = nn.ReLu()
		self.conv2 = nn.Conv2d(32, 64,
							   kernel_size= kernel_size,
							   stride=stride,
							   padding= kernel_size//2)
		self.lstm = nn.GRU(input_size=64,
						   hidden_size=hidden_dims,
						   num_layers=1,
						   bidirectional=False)
		self.linear = nn.Linear(hidden_dims, num_classes)
		self.softmax = nn.Softmax()

	def forward(x):
		x = self.conv1(x)
		x = self.relu(x)
