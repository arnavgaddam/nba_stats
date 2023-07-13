import pandas as pd
import json

class Player:

    playerTable = {}

    def __init__(self, data):
        self.data = data