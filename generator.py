import random as rm
import pickle

"""
Inputs:
User id (Assume max of 10k ig?)
Number of previous orders (divide by theoretical max of 1 per day everyday) (in other words, a ratio of how many days they’ve gotten starbucks out of the total)
What day of the year it is (out of 365)
User’s favorite of the 20 drinks (id) on “menu” (divide by 20)
Price of user’s favorite drink ($3 - $8)
Weather (0 for blistering hot, 1 for blizzard) (Sunny ~3/10, Sunny but kinda cold ~5/10, overcast ~6/10, raining ~8/10, rainstorm ~9/10, blizzard 1)
Day of the week (more likely to go to starbucks on a weekday than on weekend) (0 to 7, 0 as Sunday)

Outputs:
what time of day they open the app/order food if in person (selection of times between 4:30am and 8:30pm, in 30 min increments) (convert to minutes, divide by 1440)
	(if not using app, this represents when they order in person)

Generating data should be in 30 min ticks, 365 days a year, with maybe 3 years worth, per person.
Things to consider:
	When the person does check app/order vs the majority when they aren’t.
	Some people will consistently get it during weekdays, except maybe when weather is bad
	Some people go after work/school
	Some people occasionally get it



Input data
[
[0 to 1, 0 to 1, 0 to 1, 0 to 1, 0 to 1, ..., 0 to 1],
[0 to 1, 0 to 1, 0 to 1, 0 to 1, 0 to 1, ..., 0 to 1],
[0 to 1, 0 to 1, 0 to 1, 0 to 1, 0 to 1, ..., 0 to 1],
[0 to 1, 0 to 1, 0 to 1, 0 to 1, 0 to 1, ..., 0 to 1]
]

Output data
[
[0 to 1, 0 to 1, 0 OR 1],
[0 to 1, 0 to 1, 0 OR 1],
[0 to 1, 0 to 1, 0 OR 1],
[0 to 1, 0 to 1, 0 OR 1]
]
"""

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
weather_weights_summer = [5, 10, 20, 30, 15, 10, 15, 10, 10, 5, 0]
weather_weights_spring = [0, 5, 10, 20, 30, 20, 10, 10, 10, 10, 5]
weather_weights_winter = [0, 0, 5, 15, 30, 30, 20, 10, 10, 10, 10]
weather_weights_fall = [5, 5, 10, 30, 30, 20, 10, 10, 10, 5, 5]


"""
User id (Assume max of 10k ig?)
-Number of previous orders (divide by theoretical max of 1 per day everyday) (in other words, a ratio of how many days they’ve gotten starbucks out of the total)
What day of the year it is (out of 365)
User’s favorite of the 20 drinks (id) on “menu” (divide by 20)
Price of user’s favorite drink ($3 - $8)
Weather (0 for blistering hot, 1 for blizzard) (Sunny ~3/10, Sunny but kinda cold ~5/10, overcast ~6/10, raining ~8/10, rainstorm ~9/10, blizzard 1)
Day of the week (more likely to go to starbucks on a weekday than on weekend) (0 to 7, 0 as Sunday)
"""
# choose_to_order returns a time selected from times
# make them less likely to order if it's expensive (>5)
# more likely to go on a weekday than on weekend
# unlikely to go if too hot/too cold (weather == 0 or weather == 9 or weather == 10 or weather == 8)
# if id % 11 = 5 or 8, they go every weekday, unless conditions prevent them
# if id % 101 == 0, the person is an outlier
def choose_to_order(id, day, fav_drink, price, weather, day_of_week, preferred_time):
	return 0

def generate(num):
	input_data = []
	output_data = []

	
	for i in range(num):

		user_fav_drink = rm.choice(drinks)
		if(i % 11 == 5 or i % 11 == 8):
			price_of_fav = rm.choice(cheap_prices)
		else:
			price_of_fav = rm.choice(prices)
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

				# what time of day they open the app/order food if in person (selection of times between 4:30am and 8:30pm, in 30 min increments) (convert to minutes, divide by 1440)
				#   (if not using app, this represents when they order in person)

				# Choose what time the user orders. If 0, user did not order.
				output = choose_to_order(i, day, user_fav_drink, price_of_fav, single_input[4]*10, day_of_week, preferred_time) / 1440

				input_data.append(single_input)
				output_data.append(output)

	# zip together the input with output, shuffle, then return the unzipped code
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

X, y = generate(1)

#save_data('test', X, y)

#X, y = load_data('test')

print(X, y)

