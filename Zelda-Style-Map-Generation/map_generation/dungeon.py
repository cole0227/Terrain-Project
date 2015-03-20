import profile
import random
import copy
import itertools
import sys


def _AStar(start, goal):
    def heuristic(a, b):
        ax, ay = a
        bx, by = b
        return abs(ax - bx) + abs(ay - by)

    def reconstructPath(n):
        if n == start:
            return [n]
        return reconstructPath(cameFrom[n]) + [n]

    def neighbors(n):
        x, y = n
        return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)

    closed = set()
    open = set()
    open.add(start)
    cameFrom = {}
    gScore = {start: 0}
    fScore = {start: heuristic(start, goal)}

    while open:
        current = None
        for i in open:
            if current is None or fScore[i] < fScore[current]:
                current = i

        if current == goal:
            return reconstructPath(goal)

        open.remove(current)
        closed.add(current)

        for neighbor in neighbors(current):
            if neighbor in closed:
                continue
            g = gScore[current] + 1

            if neighbor not in open or g < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = g
                fScore[neighbor] = gScore[neighbor] + heuristic(neighbor, goal)
                if neighbor not in open:
                    open.add(neighbor)
    return ()


def generate(cellsX, cellsY, cellSize=8, rounded=False):
    # 1. Divide the map into a grid of evenly sized cells.

    class Cell(object):
        def __init__(self, x, y, id):
            self.x = x
            self.y = y
            self.id = id
            self.connected = False
            self.connectedTo = []
            self.room = None

        def connect(self, other):
            self.connectedTo.append(other)
            other.connectedTo.append(self)
            self.connected = True
            other.connected = True

    cells = {}
    for y in range(cellsY):
        for x in range(cellsX):
            c = Cell(x, y, len(cells))
            cells[(c.x, c.y)] = c

    # 2. Pick a random cell as the current cell and mark it as connected.
    current = lastCell = firstCell = random.choice(cells.values())
    current.connected = True

    # 3. While the current cell has unconnected neighbor cells:
    def getNeighborCells(cell):
        for x, y in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            try:
                yield cells[(cell.x + x, cell.y + y)]
            except KeyError:
                continue

    while True:
        unconnected = filter(lambda x: not x.connected, getNeighborCells(current))
        if not unconnected:
            break

        # 3a. Connect to one of them.
        neighbor = random.choice(unconnected)
        current.connect(neighbor)

        # 3b. Make that cell the current cell.
        current = lastCell = neighbor

    # 4. While there are unconnected cells:
    while filter(lambda x: not x.connected, cells.values()):
        # 4a. Pick a random connected cell with unconnected neighbors and connect to one of them.
        candidates = []
        for cell in filter(lambda x: x.connected, cells.values()):
            neighbors = filter(lambda x: not x.connected, getNeighborCells(cell))
            if not neighbors:
                continue
            candidates.append((cell, neighbors))
        cell, neighbors = random.choice(candidates)
        cell.connect(random.choice(neighbors))

    # 5. Pick 0 or more pairs of adjacent cells that are not connected and connect them.
    extraConnections = random.randint((cellsX + cellsY) / 4, int((cellsX + cellsY) / 1.2))
    maxRetries = 10
    while extraConnections > 0 and maxRetries > 0:
        cell = random.choice(cells.values())
        neighbor = random.choice(list(getNeighborCells(cell)))
        if cell in neighbor.connectedTo:
            maxRetries -= 1
            continue
        cell.connect(neighbor)
        extraConnections -= 1

    # 6. Within each cell, create a room of random shape
    rooms = []
    for cell in cells.values():
        width = random.randint(3, cellSize - 2)
        height = random.randint(3, cellSize - 2)
        x = (cell.x * cellSize) + random.randint(1, cellSize - width - 1)
        y = (cell.y * cellSize) + random.randint(1, cellSize - height - 1)
        floorTiles = []
        if(rounded):
            for i in range(width):
                for j in range(height):

                    # ignore the corners
                    if(not(i+j==0 or (i==0 and j == width-1) or (i == width-1 and j==0) or (i+j == width*2-2))):

                        floorTiles.append((x + i, y + j))
        else:
            for i in range(width):
                for j in range(height):
                    floorTiles.append((x + i, y + j))

        cell.room = floorTiles
        rooms.append(floorTiles)

    # 7. For each connection between two cells:
    connections = {}
    for c in cells.values():
        for other in c.connectedTo:
            connections[tuple(sorted((c.id, other.id)))] = (c.room, other.room)
    for a, b in connections.values():
        # 7a. Create a random corridor between the rooms in each cell.
        start = random.choice(a)
        end = random.choice(b)

        corridor = []
        for tile in _AStar(start, end):
            if tile not in a and not tile in b:
                corridor.append(tile)
        rooms.append(corridor)

    # 8. Place staircases in the cell picked in step 2 and the lest cell visited in step 3b.
    stairsUp = random.choice(firstCell.room)
    stairsDown = random.choice(lastCell.room)

    # create tiles
    tiles = {}
    tilesX = cellsX * cellSize
    tilesY = cellsY * cellSize
    for x in range(tilesX):
        for y in range(tilesY):
            tiles[(x, y)] = "#"
    for xy in itertools.chain.from_iterable(rooms):
        tiles[xy] = "."

    # every tile adjacent to a floor is a wall
    def getNeighborTiles(xy):
        tx, ty = xy
        for x, y in ((-1, -1), (0, -1), (1, -1),
                     (-1, 0),           (1, 0),
                     (-1, 1),  (0, 1),  (1, 1)):
            try:
                yield tiles[(tx + x, ty + y)]
            except KeyError:
                continue

    for xy, tile in tiles.iteritems():
        if not tile == "." and "." in getNeighborTiles(xy):
            tiles[xy] = "#"
    tiles[stairsUp] = "<"
    tiles[stairsDown] = ">"

    for y in range(tilesY):
        for x in range(tilesX):
            pass
            #sys.stdout.write(tiles[(x, y)])
            #sys.stdout.write("\n")

    def get_map():
           return tiles

    return tiles

