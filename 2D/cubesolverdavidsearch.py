from cube import Cube
from cubesolver import CubeSolver
from copy import deepcopy


class SearchSolver(CubeSolver):
    '''
    This is a search based method of solving the cube layer by layer
    '''

    def __init__(self):
        CubeSolver.__init__(self, 3) # Solves 3x3x3 cubes
        self.currentAlgorithmSteps = []
        self.currentCube = None


    def FirstLayer(self):
        '''
        Does a search based solve on the first layer of the cube
        Should have an upper bound of
        '''
        if not self.currentAlgorithmSteps:
            faces = self.currentCube.faces() # (top, front, right, back, left, bottom)
            # Rotate the cube so the white face is on the top
            if faces[0][1][1] == Cube.White:
                if faces[1][1][1] != Cube.Red:
                    self.currentAlgorithmSteps += [Cube.Middle]
            elif faces[1][1][1] == Cube.White:
                self.currentAlgorithmSteps += [Cube.Center]
            elif faces[2][1][1] == Cube.White:
                self.currentAlgorithmSteps += [Cube.Middle_, Cube.Center]
            elif faces[3][1][1] == Cube.White:
                self.currentAlgorithmSteps += [Cube.Center_]
            elif faces[4][1][1] == Cube.White:
                self.currentAlgorithmSteps += [Cube.Middle, Cube.Center]
            elif faces[5][1][1] == Cube.White:
                self.currentAlgorithmSteps += [Cube.Center, Cube.Center]
            else:
                raise ValueError("Unsolvable cube")
        CubeSolver.update(self)


    def SecondLayer(self):
        pass


    def FinalLayer(self):
        pass
