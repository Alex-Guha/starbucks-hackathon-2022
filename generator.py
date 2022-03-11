import random as rm
import pickle

drinks = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
prices = [3.,4.,5.,6.,7.,3.5,4.5,5.5,6.5]
cheap_prices = [3., 4., 5., 3.5, 4.5]
times = [270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600, 
		 720, 750,
		 840, 870, 900, 930, 960, 990, 1020, 1050, 1080]
time_weights = [5, 5, 10, 10, 10, 15, 15, 10, 5, 10, 5, 5,
				5, 5,
				5, 5, 10, 10, 10, 5, 5, 5, 5]
weather = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
weather_weights_summer = [1, 5, 20, 30, 15, 10, 15, 10, 10, 5, 0]
weather_weights_spring = [0, 5, 10, 20, 30, 20, 10, 10, 10, 5, 0]
weather_weights_winter = [0, 0, 5, 15, 30, 30, 20, 10, 10, 10, 1]
weather_weights_fall = [1, 5, 10, 30, 30, 20, 10, 10, 10, 5, 0]

# Return should be a time selected from times
def choose_to_order(iden, day, fav_drink, price, weather, day_of_week, preferred_time):
	if(rm.choices([1,2], [5, 95])[0] == 2): # Some randomness, such that 1/20 times the person will not come in, regardless of other factors
		if(weather == 0): # less likely to come in at all, high likelihood of buying cold drink
			if(iden % 11 == 5 or iden % 11 == 8): # regular morning every weekday customer
				if(not(day_of_week == 0 or day_of_week == 1)): # If weekday
					if(fav_drink < 15 and rm.choices([1,2], [50, 50])[0] == 1):
						# 50/50 odds a hot drink preferring regular will not come in on an extremely hot day
						return 0
					elif(fav_drink < 15):
						return preferred_time
					elif(fav_drink > 14): # Cold drink preferrer will come
						return preferred_time
				else: # weekend
					if(fav_drink < 15 and rm.choices([1,2], [10, 90])[0] == 2):
						# 9 in 10 times, hot drink preferring regular will not come on extremely hot weekend
						return 0
					elif(fav_drink < 15):
						# If they do come, it's at a random time
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]
					elif(fav_drink > 14 and rm.choices([1,2], [25, 75])[0] == 2):
						# 3 in 4 time, a cold drink preferring regular will not come
						return 0
					else:
						# If they do come, it's at a random time
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]

			else: # no need to consider weekend vs weekday for non-regular everyday types
				if(rm.choices([1,2], [60, 40])[0] == 1): # Due to weather, only 60% chance customer comes in
					if(preferred_time <= 600): # Morning go-ers
						if(price > 5): # If they like a more expensive drink
							if(fav_drink < 15 and rm.choices([1,2], [5, 95])[0] == 2):
								# If they like hot drink, 5% chance they come in
								return 0
							elif(fav_drink < 15):
								return preferred_time
							elif(fav_drink > 14 and rm.choices([1,2], [10, 90])[0] == 1):
								return preferred_time
							else:
								return 0
						else: # Cheaper drink preferrers
							if(fav_drink < 15 and rm.choices([1,2], [10, 90])[0] == 2):
								return 0
							elif(fav_drink < 15):
								return preferred_time
							elif(fav_drink > 14 and rm.choices([1,2], [20, 80])[0] == 1):
								return preferred_time
							else:
								return 0

					else: # after noon
						if(price > 5):
							if(fav_drink < 15 and rm.choices([1,2], [5, 95])[0] == 2):
								return 0
							elif(fav_drink < 15):
								return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [75, 25])[0]
							elif(fav_drink > 14 and rm.choices([1,2], [30, 70])[0] == 1):
								return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [75, 25])[0]
							else:
								return 0
						else:
							if(fav_drink < 15 and rm.choices([1,2], [10, 90])[0] == 2):
								return 0
							elif(fav_drink < 15):
								return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [85, 15])[0]
							elif(fav_drink > 14 and rm.choices([1,2], [35, 65])[0] == 1):
								return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [75, 25])[0]
							else:
								return 0
				else:
					return 0

		elif(weather == 1):
			# similar to weather = 0, just more likely for people to go out
			if(iden % 11 == 5 or iden % 11 == 8): # regular morning every weekday customer
				if(not(day_of_week == 0 or day_of_week == 1)): # If weekday
					if(fav_drink < 15 and rm.choices([1,2], [35, 65])[0] == 1):
						# 35/65 odds a hot drink preferring regular will not come in on a moderately hot day
						return 0
					elif(fav_drink < 15):
						return preferred_time
					elif(fav_drink > 14):
						# Cold drink preferrer will come
						return preferred_time

				else: # weekend
					if(fav_drink < 15 and rm.choices([1,2], [10, 90])[0] == 2):
						# 9 in 10 times, hot drink preferring regular will not come on moderately hot weekend
						return 0
					elif(fav_drink < 15):
						# If they do come, it's at a random time
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]
					elif(fav_drink > 14 and rm.choices([1,2], [20, 80])[0] == 2):
						# a cold drink preferring regular will not come
						return 0
					else:
						# If they do come, it's at a random time
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]

			else: # no need to consider weekend vs weekday for non-regular everyday types
				if(rm.choices([1,2], [50, 50])[0] == 1): # Due to weather, only 50% chance customer comes in
					if(preferred_time <= 600): # Morning go-ers
						if(price > 5): # If they like a more expensive drink
							if(fav_drink < 15 and rm.choices([1,2], [10, 90])[0] == 2):
								# If they like hot drink, 10% chance they come in
								return 0
							elif(fav_drink < 15):
								return preferred_time
							elif(fav_drink > 14 and rm.choices([1,2], [20, 80])[0] == 1):
								return preferred_time
							else:
								return 0
						else: # Cheaper drink preferrers
							if(fav_drink < 15 and rm.choices([1,2], [15, 85])[0] == 2):
								return 0
							elif(fav_drink < 15):
								return preferred_time
							elif(fav_drink > 14 and rm.choices([1,2], [40, 60])[0] == 1):
								return preferred_time
							else:
								return 0

					else: # after noon
						if(price > 5):
							if(fav_drink < 15 and rm.choices([1,2], [5, 95])[0] == 2):
								return 0
							elif(fav_drink < 15):
								return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [75, 25])[0]
							elif(fav_drink > 14 and rm.choices([1,2], [30, 70])[0] == 1):
								return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [75, 25])[0]
							else:
								return 0
						else:
							if(fav_drink < 15 and rm.choices([1,2], [10, 90])[0] == 2):
								return 0
							elif(fav_drink < 15):
								return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [85, 15])[0]
							elif(fav_drink > 14 and rm.choices([1,2], [35, 65])[0] == 1):
								return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [75, 25])[0]
							else:
								return 0
				else:
					return 0

		elif(weather == 2):
			# Slightly warmer than usual, more or less a pleasant day
			if(iden % 11 == 5 or iden % 11 == 8): # regular morning every weekday customer
				if(not(day_of_week == 0 or day_of_week == 1)): # If weekday
					if(fav_drink < 15 and rm.choices([1,2], [10, 90])[0] == 1):
						# 10/90 odds a hot drink preferring regular will not come in on a slightly hot day
						return 0
					elif(fav_drink < 15):
						return preferred_time
					elif(fav_drink > 14):
						# Cold drink preferrer will come
						return preferred_time

				else: # weekend
					if(fav_drink < 15 and rm.choices([1,2], [10, 90])[0] == 2):
						# 9 in 10 times, hot drink preferring regular will not come on slightly hot weekend
						return 0
					elif(fav_drink < 15):
						# If they do come, it might be at a random time
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]
					elif(fav_drink > 14 and rm.choices([1,2], [20, 80])[0] == 2):
						# a cold drink preferring regular will not come
						return 0
					else:
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]

			else: # no need to consider weekend vs weekday for non-regular everyday types
				if(preferred_time <= 600): # Morning go-ers
					if(price > 5): # If they like a more expensive drink
						if(fav_drink < 15 and rm.choices([1,2], [30, 70])[0] == 2):
							# If they like hot drink, 30% chance they come in
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [50, 50])[0] == 1):
							return preferred_time
						else:
							return 0
					else: # Cheaper drink preferrers
						if(fav_drink < 15 and rm.choices([1,2], [40, 60])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [50, 50])[0] == 1):
							return preferred_time
						else:
							return 0

				else: # after noon
					if(price > 5):
						if(fav_drink < 15 and rm.choices([1,2], [30, 70])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [40, 60])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
					else:
						if(fav_drink < 15 and rm.choices([1,2], [40, 60])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [50, 50])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0

		elif(weather == 3 and weather == 4):
			# Sunny and pleasant
			if(iden % 11 == 5 or iden % 11 == 8): # regular morning every weekday customer
				if(not(day_of_week == 0 or day_of_week == 1)): # If weekday, regular goes.
					return preferred_time

				else: # weekend
					if(fav_drink < 15 and rm.choices([1,2], [15, 85])[0] == 2):
						return 0
					elif(fav_drink < 15):
						# If they do come, it might be at a random time
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]
					elif(fav_drink > 14 and rm.choices([1,2], [15, 85])[0] == 2):
						# a cold drink preferring regular will not come
						return 0
					else:
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]

			else: # no need to consider weekend vs weekday for non-regular everyday types
				if(preferred_time <= 600): # Morning go-ers
					if(price > 5): # If they like a more expensive drink, 65% chance they go
						if(fav_drink < 15 and rm.choices([1,2], [65, 35])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [65, 35])[0] == 1):
							return preferred_time
						else:
							return 0
					else: # Cheaper drink preferrers 70% chance they go
						if(fav_drink < 15 and rm.choices([1,2], [70, 30])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [70, 30])[0] == 1):
							return preferred_time
						else:
							return 0

				else: # after noon
					if(price > 5):
						if(fav_drink < 15 and rm.choices([1,2], [65, 35])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [65, 35])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
					else:
						if(fav_drink < 15 and rm.choices([1,2], [70, 30])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [70, 30])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
		elif(weather == 5):
			if(iden % 11 == 5 or iden % 11 == 8): # regular morning every weekday customer
				if(not(day_of_week == 0 or day_of_week == 1)): # If weekday, regular goes.
					return preferred_time

				else: # weekend
					if(fav_drink < 15 and rm.choices([1,2], [15, 85])[0] == 2):
						return 0
					elif(fav_drink < 15):
						# If they do come, it might be at a random time
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]
					elif(fav_drink > 14 and rm.choices([1,2], [10, 90])[0] == 2):
						# a cold drink preferring regular will not come
						return 0
					else:
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]

			else: # no need to consider weekend vs weekday for non-regular everyday types
				if(preferred_time <= 600): # Morning go-ers
					if(price > 5): # If they like a more expensive drink, 65% chance they go
						if(fav_drink < 15 and rm.choices([1,2], [65, 35])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [60, 40])[0] == 1):
							return preferred_time
						else:
							return 0
					else: # Cheaper drink preferrers 70% chance they go
						if(fav_drink < 15 and rm.choices([1,2], [70, 30])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [65, 35])[0] == 1):
							return preferred_time
						else:
							return 0

				else: # after noon
					if(price > 5):
						if(fav_drink < 15 and rm.choices([1,2], [65, 35])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [60, 40])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
					else:
						if(fav_drink < 15 and rm.choices([1,2], [70, 30])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [65, 35])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
		elif(weather == 6):
			# overcast
			if(iden % 11 == 5 or iden % 11 == 8): # regular morning every weekday customer
				if(not(day_of_week == 0 or day_of_week == 1)): # If weekday, regular goes.
					return preferred_time

				else: # weekend
					if(fav_drink < 15 and rm.choices([1,2], [15, 85])[0] == 2):
						return 0
					elif(fav_drink < 15):
						# If they do come, it might be at a random time
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]
					elif(fav_drink > 14 and rm.choices([1,2], [10, 90])[0] == 2):
						# a cold drink preferring regular will not come
						return 0
					else:
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]

			else: # no need to consider weekend vs weekday for non-regular everyday types
				if(preferred_time <= 600): # Morning go-ers
					if(price > 5): # If they like a more expensive drink, 65% chance they go
						if(fav_drink < 15 and rm.choices([1,2], [65, 35])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [55, 45])[0] == 1):
							return preferred_time
						else:
							return 0
					else: # Cheaper drink preferrers 70% chance they go
						if(fav_drink < 15 and rm.choices([1,2], [70, 30])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [60, 40])[0] == 1):
							return preferred_time
						else:
							return 0

				else: # after noon
					if(price > 5):
						if(fav_drink < 15 and rm.choices([1,2], [65, 35])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [55, 45])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
					else:
						if(fav_drink < 15 and rm.choices([1,2], [70, 30])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [60, 40])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
		elif(weather == 7):
			# Drizzling/light rain/potential for rain
			if(iden % 11 == 5 or iden % 11 == 8): # regular morning every weekday customer
				if(not(day_of_week == 0 or day_of_week == 1)): # If weekday, regular goes.
					if(rm.choices([1,2], [15, 85])[0] == 2):
						return preferred_time
					else:
						return 0

				else: # weekend
					if(fav_drink < 15 and rm.choices([1,2], [5, 95])[0] == 2):
						return 0
					elif(fav_drink < 15):
						# If they do come, it might be at a random time
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]
					elif(fav_drink > 14 and rm.choices([1,2], [3, 97])[0] == 2):
						# a cold drink preferring regular will not come
						return 0
					else:
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]

			else: # no need to consider weekend vs weekday for non-regular everyday types
				if(preferred_time <= 600): # Morning go-ers
					if(price > 5): # If they like a more expensive drink
						if(fav_drink < 15 and rm.choices([1,2], [35, 65])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [30, 70])[0] == 1):
							return preferred_time
						else:
							return 0
					else: # Cheaper drink preferrers
						if(fav_drink < 15 and rm.choices([1,2], [40, 60])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [35, 65])[0] == 1):
							return preferred_time
						else:
							return 0

				else: # after noon
					if(price > 5):
						if(fav_drink < 15 and rm.choices([1,2], [35, 65])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [30, 70])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
					else:
						if(fav_drink < 15 and rm.choices([1,2], [40, 60])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [35, 65])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
		elif(weather == 8):
			# Raining
			if(iden % 11 == 5 or iden % 11 == 8): # regular morning every weekday customer
				if(not(day_of_week == 0 or day_of_week == 1)): # If weekday, regular goes.
					if(rm.choices([1,2], [15, 85])[0] == 2):
						return preferred_time
					else:
						return 0

				else: # weekend
					if(fav_drink < 15 and rm.choices([1,2], [1, 99])[0] == 1):
						return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [50, 50])[0]
					else:
						return 0

			else: # no need to consider weekend vs weekday for non-regular everyday types
				if(preferred_time <= 600): # Morning go-ers
					if(price > 5): # If they like a more expensive drink
						if(fav_drink < 15 and rm.choices([1,2], [20, 80])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [10, 90])[0] == 1):
							return preferred_time
						else:
							return 0
					else: # Cheaper drink preferrers
						if(fav_drink < 15 and rm.choices([1,2], [25, 75])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return preferred_time
						elif(fav_drink > 14 and rm.choices([1,2], [15, 85])[0] == 1):
							return preferred_time
						else:
							return 0

				else: # after noon
					if(price > 5):
						if(fav_drink < 15 and rm.choices([1,2], [15, 85])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [5, 95])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
					else:
						if(fav_drink < 15 and rm.choices([1,2], [20, 80])[0] == 2):
							return 0
						elif(fav_drink < 15):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						elif(fav_drink > 14 and rm.choices([1,2], [10, 90])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0

		elif(weather == 9):
			# Rainstorm
			if(iden % 11 == 5 or iden % 11 == 8): # regular morning every weekday customer
				if(not(day_of_week == 0 or day_of_week == 1)): # If weekday, regular goes.
					if(rm.choices([1,2], [5, 95])[0] == 1):
						return preferred_time
					else:
						return 0
				else: # weekend
					return 0

			else: # no need to consider weekend vs weekday for non-regular everyday types
				if(preferred_time <= 600): # Morning go-ers
					if(fav_drink < 15 and rm.choices([1,2], [3, 97])[0] == 1):
						return preferred_time
					else:
						return 0

				else: # after noon
					if(price > 5):
						if(fav_drink < 15 and rm.choices([1,2], [2, 98])[0] == 1):
							return rm.choices([preferred_time, rm.choices(times, time_weights)[0]], [90, 10])[0]
						else:
							return 0
		elif(weather == 10):
			return 0

	else:
		return 0

	# Just in case...
	return 0



def generate(start, num):
	input_data = []
	output_data = []

	for i in range(start, num):

		user_fav_drink = rm.choice(drinks)
		if(i % 11 == 5 or i % 11 == 8):
			price_of_fav = rm.choice(cheap_prices)
		else:
			price_of_fav = rm.choice(prices)

		if(i % 11 == 5 or i % 11 == 8):
			preferred_time = rm.choices([270, 300, 330, 360, 390, 420, 450, 480, 510, 540, 570, 600],
										[5, 5, 10, 10, 10, 15, 15, 10, 5, 10, 5, 5])[0]
		else:
			preferred_time = rm.choices(times, time_weights)[0]

		for year in range(3):
			# per day for 3 years
			for day in range(365):
				day_of_week = day % 7

				single_input = [i / num] # initialize each input array with user id

				single_input.append(day / 365)

				single_input.append(user_fav_drink / 20)

				single_input.append(price_of_fav / 8)

				if(334 < day or day < 60): # winter
					single_input.append(rm.choices(weather, weather_weights_winter)[0] / 10)
				elif(59 < day and day < 152): # spring
					single_input.append(rm.choices(weather, weather_weights_spring)[0] / 10)
				elif(153 < day and day < 244): # summer
					single_input.append(rm.choices(weather, weather_weights_summer)[0] / 10)
				else: # fall
					single_input.append(rm.choices(weather, weather_weights_fall)[0] / 10)

				single_input.append(day_of_week / 7)

				# Choose what time the user orders. If 0, user did not order.
				time_chosen = choose_to_order(i, day, user_fav_drink, price_of_fav, single_input[4]*10, day_of_week, preferred_time)

				output = 0
				for index, time in enumerate(times):
					if(time_chosen == time):
						output = index
						break

				input_data.append(single_input)
				output_data.append(output)

	# zip together the input with output, shuffle, then return the unzipped lists
	shuffled = list(zip(input_data, output_data))
	rm.shuffle(shuffled)
	input_data, output_data = zip(*shuffled)
	return list(input_data), list(output_data)

def save_data(path, X, y):
	with open(path, 'wb') as f:
		pickle.dump(list(zip(X, y)), f)

def load_data(path):
	with open(path, 'rb') as f:
		X, y = zip(*pickle.load(f))
		return list(X), list(y)


if __name__ == "__main__":
	X, y = generate(0, 100)

	#print(X, y)

	save_data('data_100', X, y)

	#X, y = load_data('test')