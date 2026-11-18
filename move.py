class Move:
    def __init__(self, kind, source, dest, count, flipped):
        self.kind = kind          
        self.source = source      
        self.dest = dest          
        self.count = count        
        self.flipped = flipped    