from random import randint, choice
from time import sleep
from graphics import *

class Player:
    def __init__(self, w, h):
        self.startPos = [w/2, h-(h/5)]
        self.lifes = 3
        self.speed = 2
        self.player = Image(Point(self.startPos[0], self.startPos[1]), "Assets/Player/PlayerRight.png")
        self.dir = "Right"


class Object:
    def __init__(self, w, h):
        self.available = ["Lamp", "Lamp", "Speaker"]
        self.startPos = [randint(0, w), randint(-200, -31)]
        self.speed = 2.5
        self.vel = [0, 0.02]
        self.acc = [0, 0]
        self.gravity = [0, 9.8]
        self.hasMoved = 0
        self.type = choice(self.available)

        if self.type == "Lamp":
            self.obj = Image(Point(self.startPos[0], self.startPos[1]), "Assets/Objects/Lamp.png")
        elif self.type == "Speaker":
            self.obj = Image(Point(self.startPos[0], self.startPos[1]), "Assets/Objects/Speaker.png")

    def addForce(self, force):
        self.acc[1] += force[1]

    def update(self):
        self.vel[1] +=self.acc[1]
        self.obj.move(self.vel[0], self.vel[1])
        self.acc = [0, 0]

def borderCollide(player, screenWidth):
    if player.getAnchor().getX()-player.getWidth()/2 <= 0:
        return True
    elif player.getAnchor().getX()+player.getWidth()/2 >= screenWidth:
        return True
    else:
        return False

def checkCollide(p, object):
    if p.player.getAnchor().getX() > object.obj.getAnchor().getX():
        xDist = p.player.getAnchor().getX()-object.obj.getAnchor().getX()
    else:
        xDist = object.obj.getAnchor().getX()-p.player.getAnchor().getX()

    if p.player.getAnchor().getY() > object.obj.getAnchor().getY():
        yDist = p.player.getAnchor().getY()-object.obj.getAnchor().getY()
    else:
        yDist = object.obj.getAnchor().getY()-p.player.getAnchor().getY()

    if yDist <= p.player.getHeight()/2 and xDist <= p.player.getWidth()/2:
        return True
    else:
        return False

def checkNewWave(iters, waveIterAmount):
    if iters == waveIterAmount:
        return True
    else:
        return False

