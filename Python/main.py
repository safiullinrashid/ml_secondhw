import pygame
import math

# Инициализация Pygame
pygame.init()

# Создание окна
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("DBSCAN Clustering")

# Цвета
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_yellow = (255, 255, 0)
color_blue = (0, 0, 255)
cluster_colors = [color_red, color_green, color_blue, color_yellow, (255, 0, 255), (0, 255, 255)]  # Цвета для кластеров

# Список точек
list_of_dots = []

# Класс для представления точки
class Dot:
    def __init__(self, x_coord, y_coord):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.cluster_id = None  # Кластер, к которому принадлежит точка (None, если не определен)
        self.dot_color = color_black  # Цвет "флажка" для точки

    def __repr__(self):
        return f"Dot({self.x_coord}, {self.y_coord})"

# Функция для отрисовки точек
def draw_dots():
    for dot in list_of_dots:
        color = dot.dot_color if dot.cluster_id is None else cluster_colors[dot.cluster_id % len(cluster_colors)]
        pygame.draw.circle(window, color, (dot.x_coord, dot.y_coord), 3)

# Функция для вычисления евклидова расстояния между двумя точками
def euclidean_distance(dot1, dot2):
    return math.sqrt((dot1.x_coord - dot2.x_coord)**2 + (dot1.y_coord - dot2.y_coord)**2)

# Функция для поиска всех точек в заданном радиусе eps от точки d
def region_query(dot, eps):
    neighbors = []
    for neighbor_dot in list_of_dots:
        if euclidean_distance(dot, neighbor_dot) <= eps:
            neighbors.append(neighbor_dot)
    return neighbors

# Функция для расширения кластера
def expand_cluster(dot, neighbors, cluster_id, eps, min_pts):
    cluster = [dot]
    for neighbor in neighbors:
        if neighbor.cluster_id is None:  # Если точка не принадлежит ни одному кластеру
            neighbor.cluster_id = cluster_id  # Добавляем ее в текущий кластер
            cluster.append(neighbor)
            neighbor_neighbors = region_query(neighbor, eps)
            if len(neighbor_neighbors) >= min_pts:
                neighbors.extend(neighbor_neighbors)
    return cluster

# Функция для кластеризации точек с помощью DBSCAN
def dbscan(eps, min_pts):
    cluster_id = 0
    for dot in list_of_dots:
        if dot.cluster_id is None:  # Если точка не принадлежит ни одному кластеру
            neighbors = region_query(dot, eps)
            if len(neighbors) >= min_pts:  # Если точка является ядром
                dot.dot_color = color_green  # Выдаем зеленый "флажок"
                cluster = expand_cluster(dot, neighbors, cluster_id, eps, min_pts)
                for d in cluster:
                    d.cluster_id = cluster_id
                    d.dot_color = color_green  # Выдаем зеленый "флажок" всем точкам в кластере
                cluster_id += 1
            else:  # Если точка является шумом
                dot.dot_color = color_yellow  # Выдаем желтый "флажок"
                dot.cluster_id = -1  # Помечаем ее как шум

# Функция для выдачи "флажков" точкам
def assign_flags():
    for dot in list_of_dots:
        if dot.cluster_id is None:
            dot.dot_color = color_red  # Выдаем красный "флажок" неклассифицированным точкам

# Главный цикл
running = True
flagging_mode = False  # Флаг для режима выдачи "флажков"
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:

    # Добавление новой точки при нажатии мыши
            x, y = event.pos
            new_dot = Dot(x, y)
            list_of_dots.append(new_dot)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flagging_mode = True  # Включаем режим выдачи "флажков"

                assign_flags()  # Выдаем "флажки" точкам
                dbscan(20, 3)  # Запускаем алгоритм DBSCAN

    # Очистка экрана
    window.fill(color_white)

    # Отрисовка точек
    draw_dots()

    # Обновление экрана
    pygame.display.flip()

    # Выход из режима выдачи "флажков"
    if flagging_mode:
        flagging_mode = False

# Завершение Pygame
pygame.quit()

