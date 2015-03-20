import random
import sys
from operator import itemgetter

class NullWriter(object):
	def write(self, arg):
		pass
oldstdout = sys.stdout
sys.stdout = NullWriter() # disable output
execfile("rpg lists and generators.py")
sys.stdout = oldstdout # enable output

'''
Some form of automatic writing
-each character has a map of character relations for all characters.
	100 or greater is love
	80 or greater is respect/friend
	60 or greater is like
	40 or greater is neutral
	20 or greater is dislike
	0 or more is dispise
	0 or less is hate
-each character has stats determining:
	-how close someone has to be to them for them to kill for that person
	-and how much they have to dislike someone in order to want that person dead
	-how likely they are to invite people over on their turn
	-how many people they invite
	-how likely they are to accept invites for each level of relations
	-how much reputation they assign to killing, insulting, kindness for each level of relations
	-a list of people they will not kill (i.e. family in game of thrones)
	-likelyhood of writing/telling/visiting to another player for each level of relations
	-how likely it is that they believe player writing/visiting/telling for each level of relations
-there is also a sense of spaces.
	-on each player's turn may write/visit another player, telling them of the actions they witnessed during any scene since their last turn.
	-every character has a home. they invite people they like into their homes on their turn for a scene. homes exist in cities, limiting their invitations to those who live in that city
	-at a scene, each player may insult or be kind towards each other person, or tell them about a previous scene they were in where the other was not present
	-at a scene, each player may kill another player, removing them from the game
-people only react the events they know of
-
'''

ActorList = []
PositionThreshold = [100,80,60,40,20,0]
PositionThresholdTitles = ["Love","Respect","Like","Neutral","Dislike","Dispise","Hate"]
TodayDate="the first of frostivus"

class RelationChart(object):

	def __init__(self,actors,index):

		self.m_size  =  len(actors)
		self.m_index = index
		self.m_chart = [[-10000 for x in xrange(self.m_size)] for x in xrange(self.m_size)] 

		for x in range(0,self.m_size):
			for y in range(0,self.m_size):
				self.m_chart[x][y] = random.randint(41,59)

	def get(self,x,y):

		return self.m_chart[x][y]

	def set(self,x,y,val):

		self.m_chart[x][y] = val

	def adjust(self,x,y,val):

		self.m_chart[x][y] += val

	def hated(self):
		
		return min(enumerate(self.m_chart[self.m_index]), key=itemgetter(1))[0]

	def min(self):

		return min(self.m_chart[self.m_index])

class Actor(object):

	def __init__(self,name,actors):

		self.m_actionThresholds = {"kill":20,"kill_for":90,"tell":50,"want_dead":25,"reveal_want_dead":75}
		self.m_reactionThresholds = {"kill":(0,-5,-15,-15,-20,-20,-22),"want_dead":(0,-2,-5,-5,-10,-10,-12),"tell":(0,+2,+2,+2,-2,-2,-4),"compliment":(0,+3,+2,+2,+1,+1,+1),"insult":(0,-6,-6,-6,-7,-8,-10)}
		self.m_name = name
		self.m_chartIndex = len(actors)
		self.m_chart = RelationChart(actors,self.m_chartIndex)
		self.m_events = []
		self.m_alive = True

	def n(self):

		return self.m_chartIndex

	def genChart(self,actors):

		self.m_chart = RelationChart(actors,self.m_chartIndex)
		self.m_chart.set(self.m_chartIndex,self.m_chartIndex,110)

	def genReaction(self,action,actorIndex):

		val = self.m_chart.get(self.m_chartIndex,actorIndex)
		n = len(PositionThreshold)-1
		for i in range(0,len(PositionThreshold)-1):
			if(val > PositionThreshold[i]):
				n = i
				break
		if(self.m_chartIndex != actorIndex):
			print "\t\t",self.m_name,"feels",PositionThresholdTitles[n],"["+str(val)+"] towards",ActorList[actorIndex].m_name,"before his",action,"["+str(self.m_reactionThresholds[action][n])+"]"
		return self.m_reactionThresholds[action][n]

	def getOpinion(self,a):

		return self.m_chart.get(self.m_chartIndex,a)

	def findMostHated(self,actorsInScene):

		self.m_chart[self.m_chartIndex]
		actorsHatred = []
		for a in actorsInScene:
			actorsHatred = self.m_chart[self.m_chartIndex][a]
		return min(enumerate(actorsHatred), key=itemgetter(1))[0]


	def makeEvent(self,actorsInScene):

		hate = self.findMostHated(actorsInScene)
		
		if(self.getOpinion(hate) < self.m_actionThresholds["kill"]):
			print "somebody is killable!"


	def witness(self, event):
		if(self.m_alive and not(event in self.m_events)):
			self.m_events.append(event)

			if(type(event) == Event_Kill):
				r = self.genReaction("kill",event.perp)
				self.m_chart.adjust(event.perp,event.target,r)
				self.m_chart.adjust(self.m_chartIndex,event.perp,r)
				if(event.target == self.m_chartIndex):
					self.m_chart.adjust(event.perp,event.target,-50)
					self.m_alive = False

			if(type(event) == Event_Tell):
				r = self.genReaction("tell",event.perp)
				self.m_chart.adjust(event.perp,event.target,r)
				self.m_chart.adjust(self.m_chartIndex,event.perp,r)
				
				if(event.event != None and self.m_chartIndex == event.target):
					self.witness(event.event)

			if(type(event) == Event_Want_Dead):
				r = self.genReaction("want_dead",event.perp)
				self.m_chart.adjust(event.perp,event.target,r)
				self.m_chart.adjust(self.m_chartIndex,event.perp,r)
				if(event.target == self):
					self.m_chart.adjust(event.perp,event.target,r)
					self.m_chart.adjust(self.m_chartIndex,event.perp,r)

			if(type(event) == Event_Insult):
				r = self.genReaction("insult",event.perp)
				self.m_chart.adjust(event.perp,event.target,r)
				self.m_chart.adjust(self.m_chartIndex,event.perp,r)
				if(event.target == self):
					self.m_chart.adjust(self.m_chartIndex,event.perp,r)

			if(type(event) == Event_Compliment):
				r = self.genReaction("compliment",event.perp)
				self.m_chart.adjust(event.perp,event.target,r)
				self.m_chart.adjust(self.m_chartIndex,event.perp,r)
				if(event.target == self):
					self.m_chart.adjust(self.m_chartIndex,event.perp,r)


	def clearEvents(self):

		self.m_events = [];

	def randomEvent(self):

		if(len(self.m_events) > 0):
			return random.choice(self.m_events)
		else:
			return None

	def __str__(self):

		return str(self.m_name) + str(self.m_chart.m_chart)

