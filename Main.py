def find_pathes(field, number, last_x, last_y, pathes):
    if number is None:
        is_correct = True
        for num in pathes:
            x, y = pathes[num][-1]
            if field[x][y] != num:
                is_correct = False
        if is_correct:
            yield pathes
    else:
        new_pathes = {}
        for num in pathes:
            new_pathes[num] = [(x_, y_) for (x_, y_) in pathes[num]]

        new_field = [[el for el in row] for row in field]

        for (x, y) in get_neighbours(last_x, last_y):
            if 0 <= x < len(field) and 0 <= y < len(field[0]):
                if (x, y) not in new_pathes[number]:
                    if field[x][y] is None or field[x][y] == number:
                        if field[x][y] is None:
                            new_field[x][y] = 0
                        new_pathes[number].append((x, y))
                        number_, (new_x, new_y) = find_min_relations(field, new_pathes)
                        for path in find_pathes(new_field, number_, new_x, new_y, new_pathes):
                            yield path
                        new_field = [[el for el in row] for row in field]
                        for num in pathes:
                            new_pathes[num] = [(x_, y_) for (x_, y_) in pathes[num]]
        yield None


def find_min_relations(field, pathes):
    minimum = 5
    min_coords = (None, None)
    min_number = None
    for number in pathes:
        last_x, last_y = pathes[number][-1]
        if len(pathes[number]) == 1 or field[last_x][last_y] != number:
            relations = 0
            for (x, y) in get_neighbours(last_x, last_y):
                if 0 <= x < len(field) and 0 <= y < len(field[0]):
                    if (x, y) not in pathes[number]:
                        if field[x][y] is None or field[x][y] == number:
                            relations += 1
            if relations < minimum:
                minimum = relations
                min_coords = (last_x, last_y)
                min_number = number
    return min_number, min_coords


def get_neighbours(x, y):
    return [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]


from_down_to_left_turning = '┐'
from_down_to_right_turning = '┌'
from_up_to_left_turning = '└'
from_up_to_right_turning = '┘'
horizontal = '—'
vertical = '|'

field = [[None, None, None, None, None, 3, 4],
         [None, None, 1, None, None, 5, None],
         [None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None],
         [2, None, None, None, 5, None, None],
         [None, None, 2, None, None, 3, None],
         [1, 4, None, None, None, None, None]]

pathes = {}
for i in range(len(field)):
    for j in range(len(field[i])):
        if field[i][j] is not None and field[i][j] not in pathes.keys():
            pathes[field[i][j]] = [(i, j)]

number, (x, y) = find_min_relations(field, pathes)
variants = find_pathes(field, number, x, y, pathes)

for variant in variants:
    if variant is not None:
        field_copy = [[el for el in row] for row in field]
        for number in variant:
            for j in range(1, len(variant[number]) - 1):
                previous_x = variant[number][j - 1][0]
                previous_y = variant[number][j - 1][1]
                x = variant[number][j][0]
                y = variant[number][j][1]
                next_x = variant[number][j + 1][0]
                next_y = variant[number][j + 1][1]
                if abs(next_x - previous_x) == 2:
                    field_copy[x][y] = vertical
                if abs(next_y - previous_y) == 2:
                    field_copy[x][y] = horizontal
                if y > previous_y and x < next_x or x < previous_x and y > next_y:
                    field_copy[x][y] = from_down_to_left_turning
                if y < previous_y and x < next_x or x < previous_x and y < next_y:
                    field_copy[x][y] = from_down_to_right_turning
                if y < previous_y and x > next_x or x > previous_x and y < next_y:
                    field_copy[x][y] = from_up_to_left_turning
                if y > previous_y and x > next_x or x > previous_x and y > next_y:
                    field_copy[x][y] = from_up_to_right_turning
        for i in range(len(field_copy)):
            for j in range(len(field_copy[i])):
                if field_copy[i][j] is None:
                    field_copy[i][j] = ' '

        for row in field_copy:
            for el in row:
                print(el, end=' ')
            print()
        print()
