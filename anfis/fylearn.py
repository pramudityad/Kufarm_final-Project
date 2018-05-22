from fylearn.nfpc import FuzzyPatternClassifier
from fylearn.garules import MultimodalEvolutionaryClassifier
from fylearn.fpt import FuzzyPatternTreeTopDownClassifier

C = (FuzzyPatternClassifier(),
     MultimodalEvolutionaryClassifier(),
     FuzzyPatternTreeTopDownClassifier())

for c in C:
    print (c.fit(X, y).predict([1, 2, 3, 4]))