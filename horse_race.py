import random as RD
import threading as TH
import time
import os
import pandas as pd

class Validate:
    @classmethod
    def isNumber(cls, value):
        return isinstance(value, int) or isinstance(value, float)

    @classmethod
    def between(cls, valueA: int, valueB: int, value):
        return cls.isNumber(value) and value in range(valueA, valueB+1)


class Horse:
    def __init__(self, name: str):
        self.speed = 0
        self.name = name
        self.id = None
        self.position = 0
        self.totalTime = 0
        
    def run(self, to: int, race):
        self.speed = RD.randint(1, 5)
        
        while (to > self.position) and race.raceInProgress:                                                
            if to - self.position > self.speed:
                self.position += self.speed
                self.totalTime += 1
            else:
                self.totalTime += round((to-self.position)/self.speed,2)
                self.position = to

            self.randomSpeed()
            time.sleep(1)

    def icon(self):       
            return '-RP' if self.position%2 == 0 else '~PR'
       
    def atFinishLine(self, finishLine:int):
        return self.position == finishLine

    def randomSpeed(self):
        self.speed = RD.randint(self.minSpeed(), self.maxSpeed())

    def decelerate(self):
        return self.speed - RD.randint(1, 3)

    def accelerate(self):
        return self.speed + RD.randint(1, 3)

    def minSpeed(self):
        return max(self.decelerate(), 1)

    def maxSpeed(self):
        return min(self.accelerate(), 5)

    def assignID(self, id):
        self.id = id


class Race:
    def __init__(self, raceDistance: int, horseNames: list, maxHorses=20):
        self.horses = []
        self.threads = []
        self._avaibleIDs = list(range(1, 101))
        self.raceDistance = raceDistance
        self.raceInProgress = False
        self.winner = None

        columns = ['Nombre', 'Número', 'Metros']
        self.df = pd.DataFrame(columns=columns)
        
        if not Validate.between(2, maxHorses, len(horseNames)):
            raise ValueError(f'La cantidad de caballos debe estar entre 2 y {maxHorses} caballos')

        self._generateIDs(horseNames)

    def addHorses(self, horseList: list):
        self.horses.append(horseList)

    def totalHorses(self):
        return len(self.horses)

    def _avaibleID(self, id: int):
        return id in self._avaibleIDs

    def _removeAvaiableID(self, id: int):
        self._avaibleIDs.pop(id)

    def _assignID(self, horse: Horse):
        id = self._selectRandomID(self._randomID)
        horse.assignID(id)
        self._removeAvaiableID(id)

    def _randomID(self):
        return RD.randint(1, len(self._avaibleIDs))

    def _selectRandomID(self, id):
        while not self._avaibleID(id):
            id = self._randomID()

        return id

    def _generateIDs(self, horseNames):
        for horse in horseNames:
            horse = Horse(name=horse)
            self._assignID(horse)
            self.horses.append(horse)

    def _horseNames(self):
        return [horse.name for horse in self.horses]

    def _horseIDs(self):
        return [horse.id for horse in self.horses]

    def horseInfo(self):

        longWord = max(self._horseNames(), key=len)

        def _tab(word):
            spaces = " " * (len(longWord) - len(word) + 2 if _LONGWORD(longWord) else 16 - len(word))
            return spaces

        def _LONGWORD(word):
            length = len(word)
            return True if length > 14 else False

        print('-----------------------------------')
        print(f'Nombre Caballo{_tab("Nombre Caballo")}|  Número')
        print('-----------------------------------')

        for horse in self.horses:
            print(f'{horse.name}{_tab(horse.name)}|  {horse.id}')

    def start(self):
        self.raceInProgress = True
        self._createThread()
        self._startThreads()
        self._endRace()

    def _createThread(self):
        for horse in self.horses:
            thread = TH.Thread(target=horse.run, args=(self.raceDistance,self,))
            self.threads.append(thread)

    def _startThreads(self):
        for thread in self.threads:
            thread.start()

    def _endRace(self):
        distances = []     

        def posSimulation(horse):
            return ' '*horse.position

        def clear_screen():
            os.system('cls' if os.name == 'nt' else 'clear')

        def longestName():
            return max(self._horseNames(), key=len)

        while self.raceInProgress:
            time.sleep(0.99)
            clear_screen()

            print('GRAND PREMIO JOCKEY CLUB V.1.0.0 | Pablo Foglia (c)')
            print('---------------------------------------------------')
            print()
            for horse in self.horses:                
                gap = ' '*(self.raceDistance - horse.position)
                nameGap = ' '*(len(longestName()) - len(horse.name))
                print(f'{horse.name}{nameGap}|{posSimulation(horse)}{horse.icon()}{gap}|Finish|')
            
            for horse in self.horses:
                if horse.position == self.raceDistance: 
                    self.raceInProgress = False
                    self.winner = horse
        
        for thread in self.threads:
            thread.join()

        for horse in self.horses:
            distances.append(horse.position)
        
        self.df = self.df.assign(Nombre=self._horseNames(), Número=self._horseIDs(), Metros=distances)
        
        print()
        print(f'El caballo {self.winner.name} ganó la carrera a los {self.winner.totalTime} segundos.')
        
        time.sleep(5)
        clear_screen()
        print(self.df.head(20))
        time.sleep(5)
        clear_screen()
        print(f'|||| GAME OVER ||||')
        

horses = ["Rayo", "Fuego", "Trueno", "Viento", "Veloz",
          "Relámpago", "Centella", "Bravo", "Dorado", "Galope","Gato"]

race = Race(raceDistance=100, horseNames=horses)

race.start()