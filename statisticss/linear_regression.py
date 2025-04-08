def linear_regression(data): # array of Xs and Ys
    x, y = data[0], data[1]
    n = len(x)
    x_min = min(x)
    x_max = max(x)
    x2_sum = sum(i ** 2 for i in x)
    y2_sum = sum(i ** 2 for i in y)
    xy_sum = sum(i * j for i,j in zip(x,y))

    SSxx = x2_sum - (sum(x) ** 2) / n
    SSxy = xy_sum - (sum(x) * sum(y)) / n
    SSyy = y2_sum - (sum(y) ** 2) / n

    b = SSxy / SSxx
    a = (sum(y) / n) - b * (sum(x) / n)
    
    r2 = (b * SSxy) / SSyy
    r = SSxy / (SSxx * SSyy) ** 0.5
    
    def regression_equation():
        return f"Regression Equation: y = {a:.4f} + {b:.4f}x, x in range [{x_min}, {x_max}]"
    def coefficient_of_determination():
        return f"Coefficient of Determination (R²): {r2:.4f}"
    def coefficient_of_correlation():
        return f"Coefficient of Correlation (r): {r:.4f}"
    def predict(X):
        return a + b*X
    return regression_equation(), coefficient_of_determination(), coefficient_of_correlation()

def result(data):
    equation, r_squared, correlation, predict_func = linear_regression(data)
    print("Linear Regression: ")
    print(equation)
    print(r_squared)
    print(correlation)
    print('------------------------')

# Make predictions
# x_new = 19
# predicted_y = predict_func(x_new)
# print(f"Predicted y for x = {x_new}: {predicted_y:.4f}")
# print('------------------------')

