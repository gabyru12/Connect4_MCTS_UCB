from collections import Counter
import math
import pandas as pd

class DecisionNode:
    def __init__(self, feature=None, children=None, result=None):
        self.feature = feature
        self.children = children  # dict: valor -> sub-árvore
        self.result = result

class ID3Tree:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.root = None

    def fit(self, data, features):
        self.root = self._id3(data, features, depth=0)

    def _id3(self, data, features, depth):
        labels = data['50kIter']
        mode_val = labels.mode()
        if len(set(labels)) == 1 or len(features) == 0 or (self.max_depth is not None and depth >= self.max_depth):
            return DecisionNode(result=mode_val.iloc[0] if not mode_val.empty else None)
        best_gain = 0
        best_feature = None
        for feature in features:
            gain = information_gain_categorical(data, feature)
            if gain > best_gain:
                best_gain = gain
                best_feature = feature
        if best_gain == 0:
            return DecisionNode(result=mode_val.iloc[0] if not mode_val.empty else None)
        next_features = [f for f in features if f != best_feature]
        children = {}
        for value, subset in data.groupby(best_feature):
            children[value] = self._id3(subset, next_features, depth + 1)
        return DecisionNode(feature=best_feature, children=children)

    def classify(self, row):
        node = self.root
        # If row is a DataFrame with one row, convert to Series
        if isinstance(row, pd.DataFrame):
            row = row.iloc[0]
        while node.result is None:
            feature = node.feature
            value = row[feature]  # Get the value for this feature
            if value in node.children:
                node = node.children[value]
            else:
                # Handle unknown value (e.g., majority class or random)
                break
        return node.result

def entropy(data):
    labels = data.iloc[:, -1]
    total = len(labels)
    counts = Counter(labels)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())

def information_gain_categorical(data, feature):
    base_entropy = entropy(data)
    values = data[feature].unique()
    weighted_entropy = 0

    for value in values:
        subset = data[data[feature] == value]
        weighted_entropy += (len(subset) / len(data)) * entropy(subset)
        
    return base_entropy - weighted_entropy