import random as rnd
import prettytable as prettytable
import time
import sys


POPULATION_SIZE = 64
TOURNAMENT_SELECTION_SIZE = 12
MUTATION_RATE = 0.1

#=======================================================================================================================


class Data:
    #The Meeting_time's array contain ['ID', 'Day and Hour', 'Day']
    MEETING_TIME = [[1, "Saturday 08:00 - 10:00" ,"Saturday"],[2, "Saturday 10:00 - 12:00","Saturday"],[3, "Saturday 02:00 - 04:00","Saturday"],[4, "Saturday 04:00 - 06:00","Saturday"],
                    [5, "Sunday 08:00 - 10:00","Sunday"],[6, "Sunday 10:00 - 12:00","Sunday"],[7, "Sunday 02:00 - 04:30","Sunday"],[8, "Sunday 04:30 - 06:00","Sunday"],
                    [9, "Monday 08:00 - 10:00","Monday"],[10, "Monday 10:00 - 12:00","Monday"],[11, "Monday 02:00 - 04:00","Monday"],[12, "Monday 04:00 - 06:00","Monday"],
                    [13, "Tuesday 08:00 - 10:00","Tuesday"],[14, "Tuesday 10:00 - 12:00","Tuesday"],[15, "Tuesday 02:00 - 04:00","Tuesday"],[16, "Tuesday 04:00 - 06:00","Tuesday"]
                    ]
    #The Room's array contain ['ID', 'capacity']
    ROOMS = [["R126", 45] ,["R128" , 35] , ["R130", 30], ["R131", 40]]

    PROFESSOR = [["I1", "Pro ALi Ramzi"],
                  ["I2", "Pro Razavian"],
                  ["I3", "Pro Ali Moradi"],
                  ["I4", "Dr Shirdel"]
                  ]
    #The Lesson's array is contain ['ID', 'Lesson','Entrance of University', 'Number of lesson','Maximum number of students','Must be or not be in one day','Lessons in tandem']
    LESSON = [
        ["L0", "Programming Basics", 1398, 3, 30 , 'MustNotBeInOneDay', '-'],
        ["L1", "Math One", 1398, 4, 40, 'MustNotBeInOneDay', '-'],
        ["L2", "Technical language", 1397, 2, 25, 'MustNotBeInOneDay', '-'],
        ["L3", "Data Structure", 1397, 4, 35, 'MustNotBeInOneDay', '-'],
        ["L4", "Computer systems", 1397, 4, 35, 'MustBeInOneDay', 'tandem'],
        ["L5", "operating system", 1396, 4, 30, 'MustNotBeInOneDay', '-'],
        ["L6", "Matrix", 1396, 3, 40, 'MustBeInOneDay', 'tandem'],
        ["L7", "Artificial intelligence", 1395, 3, 25, 'MustNotBeInOneDay', '-'],
        ["L8", "Graph", 1395, 3, 40, '-', '-'],
        ["L9", "Entrepreneurship", 1397, 2, 40, '-', '-']

    ]

    def __init__(self):
        self._room =[]; self._meetingTimes = []; self._professors = []; self._lesson = []

        #Putting all the rooms in A _room's array
        for i in range (0, len(self.ROOMS)):
            self._room.append(Room(self.ROOMS[i][0], self.ROOMS[i][1]))

        #Putting all the meetingTimes in _meetingTime's Array
        for i in range (0, len(self.MEETING_TIME)):
            self._meetingTimes.append(MeetingTime(self.MEETING_TIME[i][0], self.MEETING_TIME[i][1],self.MEETING_TIME[i][2]))

        #Putting all the Lesson in _lesson's Array
        for i in range (0, len(self.LESSON)):
            self._lesson.append(Lesson(self.LESSON[i][0], self.LESSON[i][1],self.LESSON[i][2],self.LESSON[i][3],self.LESSON[i][4],self.LESSON[i][5],self.LESSON[i][6]))

        # Putting all the professor in _professors Array
        for i in range (0, len(self.PROFESSOR)):
            self._professors.append(Professor(self.PROFESSOR[i][0], self.PROFESSOR[i][1]))


    #====================================================

        #In each variable, the function represents the professor and the lessons it offers and the empty times
        pro1 = ProfessorInfo( self._professors[0], [self._lesson[3],self._lesson[4], self._lesson[7]], [self._meetingTimes[4], self._meetingTimes[6], self._meetingTimes[7],self._meetingTimes[8],self._meetingTimes[10],self._meetingTimes[12],self._meetingTimes[14],self._meetingTimes[15]])
        pro2 = ProfessorInfo( self._professors[1], [self._lesson[0],self._lesson[2], self._lesson[5]],[self._meetingTimes[0], self._meetingTimes[1], self._meetingTimes[4], self._meetingTimes[5], self._meetingTimes[11],self._meetingTimes[13],self._meetingTimes[14]])
        pro3 = ProfessorInfo( self._professors[2], [self._lesson[1],self._lesson[6], self._lesson[8]],[self._meetingTimes[0], self._meetingTimes[2], self._meetingTimes[6], self._meetingTimes[7], self._meetingTimes[8], self._meetingTimes[10], self._meetingTimes[14], self._meetingTimes[15]])
        pro4 = ProfessorInfo( self._professors[3],[self._lesson[9]] , [self._meetingTimes[5], self._meetingTimes[3],self._meetingTimes[2],self._meetingTimes[11]])

        self._Professors = [pro1, pro2, pro3, pro4]


    #===================================================

    #Function contains all rooms and related information
    def get_rooms(self): return self._room
    #+++++++++++++++++++++++++++++++++++

    #Function containing professor and id
    def get_professors(self): return self._professors
    #+++++++++++++++++++++++++++++++++++

    # Function containing time and information provided
    def get_meetingTimes(self): return self._meetingTimes
    #++++++++++++++++++++++++++++++++++++

    # The table contains all the professors and information provided
    def get_professorsINFO(self): return self._Professors
    #+++++++++++++++++++++++++++++++++++


