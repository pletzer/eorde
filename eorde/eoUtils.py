import numpy

def get2D(x, y):
    return numpy.meshgrid(x, y, indexing='ij')


