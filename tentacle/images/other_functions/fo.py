class FloatingPointOperation:
    """Floating Point Operation Class"""
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Addition operation"""
        return a + b
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtraction operation"""
        return a - b
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiplication operation"""
        return a * b
    
    @staticmethod
    def divide(a: float, b: float) -> float:
        """Division operation"""
        if b == 0:
            raise ValueError("Divisor cannot be zero")
        return a / b
    
    @staticmethod
    def round_to_decimal(number: float, decimal_places: int = 2) -> float:
        """Round a float to specified decimal places"""
        return round(number, decimal_places)
    
    @staticmethod
    def complex_calculation(iterations: int = 1000000) -> float:
        """Perform a complex time-consuming calculation"""
        result = 0.0
        for i in range(iterations):
            result += (i ** 0.5) / (i + 1)
        return result

# Test cases
if __name__ == "__main__":
    # Create floating point operation instance
    fp = FloatingPointOperation()
    
    # Test addition
    print("\nTesting addition:")
    result = fp.add(3.14, 2.86)
    print(f"3.14 + 2.86 = {result}")
    
    # Test subtraction
    print("\nTesting subtraction:")
    result = fp.subtract(10.5, 4.2)
    print(f"10.5 - 4.2 = {result}")
    
    # Test multiplication
    print("\nTesting multiplication:")
    result = fp.multiply(2.5, 4.0)
    print(f"2.5 * 4.0 = {result}")
    
    # Test division
    print("\nTesting division:")
    try:
        result = fp.divide(9.6, 2.4)
        print(f"9.6 / 2.4 = {result}")
        
        # Test division by zero
        result = fp.divide(5.0, 0)
    except ValueError as e:
        print(f"Division error: {e}")
    
    # Test rounding
    print("\nTesting rounding:")
    number = 3.14159
    for decimal_places in [2, 3, 4]:
        result = fp.round_to_decimal(number, decimal_places)
        print(f"Rounding {number} to {decimal_places} decimal places: {result}")
    
    # Test complex calculation
    print("\nTesting complex calculation:")
    print("This may take a few seconds...")
    result = fp.complex_calculation()
    print(f"Complex calculation result: {result}")
    
    # 添加更多复杂计算测试
    print("\n测试不同规模的复杂计算:")
    iterations_list = [100000, 500000, 1000000, 2000000]
    for iters in iterations_list:
        print(f"\n使用 {iters} 次迭代进行计算...")
        import time
        start_time = time.time()
        result = fp.complex_calculation(iters)
        end_time = time.time()
        print(f"结果: {result}")
        print(f"耗时: {end_time - start_time:.2f} 秒")
    
    # 测试大规模浮点运算
    print("\n测试大规模连续运算:")
    start_time = time.time()
    result = 0.0
    operations = 1000000
    for i in range(operations):
        result = fp.add(result, 1.0/fp.round_to_decimal(i+1, 5))
        if i % 250000 == 0:
            print(f"完成 {i} 次运算...")
    end_time = time.time()
    print(f"最终结果: {fp.round_to_decimal(result, 4)}")
    print(f"总耗时: {end_time - start_time:.2f} 秒")