#=======================================================================================================================

class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numbOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True



    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): return self._numbOfConflicts

    def get_fitness(self):
        if(self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):


        professor = self._data.get_professorsINFO()
        for i in range(0, len(professor)):
            # ******************  Lessons taught by Professor "i"  **********************
            lessons = professor[i].get_lessonName()

            # ****************** Empty Times Professor "i" ***********************
            TimePro = professor[i].get_freeTimes()

            for j in range(0,len(lessons)):

                # ***************  Number of lesson units *********************
                NumberOfUnits = lessons[j].get_NumberOfUnits()
                # *************** Offers fixed weekly classes *****************
                for k in range(0,int(NumberOfUnits/2)):
                    newClass = Class(self._classNumb,lessons[j],'fixed')
                    self._classNumb += 1
                    #************ Set a meeting Time randomly but from professor's time **********
                    newClass.set_meetingTime(TimePro[rnd.randrange(0, len(TimePro))])
                    #********* Set a room randomly ********
                    newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                    #****** set the Professor intended *********
                    newClass.set_professor(professor[i].get_pro())
                    # ********* Append the new class to the _classes array ***********
                    self._classes.append(newClass)

                #************** Offer classes with odd unit numbers. For even or odd weeks ********
                if NumberOfUnits % 2 != 0:
                    if rnd.random() >= 0.5:
                        newClass = Class(self._classNumb, lessons[j], 'even')

                    else:
                        newClass = Class(self._classNumb, lessons[j], 'odd')
                    self._classNumb += 1
                    newClass.set_meetingTime(TimePro[rnd.randrange(0, len(TimePro))])
                    newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                    newClass.set_professor(professor[i].get_pro())
                    self._classes.append(newClass)

        return self
    def calculate_fitness(self):
        self._numbOfConflicts = 0
        classes = self.get_classes()
        for i in range(0,len(classes)):

            # Check the number of students with room capacity
            if (classes[i].get_room().get_seatingCapacity() < classes[i].get_Lesson().get_capacity()): self._numbOfConflicts += 1

            for j in range(0, len(classes)):
                if (j > i):
                    # Check if class i and class j offered in the same time and their id are different
                    if classes[i].get_meetingTime() == classes[j].get_meetingTime() and classes[i].get_id() !=classes[j].get_id():
                        # If the room belongs to two classes simultaneously
                        if classes[i].get_room() == classes[j].get_room():
                            # Check if class i OR class j is fixed , we increase _numbOfConflicts to reduce fitness
                            if classes[j].get_kindOddOrNot() == 'fixed' or classes[i].get_kindOddOrNot() == 'fixed' :
                                self._numbOfConflicts += 1
                            # Check if class i and class j is both 'fixed' or 'even' or 'odd' , we increase _numbOfConflicts to reduce fitness
                            elif classes[i].get_kindOddOrNot() == classes[j].get_kindOddOrNot():
                                self._numbOfConflicts += 1
                        # Check if the Professor have to class in the same time
                        if classes[i].get_professor() == classes[j].get_professor(): self._numbOfConflicts += 1
                        # Check if the Entrance x year have lesson in the same time
                        if classes[i].get_Lesson().get_ForEnter() == classes[j].get_Lesson().get_ForEnter(): self._numbOfConflicts += 1
                    # Check if the lessons have the same name
                    if classes[i].get_Lesson().get_lessonName() == classes[j].get_Lesson().get_lessonName():
                        # Check if the lesson have same name and Not in one
                        if classes[i].get_meetingTime().get_day() == classes[j].get_meetingTime().get_day() and classes[i].get_Lesson().get_MustBeOrNOtInOneDay() == 'MustNotBeInOneDay' : self._numbOfConflicts += 1
                        # Check if the lesson have same name and in one day
                        if classes[i].get_meetingTime().get_day() != classes[j].get_meetingTime().get_day() and classes[i].get_Lesson().get_MustBeOrNOtInOneDay() == 'MustBeInOneDay' :self._numbOfConflicts += 1

                        # Check if the lesson in one day and tandem
                        if classes[i].get_meetingTime().get_day() == classes[j].get_meetingTime().get_day() and classes[i].get_Lesson().get_MustBeOrNOtInOneDay() == 'MustBeInOneDay' :
                            if classes[i].get_Lesson().get_InDayThanTandem() == 'tandem' :
                                if classes[i].get_meetingTime().get_id() == classes[j].get_meetingTime().get_id() + 1 : self._numbOfConflicts += 0
                                elif classes[i].get_meetingTime().get_id() == classes[j].get_meetingTime().get_id() - 1: self._numbOfConflicts += 0
                                else: self._numbOfConflicts += 1

        # If fitness will return 1.0
        return 1 / (self._numbOfConflicts + 1 )
    def __str__(self):
        # putting Information of array (_class) in string (returnValue)
        returnValue = ""
        for i in range(0, len(self._classes) - 1 ):
            returnValue += str(self._classes[i]) + ", "
        returnValue += str(self._classes[len(self._classes)- 1])
        return returnValue

