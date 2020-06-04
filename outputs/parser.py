class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.id_token = 0
		self.actual_token = self.tokens[self.id_token]
		self.last_token = ''
		#self.advance()

	def advance( self ):
		self.id_token += 1
		if self.id_token < len(self.tokens):
			self.actual_token = self.tokens[self.id_token]
			self.last_token = self.tokens[self.id_token - 1]

	def expect(self, item):
		og = self.id_token
		possible = False
		if item != None:
			try:
				item
				possible = True
			except:
				possible = False
		self.id_token = og
		self.actual_token = self.tokens[self.id_token]
		self.last_token = self.tokens[self.id_token - 1]
		return possible

	def read(self, item, type = False):
		if type:
			if self.actual_token.type == item:
				self.advance()
			#else:
				#print('expected ', item, ' got ', self.actual_token.type)
		else:
			if self.actual_token.value == item:
				self.advance()
			#else:
				#print('expected ', item, ' got ', self.actual_token.value)
	value, result, value1, value2 = 0,0,0,0
	def Expr(self):
		while self.expect(self.Stat()):
			self.Stat()
			self.read(";")
		self.read(".")

	def Stat(self):
		value=0
		self.Expression(value)
		print(str(value))

	def Expression(self,result):
		result1,result2=0,0
		self.Term(result1)
		while self.expect(self.read("+")) or self.expect(self.read("-")):
			if self.expect(self.read("+")):	
				self.read("+")
				self.Term(result2)
				result1+=result2
	
			elif self.expect(self.read("-")):
				self.read("-")
				self.Term(result2)
				result1-=result2
		result=result1

	def Term(self,result):
		result1,result2=0,0
		self.Factor(result1)
		while self.expect(self.read("*")) or self.expect(self.read("/")):
			if self.expect(self.read("*")):	
				self.read("*")
				self.Factor(result2)
				result1*=result2
	
			elif self.expect(self.read("/")):
				self.read("/")
				self.Factor(result2)
				result1/=result2
		result=result1

	def Factor(self,result):
		signo=1
		if self.expect(self.read('-')):
			self.read("-")
			signo=-1
		if self.expect(self.Number(result)):
			self.Number(result)
			
		elif self.expect(self.read("(")):
			self.read("(")
			self.Expression(result)
			self.read(")")
		result*=signo

	def Number(self,result):
		self.read('number', True)
		result=int(self.last_token.value)

