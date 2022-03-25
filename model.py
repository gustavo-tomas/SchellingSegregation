from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.batchrunner import BatchRunner
from mesa.datacollection import DataCollector
from datetime import datetime
from random import seed
from random import random

class SchellingAgent(Agent):
    """
    Schelling segregation agent
    """

    def __init__(self, pos, model, agent_type):
        """
        Create a new Schelling agent.

        Args:
           unique_id: Unique identifier for the agent.
           x, y: Agent initial location.
           agent_type: Indicator for the agent's type (minority=1, majority=0)
        """
        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    def step(self):
        similar = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1
        
        # gera um numero aleatorio que representa o medo dos agentes
        # seed(1)
        self.fear = random()

        # If unhappy, move: por falta de vizinhos semelhantes ou muito medo
        if similar < self.model.homophily or self.fear > self.model.fear:
            self.model.grid.move_to_empty(self)
        # contabiliza agentes felizes
        else:
            self.model.happy += 1
            if self.type == 1:
                self.model.happy_blue_agents_count += 1
            else:
                self.model.happy_red_agents_count += 1


class Schelling(Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height=20, width=20, density=0.8, minority_pc=0.2, homophily=3, fear=0.8):

        self.total_satisfaction_index = 0 # o indice total de agentes satisfeitos
        self.blue_satisfaction_index  = 0 # o indice de agentes azuis satisfeitos
        self.red_satisfaction_index   = 0 # o indice de agentes vermelhos satisfeitos
        self.total_blue_agents_count  = 0 # o total de agentes azuis
        self.total_red_agents_count   = 0 # o total de agentes vermelhos
        self.happy_blue_agents_count  = 0 # o numero de agentes azuis felizes
        self.happy_red_agents_count   = 0 # o numero de agentes vermelhos felizes

        self.fear = fear                  # a medida de medo suportado
        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.happy = 0
        self.datacollector = DataCollector(
            {
                "happy": "happy",
                "total_satisfaction_index": lambda m: self.total_satisfaction_index,
                "blue_satisfaction_index": lambda m: self.blue_satisfaction_index,
                "red_satisfaction_index": lambda m: self.red_satisfaction_index,
            },
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_pc:
                    agent_type = 1
                    self.total_blue_agents_count += 1
                else:
                    agent_type = 0
                    self.total_red_agents_count += 1
                agent = SchellingAgent((x, y), self, agent_type)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)
        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """

        # calcula o indice de satisfacao dos azuis e vermelhos
        self.blue_satisfaction_index = float(self.happy_blue_agents_count / max(self.total_blue_agents_count, 1))
        self.red_satisfaction_index  = float(self.happy_red_agents_count / max(self.total_red_agents_count, 1))
        
        # calcula o indice de satisfacao total
        total_agents = self.total_blue_agents_count + self.total_red_agents_count
        happy_agents = self.happy_blue_agents_count + self.happy_red_agents_count
        self.total_satisfaction_index = float(happy_agents / total_agents)

        self.happy = 0  # Reset counter of happy agents
        self.happy_blue_agents_count = 0
        self.happy_red_agents_count = 0
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False

def happy(model):
    return model.happy

def density(model):
    return model.density

def minority_pc(model):
    return model.minority_pc

def homophily(model):
    return model.homophily

def fear(model):
    return model.fear

def total_satisfaction_index(model):
    return model.total_satisfaction_index

def blue_satisfaction_index(model):
    return model.blue_satisfaction_index

def red_satisfaction_index(model):
    return model.red_satisfaction_index

def batch_run():
    # a tolerancia e fixada para testar seus efeitos no modelo, principalmente sobre a 
    # variavel total satisfaction index e blue/red satisfaction index
    number_iterations = 200
    max_steps_per_simulation = 200
    fear_tolerance = 0.1

    fixed_params = {
        "height": 20,
        "width": 20,
        "fear": fear_tolerance
    }
    # densidade, fracao da minoria e homofilia sao testadas em intervalos de 4
    variable_params = {
        "density": [0.1, 0.2, 0.4, 0.8],
        "minority_pc": [0.1, 0.2, 0.4, 0.8],
        "homophily": [1, 3, 6, 7]
    }
    
    batch_run = BatchRunner(
        Schelling,
        variable_params,
        fixed_params,
        iterations=number_iterations,
        max_steps=max_steps_per_simulation,
        model_reporters = {
            "Density": density,
            "MinorityPC": minority_pc,
            "Homophily": homophily,
            "FearTolerance": fear,
            "HappyAgents": happy,
            "TotalSatisfactionIndex": total_satisfaction_index,
            "BlueSatisfactionIndex": blue_satisfaction_index,
            "RedSatisfactionIndex": red_satisfaction_index,
        },
        agent_reporters = {
            "Position": "pos",
            "AgentType": "type",
            "Fear": "fear"
        }
    )
    batch_run.run_all()

    run_model_data = batch_run.get_model_vars_dataframe()
    run_agent_data = batch_run.get_agent_vars_dataframe()

    now = str(datetime.now().date())
    file_name_suffix = ("_fear_" + str(fear_tolerance) + "_" + now)
    run_model_data.to_csv("results/model_data" + file_name_suffix + ".csv")
    run_agent_data.to_csv("results/agent_data" + file_name_suffix + ".csv")

# descomentar para coletar os dados e gerar os .csv
# batch_run()