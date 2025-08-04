from enum import Enum

class VectorDBEnum(Enum):
    
    QDRANT = "QDRANT"
    

class DistanceMethodEnum(Enum):
    
    DOT= "dot"
    COSINE = "cosine"