class Constant(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


POSITIVE = "positive"
NEGATIVE = "negative"

INDICATORS = Constant(
    type=(POSITIVE, NEGATIVE), ex_ante=(1, 2, 3, 4, 5), ex_post=(1, 2, 3, 4, 5),
)

EFFECT = Constant(
    {
        POSITIVE: {
            -4: "Extremely Negative",
            -3: "Highly Negative",
            -2: "Negative",
            0: "Neutral",
            1: "Slightly Positive",
            2: "Positive",
            3: "Highly Positive",
            4: "Extremely Positive",
        },
        NEGATIVE: {
            4: "Extremely Negative",
            3: "Highly Negative",
            2: "Negative",
            0: "Neutral",
            -1: "Slightly Positive",
            -2: "Positive",
            -3: "Highly Positive",
            -4: "Extremely Positive",
        },
    }
)
