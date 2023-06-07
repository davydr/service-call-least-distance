from ortools.linear_solver import pywraplp

# Employee starting positions
starting_positions = {
    'Employee1': (0, 0),
    'Employee2': (0, 5),
    'Employee3': (5, 0),
    'Employee4': (5, 5),
    'Employee5': (10, 0),
    'Employee6': (10, 5),
    'Employee7': (15, 0),
    'Employee8': (15, 5),
    'Employee9': (20, 0),
    'Employee10': (20, 5),
}

# Service calls and assigned slots
service_calls = {
    'ServiceCall1': (2, 3),  # (x, y) coordinates
    'ServiceCall2': (7, 2),
    'ServiceCall3': (12, 1),
    'ServiceCall4': (18, 4),
    'ServiceCall5': (4, 2),
    'ServiceCall6': (9, 3),
    'ServiceCall7': (14, 4),
    'ServiceCall8': (19, 1),
}

assigned_slots = {
    'ServiceCall1': '9 AM',
    'ServiceCall2': '9 AM',
    'ServiceCall3': '11 AM',
    'ServiceCall4': '11 AM',
    'ServiceCall5': '1 PM',
    'ServiceCall6': '1 PM',
    'ServiceCall7': '3 PM',
    'ServiceCall8': '3 PM',
}

# Calculate the distance between two points using Euclidean distance
def calculate_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def main():
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Create variables
    employees = list(starting_positions.keys())
    calls = list(service_calls.keys())
    slots = ['9 AM', '11 AM', '1 PM', '3 PM', '5 PM']

    x = {}
    for employee in employees:
        for call in calls:
            x[employee, call] = solver.BoolVar('x[%s,%s]' % (employee, call))

    # Create constraints
    # Each service call is assigned to exactly one employee
    for call in calls:
        solver.Add(sum(x[employee, call] for employee in employees) == 1)

    # Each employee is assigned at most one service call per slot
    for employee in employees:
        for slot in slots:
            solver.Add(sum(x[employee, call] for call in calls if assigned_slots[call] == slot) <= 1)

    # Objective function: Minimize total travel distance
    objective = solver.Objective()
    for employee in employees:
        for call in calls:
            objective.SetCoefficient(x[employee, call], calculate_distance(starting_positions[employee], service_calls[call]))

    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Total travel distance:', objective.Value())
        print('Assignment:')
        for employee in employees:
            for call in calls:
                if x[employee, call].solution_value() > 0:
                    print(f'{employee} -> {call} ({assigned_slots[call]})')

if __name__ == '__main__':
    main()
