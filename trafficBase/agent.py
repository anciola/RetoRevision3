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
    def __init__(self, unique_id, pos, model):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.id = unique_id
        self.model = model
        self.pos = pos
        self.direccion = None

    # funcion de movimiento
    def move(self, pos):
        """
        moves the car on the road
        """
        # Checks which grid cells are empty
        #freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        #next_moves = [p for p, f in
                      #zip(possible_steps, freeSpaces)
                      #if f]
        #vecinos = self.model.grid.get_neighborhood(
        #    self.pos,
        #    moore=False,  # Boolean for whether to use
                          # Moore neighborhood (including diagonals) or
                          # Von Neumann (only up/down/left/right).
        #    include_center=False)
        
        # posiciones_siguientes = []
        # for posicion in vecinos:
        #     contenidos = self.model.grid.get_cell_list_contents([posicion])
        #     print('contenidos de posicion' +
        #           str(posicion) + ": " + str(contenidos))
        #     calles = [obj for obj in contenidos if isinstance(obj, Road)]
        #     if calles < 0:
        #         posiciones_siguientes.append(posicion)

        # siguiente = self.random.choice(posiciones_siguientes)
        self.model.grid.move_agent(self, pos)
        
        #next_move = self.random.choice(next_moves)
        # Now move:
        #if self.random.random() < 0.1:
            #self.model.grid.move_agent(self, next_move)
            #self.steps_taken += 1

        # If the cell is empty, moves the agent to that cell;
        # otherwise, it stays at the same position
        #if freeSpaces[self.direction]:


    # funcion de paso
    def step(self):
        """
        Determines the new direction it will take, and then moves
        """
        print("soy el coche" + str(self.id))
        print("estoy en " + str(self.pos))

        # Leer Ubicacion actual
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        (x, y) = self.pos


        calle = [obj for obj in this_cell if isinstance(obj, Road)]
        if len(calle) != 0:
            calle = calle[0]
            if calle.direction == "Left":
                x -= 1
                self.direccion = "Left"
            elif calle.direction == "Right":
                x += 1
                self.direccion = "Right"
            elif calle.direction == "Up":
                y += 1
                self.direccion = "Up"
            elif calle.direction == "Down":
                y += 1
                self.direccion = "Down"

            if x < self.model.width and y < self.model.height:
                siguiente_posicion = (x, y)
            else:
                siguiente_posicion = self.pos
            
            contenidos = self.model.grid.get_cell_list_contents([siguiente_posicion])
            auto = [obj for obj in contenidos if isinstance(obj, Car)]
            semaforo = [obj for obj in contenidos if isinstance(obj, Traffic_Light)]
            if len(semaforo) == 0:
                if len(auto) == 0:
                    self.move(siguiente_posicion)
                else:
                    print('Hay un auto, no me puedo mover')
                    # checar opcion rebasar:
                    # diagonal enfrente, diagonal atras, a un lado todas vacias
            else:
                semaforo = semaforo[0]
                print('Hay un semaforo, prefiero no jugarmela')
                if semaforo.color == True:
                    self.move(siguiente_posicion)
                else:
                    print("el semaforo esta en rojo, no me puedo mover")
        
        semaforo = [obj for obj in this_cell if isinstance(obj, Traffic_Light)]
        if len(semaforo) != 0:
            if self.direccion == "Left":
                self.move((x-1, y))
            if self.direccion == "Right":
                self.move((x+1, y))
            if self.direccion == "Up":
                self.move((x, y+1))
            if self.direccion == "Down":
                self.move((x, y-1))
        

        #       si si esta/no esta/ hay semaforo
        #       se mueve, no se mueve,
        #       checa estado del semaforo
        #           si es verde/rojo
        #           avanza/ no avanza
        #
        # self.direction = self.random.randint(0,8)
        # print(f"Agente: {self.unique_id} movimiento {self.direction}")

        #espacio_libre = cell is empty (posicion)
        #if semaforo.color = True and espacio_libre:
        #self.move()
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
        self.recien_creo = False
        self.model = model
        self.id = unique_id

    def step(self):
        # obten estado de calles vecinas
        vecinos = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,  # Boolean for whether to use
                          # Moore neighborhood (including diagonals) or
                          # Von Neumann (only up/down/left/right).
            include_center=False)

        print('vecinos:' + str(vecinos))

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
                    if self.recien_creo == False:
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
                    # print('no encuentro nada')
                    
                    if flip:
                        print('auto generado! en ' + str(posicion))
                        print()
                        car = Car(self.model.next_id(), posicion, self.model)
                        self.model.grid.place_agent(car, posicion)
                        self.model.schedule.add(car)
                        self.recien_creo = True

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
        self.model = model

    def step(self):
        pass
