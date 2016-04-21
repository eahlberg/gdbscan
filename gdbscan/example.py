from gdbscan import GDBSCAN, Points
import math


UNCLASSIFIED = -2


class Point:
    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val
        self.cluster_id = UNCLASSIFIED

    def __repr__(self):
        return '(x:{}, y:{}, val:{}, cluster:{})' \
            .format(self.x, self.y, self.val, self.cluster_id)


def n_pred(p1, p2):
    return all([math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2) <= 1,
                abs(p1.val - p2.val) <= 1])


def w_card(points):
    return len(points)


def test():
    p1 = Point(0, 0, 1)
    p2 = Point(0, 1, 2)
    p2 = Point(1, 0, 3)
    p3 = Point(2, 1, 1)
    p4 = Point(2, 2, 2)
    p4 = Point(1, 2, 3)

    points = [p1, p2, p3, p4]

    clustered = GDBSCAN(Points(points), n_pred, 0, w_card)
    print clustered


if __name__ == '__main__':
    test()
