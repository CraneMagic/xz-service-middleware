def path_algorithm_easy(cranePosition, sourcePosition, targetPosition, priority='xx', craneMaxHeight=0):
    positions = []
    if priority == 'xx':
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(cranePosition['zAxis']), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(int(sourcePosition['zAxis'])), 'grab') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(int(targetPosition['zAxis'])), 'release') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    elif priority == 'xy':
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(cranePosition['zAxis']), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(int(sourcePosition['zAxis'])), 'grab') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(int(targetPosition['zAxis'])), 'release') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    elif priority == 'yx':
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(cranePosition['zAxis']), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(int(sourcePosition['zAxis'])), 'grab') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(int(targetPosition['zAxis'])), 'release') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    elif priority == 'yy':
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(cranePosition['zAxis']), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(int(sourcePosition['zAxis'])), 'grab') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(int(targetPosition['zAxis'])), 'release') })
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    return positions

def path_algorithm_two_point(cranePosition, targetPosition):
    positions = []
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(cranePosition['zAxis']), 'move') })
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    return positions


def path_algorithm_four_point(cranePosition, sourcePosition, targetPosition, resetPosition, priority='xxx', craneMaxHeight=0):
    positions = []
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(cranePosition['zAxis']), 'move') })
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(0), 'move') })

    print('Priority cranePosition -> sourcePosition', priority[0])
    if priority[0] == 'x':
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(cranePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    elif priority[0] == 'y':
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(cranePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(int(sourcePosition['zAxis'])), 'grab') })
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })

    print('Priority cranePosition -> sourcePosition', priority[1])
    if priority[1] == 'x':
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(sourcePosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    elif priority[1] == 'y':
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(sourcePosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })

    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(int(targetPosition['zAxis'])), 'release') })
    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })

    print('Priority cranePosition -> sourcePosition', priority[2])
    if priority[2] == 'x':
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(resetPosition['xAxis']), '{:0>6d}'.format(targetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })
    elif priority[2] == 'y':
        positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(targetPosition['xAxis']), '{:0>6d}'.format(resetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })

    positions.append({ 'Point': '%s,%s,%s,%s' % ('{:0>6d}'.format(resetPosition['xAxis']), '{:0>6d}'.format(resetPosition['yAxis']), '{:0>6d}'.format(0), 'move') })

    return positions