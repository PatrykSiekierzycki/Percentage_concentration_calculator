import usefull_functions as uf


"""
Brief: Calculate and return percentage concentration of solution by mass.
Param: 
    mass_of_solut: int/float
    mass_of_solution: int/float
Return:
    percentage_concentration: float
"""
def calculate_percentage_concentration(mass_of_solut, mass_of_solution):
    
    proper_dtypes = [int, float]

    if type(mass_of_solut) not in proper_dtypes or type(mass_of_solution) not in proper_dtypes:
        print("Wrong data type. Expected for both arguments: float type.")
        uf.waitForEnter()
        exit(1)
    
    if type(mass_of_solut) is int:
        mass_of_solut = float(mass_of_solut)
    if type(mass_of_solution) is int:
        mass_of_solution = float(mass_of_solution)

    percentage_concentration = (mass_of_solut * 100.0)/mass_of_solution
    
    return percentage_concentration

"""
Brief: Calculate and return mass of solut.
Param:
    percentage_concentration: int/float
    mass_of_solution: int/float
Return:
    mass_of_solut: float
"""
def calculate_mass_of_solut(percentage_concentration, mass_of_solution):
    
    proper_dtypes = [int, float]

    if type(percentage_concentration) not in proper_dtypes or type(mass_of_solution) not in proper_dtypes:
        print("Wrong data type. Expected for both arguments: float type.")
        uf.waitForEnter()
        exit(1)
    
    if type(percentage_concentration) is int:
        percentage_concentration = float(percentage_concentration)
    if type(mass_of_solution) is int:
        mass_of_solution = float(mass_of_solution)

    mass_of_solut = (percentage_concentration * mass_of_solution) / 100
    
    return mass_of_solut

"""
Brief: Calculate and return mass of solution.
Param:
    mass_of_solut: int/float
    percentage_concentration: int/float
Return:
    mass_of_solution: float
"""
def calculate_mass_of_solution(mass_of_solut, percentage_concentration):
    
    proper_dtypes = [int, float]

    if type(mass_of_solut) not in proper_dtypes or type(percentage_concentration) not in proper_dtypes:
        print("Wrong data type. Expected for both arguments: float type.")
        uf.waitForEnter()
        exit(1)
    
    if type(mass_of_solut) is int:
        mass_of_solut = float(mass_of_solut)
    if type(percentage_concentration) is int:
        percentage_concentration = float(percentage_concentration)

    mass_of_solution = (mass_of_solut * 100) / percentage_concentration
    
    return mass_of_solution

"""
Brief: take data and preper them for other functions.
Param:
    concentration_1: int
    concentration_2: int
    expected_concentration: int
Return:
    tuple
"""
def cross_rule(concentration_1, concentration_2, expected_concentration):

    flag_reverse = False

    if concentration_1 < concentration_2:

        flag_reverse = True

        buffor = concentration_1
        concentration_1 = concentration_2
        concentration_2 = buffor
        del buffor

    first_proportion = abs(concentration_1 - expected_concentration)
    second_proportion = abs(concentration_2 - expected_concentration)

    # Eventually shorten proportion:
    can_shorten = is_possible_to_shorten_proportion(first_proportion, second_proportion)
    if can_shorten is True:
        proportions = shorten_proportion(first_proportion, second_proportion)
        first_proportion = proportions[0]
        second_proportion = proportions[1]
    
    # Eventually reverse proportion:
    if flag_reverse:
        buffor = first_proportion
        first_proportion = second_proportion
        second_proportion = buffor
        del buffor
    
    return first_proportion, second_proportion

"""
Brief: Method check is it possible to shorten proportion.
Param:
    concentration_1: int
    concentration_2: int
Return: Bool:
    flag: bool
        True - if it is possible to shorten.
        False - if it is not possible to shorten.
"""
def is_possible_to_shorten_proportion(concentration_1, concentration_2):

    flag = False

    for number in range(2, concentration_2 + 1):
        if concentration_1 % number == 0 and concentration_2 % number == 0:
            flag = True

    return flag

"""
Brief: Method to shorten proportions.
Param:
    concentration_1: int
    concentration_2: int
Return: 
    int - proportion for first solution.
    int - proportion for second solution.
"""
def shorten_proportion(concentration_1, concentration_2):

    while is_possible_to_shorten_proportion(concentration_1, concentration_2):

        if concentration_1 == concentration_2:
            return 1, 1
        for number in range(1, concentration_1):

            if concentration_1 % number == 0 and concentration_2 % number == 0:
                concentration_1 = int(concentration_1 / number)
                concentration_2 = int(concentration_2 / number)

    return concentration_1, concentration_2