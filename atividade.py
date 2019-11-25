import math
import random
from matplotlib import pyplot as plt
def scalar_multiply (escalar, vetor):
    return [escalar * i for i in vetor]
 
def vector_sum (vetores):
    resultado = vetores[0]
    for vetor in vetores[1:]:
        resultado = [resultado[i] + vetor[i] for i in range (len(resultado))]
    return resultado
 
def vector_mean (vetores):
    return scalar_multiply (1/len(vetores), vector_sum(vetores))
 
 
def test_vector_mean ():
    a = [1, 2, 3]
    b = [1, 3, 2]
    c = [1, 1, 1]
    r = vector_mean ([a, b, c])
    for elemento in r:
        print (elemento)
 
def dot (v, w):
    return sum (v_i * w_i for v_i, w_i in zip (v, w))
 
def vector_subtract (v, w):
    return [v_i - w_i for v_i, w_i in zip (v, w)]
    
def sum_of_squares (v):
    return dot (v, v)
 
 
def squared_distance (v, w):
    return sum_of_squares (vector_subtract (v, w))
 
def distance (v, w):
    return math.sqrt (squared_distance(v, w))
 
 
class KMeans:
    def __init__ (self, k, means = None):
        self.k = k
        self.means = means
    def classify (self, ponto):
        return min (range (self.k), key= lambda i: distance (ponto, self.means[i]))
    def train (self, pontos):
        self.means = random.sample (pontos, self.k) if self.means == None else self.means
        assignments = None
        while True:
            new_assignments = list(map (self.classify, pontos))
            if new_assignments == assignments:
                return
            assignments = new_assignments
            for i in range (self.k):
                i_points = [p for p, a in zip (pontos, assignments) if a == i]
                if i_points:
                    self.means[i] = vector_mean (i_points)
 
 
 
def gera_base (n):
    base = []
    for _ in range (n // 3):
        x = random.randint (-50, -40)
        y = random.randint (0, 10)
        while (x, y) in base:
            x = random.randint (-50, -40)
            y = random.randint (0, 10)
        base.append((x, y))
    
    for _ in range (n // 3):
        x = random.randint(-40, -10)
        y = random.randint(-10, 0)
        while (x, y) in base:
            x = random.randint(-40, -10)
            y = random.randint(-10, 0)
        base.append((x, y))
 
    for _ in range (n // 3):
        x = random.randint(10, 20)
        y = random.randint(10, 20)
        while (x, y) in base:
            x = random.randint(10, 20)
            y = random.randint(10, 20)
        base.append((x, y))
    return base
 
def test_gera_base():
    base = gera_base (12)
    for elemento in base:
        print (elemento)
    
 
def calcula_somatorio_de_distancias (base, kmeans):
    soma = 0
    for instancia in base:
        dist = distance (instancia, kmeans.means[0])
        for centroide in kmeans.means[1:]:
            if distance (instancia, centroide) < dist:
                dist = distance (instancia, centroide)
        soma += dist    
    return soma
 
 
def test_calcula_somatorio_de_distancias ():
    base = gera_base (3)
    kmeans =  KMeans (3)
    kmeans.train(base)
    print (f'Total: {calcula_somatorio_de_distancias(base, kmeans):.2f}')
 
def exibe_grafico (base, representantes=[], distancia=-1):
    g1_x = [v[0] for v in base[:len(base) // 3]]
    g1_y = [v[1] for v in base[:len (base) // 3]]
 
    g2_x = [v[0] for v in base[len(base) // 3:len(base) // 3 * 2]]
    g2_y = [v[1] for v in base[len(base) // 3:len(base) // 3 * 2]]
    
    g3_x = [v[0] for v in base[len(base) // 3 * 2:]]
    g3_y = [v[1] for v in base[len(base) // 3 * 2:]]
 
    plt.scatter (g1_x, g1_y, marker='8')
    plt.scatter (g2_x, g2_y, marker='D')
    plt.scatter (g3_x, g3_y, marker='^')
 
    for representante in representantes:
        plt.scatter (representante[0], representante[1], marker="$+$")
    
    plt.title (f'Somatório de distâncias: {distancia:.2f}')
 
    plt.show()
    
def test_exibe_grafico ():
    base = gera_base (12)
    exibe_grafico(base)
 
def test_final ():
    base = gera_base (90)
    kmeans = KMeans (90)
    kmeans.train(base)
    distancia = calcula_somatorio_de_distancias(base, kmeans)
    exibe_grafico(base, kmeans.means, distancia)
	

	
# Implemente a seguinte função. Para cada valor de k (a partir de 2), ela executa o algoritmo 
# KMeans i vezes e utiliza a função da aula de cálculo de distâncias, a fim de obter a distância
# média, m. Ela deve devolver o menor valor de k tal que m < limiar.
def obtem_melhor_k (base, i, limiar):
    distancia = limiar
    n = 2
    while distancia >= limiar:
        k = n
        distancia = 0
        for _ in range(i):
            kmeans = KMeans(k)
            kmeans.train(base)
            distancia += calcula_somatorio_de_distancias(base, kmeans)
        distancia /= i
        n += 1
        #print(f' Valor de k: {k}')
        #print(f' Distância média: {distancia:.2f}')
    #print(f' Valor de k: {k}')
    print(f'O Valor de k = {k}, que mais se aproxima do limite {limiar} aponta uma distância média: {distancia:.2f}')
    return k

def test_obtem_melhor_k ():
    base = gera_base (120)
    obtem_melhor_k (base, 5, 1000)


 
 
def main ():
    test_final()
    #test_exibe_grafico()
    #test_calcula_somatorio_de_distancias()
    #test_gera_base() 
	test_obtem_melhor_k ()
main()