#Andrew Bernal
#This is a test of how I can image a chess board in python
#Last modified 12/10/21
#V6 Is going to be the test of v5, hook it up to a video camera baby
#fails due to shadows and strange histogram output when nothing on the board is different
import SquareClass
import cv2
import numpy
#used for legal move checking
import chess
# Used for text to speech
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

#instantiates a chessboard
board = chess.Board()
#instantiates the verbal engine or something, idk how to use this package
engine = pyttsx3.init()
#gets the legal moves on the chessboard
board.legal_moves

def moveChecks(move):
    #Checks if the move is legal
    if(chess.Move.from_uci(str(move)) in board.legal_moves == True):
        #enter the move into the lichess game
        moveFT(move)
        #enter the move into the python board
        board.push_uci(str(move))
        #verbally says the move in SAN not uci notation
        engine.say(board.variation_san([chess.Move.from_uci(str(move))]))
        engine.runAndWait()
    else:
        engine.say(f'{move} is illegal')
        engine.runAndWait()
    #checks if stalemate
    if(board.is_stalemate()):
        #verbally say stalemate
        engine.say("draw by stalemate")
        engine.runAndWait()
        #exit the loop
        return "end loop"
    if(board.is_insufficient_material()):
        #verbally say draw by insufficent material
        engine.say("draw by insufficent material")
        engine.runAndWait()
        #exit the loop
        return "end loop"
    #checks if checkmate
    if(board.is_checkmate()):
        #verbally say checkmate
        engine.say("Checkmate")
        engine.runAndWait()
        #say which side won
        #exit the loop
        return "end loop"
    #checks if check
    if(board.is_check()):
        #verbally say check
        engine.say("Check")
        engine.runAndWait()

    #checks if promotion, and auto promotes to a queen
    if chess.Move.from_uci(move + "q") in board.legal_moves:
        move = move + 'q'

def checkLegalMoves(possibleMoves):
    #The method should be able to check for multiple possible legal moves, and if they exist, then have the program wait until there is only 1
    possibilities = list()
    for h in range(0, len(possibleMoves)):
        for q in range(0, len(possibleMoves)):
            if(h != q):
                move = str(possibleMoves[h]) + str(possibleMoves[q])
                if(chess.Move.from_uci(str(move)) in board.legal_moves):
                    possibilities.append(move)
    return possibilities

#initializes the driver
ser = Service("C:\\Dev\\WebDrivers\\chromedriver.exe")
driver = webdriver.Chrome(service=ser)


#this is my code, logs into lichess
def log_into_lichess():
    # opens the website login page
    driver.get('https://lichess.org/login?referrer=/')
    #the user should change their username and password in the code
    username = "MR-Mister"
    password = "dododoBologanIsCOol#!231"

    #gets the username and password box locations
    usernameBox = driver.find_element(By.NAME, 'username')
    passwordBox = driver.find_element(By.NAME, 'password')

    #logs into the website
    usernameBox.send_keys(username)
    passwordBox.send_keys(password)
    passwordBox.send_keys(Keys.ENTER)

#starts a new 10 minute game on lichess
def start_10_min():
    # navigates back to start a new game
    driver.find_element(By.CLASS_NAME, 'site-title').click()
    driver.find_element(By.CSS_SELECTOR, '#main-wrap > main > div.lobby__app.lobby__app-pools > div.lobby__app__content.lpools > div:nth-child(7)').click()


#slightly modified from https://github.com/tazjel/lichess-cheatbot/blob/master/bot.py
def click_square(square):
    column_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    x = column_map[square[0]]
    y = int(square[1]) - 1
    # determine orientation of the lichess board
    boardL = driver.find_element(By.CSS_SELECTOR, '#main-wrap > main > div.round__app.variant-standard > div.round__app__board.main-board > div > cg-container > cg-board')
    orientation = boardL.get_attribute("class")
    if 'orientation-black' in orientation:
        x = 7 - x
    else:
        y = 7 - y
    print(orientation)
    print((x, y))
    x = x * 64 + 32
    y = y * 64 + 32

    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(boardL, x, y)
    action.click()
    action.perform()

#FT stands for 'From To', moves from a square to another square
def moveFT(moveInput):
    click_square(moveInput[0:2])
    click_square(moveInput[2:4])

#the start of the cv2 portion of the program
#sets the number for the camera
camera = 1
#initalizes video capture
cap = cv2.VideoCapture(camera)

#gets a frame
ret, frame = cap.read()
while(ret == False):
    print("The capture was unsucessful, I will try again")
    ret, frame = cap.read()
