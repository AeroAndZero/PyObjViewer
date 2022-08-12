n = 0
try : 
    n = abs(int(input("Enter N : ")))
except Exception as e:
    print(e)

if n < 2 or n > 10000:
    print("Wrong Input")
    quit()

results = []
for i in range(2,n+1):
    temp = i
    answer = 0
    while temp > 0:
        answer += (temp % 10) ** 3
        temp -= temp % 10
        temp /= 10

    if answer == i:
        results.append(int(answer))

if len(results) != 0:
    print(" ".join(str(x) for x in results))
else:
    print("No Number Found")
