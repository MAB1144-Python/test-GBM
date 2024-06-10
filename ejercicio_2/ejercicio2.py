def process_case(case):
    # Extract the number of Grand Prix and pilots
    G, P = case[0]
    
    # Extract race results
    races = case[1:G+1]
    
    # Extract the number of scoring systems
    S = case[G+1][0]
    
    # Extract scoring systems
    scoring_systems = case[G+2:G+2+S]
    
    return G, P, races, S, scoring_systems

def calculate_points(G, P, races, scoring_system):
    K = scoring_system[0]
    points = scoring_system[1:K+1]
    total_points = [0] * P
    
    for race in races:
        for pilot in range(P):
            position = race[pilot]
            if position <= K:
                total_points[pilot] += points[position-1]
    
    return total_points

def find_winners(total_points):
    max_points = max(total_points)
    winners = [i + 1 for i, points in enumerate(total_points) if points == max_points]
    return winners

def main():
    # Caso de prueba
    casos = list([
    [1, 3],
    [3, 2, 1],  # piloto 1 llegó de tercero, piloto 2 llegó de segundo y piloto 3 llegó de primero
    [3],        # número de sistemas de puntuación
    [3, 5, 3, 2],  # primer sistema de puntuación
    [3, 5, 3, 1],  # segundo sistema de puntuación
    [3, 1, 1, 1],   # tercer sistema de puntuación
    [3,10],
    [1,2,3,4,5,6,7,8,9,10],
    [10,1,2,3,4,5,6,7,8,9],
    [9,10,1,2,3,4,5,6,7,8,],
    [2],
    [5,5,4,3,2,1],
    [3,10,5,1],
    [2,4],
    [1,3,4,2],
    [4,1,3,2],
    [2],
    [3,3,2,1],
    [3,5,4,2],
    [0,0]]) #caso de salida
    # Procesar el caso de prueba
    i=int(0)
    j=int(0)
    caso = True
    while casos[:][i] != [0,0]:
        GP = []
        GP.append(casos[:][i])
        while len(casos[:][i]) != 2:
            i+=1
        j = i+1
        while len(casos[:][j]) != 2:
            GP.append(casos[:][j])
            j+=1
        j-=1
        i = j+1

        G, P, races, S, scoring_systems = process_case(GP)
        
        for scoring_system in scoring_systems:
            total_points = calculate_points(G, P, races, scoring_system)
            winners = find_winners(total_points)
            print(' '.join(map(str, winners)))

if __name__ == "__main__":
    main()