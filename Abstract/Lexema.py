from Abstract.Abstract import Expression

class Lexema(Expression):
    def __init__(self, lexema, fila, columna):
        self.lexema = lexema
        self.fila = fila
        self.columna = columna
        super().__init__(fila, columna)

    def execute(self, environment):
        return self.lexema
    
    def getFila(self):
        return self.fila

    def getColumna(self):
        return self.columna

    """def getFila(self):
        return super().getFila()

    def getColumna(self):
        return super().getColumna()"""