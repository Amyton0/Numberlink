import colorama


def find_pathes(field, number, last_x, last_y, pathes):
    if number is None:
        is_correct = True
        for num in pathes:
            x, y = pathes[num][-1]
            if field[x][y] != num:
                is_correct = False
        if is_correct:
            if pathes is not None:
                print(pathes)
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


def enter_field(lines, columns):
    print(f'Введите {lines} строк, в каждой должно быть {columns} '
          f'чисел, числа нужно разделять пробелом, пустое поле обозначается нулём')
    field = []
    for i in range(lines):
        while len(field) < i + 1:
            try:
                line = [None if el == '0' else int(el) for el in input().split()]
                if len(line) != columns:
                    raise Exception
                field.append(line)
            except Exception:
                print(colorama.Fore.RED + "Неверно введена строка")
    return field


from_down_to_left_turning = '┐'
from_down_to_right_turning = '┌'
from_up_to_left_turning = '└'
from_up_to_right_turning = '┘'
horizontal = '—'
vertical = '|'

colorama.init(autoreset=True)

is_exit = False

while not is_exit:
    lines = None
    columns = None

    while lines is None or columns is None:
        try:
            lines, columns = map(int,
                                 input('Введите размеры поля через пробел: сначала количество строк, потом — столбцов: ')
                                 .split())
        except Exception:
            print(colorama.Fore.RED + "Неверно введён размер поля")

    field = []
    numbers_of_numbers = {}
    are_numbers_correct = False
    while not are_numbers_correct:
        field = enter_field(lines, columns)

        are_numbers_correct = True
        numbers_of_numbers = {}

        for i in range(lines):
            for j in range(columns):
                if field[i][j] is not None and field[i][j] not in numbers_of_numbers.keys():
                    numbers_of_numbers[field[i][j]] = 1
                elif field[i][j] is not None:
                    numbers_of_numbers[field[i][j]] += 1

        for number_ in numbers_of_numbers:
            if numbers_of_numbers[number_] != 2:
                are_numbers_correct = False
        if not are_numbers_correct:
            print(colorama.Fore.RED + "Не каждого числа на поле по 2")

    pathes = {}
    for i in range(lines):
        for j in range(columns):
            if field[i][j] is not None and field[i][j] not in pathes.keys():
                pathes[field[i][j]] = [(i, j)]

    number, (x, y) = find_min_relations(field, pathes)
    variants = find_pathes(field, number, x, y, pathes)

    if variants is None:
        print(colorama.Fore.RED + 'Решений не найдено')
    else:
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
    is_ex = input('Чтобы выйти, введите exit, чтобы начать заново, введите что-нибудь другое')

    if is_ex == 'exit':
        is_exit = True