# Jason's Hacks begin here:

def dungeon_print(tiles, cellsX, cellsY=-1, cellSize=8):

    if(cellsY==-1):
        cellsY = cellsX

    for y in range(cellsY*cellSize):
        for x in range(cellsX*cellSize):
            sys.stdout.write(tiles[(x,y)])
        sys.stdout.write("\n")

    cellsY=-1

def dungeon_print_delta(tiles, tiles2, cellsX, cellsY=-1, cellSize=8):

    if(cellsY==-1):
        cellsY = cellsX

    for y in range(cellsY*cellSize):
        for x in range(cellsX*cellSize):
            if(tiles[(x,y)] != tiles2[(x,y)]):
                sys.stdout.write("O")
            else:
                sys.stdout.write(tiles[(x,y)])
        sys.stdout.write("\n")

    cellsY=-1

def round_out_dungeon(inputTiles):

    tiles = copy.deepcopy(inputTiles)

    def getNeighborTiles(xy):
        tx, ty = xy
        for x, y in ((-1, -1), (0, -1), (1, -1),
                     (-1, 0), (1, 0),
                     (-1, 1), (0, 1), (1, 1)):
            try:
                yield tiles[(tx + x, ty + y)]
            except KeyError:
                continue

    def getNeighborSum(xy):

        count = 0
        tx, ty = xy

        for x, y in ((-1, -1), (0, -1), (1, -1),
                     (-1, 0),           (1, 0),
                     (-1, 1),  (0, 1),  (1, 1)):
            try:
                if (tiles[(tx + x, ty + y)] != "#"):
                    count += 1
            except KeyError:
                continue

        return count

    def getNeighborBeside(xy, beside):

        count = 0
        tx, ty = xy

        for x, y in ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0),(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)):
            if(count == beside):
                return True
            try:
                if (tiles[(tx + x, ty + y)] != "#"):
                    count += 1
                else:
                    count = 0
            except KeyError:
                continue

        return False

    for xy, tile in tiles.iteritems():

        c = getNeighborSum(xy)
        nt = getNeighborBeside(xy,3)
        nw = getNeighborBeside(xy,2)
        if tile == "#":
            if c > 4:
                tiles[xy] = "."
            else:
                try:
                    if(tiles[(xy[0]-1,xy[1])]=="." and tiles[(xy[0]+1,xy[1])]==".") or (tiles[(xy[0],xy[1]-1)]=="." and tiles[(xy[0],xy[1]+1)]=="."):
                        tiles[xy] = "."
                except KeyError:
                    continue

        if tile == ".":
            if c == 3 and nt:
                tiles[xy] = "#"
            if c < 3 and nw:
                tiles[xy] = "#"
    return tiles

def dungeon_erode(inputTiles):

    tiles = copy.deepcopy(inputTiles)

    def getNeighborSumInput(xy):

        count = 0
        tx, ty = xy

        for x, y in ((-1, -1), (0, -1), (1, -1),
                     (-1, 0),           (1, 0),
                     (-1, 1),  (0, 1),  (1, 1)):
            try:
                if (inputTiles[(tx + x, ty + y)] != "#"):
                    count += 1
            except KeyError:
                continue

        return count

    maxX = 0
    maxY = 0

    for xy, tile in tiles.iteritems():

        #we need these for calulating edges later
        maxX = max(maxX,xy[0])
        maxY = max(maxY,xy[1])

        c = getNeighborSumInput(xy)

        if tile == "#":
            if c > 2 and xy[0] != 0 and xy[1] != 0:
                tiles[xy] = "."
    
    #re-edge the map
    for x in range(0,maxX+1):
        tiles[(x,maxY)] = "#"
    
    for y in range(0,maxY+1):
        tiles[(maxX,y)] = "#"

    return tiles


def dungeon_make(cellsX, cellsY, chunk_size=8, roundedness=0, erode=0):

    tiles = generate(cellsX, cellsY, chunk_size, roundedness>0)
    for i in range(roundedness):
        tiles = round_out_dungeon(tiles)
    for i in range(erode):
        tiles = dungeon_erode(tiles)
    return tiles

if __name__ == "__main__":
    size = 12
    chunk = 11
    dungeon_print(dungeon_make(size,size,chunk),size,size,chunk)
    #dungeon_print(dungeon_make(size,size,chunk,roundedness=1),size,size,chunk)
    #dungeon_print(dungeon_make(size,size,chunk,roundedness=15),size,size,chunk)
    dungeon_print(dungeon_make(size,size,chunk,roundedness=15,erode=1),size,size,chunk)
