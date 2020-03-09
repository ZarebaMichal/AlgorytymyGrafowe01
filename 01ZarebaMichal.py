from string import ascii_lowercase




def list_to_float_list(list):
    float_list = []
    for element in list:
        if element == '-':
            float_list.append(float('inf'))
        else:
            float_list.append(float(element))
    return float_list


def weight_matrix_to_list(file_name):
    weight_matrix = []
    with open(file_name) as file:
        number_of_vertices = int(next(file))
        count = 0
        while count < number_of_vertices:
            count += 1
            list = file.readline().split()
            weight_matrix.append(list_to_float_list(list))
    return weight_matrix


def create_vertices_list(weight_matrix):
    vertices_list = []
    for i in range(len(weight_matrix)):
        vertices_list.append(ascii_lowercase[i])
    return vertices_list


def remove_reversed_duplicates(iterable):
    seen = set()
    for item in iterable:
        tup = tuple(item)
        if tup not in seen:
            seen.add(tup[::-1])
            yield item


def create_edges_list(weight_matrix, vertices_list):
    edge_list = []
    for i, weights in enumerate(weight_matrix):
        for x, weight in enumerate(weights):
            if weight != float('inf'):
                edge = []
                edge.append(vertices_list[i])
                edge.append(vertices_list[x])
                edge_list.append(edge)
    edge_list = list(remove_reversed_duplicates(edge_list))
    return edge_list


def create_edges_weight_list(edge_list, weight_list, vertices_list):
    position_of_weight = []
    edges_weights = []
    for edge in edge_list:
        for vertice in edge:
            position_of_weight.append(vertices_list.index(vertice))
        edges_weights.append(weight_matrix[position_of_weight[0]][position_of_weight[1]])
        del position_of_weight[:]
    return edges_weights


def edges_weight_list_to_dict(edge_list, edges_weights):
    tuple_of_edges =  ()
    for edge in edge_list:
        tuplex = tuple(edge)
        tuple_of_edges = (tuple_of_edges) + (tuplex,)
    tuple_of_weights = tuple(edges_weights)
    zip_obj = zip(tuple_of_edges, tuple_of_weights)
    dict_of_edges_and_weights = dict(zip_obj)
    return dict_of_edges_and_weights


def create_adjacency_dictionary(weight_matrix):
    adjacency_dictionary = {}
    for i, row in enumerate(weight_matrix):
        vertice_number = i+1
        adjacency_list = []
        for x, vertice in enumerate(row):
            if vertice != float('inf'):
                adjacency_list.append(x+1)
        adjacency_dictionary[vertice_number] = adjacency_list
    return adjacency_dictionary


def create_edge_list_numbered(edge_list):
    edge_list_numbers = []
    for edge in edge_list:
        edge_in_numbers = []
        for letter in edge:
            number = ord(letter) - 96
            edge_in_numbers.append(number)
        edge_list_numbers.append(edge_in_numbers)
    return edge_list_numbers


def create_graph_dictionary(weight_matrix, adjacency_dictionary, dictionary_of_edges_and_weights_numbered):
    graph_dictionary = {}
    for x, i in enumerate(weight_matrix):
        adjacency_weights_dictionary = {}
        vertice = x + 1
        adjacencies = adjacency_dictionary[vertice]
        for adjacency in adjacencies:
            if (vertice, adjacency) in dictionary_of_edges_and_weights_numbered:
                weight = dictionary_of_edges_and_weights_numbered[vertice, adjacency]
            else:
                weight = dictionary_of_edges_and_weights_numbered[adjacency, vertice]
            adjacency_weights_dictionary[adjacency] = weight
        graph_dictionary[vertice] = adjacency_weights_dictionary
    return graph_dictionary


def print_adjancency(adjacency_dictionary):
    print("Lista nastepnikow: ")
    for vertice in adjacency_dictionary:
        print(vertice, ":", *adjacency_dictionary[vertice], sep=" ")