#stores a color version of the image
customized_image = frame
#Resizes the image
#code stolen from https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
scale_percent = 20
width = int(customized_image.shape[1] * scale_percent / 100)
height = int(customized_image.shape[0] * scale_percent / 100)
dim = (width, height)
customized_image = cv2.resize(customized_image, dim, interpolation=cv2.INTER_AREA)
#creates several windows with names corresponding to their purpose
#cv2.namedWindow('Original Image')
#cv2.namedWindow('Grayscale Image')
cv2.namedWindow('Customized Image')

#stores a grayscale version of the image
grayscale_image_simple = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#makes the grayscale image have 3 channels
grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR)
#rescales the grayscale image
scale_percent = 20
width = int(grayscale_image.shape[1] * scale_percent / 100)
height = int(grayscale_image.shape[0] * scale_percent / 100)
dim = (width, height)
grayscale_image = cv2.resize(grayscale_image, dim, interpolation=cv2.INTER_AREA)
#rescales the grayscale simple image
scale_percent = 20
width = int(grayscale_image_simple.shape[1] * scale_percent / 100)
height = int(grayscale_image_simple.shape[0] * scale_percent / 100)
dim = (width, height)
grayscale_image_simple = cv2.resize(grayscale_image_simple, dim, interpolation=cv2.INTER_AREA)
#cv2.imshow('Grayscale Image', grayscale_image)
#These are the number of rows and columns you have subtracted by 1. In my case, I am using 8x8 chess boards, so I input 7x7
nline = 7
ncol = 7
#finds the corners of the chessboard
ret, corners = cv2.findChessboardCorners(grayscale_image, (nline, ncol), None)
#good for visualizing the location of the chessboard corners
'''
#termination criteria (blatantly stolen from https://stackoverflow.com/questions/57161974/python-opencv-detecting-chessboard)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
customized_image = cv2.drawChessboardCorners(customized_image, (nline, ncol), corners, ret)
'''
# displays the images
#cv2.imshow('Original Image', original_image)
#cv2.imshow('Grayscale Image', grayscale_image)
cv2.imshow('Customized Image', customized_image)

