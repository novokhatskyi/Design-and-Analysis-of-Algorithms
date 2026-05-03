def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
    
def fibonacci_dp(n):
    # Ініціалізація масиву для зберігання результатів підзадач
    fib = [0] * (n + 1)
    
    # Базові випадки
    fib[0] = 0
    if n > 0:
        fib[1] = 1
    
    # Заповнення масиву
    for i in range(2, n + 1):
        fib[i] = fib[i-1] + fib[i-2]
    
    return fib[n]

    
if __name__ == "__main__":
    n = 56
    # print(f"Fibonacci number at position {n} is: {fibonacci_recursive(n)}")
    print(f"Fibonacci number at position {n} is: {fibonacci_dp(n)}")