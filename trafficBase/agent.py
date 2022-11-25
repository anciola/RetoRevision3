from mesa import Agent

# Clase de Auto
class Car(Agent):
    """
    Car
    Attributes:
        unique_id: Agent's ID
        direction:
        read the direction on the road
    """
    def __init__(self, unique_id, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)

    # funcion de movimiento
    def move(self):
        """
        Determines if the agent can move in the direction that was chosen
        """
        #possible_steps = self.model.grid.get_neighborhood(
            #self.pos,
            #moore=True,  # Boolean for whether to use
                         # Moore neighborhood (including diagonals) or
                         # Von Neumann (only up/down/left/right).
            #include_center=True)

        # Checks which grid cells are empty
        #freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        #next_moves = [p for p, f in
                      #zip(possible_steps, freeSpaces)
                      #if f]

        #next_move = self.random.choice(next_moves)
        # Now move:
        #if self.random.random() < 0.1:
            #self.model.grid.move_agent(self, next_move)
            #self.steps_taken += 1

        # If the cell is empty, moves the agent to that cell;
        # otherwise, it stays at the same position
        #if freeSpaces[self.direction]:

        vecinos = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,  # Boolean for whether to use
                          # Moore neighborhood (including diagonals) or
                          # Von Neumann (only up/down/left/right).
            include_center=False)
        
        posiciones_siguientes = []

        for posicion in vecinos:
            contenidos = self.model.grid.get_cell_list_contents([posicion])
            print('contenidos de posicion' + str(posicion) + ": " + str(contenidos))
            calles = [obj for obj in contenidos if isinstance(obj, Road)]
            if calles < 0:
                posiciones_siguientes.append(posicion)
        
        siguiente = self.random.choice(posiciones_siguientes)
        self.model.grid.move_agent(self, siguiente)

    # funcion de paso
    def step(self):
        """
        Determines the new direction it will take, and then moves
        """
        # Leer Direccion de calle en esa ubicacion,
        # checa si esta la celda a la que apunta esta vacia 
        #       si si esta/no esta/ hay semaforo
        #       se mueve, no se mueve,
        #       checa estado del semaforo
        #           si es verde/rojo
        #           avanza/ no avanza
        #
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()
        # pass

# Clase de Semaforo
class Traffic_Light(Agent):
    """
    Traffic Light agent. Tells Cars When They Can Cross And When They Cant
    """
    def __init__(self, unique_id, model, color=False, timeToChange=10):
        super().__init__(unique_id, model)
        self.color = color
        self.timeToChange = timeToChange

    def step(self):
        # modificarlo para que en vez de ser fijo, dependa de si hay coches vecinos o no, 
        # que se coordinen entre los de la misma interseccion para que solo uno este prendido a la vez
        if self.model.schedule.steps % self.timeToChange == 0:
            self.color = not self.color
        # pass

# Clase de Destino
class Destination(Agent):
    """
    Destination agent. Spawns and absorbs Cars.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        # obten estado de calles vecinas
        vecinos = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,  # Boolean for whether to use
                          # Moore neighborhood (including diagonals) or
                          # Von Neumann (only up/down/left/right).
            include_center=False)

        print('vecinos:' + str(vecinos) )

        for posicion in vecinos:
            contenidos = self.model.grid.get_cell_list_contents([posicion])
            print('contenidos de posicion' + str(posicion) + ": " + str(contenidos))
            # checar si hay autos
            calles = [obj for obj in contenidos if isinstance(obj, Road)]
            print('calles: ' + str(calles))
            coches = [obj for obj in contenidos if isinstance(obj, Car)]
            flip = self.random.choice([0, 1])
            if len(calles) > 0:
                if len(coches) > 0:
                    # si hay un coche:
                    # obtener ese objeto
                    # si 0 / 1 -> quita o no ese coche
                    print('AUTO ENCONTRADO')
                    if flip:
                        print('LO MATE')
                        contenidos = self.model.grid.get_cell_list_contents(posicion)
                        coches = [obj for obj in contenidos if isinstance(obj, Car)]
                        car = coches[0]
                        self.model.grid.remove_agent(car, posicion)
                        self.schedule.remove(car, posicion)
                else:
                    # si estan vacias:
                    # si 0 / 1 -> pones o no pones coche
                    #print('no encuentro nada')
                    if flip:
                        print('hubiera generado uno')
                        print()
                        car = Car(posicion, self)
                        self.model.grid.place_agent(car, posicion)
                        self.model.schedule.add(car)
        # pass

# Clase de Obstaculo
class Obstacle(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        pass

# Clase de Calle
class Road(Agent):
    """
    Road agent. Tells Cars Where they Should Move Next.
    """
    def __init__(self, unique_id, model, direction="Left"):
        super().__init__(unique_id, model)
        self.direction = direction

    def step(self):
        pass
