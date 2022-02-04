#Andrew Bernal
#Last modified 11/3/21
#I needed to make a bunch of squares and check them for differences in their color intensity to determine if a piece was moved there
#So I made it its own class
#Idk how to make classes, I did it in AP CS A in Java like 2 years ago (had a great teacher though, I just forget)
import numpy
class Square:
    #Initializes a square with a column and a row, like how a chess board has "a1" for example
    #c1 and c2 are expected to be arrays of size 2 containing the corner points
    #example usage is (2, "a1", [0,1], [1,1], an image from cv2)
    def __init__(self, numCreated, colRow, c1, c2):
        #breaks down c1 and c2 into usable coordinates
        self.x1 = c1[0]
        self.y1 = c1[1]
        self.x2 = c2[0]
        self.y2 = c2[1]
        self.c1 = c1
        self.c2 = c2
        #saves "numCreated" for future use
        self.numCreated = numCreated
        #algNot is short for algebraic notation, aka chess notation
        self.algNot = colRow
        #the leftmost and rightmost corners of the square
        self.coords=[(self.x1, self.y1), (self.x2, self.y2)]
        #the color of the square, white or black
        #If the number created is even and the row is 2, 4, 6, 8 then the square is white (Idk this part, I tried 1, 3, 5, 7 first but it was exactly wrong, so I flipped it)
        #The point is that just checking for evens doesn't work because h7 and a6 are the same color, for example
        if(colRow[1:2] == '2' or colRow[1:2] == '4' or colRow[1:2] == '6' or colRow[1:2] == '8'):
            if(numCreated%2 == 0):
                self.color = "white"
            else:
                self.color = "black"
        else:
            if (numCreated % 2 == 0):
                self.color = "black"
            else:
                self.color = "white"

    #calculates the baseline color for a square, to be used in the historgram. roi is short for Region of Interest
    #https://stackoverflow.com/questions/9084609/how-to-copy-a-image-region-using-opencv-in-python
    #roi = self.image[y1:y2, x1:x2]

    #sees if the square contains a piece by checking its default histogram vs its current value
    def hasPiece(self):
        if(defaultHist != currentHist):
            return True
        else:
            return False

    #I need a way to make sure all of the starting locations are filled with pieces
    def checkStartingPosition(self):
        #If all of the starting squares (a1-h1, a2-h2, a7-h7, a8-h8) have pieces
        if(hasPiece and isStartingSquare):
            return True

    #The starting squares are the first two rows of a chess board, where white and black start
    def isStartingSquare(self):
        #True for squares 0-15
        if(numCreated < 16):
            return True
        #True for squares 48-63
        elif(numCreated >= 48):
            return True
        else:
            return False