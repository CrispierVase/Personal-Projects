start = input('What is the string?\n').lower()
output = ''
alpha = ',.abcdefghijklmnopqrstuvwxyz '
for char in start:
	idx = alpha.find(char)
	for _ in range(0, idx):
		output += 'No '
	output += 'Yes '
	for _ in range(idx, len(alpha)):
		output += 'No '

print(output)