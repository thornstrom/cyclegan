import json
from PIL import Image


import argparse
import os
import numpy as np
import math
import itertools
import datetime
import time

import torchvision.transforms as transforms
from torchvision.utils import save_image, make_grid

from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable

from models import *
from datasets import *
from utils import *

import torch.nn as nn
import torch.nn.functional as F
import torch


def main():

    img_resize_height = 512
    img_resize_width = 128

    cuda = torch.cuda.is_available()

    input_shape = (3, img_resize_height, img_resize_width)

    # Initialize generator and discriminator
    G_AB = GeneratorResNet(input_shape, 9)

    if cuda:
        G_AB = G_AB.cuda()

    G_AB.load_state_dict(torch.load("saved_models/%s/G_AB_%d.pth" % ('synthetic2real', 99)))

    G_AB.eval()

    Tensor = torch.cuda.FloatTensor if cuda else torch.Tensor


    transforms_ = [
        transforms.Resize((img_resize_height, img_resize_width), Image.BICUBIC),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ]

    # Training data loader
    dataloader = DataLoader(
        ImageDataset("../../data/%s" % 'synthetic2real', transforms_=transforms_, unaligned=True),
        batch_size=1,
        #shuffle=True,
        num_workers=0,
    )

    img = iter(dataloader)
    for i in range(len(img)):
        imgs = next(img)
        real_A = Variable(imgs["A"].type(Tensor))
        fake_B = G_AB(real_A)
        save_image(fake_B, "test_folder/%s/%s" % ('domain', imgs["path"][0]), normalize=True)

if __name__ == '__main__':
    main()