class Event(object):

	def __init__(self,description,perp,target,date):

		self.description = description
		self.perp = perp
		self.target = target
		self.date=date

class Event_Insult(Event):

	pass

class Event_Compliment(Event):

	pass

class Event_Kill(Event):

	pass

class Event_Want_Dead(Event):

	pass

class Event_Tell(Event):

	def __init__(self,description,perp,target,date,event):

		Event.__init__(self,description,perp,target,date)
		self.event = event


for i in range(0,20):
	ActorList.append(Actor(firstNames[random.randint(1,len(firstNames))-1],ActorList))

for a in ActorList:
	a.genChart(ActorList)

for i in range(0,100):

	#print out every'body's least fav person
	for a in ActorList:
		if(a.m_alive):
			val = a.m_chart.min()
			n = len(PositionThreshold)-1
			for i in range(0,len(PositionThreshold)-1):
				if(val > PositionThreshold[i]):
					n = i
					break

			print a.m_name, PositionThresholdTitles[n], ActorList[a.m_chart.hated()].m_name,"[",a.m_chart.min(),"]"
		else:
			print a.m_name, "has died."
	print
	# turn order
	for a in (a for a in ActorList if a.m_alive):
		t = ActorList[random.randint(0,len(ActorList)-1)]
		if(a != t and t.m_alive):
			print
			print a.m_name+"'s Turn:"

			if(random.random() < 0.1 and a.getOpinion(t.n()) < PositionThreshold[len(PositionThreshold)-2]):
			
				e = Event_Kill(random.choice(("kills","slays","poisons")),a.n(),t.n(),TodayDate)
				ActorList[random.randint(0,len(ActorList)-1)].witness(e)
				ActorList[random.randint(0,len(ActorList)-1)].witness(e)
				a.witness(e)
				t.witness(e)

				print
				print a.m_name,e.description,t.m_name
		
			elif(random.random() < 0.3):

				e = Event_Compliment(random.choice(("compliments","eats with","drinks with")),a.n(),t.n(),TodayDate)
				ActorList[random.randint(0,len(ActorList)-1)].witness(e)
				ActorList[random.randint(0,len(ActorList)-1)].witness(e)
				ActorList[random.randint(0,len(ActorList)-1)].witness(e)
				a.witness(e)
				t.witness(e)

				print
				print a.m_name,e.description,t.m_name

			elif(random.random() < 0.3 and a.getOpinion(t.n()) < PositionThreshold[len(PositionThreshold)-4]):

				e = Event_Insult(random.choice(("insults","bullies","ignores")),a.n(),t.n(),TodayDate)
				ActorList[random.randint(0,len(ActorList)-1)].witness(e)
				ActorList[random.randint(0,len(ActorList)-1)].witness(e)
				ActorList[random.randint(0,len(ActorList)-1)].witness(e)
				a.witness(e)
				t.witness(e)

				print
				print a.m_name,e.description,t.m_name
	
			elif(random.random() < 0.5 and a.getOpinion(t.n()) < PositionThreshold[len(PositionThreshold)-3]):

				e = Event_Want_Dead("wanting to kill",a.n(),t.n(),TodayDate)
				ActorList[random.randint(0,len(ActorList)-1)].witness(e)
				ActorList[random.randint(0,len(ActorList)-1)].witness(e)
				a.witness(e)

				print
				print a.m_name,"wants",t.m_name,"to die"

			else:
				e2 = a.randomEvent()
				if(e2 != None):
				
					e = Event_Tell(random.choice(("visits","writes","tells")),a.n(),t.n(),TodayDate,e2)
					a.witness(e)
					t.witness(e)

					print
					print a.m_name,e.description,t.m_name,"about when",ActorList[e2.perp].m_name,e2.description,ActorList[e2.target].m_name
					while(type(e2) == Event_Tell):
						e2 = e2.event
						print t.m_name,"learned about",ActorList[e2.perp].m_name,e2.description,ActorList[e2.target].m_name
						a.witness(e)

				else:
					print
					print "Nothing Happened"