def get_other_edges(filename):
    other_edges = []
    with open(file_name) as file:
        number_of_lines = int(next(file))
        for i in range(number_of_lines):
            next(file)
        for line in file:
            other_edges.append(line.split())
    return other_edges


def remove_edge_from_graph(vertice1, vertice2, graph_dictionary):
    del graph_dictionary[vertice1][vertice2]
    del graph_dictionary[vertice2][vertice1]
    return graph_dictionary


def add_edge_to_graph(vertice1, vertice2, graph_dictionary):
    graph_dictionary[vertice1][vertice2] = float(3.0)
    graph_dictionary[vertice2][vertice1] = float(3.0)
    return graph_dictionary


def check_if_edge_in_graph_and_edit(graph_dictionary, other_edges):
    for edge in other_edges:
        vertice1 = int(edge[0])
        vertice2 = int(edge[1])
        try:
            x = graph_dictionary[vertice1][vertice2]
        except KeyError:
            graph_dictionary = add_edge_to_graph(vertice1, vertice2, graph_dictionary)
        else:
            graph_dictionary = remove_edge_from_graph(vertice1, vertice2, graph_dictionary)
    return graph_dictionary


def check_if_edge_in_adjacency_and_edit(other_edges, adjacency_dictionary):
    for edge in other_edges:
        vertice1 = int(edge[0])
        vertice2 = int(edge[1])
        adjacency = adjacency_dictionary[vertice1]
        for vertice in adjacency:
            if vertice == vertice2:
                adjacency.remove(vertice)
                break
            else:
                adjacency.append(vertice2)
                adjacency.sort()
                break
        adjacency = adjacency_dictionary[vertice2]
        for vertice in adjacency:
            if vertice == vertice1:
                adjacency.remove(vertice)
                break
            else:
                adjacency.append(vertice1)
                adjacency.sort()
                break
    return adjacency_dictionary


def check_if_edge_in_dict_of_weights_and_edit(other_edges, dictionary_of_edges_and_weights_numbered):
    for edge in other_edges:
        vertice1 = int(edge[0])
        vertice2 = int(edge[1])
        integer_list = []
        integer_list.append(vertice1)
        integer_list.append(vertice2)
        tuplex = tuple(integer_list)
        try:
            x = dictionary_of_edges_and_weights_numbered[tuplex]
        except KeyError:
            dictionary_of_edges_and_weights_numbered[tuplex] = float(3.0)
        else:
            del dictionary_of_edges_and_weights_numbered[tuplex]
    return dictionary_of_edges_and_weights_numbered


file_name = 'graph.txt'
vertices_list = create_vertices_list(weight_matrix_to_list(file_name))
weight_matrix = weight_matrix_to_list(file_name)
edge_list = create_edges_list(weight_matrix, vertices_list)
edge_list_numbered = create_edge_list_numbered(edge_list)
edges_weights = create_edges_weight_list(edge_list, weight_matrix, vertices_list)
dict_of_edges_and_weights = edges_weight_list_to_dict(edge_list, edges_weights)
adjacency_dictionary = create_adjacency_dictionary(weight_matrix)
dictionary_of_edges_and_weights_numbered = edges_weight_list_to_dict(edge_list_numbered, edges_weights)
graph_dictionary = create_graph_dictionary(weight_matrix, adjacency_dictionary, dictionary_of_edges_and_weights_numbered)
print(adjacency_dictionary)
print(graph_dictionary)
print(dictionary_of_edges_and_weights_numbered)
print_adjancency(adjacency_dictionary)


other_edges = get_other_edges(file_name)
graph_dictionary = check_if_edge_in_graph_and_edit(graph_dictionary, other_edges)
adjacency_dictionary = check_if_edge_in_adjacency_and_edit(other_edges, adjacency_dictionary)
dictionary_of_edges_and_weights_numbered = check_if_edge_in_dict_of_weights_and_edit(other_edges, dictionary_of_edges_and_weights_numbered)
print(adjacency_dictionary)
print(graph_dictionary)
print(dictionary_of_edges_and_weights_numbered)
print_adjancency(adjacency_dictionary)