#=======================================================================================================================

class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = []
        # Create the first population
        for i in range(0, size): self._schedules.append(Schedule().initialize())

    def get_schedules(self): return self._schedules

#=======================================================================================================================

class  GeneticAlgorithm:
    def evolve(self, population): return self._mutate_population(self._crossover_population(population))

    ##############################################

    def _crossover_population(self,pop):
        # for one time finding an empty population
        crossover_pop = Population(0)
        # Append the first table which has the best fitness
        crossover_pop.get_schedules().append(pop.get_schedules()[0])
        i = 1
        # The best parents are selected based on population size
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            # Get new Children by combining parents
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    ##############################################

    def _mutate_population(self, population):
        # doing a mutaion for each table
        for i in range(1, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    ##############################################

    def _crossover_schedule(self, schedule1, schedule2):
        # crossoverSchedule is a new table that will change all the first data by combining parents and get a new child
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if(rnd.random() > 0.5): crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else: crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    ##############################################

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        # Will do mutatation for each of parameter in one table if random letter than 0.1
        for i in range(0, len(mutateSchedule.get_classes())):
            if(MUTATION_RATE > rnd.random()): mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    ##############################################

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        # To select a parent, a set must be selected as random and that sort and reverse by fitness to get the best fitness parent in this small population
        while i < TOURNAMENT_SELECTION_SIZE:

            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda  x: x.get_fitness(), reverse=True)
        return  tournament_pop

