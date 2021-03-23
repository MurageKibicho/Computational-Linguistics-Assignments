import sys

def factorial(n: int):
    fact = 1
    for i in range(1,n + 1):
        fact = fact * i
    print(str(fact))

if __name__ == "__main__":
    n = int(sys.argv[1])
    factorial(n)