def main(width, height, win, player, changedDir, background):
    # Remaining objects
    fallingObjects = []
    maxObjAmount = 7

    # Remaining vars
    key = 5
    iterations = 0
    score = 0
    wave = 1
    waveIters = 500
    showLifes = Text(Point(110, 20), "Leben: "+str(player.lifes))
    showScore = Text(Point(190, 20), "Punkte: "+str(int(score)))
    showWave = Text(Point(270, 20), " Runde: "+str(wave))
    showLifes.setTextColor("White")
    showScore.setTextColor("White")
    showWave.setTextColor("White")
    showLifes.setStyle("bold")
    showScore.setStyle("bold")
    showWave.setStyle("bold")
    showLifes.draw(win)
    showScore.draw(win)
    showWave.draw(win)
    update(60)

    # Object Initialisation
    for i in range(randint(1, maxObjAmount)):
        i = Object(width, height)
        i.obj.draw(win)
        fallingObjects.append(i)

    # Main game loop
    player.player.draw(win)
    while True:
        key = win.checkKey()

        # Health detecting
        if player.lifes == -1:
            with open("HighScore.txt", "r+") as HighScore:
                saveRead = []
                read = str(HighScore.read())

                if int(read) < score:
                    HighScore.write(str(score))

            for i in fallingObjects:
                i.obj.undraw()
                fallingObjects.pop(fallingObjects.index(i))

            deathWin = Rectangle(Point(100, 100), Point(300, 300))
            deathWin.setFill(color_rgb(255, 36, 20))
            deathWin.setWidth(2)

            deathText = Text(Point(200, 125), "Du bist tot!")
            deathText.setStyle("bold")
            deathText.setSize(20)

            deathContinueBtn = Rectangle(Point(150, 165), Point(250, 215))
            deathQuitBtn = Rectangle(Point(150, 225), Point(250, 275))
            continueText = Text(Point(200, 190), "Wieder spielen")
            continueText.setSize(10)
            quitText = Text(Point(200, 250), "Verlassen")
            deathQuitBtn.setFill(color_rgb(207, 210, 214))
            deathContinueBtn.setFill(color_rgb(207, 210, 214))

            deathWin.draw(win)
            deathText.draw(win)
            deathQuitBtn.draw(win)
            deathContinueBtn.draw(win)
            continueText.draw(win)
            quitText.draw(win)

            while True:
                mouse = win.checkMouse()

                if mouse:
                    if mouse.getX() > 150 and mouse.getX() < 250:
                        if mouse.getY() > 165 and mouse.getY() < 215:
                            fallingObjects = []
                            background.undraw()
                            background.draw(win)
                            leaving = False

                            del player
                            player = Player(width, height)
                            main(width, height, win, player, changedDir, background)
                        elif mouse.getY() > 225 and mouse.getY() < 275:
                            win.close()
                            leaving = True
                            break

                update(60)

            if leaving:
                start()

        # Rotating player
        if key == "A" or key == "a" or key == "Left":
            if player.dir == "Left":
                player.dir = "Left"
            else:
                player.dir = "Left"
                changedDir = True
        elif key == "D" or key == "d" or key == "Right":
            if player.dir == "Right":
                player.dir = "Right"
            else:
                player.dir = "Right"
                changedDir = True
        elif key == "Escape":
            # Pause menu

            window = Rectangle(Point(100, 100), Point(300, 300))
            window.setFill(color_rgb(255, 36, 20))
            window.setWidth(2)
            window.draw(win)

            pauseText = Text(Point(200, 135), "Pause")
            resumeText = Text(Point(200, 190), "Fortsetzen")
            quitText = Text(Point(200, 250), "Verlassen")

            pauseText.setStyle("bold")
            resumeText.setStyle("bold")
            quitText.setStyle("bold")

            pauseText.setSize(20)

            resumeBtn = Rectangle(Point(150, 165), Point(250, 215))
            pauseQuitBtn = Rectangle(Point(150, 225), Point(250, 275))
            resumeBtn.setFill(color_rgb(207, 210, 214))
            resumeBtn.setOutline(color_rgb(186, 186, 186))
            pauseQuitBtn.setFill(color_rgb(207, 210, 214))
            pauseQuitBtn.setOutline(color_rgb(186, 186, 186))
            resumeBtn.draw(win)
            resumeText.draw(win)
            pauseQuitBtn.draw(win)
            quitText.draw(win)
            pauseText.draw(win)
            leaving = False

            while True:
                mousePoint = win.checkMouse()
                keyPressed = win.checkKey()

                if mousePoint:
                    if keyPressed == "Escape" or mousePoint.getX() > 150 and mousePoint.getX() < 250 and mousePoint.getY() > 165 and mousePoint.getY() < 215:
                        leaving = False
                        break
                    elif mousePoint.getX() > 150 and mousePoint.getX() < 250 and mousePoint.getY() > 225 and mousePoint.getY() < 275:
                        leaving = True
                        with open("HighScore.txt", "r+") as HighScore:
                            saveRead = []
                            read = str(HighScore.read())
                            if int(read) < score:
                                HighScore.write(str(score))

                        for i in fallingObjects:
                            i.obj.undraw()
                            fallingObjects.pop(fallingObjects.index(i))
                        break

                update(60)

            window.undraw()
            pauseText.undraw()
            resumeBtn.undraw()
            resumeText.undraw()
            pauseQuitBtn.undraw()
            quitText.undraw()
            if leaving:
                win.close()
                break

        else:
            pass

        # Moving player
        if player.dir == "Left":
            if borderCollide(player.player, width) == True:
                player.dir = "Right"
                player.player.move(player.speed*2, 0)
                changedDir = True
            else:
                player.player.move(-player.speed, 0)
        elif player.dir == "Right":
            if borderCollide(player.player, width) == True:
                player.dir = "Left"
                player.player.move(-player.speed*2, 0)
                changedDir = True
            else:
                player.player.move(player.speed, 0)
        else:
            pass

        # Changing player sprite if direction has changed
        if changedDir:
            if player.dir == "Right":
                player.player.undraw()
                newPos = [player.player.getAnchor().getX(), height-(height/5)]
                player.player = Image(Point(newPos[0], newPos[1]), "Assets/Player/PlayerRight.png")
                player.player.draw(win)
            elif player.dir == "Left":
                player.player.undraw()
                newPos = [player.player.getAnchor().getX(), height-(height/5)]
                player.player = Image(Point(newPos[0], newPos[1]), "Assets/Player/PlayerLeft.png")
                player.player.draw(win)
            else:
                player.player.undraw()
                newPos = [player.player.getAnchor().getX(), height-(height/5)]
                player.player = Image(Point(newPos[0], newPos[1]), "Assets/Player/PlayerStill.png")
                player.player.draw(win)

            changedDir = False

        # Moving all falling objects down by their speed
        popIndexes = []
        savePopIndexes = []
        for faller in range(len(fallingObjects)):
            # if settingsDict["1"] == False:
            #     if fallingObjects[faller].obj.getAnchor().getY() >= height+(fallingObjects[faller].obj.getHeight()/2):
            #         popIndexes.append(faller)
            #         savePopIndexes.append(faller)
            #         fallingObjects[faller].obj.undraw()
            #         fallingObjects[faller].hasMoved = False
            #     else:
            #         fallingObjects[faller].hasMoved = False
            #         fallingObjects[faller].obj.move(0, fallSpeed)
            #         fallingObjects[faller].hasMoved = True
            # else:
            #     fallingObjects[faller].addForce(fallingObjects[faller].gravity)
            #     fallingObjects[faller].update()

            if fallingObjects[faller].obj.getAnchor().getY() >= height+(fallingObjects[faller].obj.getHeight()/2):
                popIndexes.append(faller)
                savePopIndexes.append(faller)
                fallingObjects[faller].obj.undraw()
                fallingObjects[faller].hasMoved = False
            else:
                fallingObjects[faller].hasMoved = False
                fallingObjects[faller].obj.move(0, fallingObjects[faller].speed)
                fallingObjects[faller].hasMoved = True

        for i in popIndexes:
            try:
                fallingObjects.pop(i)
            except:
                for j in savePopIndexes:
                    fallingObjects.pop(j)

        for faller in fallingObjects:
            if faller.hasMoved:
                pass
            else:
                faller.obj.undraw()
                fallingObjects.pop(fallingObjects.index(faller))

        # Collision detection
        popped = 0
        for i in range(len(fallingObjects)):
            i -= popped
            if checkCollide(player, fallingObjects[i]):
                fallingObjects[i].obj.undraw()
                fallingObjects.pop(i)
                popped += 1
                player.lifes -= 1
                showLifes.setText("Leben: "+str(player.lifes))
                player.player.undraw()
                sleep(0.25)
                player.player.draw(win)
                sleep(0.25)
                player.player.undraw()
                sleep(0.25)
                player.player.draw(win)

        # Sprite redrawing after wave
        iterations += 1
        score += 1
        if checkNewWave(iterations, waveIters):
            iterations = 0
            waveIters += 10
            player.lifes = 3
            wave += 1
            for faller in fallingObjects:
                faller.obj.undraw()

            fallingObjects = []
            background.undraw()
            background.draw(win)
            player.player.undraw()
            player.player.draw(win)
            showLifes.undraw()
            showScore.undraw()
            showWave.undraw()
            showLifes.setText("Leben: "+str(player.lifes))
            showWave.setText(" Runde: "+str(wave))
            showLifes.draw(win)
            showScore.draw(win)
            showWave.draw(win)
            sleep(1)
        else:
            # Adding more falling objects
            if randint(0, 200) <= 1:
                for i in range(randint(1, 3)):
                    i = Object(width, height)
                    i.obj.draw(win)
                    fallingObjects.append(i)

        if score%100 == 0:
            showScore.setText("Punkte: "+str(int(score/100)))

        update(60)

    start()