# ===================================================================================================================


class Professor:
    def __init__(self, id, name):
        self._id = id
        self._name = name
    def get_id(self): return self._id
    def get_name(self): return self._name
    def __str__(self): return self._name

#=======================================================================================================================

class Room:
    def __init__(self, number, seatingCapacity):
        self._number = number
        self._seatingCapacity = seatingCapacity
    def get_number(self): return self._number
    def get_seatingCapacity(self): return self._seatingCapacity

#=======================================================================================================================

class MeetingTime:
    def __init__(self, id, time, day):
        self._id = id
        self._time = time
        self._day = day
    def get_id(self): return self._id
    def get_time(self): return self._time
    def get_day(self): return self._day


#=======================================================================================================================

class ProfessorInfo:
    def __init__(self, pro, lesson, freeTimes):

        self._pro = pro
        self._lesson = lesson
        self._freeTimes = freeTimes

    def get_lessonName(self):
        return self._lesson

    def get_pro(self):return self._pro
    def get_freeTimes(self):return self._freeTimes

#=======================================================================================================================

class Lesson:
    def __init__(self, id ,lesson,ForEnter,NumberOfUnits,capacity, MustBeOrNOtInOneDay, InDayThanTandem):
        self._id= id
        self._lesson = lesson
        self._ForEnter = ForEnter
        self._NumberOfUnits = NumberOfUnits
        self._capacity = capacity
        self._MustBeOrNOtInOneDay = MustBeOrNOtInOneDay
        self._InDayThanTandem = InDayThanTandem

    def get_id(self): return self._id

    def get_lessonName(self): return self._lesson
    def get_ForEnter(self): return self._ForEnter
    def get_NumberOfUnits(self): return self._NumberOfUnits
    def get_capacity(self): return self._capacity
    def get_MustBeOrNOtInOneDay(self): return self._MustBeOrNOtInOneDay
    def get_InDayThanTandem(self): return self._InDayThanTandem

#=======================================================================================================================

class Class:
    def __init__(self, id, Lesson, kindOddOrNot):
        self._id = id
        self._Lesson = Lesson
        self._kindOddOrNot = kindOddOrNot
        self._professor = None
        self._meetingTime = None
        self._room = None

    def get_id(self): return self._id
    def get_Lesson(self): return self._Lesson
    def get_kindOddOrNot(self): return self._kindOddOrNot
    def get_professor(self): return self._professor
    def get_meetingTime(self): return self._meetingTime
    def get_room(self): return self._room

    def set_professor(self, professor): self._professor = professor
    def set_meetingTime(self, meetingTime): self._meetingTime = meetingTime
    def set_room(self, room): self._room = room


    def __str__(self):
        return str(self.get_Lesson().get_lessonName()) + "," + str(self._meetingTime.get_time())+' -- | '

#=======================================================================================================================


