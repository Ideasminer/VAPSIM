class Spot():
    def __init__(self, *args):
        # *args: need at least 2(name, centriod), at most 4(name, centriod, occupy, size)
        # name : ID of the parking spot, int, required
        # centriod : (x, y), tuple, required
        # occupy : 1/0, int, default 0
        # size : (width, height), tuple, default (3.0, 5.0)
        # border : [rt, rb, lb, lt], list, auto generate
        if args:
            if len(args) < 2:
                raise ValueError("Expects at least 2 args: name(int) and centriod(tuple)")
            else:
                self.name = args[0]
                self.centriod = args[1]
                if len(args) == 2:
                    self.occupy = 0
                    self.size = (3.0, 5.0)
                if len(args) == 3:
                    self.occupy = args[2]
                    self.size = (3.0, 5.0)
                if len(args) == 4:
                    self.occupy = args[2]
                    self.size = args[3]
            self.border = self.get_border(self.size)
        else:
            raise ValueError("Need at least 2(name, centriod), at most 4(name, centriod, occupy, size)")

    def get_border(self, size):
        # All the parking spots are located horizontally in stack
        x, y = self.centriod
        width = size[0]
        length = size[1]
        rt = (x + length / 2, y + width / 2)
        rb = (x + length / 2, y - width / 2)
        lb = (x - length / 2, y - width / 2)
        lt = (x - length / 2, y + width / 2)
        return [rt, rb, lb, lt] # rt: right-top, rb: right-bottom, lb: left-bottom, lt: left-top

    def updateOccupy(self, status):
        self.occupy = status

    def __repr__(self):
        return str(self.name)

class Stack(Spot):
    def __init__(self, *args, **kwargs):
        # use args to pass in herit params like name, centriod, occupy and size
        # use kwargs to pass in additional params like spotNum(Xi), direction(+x: 1, -x: 0)
        # Params List:
            # name, int
            # centriod, tuple
            # occupy, int, modified - use inteager to present the number of vehs in the stack
            # size, tuple, present the basic parking spot size, not the size of this stack
            # border, list, auto generate, but modify the params which pass in the get_border function
            # containerNum, int, present how many parking spot in this stack, required
            # direction, int, 1/0, (+x: 1, -x: 0), default 1 (+x)
            # containerList, list of parking spot in this stack, auto generate
        # Expect:
            # args pass in at least 2 params, at most 4, if you do not pass in args, at least use kwargs to give params
            # kwargs need at least spotNum param
        if args:
            super(Stack, self).__init__(*args)
        else:
            if kwargs:
                paramNums = kwargs.keys()
                if "name" in paramNums and "centriod" in paramNums:
                    if "occupy" in paramNums:
                        if "size" in paramNums:
                            super(kwargs.get("name"), kwargs.get("centriod"), kwargs.get("occupy"), kwargs.get("size"))
                        else:
                            super(kwargs.get("name"), kwargs.get("centriod"), kwargs.get("occupy"))
                    else:
                        super(kwargs.get("name"), kwargs.get("centriod"))
                else:
                    raise ValueError("Need name and centriod")
            else:
                raise ValueError("You haven't passed in any kwarg")
        if kwargs:
            paramNums = kwargs.keys()
            if "containerNum" in paramNums:
                self.containerNum = kwargs.get("containerNum")
                if "direction" in paramNums:
                    self.direction = kwargs.get("direction")
                else:
                    self.direction = 1
            else:
                raise ValueError("containerNum is required")
        self.border = self.get_border((self.size[0], self.size[1] * self.containerNum))
        self.containerList = self.auto_generate()
        self.occupy = sum([i.occupy for i in self.containerList])
    
    def auto_generate(self):
        containerList = []
        num = self.containerNum
        size = self.size
        direction = self.direction
        stack_centriod = self.centriod
        if direction: # direction == 1 +x
            start_centriod = (stack_centriod[0] + (float(num) - 1) / 2 * size[1], stack_centriod[1])
        else:
            start_centriod = (stack_centriod[0] - (float(num) - 1) / 2 * size[1], stack_centriod[1])
        for i in range(num):
            name = i
            if direction:
                centriod = (start_centriod[0]- size[1], start_centriod[1])
            else:
                centriod = (start_centriod[0]+ size[1], start_centriod[1])
            size = size
            occupy = 0
            newContainer = Spot(name, centriod, occupy, size)
            containerList.append(newContainer)
        return containerList

    def updateOccupy(self):
        self.occupy = sum([i.occupy for i in self.containerList])

    def __repr__(self):
        return str({
            "name" : self.name,
            "containerNum": self.containerNum,
            "direction": self.direction
        })

