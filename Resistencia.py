class Resistencia:
	def __init__(self,nombre,valor,estado,Xrec,Yrec,enlace1,enlace2):
		self.nombre=nombre
		self.valor=valor
		self.estado=estado
		self.Xrec=Xrec
		self.Yrec=Yrec
		self.enlace1=enlace1
		self.enlace2=enlace2

	def set_nombre(self,nombre):
		self.nombre = nombre
	def get_nombre(self):
		return self.nombre
	
	def set_valor(self,valor):
		self.valor = valor
	def get_valor(self):
		return self.valor
	
	def set_estado(self,estado):
		self.estado = estado
	def get_estado(self):
		return self.estado

	def set_Xrec(self,Xrec):
		self.Xrec =	Xrec
	def get_Xrec(self):
		return self.Xrec

	def set_Yrec(self,Yrec):
		self.Yrec =	Yrec
	def get_Yrec(self):
		return self.Yrec

	def set_enlace1(self,enlace1):
		self.enlace1 = enlace1
	def get_enlace1(self):
		return self.enlace1

	def set_enlace2(self,enlace2):
		self.enlace2 = enlace2
	def get_enlace2(self):
		return self.enlace2