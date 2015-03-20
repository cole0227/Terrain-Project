# -*- coding: cp1252 -*-
import random

## {{{ http://code.activestate.com/recipes/81611/ (r2)
def int_to_roman(input):
   if type(input) != type(1):
      raise TypeError, "expected integer, got %s" % type(input)
   if not 0 < input < 4000:
      raise ValueError, "Argument must be between 1 and 3999"   
   ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
   nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')
   result = ""
   for i in range(len(ints)):
      count = int(input / ints[i])
      result += nums[i] * count
      input -= ints[i] * count
   return result



def roman_to_int(input):
   if type(input) != type(""):
      raise TypeError, "expected string, got %s" % type(input)
   input = input.upper()
   nums = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
   ints = [1000, 500, 100, 50,  10,  5,   1]
   places = []
   for c in input:
      if not c in nums:
         raise ValueError, "input is not a valid roman numeral: %s" % input
   for i in range(len(input)):
      c = input[i]
      value = ints[nums.index(c)]
      # If the next place holds a larger number, this value is negative.
      try:
         nextvalue = ints[nums.index(input[i +1])]
         if nextvalue > value:
            value *= -1
      except IndexError:
         # there is no next place.
         pass
      places.append(value)
   sum = 0
   for n in places: sum += n
   # Easiest test for validity...
   if int_to_roman(sum) == input:
      return sum
   else:
      raise ValueError, 'input is not a valid roman numeral: %s' % input
## end of http://code.activestate.com/recipes/81611/ }}}

ShipNames = ["New York", "Los Angeles", "Chicago", "Houston", "Philadelphia", "Phoenix", "San Antonio", "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Indianapolis", "San Francisco", "Columbus", "Fort Worth", "Charlotte", "Detroit", "El Paso", "Memphis", "Boston", "Seattle", "Denver", "Washington", "Nashville", "Baltimore", "Louisville", "Portland", "Oklahoma City", "Milwaukee", "Las Vegas", "Albuquerque", "Tucson", "Fresno", "Sacramento", "Long Beach", "Kansas City", "Mesa", "Virginia Beach", "Atlanta", "Colorado Springs", "Raleigh", "Omaha", "Miami", "Oakland", "Tulsa", "Minneapolis", "Cleveland", "Wichita", "Arlington", "New Orleans", "Bakersfield", "Tampa", "Honolulu", "Anaheim", "Aurora", "Santa Ana", "St. Louis", "Riverside", "Corpus Christi", "Pittsburgh", "Lexington", "Anchorage", "Stockton", "Cincinnati", "Saint Paul", "Toledo", "Newark", "Greensboro", "Plano", "Henderson", "Lincoln", "Buffalo", "Fort Wayne", "Jersey City", "Chula Vista", "Orlando", "St. Petersburg", "Norfolk", "Chandler", "Laredo", "Madison", "Durham", "Lubbock", "Winston–Salem", "Garland", "Glendale", "Hialeah", "Reno", "Baton Rouge", "Irvine", "Chesapeake", "Irving", "Scottsdale", "North Las Vegas", "Fremont", "Gilbert", "San Bernardino", "Boise", "Birmingham", "Rochester", "Richmond", "Spokane", "Des Moines", "Montgomery", "Modesto", "Fayetteville", "Tacoma", "Shreveport", "Fontana", "Oxnard", "Aurora", "Moreno Valley", "Akron", "Yonkers", "Columbus", "Augusta", "Little Rock", "Amarillo", "Mobile", "Huntington Beach", "Glendale", "Grand Rapids", "Salt Lake City", "Tallahassee", "Huntsville", "Worcester", "Knoxville", "Grand Prairie", "Newport News", "Brownsville", "Santa Clarita", "Overland Park", "Providence", "Jackson", "Garden Grove", "Oceanside", "Chattanooga", "Fort Lauderdale", "Rancho Cucamonga", "Santa Rosa", "Port St. Lucie", "Ontario", "Tempe", "Vancouver", "Springfield", "Cape Coral", "Pembroke Pines", "Sioux Falls", "Peoria", "Lancaster", "Elk Grove", "Corona", "Eugene", "Salem", "Palmdale", "Salinas", "Springfield", "Pasadena", "Rockford", "Pomona", "Hayward", "Fort Collins", "Joliet", "Escondido", "Kansas City", "Torrance", "Bridgeport", "Alexandria", "Sunnyvale", "Cary", "Lakewood", "Hollywood", "Paterson", "Syracuse", "Naperville", "McKinney", "Mesquite", "Clarksville", "Savannah", "Dayton", "Orange", "Fullerton", "Pasadena", "Hampton", "McAllen", "Killeen", "Warren", "West Valley City", "Columbia", "New Haven", "Sterling Heights", "Olathe", "Miramar", "Thousand Oaks", "Frisco", "Cedar Rapids", "Topeka", "Visalia", "Waco", "Elizabeth", "Bellevue", "Gainesville", "Simi Valley", "Charleston", "Carrollton", "Coral Springs", "Stamford", "Hartford", "Concord", "Roseville", "Thornton", "Kent", "Lafayette", "Surprise", "Denton", "Victorville", "Evansville", "Midland", "Santa Clara", "Athens", "Allentown", "Abilene", "Beaumont", "Vallejo", "Independence", "Springfield", "Ann Arbor", "Provo", "Peoria", "Norman", "Berkeley", "El Monte", "Murfreesboro", "Lansing", "Columbia", "Downey", "Costa Mesa", "Inglewood", "Miami Gardens", "Manchester", "Elgin", "Wilmington", "Waterbury", "Fargo", "Arvada", "Carlsbad", "Westminster", "Rochester", "Gresham", "Clearwater", "Lowell", "West Jordan", "Pueblo", "San Buenaventura (Ventura)", "Fairfield", "West Covina", "Billings", "Murrieta", "High Point", "Round Rock", "Richmond", "Cambridge", "Norwalk", "Odessa", "Antioch", "Temecula", "Green Bay", "Everett", "Wichita Falls", "Burbank", "Palm Bay", "Centennial", "Daly City", "Richardson", "Pompano Beach", "Broken Arrow", "North Charleston", "West Palm Beach", "Boulder", "Rialto", "Santa Maria", "El Cajon", "Davenport", "Erie", "Las Cruces", "South Bend", "Flint", "Kenosha"]