class Area(Stack):
    def __init__(self, *args, **kwargs):
        # herit from Stack class
        # addtional param: baseNum (Xi), and use containerNum to present the number of stacks(Yi)
        # use containerList to present the list of stacks
        # use direction to represent : the name rank (from top - bottom or from bottom to top)(1: +y, 0:-y), re-write auto-generate function
        # use stack_direction to represent the stacks' direction
        if "baseNum" in kwargs.keys():
            self.baseNum = kwargs.get("baseNum")
        else:
            raise ValueError("baseNum is required")
        if "stack_direction" in kwargs.keys():
            self.stack_direction = kwargs.get("stack_direction")
        else:
            self.stack_direction = 1
        super(Area, self).__init__(*args, **kwargs)
        self.border = self.get_border((self.size[0] * self.containerNum, self.size[1] * self.baseNum))
        self.containerList = self.auto_generate()
        self.occupy = sum([i.occupy for i in self.containerList])
    
    def auto_generate(self):
        containerList = []
        num = self.containerNum
        size = (self.size[0], self.size[1] * self.baseNum)
        direction = self.direction
        stack_centriod = self.centriod
        if direction: # direction == 1 +y
            start_centriod = (stack_centriod[0], stack_centriod[1] + (float(num) - 1) / 2 * size[0])
        else:
            start_centriod = (stack_centriod[0], stack_centriod[1] - (float(num) - 1) / 2 * size[0])
        for i in range(num):
            name = i
            if direction:
                centriod = (start_centriod[0], start_centriod[1] - size[0])
            else:
                centriod = (start_centriod[0], start_centriod[1] + size[0])
            occupy = 0
            newContainer = Stack(name, centriod, occupy, self.size, direction = self.stack_direction, containerNum = self.baseNum)
            containerList.append(newContainer)
        return containerList

    def __repr__(self):
        return str({
            "name" : self.name,
            "X": self.baseNum,
            "Y": self.containerNum,
            "direction" : self.direction,
            "stack_direction" : self.stack_direction
        })

class Lot():
    def __init__(self, *args):
        # args[0] : parking matrix, dimension: 2, shape:(i, 2) 
            # i refers to the number of parking areas in the lot
            # 2 refers to (j,k)
            # j refers to the number of stacks in the area
            # k refers to the number of spots in the stack
        # args[1] : corridor matrix, dimensions: 2, shape(i - 1, 2)
            # i - 1 refer the number of corridors between the parking areas
            # 2 refers to the Ei and Gi, Ei is the number of lanes for clear-way, Gi is the number of lanes for temp parking way
        # args[2] : in-out param, dimension: 1, number of lanes
        # all params are required
        # auto generate param: occupy
            # occupy : matrix, dimension : 2, shape: (i, j), like [[k1, k2, k3, k4], [k1, k2, k3, k4]]
            # refers to the the number of parking spot occupied
            # initialize with 0
        if args:
            if len(args) != 3:
                raise ValueError("All params are required: parking matrix, corridor matrix and in-out lane number")
            else:
                self.parking, self.corridor, self.outway = args
        else:
            raise ValueError("All params are required: parking matrix, corridor matrix and in-out lane number")
        self.occupy = [[0 for j in range(self.parking[i][0])] for i in range(len(self.parking))]

    def area_generate(self, spot_size, corridor_width, area_direction):
        # initial areaList
        areaList = []
        area_num = len(self.parking)
        parking = self.parking
        for i in range(area_num):
            stack_num = parking[i][0]
            spot_num = parking[i][1]
            name = i
            area_direction = area_direction
            stack_direction = (i + 1) % 2
            if i == 0:
                x = spot_num / 2 * spot_size[1]
                y = stack_num / 2 * spot_size[0]
                centriod = (x, y)
            else:
                start_x = parking[i - 1][1] * spot_size[0] + sum(self.corridor[i - 1]) * corridor_width
                x = spot_num / 2 * spot_size[1] + start_x
                y = stack_num / 2 * spot_size[0]
                centriod = (x, y)
            occupy = 0
            newArea = Area(name, centriod, occupy, spot_size, baseNum = spot_num, containerNum = stack_num, direction = area_direction, stack_direction = stack_direction)
            areaList.append(newArea)
        return areaList

    def updateLot(self, parking, corridor, outway):
        # update facility's decision params
        self.parking, self.corridor, self.outway = parking, corridor, outway

    def assign_demand(self, assign_matrix, areaList):
        self.occupy = assign_matrix
        for i in range(len(self.occupy)):   # Area i
            for j in range(len(self.occupy[i])):         # Stack j in Area i
                stack_occupy = assign_matrix[i][j]
                spotList = areaList[i].containerList[j].containerList
                if stack_occupy > len(spotList):
                    raise ValueError("Wrong assign matrix, value larger than capacity")
                [k_null.updateOccupy(0) for k_null in spotList[:(len(spotList) - stack_occupy)]]
                [k_occu.updateOccupy(1) for k_occu in spotList[(len(spotList) - stack_occupy): ]]
                areaList[i].containerList[j].updateOccupy()
            areaList[i].updateOccupy()
