import pyglet
def load_config():
    if __name__ == '__main__':
        filename = '../config'
    else:
        filename = 'config'
    with open(filename, 'r') as config:
        contents = config.read().split('\n')
        tmp = contents.copy()
        for option in contents:
            if '#' in option:
                tmp.remove(option)
        contents = tmp.copy()
        del tmp
        # this is hard coded and could probably be optimized later
        light_color = contents[0][1:-1].split(',')
        for idx, val in enumerate(light_color):
            light_color[idx] = int(val)
        dark_color = contents[1][1:-1].split(',')
        for idx, val in enumerate(dark_color):
            dark_color[idx] = int(val)
        win_size = contents[2][1:-1].split(',')
        for idx, val in enumerate(win_size):
            win_size[idx] = int(val)
        cell_size = int(contents[3])
        if cell_size * 8 > win_size[0]:
            cell_size = int(win_size[0] / 8) + 1
        return tuple(light_color), tuple(dark_color), tuple(win_size), int(cell_size)