def GetName():

    
    name = ''.join(["USS ",random.choice(ShipNames)])
    
    if (random.random()>0.5):

       name = ''.join([name," ",int_to_roman(int(random.triangular(2,8,2)))])

    return name



class Ship:

    '''
    Health = 43*bulk + 29*toughness
    Energy = 13*Cores + 5 * Grace
    attack = cores*3+grace
    Armour = 5*Toughness + 2*Bulk
    Block = 3*toughness + 2*bulk
    block_chance = 0.3*toughness+0.5*grace+0.1*cores
    '''

    name = "USS Enterprise"
    health = 34
    energy = 21
    attack = 1
    penetration = 1
    armour = 2
    block = 2
    block_chance = 2
    death = 1
    
    Attribute_Bulk = 1
    Attribute_Toughness = 1
    Attribute_Grace = 1
    Attribute_Cores = 1
    Attribute_Growth_Bulk = 1
    Attribute_Growth_Toughness = 1
    Attribute_Growth_Grace = 1
    Attribute_Growth_Cores = 1
    Attribute_Level = 1

    def __init__(self,level):
        self.name = GetName()
        
        self.Attribute_Level = level
        self.Attribute_Growth_Bulk = random.triangular(1,4,2)
        self.Attribute_Growth_Toughness = random.triangular(1,4,2)
        self.Attribute_Growth_Grace = random.triangular(1,4,2)
        self.Attribute_Growth_Cores = random.triangular(1,4,2)
        self.Attribute_Bulk = random.randint(10,30) + int(self.Attribute_Level*self.Attribute_Growth_Bulk)
        self.Attribute_Toughness = random.randint(10,30) + int(self.Attribute_Level*self.Attribute_Growth_Toughness)
        self.Attribute_Grace = random.randint(10,30) + int(self.Attribute_Level*self.Attribute_Growth_Grace)
        self.Attribute_Cores = random.randint(10,30) + int(self.Attribute_Level*self.Attribute_Growth_Cores)

        self.health = 43 * self.Attribute_Bulk + 29 * self.Attribute_Toughness
        self.energy = 13 * self.Attribute_Cores + 5 * self.Attribute_Grace
        self.attack = 4 * self.Attribute_Cores + self.Attribute_Grace
        self.penetration = 2 * self.Attribute_Cores + self.Attribute_Grace
        self.armour = 7 * self.Attribute_Toughness + 2 * self.Attribute_Bulk
        self.block = 3 * self.Attribute_Toughness + 1 * self.Attribute_Bulk
        self.block_chance = int(0.1 * self.Attribute_Toughness + 0.2 * self.Attribute_Grace + 0.03 * self.Attribute_Cores)
        
        self.death = self.attack - (self.block-self.penetration)*self.block_chance/100
        self.death = self.death * (1 - self.armour**0.5 / 100)
        self.death = self.health/self.death
        
    def __str__(self):
        return ''.join([
            self.name,
            "\n==========================",
            "\nLevel:\t\t",str(self.Attribute_Level),
            "\n--------------------------",
            "\nBulk:\t\t",      str(self.Attribute_Bulk),"(+",       str(int(100*self.Attribute_Growth_Bulk)/100.0),")",
            "\nToughness:\t",   str(self.Attribute_Toughness),"(+",  str(int(100*self.Attribute_Growth_Toughness)/100.0),")",
            "\nGrace:\t\t",     str(self.Attribute_Grace),"(+",      str(int(100*self.Attribute_Growth_Grace)/100.0),")",
            "\nCores:\t\t",     str(self.Attribute_Cores),"(+",      str(int(100*self.Attribute_Growth_Cores)/100.0),")",
            "\n--------------------------",
            "\nHealth:\t\t",str(self.health),
            "\nEnergy:\t\t",str(self.energy),
            "\nAttack:\t\t",str(self.attack),"-",str(self.penetration),
            "\nArmour:\t\t",str(self.armour),"-",str(int(self.armour**0.5)),"%",
            "\nBlock:\t\t",str(self.block),"-",str(self.block_chance),"%",
            "\n--------------------------",
            "\nKills Self in: ",str(int(self.death))," attacks",
            "\n==========================",
            "\n"])


for x in range(42):

    y=Ship(int(random.triangular(1,50,25)))
    print y


    



























