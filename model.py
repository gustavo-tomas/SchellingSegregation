from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.batchrunner import BatchRunner
from mesa.datacollection import DataCollector
from datetime import datetime

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

        # If unhappy, move:
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class Schelling(Model):
    """
    Model class for the Schelling segregation model.
    """

    # adiciona a quantidade máxima de passos
    def __init__(self, height=20, width=20, density=0.8, minority_pc=0.2, homophily=3, max_steps=100):
        """ """

        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily
        self.max_steps = max_steps

        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(width, height, torus=True)

        self.happy = 0
        self.datacollector = DataCollector(
            {
                "happy": "happy",
                "steps": lambda m: self.schedule.steps},  # Model-level count of happy agents
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
                else:
                    agent_type = 0

                agent = SchellingAgent((x, y), self, agent_type)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)

    # para se a quantidade máxima de passos for excedida
    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """

        if self.schedule.steps >= self.max_steps:
            self.running = False

        self.happy = 0  # Reset counter of happy agents
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

def max_steps(model):
    return model.max_steps

def batch_run():
    number_iterations = 10
    max_steps_per_simulation = 400
    max_steps_p = 400

    fixed_params = {
        "height": 20,
        "width": 20,
        "max_steps": max_steps_p
    }
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
            "MaxSteps": max_steps,
            "HappyAgents": happy
        },
        agent_reporters = {
            "Position": "pos",
            "AgentType": "type"
        }
    )
    batch_run.run_all()

    run_model_data = batch_run.get_model_vars_dataframe()
    run_agent_data = batch_run.get_agent_vars_dataframe()

    now = str(datetime.now().date())
    file_name_suffix = ("_steps_" + str(max_steps_p) + "_" + now)
    run_model_data.to_csv("results/model_data" + file_name_suffix + ".csv")
    run_agent_data.to_csv("results/agent_data" + file_name_suffix + ".csv")

batch_run()