

class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints


def revise(csp, xi, xj):
    revised = False
    for x in csp.domains[xi]:
        if not any(csp.constraints(xi, x, xj, y) for y in csp.domains[xj]):
            csp.domains[xi].remove(x)
            revised = True
    return revised


def ac3(csp, queue=None):
    if queue is None:
        queue = [(xi, xj) for xi in csp.variables for xj in csp.neighbors[xi]]

    while queue:
        (xi, xj) = queue.pop(0)
        if revise(csp, xi, xj):
            if not csp.domains[xi]:
                return False
            for xk in csp.neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True


def minimum_remaining_values(csp, assignment):
    unassigned_vars = [var for var in csp.variables if assignment[var] is None]
    mrv_var = min(unassigned_vars, key=lambda var: len(csp.domains[var]))
    return mrv_var

finalResult  = [] 
def backtracking_search(csp):

    #storing the all the steps involved 
    

    # Initialize variables and domains
    assignment = {}
    for var in csp.variables:
        assignment[var] = None

    domains = {}
    for var in csp.variables:
        domains[var] = set(csp.domains[var])

    # Initialize failed values for each variable
    failed_values = {}
    for var in csp.variables:
        failed_values[var] = set()

    # Perform AC-3 to ensure arc consistency
    if not ac3(csp):
        return None, None, None

    # Define recursive helper function
    def backtrack(assignment, domains, failed_values, order):
        # Check if all variables are assigned
        if all(assignment.values()):
            return assignment, order, domains

        # Choose unassigned variable with minimum remaining values
        var = minimum_remaining_values(csp, assignment)

        # Try each value in the domain of the selected variable
        for value in domains[var]:
            # Check if value has already failed
            if value in failed_values[var]:
                continue

            # Assign value to variable and remove it from domain
            assignment[var] = value
            domains[var].remove(value)
            order.append(var)

            # Perform AC-3 to ensure arc consistency
            if ac3(csp, [(var, neighbor) for neighbor in csp.neighbors[var]]):
                # Recursively backtrack to assign remaining variables
                result = backtrack(assignment, domains, failed_values, order)
                if result:
                    # print("---------------result------------------")
                    # print(result)
                    
                    finalResult.append(result[0])
                    return result
                   
            # If AC-3 fails, add value to list of failed values for variable
            failed_values[var].add(value)

            # Unassign variable and restore its domain
            assignment[var] = None
            domains[var].add(value)
            order.pop()

        # If no value works for the variable, return failure
        return None

    # Call recursive helper function to start search
    order = []
    result =  backtrack(assignment, domains, failed_values, order)
  
    return result


def get_neighbors(variable):
    row = variable[0]
    col = variable[1]
    neighbors = set()

    # Add all variables in same row
    for c in range(9):
        if (row, c) != (row, col):
            neighbors.add((row, c))

    # Add all variables in same column
    for r in range(9):
        if (r, col) != (row, col):
            neighbors.add((r, col))

    # Add all variables in same 3x3 square
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if (r, c) != (row, col):
                neighbors.add((r, c))

    return neighbors


def sudoku_constraint(xi, x, xj, y):
    if xi[0] == xj[0]:  # same row
        return x != y
    if xi[1] == xj[1]:  # same column
        return x != y
    if xi[0] // 3 == xj[0] // 3 and xi[1] // 3 == xj[1] // 3:  # same box
        return x != y
    if x == y:  # same value
        return False
    return True


def solve_sudoku(puzzle):
    # Convert puzzle to a dict with tuple keys
    puzzle = {(row, col): puzzle[row][col] for row in range(9) for col in range(9)}

    # Define the variables and domains for the CSP
    variables = puzzle.keys()
    domains = {var: list(range(1, 10)) if puzzle[var] == 0 else [puzzle[var]] for var in variables}

    # Define the neighbors for each variable
    neighbors = {var: get_neighbors(var) for var in variables}

    # Define the constraints for the CSP
    constraints = lambda xi, x, xj, y: x != y


    # Create the CSP object
    csp = CSP(variables, domains, neighbors, constraints)

    # Use AC3 to reduce the domains of the variables
    ac3(csp, [(var, neighbor) for var in variables for neighbor in neighbors[var]])

    # Use backtracking to solve the CSP
    return backtracking_search(csp)


# Call the solve_sudoku function with the puzzle as an argument

def formatTheOutput(data):
    solutionMatrix   = [[] for i in range(9)]
    for j in data:
        solutionMatrix[j[0]].append(data[j])
    return solutionMatrix
def formateOutputStep6(data):
    temp = [ [set() for i in range(9)] for i in range (9)] 
    for i in range(len(data)):
        for j in range(len(data[i])):
            for k in range(len(data[i][j])):
                temp[j][k].add(data[i][j][k])
    return temp 
def startSolver(puzzle):
    data  = solve_sudoku(puzzle)
    return formatTheOutput(data[0])

