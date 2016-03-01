import datetime

def main():
	for y in range(1900, 2101):
		try:
			_ = datetime.date(y, 2, 29)
		except ValueError:
			if y % 4 == 0:
				print(y)


if __name__ == '__main__':
	main()
