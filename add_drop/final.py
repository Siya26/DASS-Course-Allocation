import csv
from collections import defaultdict

final_cycles = []
students = []
prev_course = []

class Graph:
    def __init__(self,vertices):
        self.array = {}                     # array to store weights of edges between vertices u and v
        self.graph = defaultdict(list)      # keys = nodes, values = list of neighbours and weights of edges
        self.V = vertices                   # no of vertices = no of courses + no of students

    # adds the edge betweeen u and v
    def addEdge(self, u, v, w):
        self.graph[u].append([v,w])     # v = neighbour of u
        self.array[(u,v)] = w           # w = weight of edge =(u, v)
    
    # removes the edge between u and v
    def removeEdge(self,u,v):
        copy = list(self.graph[u])
        for i, (vertex, w) in enumerate(copy):
            if vertex == v:
                del copy[i]
                break

        self.graph[u] = copy

    # function to print graph
    def printGraph(self):
        for node in self.graph:
            for i in range(len(self.graph[node])):
                print("attached node , weight",self.graph[node][i][0],self.graph[node][i][1])

    # function to output the allocated students
    def allocateStudents(self):
        allocation = []
        allocated_students = []
        allocation.append(["Student Name","Allocated Course"])
        for cycle in final_cycles:
            
            if(cycle[0] not in students):
                cycle.append(cycle.pop(0))
            for i in range(0,len(cycle),2):
                allocated_students.append(cycle[i])         # allocated_students is the list of students who have been 
                allocation.append([cycle[i],cycle[i+1]])    # allocated a new course in add/drop
       
        result = [x for x in students if x not in allocated_students]   # result is the list of students who haven't been
                                                                        # allocated any course during add/drop
        newAllocation=self.allocateUncycles(result)
        
        with open('allocated_add_drop.csv',"w") as fd1:

            writer = csv.writer(fd1)
            writer.writerows(allocation)                     # allocation is the list of courses allocated to students in add/drop
            writer.writerows(newAllocation)

    # function to allocate non-overbooked courses
    def allocateUncycles(self,array):
        newAllocation = []  # list to store allocated non-overbooked courses
        unAllocated =[]     # list to store courses which don't change during add/drop
        left_seats = {}     # dictionary to store the number of seats left in each course
        for key in seats.keys() & allocated_seats.keys():
            left_seats[key] = seats[key] - allocated_seats[key]
        
        for x in array:
            flag=0
            for y in preferences[x]:    # if course y is in preferences of x
                if(left_seats[y]):      # and if seats are left in course y
                    flag=1
                    newAllocation.append([x,y]) 
                    left_seats[y] -=1   # decrease the no. of remaining seats of the added course by 1
                    left_seats[prev_course[students.index(x)]] +=1       # increase the no. of remaining seats of the dropped course by 1
                    break
            if(flag==0):
                unAllocated.append([x,prev_course[students.index(x)]])  # allocated course does not change

        return newAllocation+unAllocated
           
    
    def dfs(self, node, visited, stack, cycles):
        visited[node] = True
        stack.append(node)      
        for neighbor in self.graph[node]:
            if neighbor[0] in stack:
                cycle = stack[stack.index(neighbor[0]):]    # cycle has been found
                cycles.append(cycle)
            elif not visited[neighbor[0]]:
                self.dfs(neighbor[0], visited, stack, cycles)
        stack.pop()

    # function to find ALL the cycles present in the graph 
    def find_cycles(self):
        visited = defaultdict(lambda: False)    # dict to keep track of visited nodes
        stack = []
        cycles = []                             # cycles is the list of ALL the cycles in the graph
        for node in list(self.graph.keys()):
            if not visited[node]:
                self.dfs(node, visited, stack, cycles)
        return cycles
    
    # function to find disjoint cycles
    def findDisjointCycles(self,cycles,disjoint_edges):
        
        disjoint_cycles = []
        for sublist in cycles:
            duplicated_sublist = sublist.copy()
            disjoint_cycles.append(duplicated_sublist)
       
        for cycle in cycles:
            length = len(cycle)
            
            for i in range(1,length):
                if((cycle[i-1],cycle[i]) in disjoint_edges) :
                    disjoint_cycles.remove(cycle)       # removing the set of cycles with common edges
                    break
            
            if(cycle in disjoint_cycles):
                if((cycle[length-1],cycle[0]) in disjoint_edges) :
                    disjoint_cycles.remove(cycle)
            
        return disjoint_cycles

    # function to allocate courses to students
    def allocate_Cycle(self,cycles):
        while (cycles is not None and len(cycles)):
            cycle = cycles[0]                           # cycle = first cycle in the list
            edges = []
            length = len(cycle)

            for i in range(1,length):
                edges.append((cycle[i-1],cycle[i]))     # edges is the list of edges present cycle
                g.removeEdge(cycle[i-1],cycle[i])       # remove the edge between the corresponding vertices
                g.array[(cycle[i-1],cycle[i])]=0        # making the weight between the corresponding vertices = 0

            edges.append((cycle[length-1],cycle[0]))
            g.removeEdge(cycle[length-1],cycle[0])

            cycles.remove(cycle)                        # remove this cycle from the list of cycles
    
            final_cycles.append(cycle)                 # final_cycles is the list of cycles that are used for allocation
            cycles = g.findDisjointCycles(cycles,edges) #find disjoint cycles
    
    # function to detect deadlocks
    def checkCycles(self):

        checkWeight = 1
        while checkWeight <= self.V:

            cycles_initial = g.find_cycles()
            if(len(cycles_initial)==0):     # there are no cycles in the graph
                break
           
            cycles=[]
            for path in cycles_initial:
                length = len(path)          # length of path/cycle
                flag=0
                for i in range(1,length):
                    if(self.array[(path[i-1],path[i])] <= checkWeight):
                        continue
                    else:
                        flag=1
                        break
                
                if(flag==0):
                    if(self.array[(path[length-1],path[0])]<=checkWeight):
                       cycles.append(path)      # cycles is the list of cycles whose 
                                                # edges are of the preference order = checkWeight
            
            if(len(cycles)):
                cycles.sort(key=len,reverse=True)   # sorting the list of cycles in decreasing order
                g.allocate_Cycle(cycles)            # to maximise the satisfaction level of students


            checkWeight+=1                          # increasing the weight of every edge

