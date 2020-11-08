# -*- coding: utf-8 -*-

"""Methuselahs are long-lived lifeforms which evolve rapidly before reaching 
a steady state after many cycles. The steady state may consist of several 
oscillators and still lifes."""

# Import modules
import numpy as np

from .base import Lifeform

class Century(Lifeform):
    """A Century Methuselah lifeform"""
    
    def ___init___(self):
        """Initialize the class"""
        super(Century, self).__init__()
        
    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((3,4))
        X[0,2:] = 1
        X[1,:3] = 1
        X[2,1] = 1
        return X
  
  
class Thunderbird(Lifeform):
    """A Thunderbird Methuselah lifeform"""
    
    def ___init___(self):
        """Initialize the class"""
        super(Thunderbird, self).__init__()
        
    @property
    def layout(self) -> np.ndarray:
        X = np.zeros((5,3))
        X[0,:] = 1
        X[2:,1] = 1
        return X