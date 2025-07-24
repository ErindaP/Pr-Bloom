def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

def update_elo(rating_a, rating_b, result_a, k=32):
    expected_a = expected_score(rating_a, rating_b)
    new_a = rating_a + k * (result_a - expected_a)
    new_b = rating_b + k * ((1 - result_a) - (1 - expected_a))
    return round(new_a), round(new_b)