#gets the difference for the x and y values, constant for every square
cond = False
#If there is stuff on the board or it is out of view, the program will let the user know instead of just crashing
while(not cond):
    try:
        xDiff = corners[3].tolist()[0][0]-corners[2].tolist()[0][0]
        yDiff = corners[3].tolist()[0][0]-corners[2].tolist()[0][0]
        # exits the loop
        cond = True
    except:
        engine.say('My view of the board is obscured')
        engine.runAndWait()
        # gets a frame
        ret, frame = cap.read()
        # stores a color version of the image
        customized_image = frame
        # Resizes the image
        # code stolen from https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
        scale_percent = 20
        width = int(customized_image.shape[1] * scale_percent / 100)
        height = int(customized_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        customized_image = cv2.resize(customized_image, dim, interpolation=cv2.INTER_AREA)
        # creates several windows with names corresponding to their purpose
        # cv2.namedWindow('Original Image')
        # cv2.namedWindow('Grayscale Image')
        cv2.namedWindow('Customized Image')

        # stores a grayscale version of the image
        grayscale_image_simple = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # makes the grayscale image have 3 channels
        grayscale_image = cv2.cvtColor(grayscale_image_simple, cv2.COLOR_GRAY2BGR)
        # rescales the grayscale image
        scale_percent = 20
        width = int(grayscale_image.shape[1] * scale_percent / 100)
        height = int(grayscale_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        grayscale_image = cv2.resize(grayscale_image, dim, interpolation=cv2.INTER_AREA)
        # rescales the grayscale simple image
        scale_percent = 20
        width = int(grayscale_image_simple.shape[1] * scale_percent / 100)
        height = int(grayscale_image_simple.shape[0] * scale_percent / 100)
        dim = (width, height)
        grayscale_image_simple = cv2.resize(grayscale_image_simple, dim, interpolation=cv2.INTER_AREA)
        # cv2.imshow('Grayscale Image', grayscale_image)
        # These are the number of rows and columns you have subtracted by 1. In my case, I am using 8x8 chess boards, so I input 7x7
        nline = 7
        ncol = 7
        # finds the corners of the chessboard
        ret, corners = cv2.findChessboardCorners(grayscale_image, (nline, ncol), None)
        # displays the image
        cv2.imshow('Customized Image', customized_image)


#the following adds the locations of all the recotangle corners on the chessboard
#creates the top and bottom corners and draws their locations on the screen
topCornersX = list()
topCornersY = list()
bottomCornersX = list()
bottomCornersY = list()
for x in range (0, 49):
    #I had difficulties putting topCorners into cv2.putText 'org' field when it was all one array, so I split it into two arrays
    topCornersX.append(int(corners[x].tolist()[0][0]) - xDiff)
    topCornersY.append(int(corners[x].tolist()[0][1]) - yDiff)
    bottomCornersX.append(int(corners[x].tolist()[0][0]))
    bottomCornersY.append(int(corners[x].tolist()[0][1]))
    #adds the h file
    if (x == 6 or x == 14 or x == 22 or x == 30 or x == 38 or x == 46):
        topCornersX.insert(x+1, bottomCornersX[x])
        topCornersY.insert(x+1, bottomCornersY[x] - yDiff)
        bottomCornersX.insert(x+1, bottomCornersX[x] + xDiff)
        bottomCornersY.insert(x+1, bottomCornersY[x])

#x == 54 is never in the loop, so it is done here instead
topCornersX.insert(55, bottomCornersX[54])
topCornersY.insert(55, bottomCornersY[54] - yDiff)
bottomCornersX.insert(55, bottomCornersX[54] + xDiff)
bottomCornersY.insert(55, bottomCornersY[54])

#adds the first rank
for x in range (0, 8):
    topCornersX.append(topCornersX[48+x])
    topCornersY.append(topCornersY[48+x]+yDiff)
    bottomCornersX.append(bottomCornersX[48+x])
    bottomCornersY.append(bottomCornersY[48+x]+yDiff)
'''
#was useful for troubleshooting the locations of topCornersX, topCornersY, bottomCornersX, and bottomCornersY
for x in range (0, 64):
    cv2.putText(customized_image, str(x), (int(topCornersX[x]), int(topCornersY[x])), cv2.FONT_HERSHEY_SIMPLEX, 1, [0, 255, 255], 5, 2)
    cv2.putText(customized_image, str(x), (int(bottomCornersX[x]), int(bottomCornersY[x])), cv2.FONT_HERSHEY_SIMPLEX, 1,[0, 0, 255], 5, 2)
    #it doesn't work unless I cast them as an int again, even though they should already be an int in the array. Anyways.
    cv2.rectangle(customized_image, (int(topCornersX[x]), int(topCornersY[x])), (int(bottomCornersX[x]), int(bottomCornersY[x])), (255, 0, 0), 2)
'''
#makes the array for the 'square' objects to be stored in
squares = list()
#Instantiates 64 squares from the square class
# initializes squares with a nested for loop
rows = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
#i is the y value of the chess board, 1, 2, 3, 4, ... 8
i = 8
#j is the x value of the chess board a, b, c, d ... h
j = - 1
for x in range(0, 64):
    if (x % 8 == 0 and x != 0):
        i = i - 1
        j = 0
    else:
        j = j + 1
    #strange things for the corners, I understood it at one point, maybe
    #makes a square from the Square class and then appends it to the squares list
    squares.append(SquareClass.Square(x, rows[j]+str(i), (topCornersX[x], topCornersY[x]), (bottomCornersY[x], bottomCornersX[x])))
'''
#confirms the squares were instantiated correctly, for debugging
#draws the square name on each square
for x in range(0, 64):
    print(f'{squares[x].numCreated} {squares[x].algNot} {squares[x].color}')
    cv2.putText(customized_image, f'{squares[x].algNot}', (int(topCornersX[x]+xDiff/4), int(topCornersY[x]+yDiff*.6)), cv2.FONT_HERSHEY_SIMPLEX, 1, [255, 0, 0], 5, 2)
'''
print("Put pieces on")
#has each square compare its current state: squareC with the previous color state: squareP
squareC = list()
squareP = list()
#will store the comparison values for squareC and square P
histCompare = list()
#I also need a masks list for the histograms
masks = list()
maskedImgForHistogram = list()
#fills both lists with 64 indexes
for x in range (0, 64):
    #C is current
    squareC.append("")
    #P is past
    squareP.append("")
    #Also needs 64 values
    histCompare.append("1")
    #create a mask for each
    masks.append("")
    maskedImgForHistogram.append("")
    #masks for the histograms
    masks[x] = numpy.zeros(grayscale_image_simple.shape[:2], numpy.uint8)
    masks[x][int(topCornersY[x]):int(bottomCornersY[x]), int(topCornersX[x]): int(bottomCornersX[x])] = 255
    #cv2.imshow(f'masks {squares[x].algNot}', masks[x])
    maskedImgForHistogram[x] = cv2.bitwise_and(customized_image, customized_image, mask=masks[x])

input("Put the pieces on and enter any input to begin")
'''
#now that the cv2 part is complete, begin the selenium part
#logs into lichess
log_into_lichess()
#waits for the login to complete
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'user_tag')))
#starts a 10 min game
start_10_min()
#waits for the game to start
#WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#main-wrap > main > div.round__app.variant-standard > div.round__app__board.main-board > div > cg-container > cg-board')))
WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main-wrap"]/main/div[1]/div[7]')))
#gets the orientation of the board
#boardO = driver.find_element(By.CSS_SELECTOR, '#main-wrap > main > div.round__app.variant-standard > div.round__app__board.main-board > div > cg-container > cg-board')
#orientation = boardO.get_attribute("class")
#gets the opponent's time
#timeOpp = driver.find_element(By.CSS_SELECTOR, 'div.rclock:nth-child(8)')
timeOpp = driver.find_element(By.XPATH, '//*[@id="main-wrap"]/main/div[1]/div[7]')
#gets the user's time
# fails because the selector changes timeUser = driver.find_element(By.CSS_SELECTOR, 'div.rclock:nth-child(9)')
timeUser = driver.find_element(By.XPATH, '//*[@id="main-wrap"]/main/div[1]/div[8]')

try:
    a = driver.find_element(By.CLASS_NAME, 'ranks black')
    myTurn = False
except:
    myTurn = True
'''
myTurn = True
keypressed = -1

z = 0
#this part of the program is going to be repeated
#esc key ends the loop
while(keypressed != 27):
    if(myTurn):
        # gets a frame
        ret, frame = cap.read()
        customized_image = frame
        # Resizes the image
        # code stolen from https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
        scale_percent = 20
        width = int(customized_image.shape[1] * scale_percent / 100)
        height = int(customized_image.shape[0] * scale_percent / 100)
        dim = (width, height)
        customized_image = cv2.resize(customized_image, dim, interpolation=cv2.INTER_AREA)

        cv2.imshow('Customized Image', customized_image)
        #finds the histogram for the current square and compares it to the past square
        for x in range(0, 64):
            # gets the histogram for the current square
            maskedImgForHistogram[x] = cv2.bitwise_and(customized_image, customized_image, mask=masks[x])
            squareC[x] = cv2.calcHist([customized_image], [0, 1, 2], masks[x], [8, 8, 8], [0, 256, 0, 256, 0, 256])
            cv2.imshow(f'masks {squares[x].algNot}', maskedImgForHistogram[x])
            #eventually this will be nested in a larger while loop, with z keeping track of the iterations
            #for the first iteration, there is no past histogram, so the two are equal
            #we do not need to update the past square, as it should be the same for the entire turn, only changing at the end
            if(z == 0):
                squareP[x] = squareC[x]
            #calculates the difference between the current and the past square state
            histCompare[x] = float(cv2.compareHist(squareC[x], squareP[x], cv2.HISTCMP_CORREL))
        #the possibleMoves list should be recreated in each iteration of the loop
        possibleMoves = list()
        for x in range(0, 64):
            #if the correlation between the two image is less than .3, then we will check if the move is legal
            if (float(histCompare[x]) < .3):
                if(squares[x].algNot not in possibleMoves):
                    possibleMoves.append(squares[x].algNot)
                    print(f'{histCompare[x]} {squares[x].algNot}')
            #try to remove values from possible moves, to mitigate the effects of shadows or squares passed over
            if float(histCompare[x] > .3 and squares[x].algNot in possibleMoves):
                index = possibleMoves.index(squares[x].algNot)
                possibleMoves.pop(index)

            if (float(histCompare[x]) < .8):
                print(f'{histCompare[x]} {squares[x].algNot}')
            #it was useful to see all the histograms for troubleshooting
            #print(f'{histCompare[x]} {squares[x].algNot}')
        z = 1
        #checks all combinations of the possible moves array for legal moves
        moves = checkLegalMoves(possibleMoves)
        #if there is only 1 legal move, then the program will make that move
        if(len(moves) == 1):
            moveFT(moves[0])
            myTurn = False
            print(moves(0))
            board.push_uci(moves[0])

            #speaks the times for both players
            engine.say(f'User has {timeUser.text} and Opponent has {timeOpp.text}')
        #if there is more than 1 legal move, then the program will wait longer
        else:
            if(len(moves) != 0):
                engine.say("More than one legal move has been input, waiting")
                engine.runAndWait()
        #print(possibleMoves)
    #if it is not our turn, then we wait for the opponent's move.
    else:
        z = 0
        #needs to be updated every move, so I do it inside the loop
        #lichess marks the last move with the class name of 'alt'
        altMove = driver.find_element(By.CLASS_NAME, 'alt')
        #checks if the move is legal
        if(altMove.text in board.legal_moves):
            #speaks the move of the opponent
            engine.say(str(altMove.text))
            engine.runAndWait()
            #makes the move on the board in the program
            board.push_san(altMove.text)

            #speaks the times for both players
            engine.say(f'User has {timeUser.text} and Opponent has {timeOpp.text}')
            myTurn = True

    cv2.imshow('Customized Image', customized_image)
    #waits for a key to be pressed
    keypressed = cv2.waitKey(20)


#cv2.waitKey(20)
#if escape key is pressed, the windows are closed
if keypressed == 27:
    cv2.destroyAllWindows()