class DisplayMgr:
    def print_available_data(self):
        print(">> All Available Data")

        self.print_room()
        self.print_professor()
        self.print_meeting_times()

    def print_room(self):
        availableRoomsTable = prettytable.PrettyTable(['room #', 'max seating capacity'])
        rooms = data.get_rooms()
        for i in range (0, len(rooms)):
            availableRoomsTable.add_row([str(rooms[i].get_number()), str(rooms[i].get_seatingCapacity())])
        print(availableRoomsTable)
    def print_professor(self):
        availableProfessorsTable = prettytable.PrettyTable(['id', 'professor'])
        professors = data.get_professors()
        for i in range(0, len(professors)):
            availableProfessorsTable.add_row([professors[i].get_id(), professors[i].get_name()])
        print(availableProfessorsTable)
    def print_meeting_times(self):
        availableMeetingTimeTable = prettytable.PrettyTable(['id', 'Meeting Time'])
        meetingTimes = data.get_meetingTimes()
        for i in range(0, len(meetingTimes)):
            availableMeetingTimeTable.add_row([meetingTimes[i].get_id(), meetingTimes[i].get_time()])
        print(availableMeetingTimeTable)

    def print_generation(self, population):
        table1 = prettytable.PrettyTable(['schedule #', 'fitness', 'classes [ class, Time]'])
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            table1.add_row([str(i), round(schedules[i].get_fitness(), 3), schedules[i].__str__() ])
        print(table1)

    def print_schedule_as_table(self, schedule):
        classes = schedule.get_classes()
        table = prettytable.PrettyTable(['Class #', "Professor(ID)", 'Lesson (ID, Entrance, MaxOfStudent, Units, MustBeOrNOtInOneDay, Tandem )', 'Room (Capacity, Kind)', "MeetingTime" ])
        for i in range(0, len(classes)):
            table.add_row([str(i+1),
                           classes[i].get_professor().get_name() + " (" + str(classes[i].get_professor().get_id()) + ")",
                           classes[i].get_Lesson().get_lessonName() + " (" + classes[i].get_Lesson().get_id() + ", " + str(classes[i].get_Lesson().get_ForEnter()) +", "+ str(classes[i].get_Lesson().get_capacity()) + ", "+ str(classes[i].get_Lesson().get_NumberOfUnits())+ ", " + classes[i].get_Lesson().get_MustBeOrNOtInOneDay()+ ", "+ classes[i].get_Lesson().get_InDayThanTandem() + ")" ,
                           classes[i].get_room().get_number() + " (" +  str(classes[i].get_room().get_seatingCapacity()) + ", " + str(classes[i].get_kindOddOrNot()) + ")" ,
                           classes[i].get_meetingTime().get_time() + " (" + str(classes[i].get_meetingTime().get_id()) + ")"
                           ])

        print(table)

#=======================================================================================================================

data = Data()
displayMgr = DisplayMgr()
displayMgr.print_available_data()
generationNumber = 0

population = Population(POPULATION_SIZE)
# Sorting and Reversing (by the fitness) to get the best fitness
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

print("\n> The Table's best fitness selected by the first population | Generation # " + str(generationNumber))

displayMgr.print_generation(population)
displayMgr.print_schedule_as_table(population.get_schedules()[0])
geneticAlgorithm = GeneticAlgorithm()

print('===============================================================================================')
starttime = time.time()
while population.get_schedules()[0].get_fitness() != 1.0:
    generationNumber += 1
    print("\n> Generation #" + str(generationNumber))
    population = geneticAlgorithm.evolve(population)
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    # displayMgr.print_generation(population)
    # displayMgr.print_schedule_as_table(population.get_schedules()[0])
    print('> Fitness is : ' , population.get_schedules()[0].get_fitness())
    endtime = time.time()
    end = endtime - starttime
    # if end >= 5.00 :
    #     print('\n*******************  TimeOut try again :( , This Table Is Not Compeleted   *********************** ')
    #     break


# displayMgr.print_generation(population)
displayMgr.print_schedule_as_table(population.get_schedules()[0])
endtime = time.time()
print("\n\n")

print("Runtime = " + str(endtime - starttime))
print("\n\n")