# def settings(win):
#     window = Rectangle(Point(100, 100), Point(300, 300))
#     window.setWidth(2)
#     window.setFill(color_rgb(255, 36, 20))
#     window.draw(win)
#
#     settingsText = Text(Point(200, 125), "Einstellungen")
#     settingsText.setStyle("bold")
#     settingsText.setSize(20)
#     settingsText.draw(win)
#
#     quitSettingsBtn = Rectangle(Point(150, 260), Point(250, 290))
#     quitSettingsBtn.setFill(color_rgb(207, 210, 214))
#     quitSettingsBtn.setOutline(color_rgb(186, 186, 186))
#     quitSettingsBtnText = Text(Point(200, 275), "Verlassen")
#     quitSettingsBtnText.setStyle("bold")
#     quitSettingsBtn.draw(win)
#     quitSettingsBtnText.draw(win)
#
#     setting1Text = Text(Point(230, 200), "Schwerkraftmodus")
#     setting1Text.setStyle("bold")
#     setting1Text.setSize(11)
#     setting1Text.draw(win)
#     setting1 = settingsDict["1"]
#
#     onBtn1 = Image(Point(140, 200), "Assets/Screen/On.png")
#     offBtn1 = Image(Point(140, 200), "Assets/Screen/Off.png")
#     offBtn1.draw(win)
#
#     while True:
#         mouse = win.getMouse()
#
#         if mouse.getX() > 140-onBtn1.getWidth()/2 and mouse.getX() < 140+onBtn1.getWidth()/2 and mouse.getY() > 200-onBtn1.getHeight()/2 and mouse.getY() < 200+onBtn1.getHeight()/2:
#             if setting1 == True:
#                 setting1 = False
#                 settingsDict["1"] = False
#                 offBtn1.undraw()
#                 onBtn1.draw(win)
#             else:
#                 setting1 = True
#                 settingsDict["1"] = True
#                 onBtn1.undraw()
#                 try:
#                     offBtn1.draw(win)
#                 except:
#                     pass
#         elif mouse.getX() > 150 and mouse.getX() < 250 and mouse.getY() > 260 and mouse.getY() < 290:
#             break
#
#     window.undraw()
#     settingsText.undraw()
#     onBtn1.undraw()
#     offBtn1.undraw()
#     setting1Text.undraw()
#     quitSettingsBtn.undraw()
#     quitSettingsBtnText.undraw()