students = []
cols = 0
seats = {}
allocated_seats={}      # dictionary which stores previously allocated courses
# courses.csv contains the details of courses
preferences = {}
with open("./courses.csv", "r") as f:
    csv_reader = csv.DictReader(f)
    cols = len(list(csv_reader))
    f.seek(0)
    count = 0
    for line in csv_reader:
        if count == 0:
            count += 1
            continue
        
        seats[line['Course Code']] = int(line['Seats'])     # dictionary to store the course limit
        allocated_seats[line['Course Code']] = 0
        
# preferences_add_drop.csv contains the details of preferences of students for add/drop 
with open("./preferences_add_drop.csv", "r") as fd:
    reader = csv.DictReader(fd)
    rows = len(list(reader))
    fd.seek(0)
    column_names = next(reader)
    heading = []
    for name in column_names:
        heading.append(name)
    length = len(heading)
    g = Graph(rows+cols)
    for line in reader:
        
        students.append(line[heading[0]])
        allocated_seats[line[heading[3]]] += 1
        prev_course.append(line[heading[3]])
        preference = []
        g.addEdge(line[heading[3]], line[heading[0]], 0)
        for i in range(4, length):
            if(line[heading[i]]):
                preference.append(line[heading[i]])
                g.addEdge(line[heading[0]], line[heading[i]], i-3)
        preferences[line[heading[0]]] = preference

    # g.printGraph()
    g.checkCycles()     
    g.allocateStudents()


        
    