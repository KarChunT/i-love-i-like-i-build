FORMULA = [
    (
        "random.uniform(-1,1) * x**2  - math.sin(y**2) + abs(y-x)",
        "random.uniform(-1,1) * y**3 - math.cos(x**2) + 2*x",
    ),
    (
        "random.uniform(-1, 1) * ( math.sin(x) ) - ( ( math.cos(y)) ) * ( math.sin(x) ) - math.pi",
        "random.uniform(-1, 1) * ( math.cos(y) ) - ( ( math.sin(x)) ) * ( math.cos(x) ) + math.pi",
    ),
    (
        "random.uniform(-1, 1) * x ** 2 + math.sin(y ** 2) + abs(x - y)",
        "random.uniform(-1, 1) * y ** 2 - math.cos(x ** 2) + abs(y - x)",
    ),
    (
        "random.uniform(-1, 1) * ( math.sin(x) - math.sin(x) * math.cos(y) ) * (math.sin(x) + math.exp(y)) + x",
        "random.uniform(-1, 1) * ( math.sin(y) - math.cos(y) * math.sin(x) ) * (math.cos(y) + math.exp(x)) + y",
    ),
    (
        "random.uniform(-1, 1) * ( math.sin(x) - math.cos(y) ) * abs(x - y) + 1 * math.cos(x)",
        "random.uniform(-1, 1) * ( math.sin(y) - math.cos(x) ) * abs(y - x) + 1 * math.sin(y)",
    ),
]
