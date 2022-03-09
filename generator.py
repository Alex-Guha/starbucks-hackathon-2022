import random as rm

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
where they are when placing orders (eg how far from store) (0 if not use app) (0 close, 1 far)
If they order in store (1 vs 0 for online)

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

choices =  [[1,2,3],
			[4,5,6],
			[7,8,9]]

# Weights in each array should sum to 100
weights =  [[1,2,1],
			[2,1,2],
			[1,2,1]]

def generate(num):
	input_data = []
	output_data = []

	# Makes [num] weighted random choices from each option, and creates an output for each
	for choice, weight in zip(choices, weights):
		input_data.append(rm.choices(choice, weight, k=num))
		# determine some way of converting each set of inputs into an output
		# output_data.append()

	input_data = list(map(list, zip(*input_data)))

	# Normalize the data such that each value is a decimal between 0 and 1
	for i, arr in enumerate(input_data):
		input_data[i][0] = arr[0] / 10000
		input_data[i][1] = arr[1] / i
		input_data[i][2] = arr[2] / 365
		input_data[i][3] = arr[3] / 20
		input_data[i][4] = arr[4] / 8
		input_data[i][6] = arr[6] / 7

		output_data[i][0] = output_data[i][0] / 1440

	rm.shuffle(zip(input_data, output_data))
	return zip(*input_data)

def save_data(path):
	with open(path, 'wb') as f:
		f.write(zip(X, y))

def load_data(path):
	with open(path, 'rb') as f:
		return zip(*f.read())

print(generate(5))