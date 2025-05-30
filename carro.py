import pygame

class carro:
	def __init__(self, origen, destino, ruta):
		self.origen = origen
		self.destino = destino
		self.ruta = ruta
	
	#def EncontrarRuta(self, origen, destino):
	#	print("Temporal EncontrarRuta")
		
	
	def Mover(self, pantalla):
		pygame.draw.circle(pantalla,(0,255,0),(0,0),100)

	#def actualizarPosicion():
	#	print("Temporal actualizarPosicion")