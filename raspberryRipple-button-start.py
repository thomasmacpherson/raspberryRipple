
#!/usr/bin/env python
"""
whackAMole.py
Simple whack a mole game for use with pfio and the RaspberryPi interface (piface)

Objective of game: A random LED will light up and you must hit the corresponding button as quickly as possible.
The amount of time you have to hit the button will get shorter as the game progresses.
"""
from __future__ import print_function
from time import sleep		# for delays
import random			# for generating the next random button flash

import pifacedigitalio as p	# piface library		


import sys, pygame
#import pipassport

#API_KEY = 'e06c2808-6a3e-45f9-9bec-fd5cfbe6252d'


pygame.init()
size = width,height = 900,700
black = 0,0,0

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
rasp = pygame.image.load("Raspi_Colour_R.png")
raspberry = pygame.transform.scale(rasp,size)
rect = raspberry.get_rect()

font = pygame.font.Font(None,60)
font2 = pygame.font.Font(None,80)
text = font.render("Your score", 1, (200, 10, 10))

text = pygame.transform.rotate(text, -90)






p.init()			# initialise pfio (sets up the spi transfers)


pfd = p.PiFaceDigital()

pfd2 = p.PiFaceDigital(1)

leds = []

for i in range(8):
	leds.append(pfd.leds[i])

for i in range(8):
	leds.append(pfd2.leds[i])

#scanText = font2.render("Scan your card", 1, (200, 10, 10))
#scanText = pygame.transform.rotate(scanText,-90)

pressText = font2.render("Press to start", 1, (200, 10, 10))
pressText = pygame.transform.rotate(pressText,-90)


welcomeText = font2.render("Welcome", 1, (200, 10, 10))
welcomeText = pygame.transform.rotate(welcomeText,-90)
yourscoreText = font2.render("Your score was", 1, (200, 10, 10))
yourscoreText = pygame.transform.rotate(yourscoreText,-90)

def screenRefresh():
	screen.fill(black)
	screen.blit(raspberry,rect)
	screen.blit(text,(20,20))
	scoreText = font.render(str(score), 1, (200, 10, 10))
	scoreText = pygame.transform.rotate(scoreText,-90)
	screen.blit(scoreText,(50,20))
	pygame.display.flip()


def quit():
	pygame.quit()
	sys.exit()

def next_colour():
	""" choses a random number between 1 and 15 to represent the coloured leds and their corresponding buttons"""
	i = random.randint(0,13)
	while i == 7:
		i = random.randint(0,13)
	return i

def flash_lights():
	for i in range(10):
		pfd.output_port.toggle()
		pfd2.output_port.toggle()
		sleep(0.1)

def check_for_quit():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				quit()

colours = ["Red","Green","Blue","Yellow","White"]	# colour list for printing to screen


while True:
	check_for_quit()
	screen.fill(black)
	screen.blit(pressText, (width/2-pressText.get_width()/2,height/2-pressText.get_height()/2))
	pygame.display.flip()
	leds[3].turn_on()
	while True:
		check_for_quit()
		#cardid = pipassport.get_card_id()
		#print("cardid {}".format(cardid))
		#userinfo = pipassport.request_user_info(API_KEY, cardid)
		#print("userinfo {}".format(userinfo))

		#if not pipassport.card_valid(userinfo):
		#
		input1 = pfd.input_port.value # see if any buttons have been hit	print("Invalid card!")
		if input1:
			
			break	
		#else:
			break
		sleep(.2)
	print("done")
	leds[3].turn_off()
	
	screen.fill(black)
	screen.blit(welcomeText, (width/2-welcomeText.get_width()/2,height/2-welcomeText.get_height()/2))
	#userText = font2.render(cardid, 1, (200, 10, 10))
	#userText = pygame.transform.rotate(userText,-90)
	#screen.blit(userText, (width/2+welcomeText.get_width()/2,height/2-welcomeText.get_height()/2))
	pygame.display.flip()
	sleep(2)
	current = next_colour() 			# create first random colour to be lit
	leds[current].turn_on()	#pfio.digital_write(current,1)			# turn colour on
			# turn off hit light
	set_time = 500					# time allowed to hit each light (starts off large and reduced after each hit)
	time_left = set_time				# countdown timer for hitting the light
	hit = 0						# the input value
	score = 0					# keep track of the player's score
	misses = 0					# keep track of how many the player misses
	hits = 0
	previous_pressed = 255
	
	
	#print( "Time left is: %s" %time_left)	# notify the player how long they have to hit each flash
	
	screenRefresh()
	while True:
		check_for_quit()

	
		
		input1 = pfd.input_port.value # see if any buttons have been hit
		input2 = pfd2.input_port.value *256
	
		full_input = input1+input2
		#print (full_input)
		
		if full_input != previous_pressed:		# check this is a new button press
			previous_pressed = full_input	# record button press for next time's check
			#print(full_input)
			if full_input > 0:
				#print("Input received")
				#print(2**current)
				#print(full_input)
				if (2**current) == full_input: # check that only the correct button was hit
					#print ("Correct!")
					leds[current].turn_off()		# turn off hit light
					previous = current
					current = next_colour()				# get next colour
				
					while current == previous:			# ensure differnt colour each time
						current = next_colour()			# get next colour
					#print ("Hits + misses ", hits + misses)
					if ((hits+misses) %30) ==29 :
						if set_time > 125:
							set_time /= 2			# reduce the time allowed to hit the light
					#		print ("Time left is: %s" %set_time)
				
					time_left = set_time				# set the countdown time
				
					score += 2
					hits += 1
					#print ("Your score %d" %score)
					
					screenRefresh()
					
	
					leds[current].turn_on()			# turn the new light on
				
	
				else:							# wrong button pressed
	
					score -= 2
					#print ("Wrong one!")
					#print ("Your score %d" %score)
					
					screenRefresh()		
					
				
		elif time_left==0:
			leds[current].turn_off()			# turn off hit light
			misses +=1						# increment misses
			#print ("Missed one!")
			score -= 1
			if misses == 10:					# too many misses = Game Over!
				break
				
			previous = current					#
			current = next_colour()					# get next colour
			
			while current == previous:				# ensure differnt colour each time
				current = next_colour()				# get next colour
					
			if ((hits + misses) %30)==29:
				if set_time > 125:
					set_time /= 2				# reduce the allowed time
					#print ("Time left is: %s" %set_time)
					
			time_left = set_time					# set the countdown time
				
			leds[current].turn_on()			# turn the new light on		
		
		time_left -=1							# decrement the time left to hit the current light
	
		
	
	pfd.output_port.all_off()				# turn all lights off	
	flash_lights()
	print("\nGame over!\n")
	print("Your score was: %s" %score)		# print the player's final score
	screen.fill(black)
	screen.blit(yourscoreText,(50,20))
	scoreText = font.render(str(score), 1, (200, 10, 10))
	scoreText = pygame.transform.rotate(scoreText,-90)
	screen.blit(scoreText,(60+yourscoreText.get_width(),30+yourscoreText.get_width()))
	pygame.display.flip()
	sleep(5)

	#pipassport.post_transaction(API_KEY, cardid, score)
	#print("Sent transaction for {} {}".format(userinfo['first_name'],
                                                     # userinfo['last_name']))
p.deinit()					# close the pfio
	

