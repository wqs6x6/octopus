import json
def fib_recursive(n):
    """
    Calculate Fibonacci number using iterative method
    Args:
        n: Integer representing the position in Fibonacci sequence
    Returns:
        Fibonacci number at position n
    """
    n = n % 30 
    if n <= 1:
        return n
    return fib_recursive(n-1) + fib_recursive(n-2)


def main(args):
    name = args.get("key1", "stranger")
    res = {}
    res["key1"] = fib_recursive(int(name))
    # print(f"Name: {name}")
    return res