def help(win):
    helpWindow = Rectangle(Point(100, 100), Point(300, 300))
    helpWindow.setWidth(2)
    helpWindow.setFill(color_rgb(255, 36, 20))
    helpWindow.draw(win)

    quitBtn = Rectangle(Point(150, 260), Point(250, 290))
    quitBtn.setFill(color_rgb(207, 210, 214))
    quitBtn.setOutline(color_rgb(186, 186, 186))
    quitBtnText = Text(Point(200, 275), "Verlassen")
    quitBtnText.setStyle("bold")
    quitBtn.draw(win)
    quitBtnText.draw(win)

    with open("help.txt", "r") as text:
        helpText = Text(Point(200, 190), text.read())
        helpText.setSize(9)
        helpText.draw(win)

    while True:
        mouse = win.checkMouse()

        if mouse:
            if mouse.getX() > 150 and mouse.getX() < 250:
                if mouse.getY() > 260 and mouse.getY() < 290:
                    break

        update(60)

    helpWindow.undraw()
    helpText.undraw()
    quitBtn.undraw()
    quitBtnText.undraw()



def start():
    # Init screen
    title = "Theater Versagen"
    width = 400
    height = 400
    win = GraphWin(title, width, height) # Theater Fail

    # UI Design
    background = Image(Point(width/2, height/2), "Assets/Screen/Background.gif")
    background.draw(win)

    titleText = Text(Point(200, 30), "Theater Versagen")
    titleText.setStyle("bold")
    titleText.setSize(27)
    titleText.setTextColor("white")
    titleText.draw(win)

    with open("HighScore.txt", "r") as HighScore:
        readText = HighScore.read()
        highScoreText = Text(Point(200, 105), str("Höchste Punktzahl:\n"+str(int(int(readText)/100))))
        highScoreText.setStyle("bold")
        highScoreText.setTextColor("white")
        highScoreText.draw(win)

    startBtn = Rectangle(Point(100, 145), Point(300, 220))
    startBtn.setFill(color_rgb(207, 210, 214))
    startBtn.setOutline(color_rgb(186, 186, 186))
    startBtnText = Text(Point(200, 182.5), "Starten")
    startBtnText.setSize(27)
    startBtnText.setStyle("bold")
    startBtn.draw(win)
    startBtnText.draw(win)

    helpBtn = Rectangle(Point(150, 240), Point(250, 270))
    helpBtn.setFill(color_rgb(207, 210, 214))
    helpBtn.setOutline(color_rgb(186, 186, 186))
    helpBtnText = Text(Point(200, 255), "Hilfe")
    helpBtnText.setStyle("bold")
    helpBtn.draw(win)
    helpBtnText.draw(win)

    # settingsBtn = Rectangle(Point(150, 280), Point(250, 310))
    # settingsBtn.setFill(color_rgb(207, 210, 214))
    # settingsBtn.setOutline(color_rgb(186, 186, 186))
    # settingsBtnText = Text(Point(200, 295), "Einstellungen")
    # settingsBtnText.setStyle("bold")
    # settingsBtnText.setSize(11)
    # settingsBtn.draw(win)
    # settingsBtnText.draw(win)

    # quitBtn = Rectangle(Point(150, 320), Point(250, 350))
    # quitBtn.setFill(color_rgb(207, 210, 214))
    # quitBtn.setOutline(color_rgb(186, 186, 186))
    # quitBtnText = Text(Point(200, 335), "Verlassen")
    # quitBtnText.setStyle("bold")
    # quitBtn.draw(win)
    # quitBtnText.draw(win)

    quitBtn = Rectangle(Point(150, 280), Point(250, 310))
    quitBtn.setFill(color_rgb(207, 210, 214))
    quitBtn.setOutline(color_rgb(186, 186, 186))
    quitBtnText = Text(Point(200, 295), "Verlassen")
    quitBtnText.setStyle("bold")
    quitBtn.draw(win)
    quitBtnText.draw(win)

    # Player initialisation
    player = Player(width, height)
    changedDir = False

    # Starting game
    while True:
        mouse = win.getMouse()
        if mouse.getX() < 300 and mouse.getX() > 100 and mouse.getY() < 220 and mouse.getY() > 145:
            titleText.undraw()
            highScoreText.undraw()
            startBtn.undraw()
            startBtnText.undraw()
            helpBtn.undraw()
            helpBtnText.undraw()
            # settingsBtn.undraw()
            # settingsBtnText.undraw()
            quitBtn.undraw()
            quitBtnText.undraw()
            main(width, height, win, player, changedDir, background)

        if mouse.getX() < 250 and mouse.getX() > 150 and mouse.getY() > 240 and mouse.getY() < 270:
            help(win)

        # if mouse.getX() < 250 and mouse.getX() > 150 and mouse.getY() > 280 and mouse.getY() < 310:
        #     settings(win)

        if mouse.getX() < 250 and mouse.getX() > 150 and mouse.getY() > 280 and mouse.getY() < 310:
            win.close()
            break
        update(60)
    exit()

# global settingsDict
# settingsDict = {"1":False}

# Starting game
if __name__ == "__main__":
    start()
