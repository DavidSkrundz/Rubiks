from cube import Cube
from cubesolver import CubeSolver
from copy import deepcopy
from random import randint
import itertools

class SearchSolver(CubeSolver):
    '''
    This is a search based method of solving the cube layer by layer
    '''

    def __init__(self):
        CubeSolver.__init__(self, 3) # Solves 3x3x3 cubes
        self.currentAlgorithmSteps = []
        self.currentCube = None
        self.FirstLayerCrossMoves = 8
        self.FirstLayerCornerMoves = 8
        self.secondlayermoves = 12
        self.thirdlayermoves = 100
        self.Moves = [-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]
        self.copy = None

    def update(self):
        self.MoveTopWhite()
        self.FirstLayerCross()
        self.FirstLayerCorner()
        self.SecondLayer()
        self.FinalLayer()
        CubeSolver.update(self)
        self.solved = True


    def MoveTopWhite(self):
        '''
        Moves the white centre to the top
        '''
        if not self.currentAlgorithmSteps:
            faces = self.currentCube.faces() # (top, front, right, back, left, bottom)
            # Rotate the cube so the white face is on the top
            if faces[0][1][1] == Cube.White:
                if faces[1][1][1] != Cube.Red:
                    self.currentAlgorithmSteps += [Cube.Middle]
                    self.copy.M()
            elif faces[1][1][1] == Cube.White:
                self.currentAlgorithmSteps += [Cube.Center]
                self.copy.C()
            elif faces[2][1][1] == Cube.White:
                self.currentAlgorithmSteps += [Cube.Middle_, Cube.Center]
                self.copy.M_()
                self.copy.C()
            elif faces[3][1][1] == Cube.White:
                self.currentAlgorithmSteps += [Cube.Center_]
                self.copy.C_()
            elif faces[4][1][1] == Cube.White:
                self.currentAlgorithmSteps += [Cube.Middle, Cube.Center]
                self.copy.M()
                self.copy.C()
            elif faces[5][1][1] == Cube.White:
                self.currentAlgorithmSteps += [Cube.Center, Cube.Center]
                self.copy.C()
                self.copy.C()
            else:
                raise ValueError("Unsolvable cube")


    def FirstLayerCross(self):
        Movesets = itertools.permutations(self.Moves, self.FirstLayerCrossMoves)
        for moveset in Movesets:
            CubeCopy = deepcopy(self.copy)
            for move in moveset:
                Cube.Moves[move](CubeCopy)
            if self.CheckCross(CubeCopy):
                self.currentAlgorithmSteps += moveset
                self.copy = CubeCopy
                break


    def FirstLayerCorner(self):
        pass

    def SecondLayer(self):
        pass

    def FinalLayer(self):
        pass


    def CheckCross(self, CubeCopy):
        faces = CubeCopy.faces()
        if (faces[0][0][1] == Cube.White and faces[3][0][1] == Cube.Orange
        and faces[4][0][1] == Cube.Green and faces[2][0][1] == Cube.Blue
        and faces[1][0][1] == Cube.Red and faces[0][2][1] == Cube.White
        and faces[0][1][0] == Cube.White and faces[0][1][2] == Cube.White):
            return True
        return False

    def solve(self, cube):
        CubeSolver.solve(self, cube)
        self.copy = deepcopy(cube)
