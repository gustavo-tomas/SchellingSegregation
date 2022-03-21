from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Schelling


class HappyElement(TextElement):
    """
    Display a text count of how many happy agents there are.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Happy agents: " + str(model.happy)

class IndexElement(TextElement):
    """
    Display a text index of the index of happy agents.
    """

    def __init__(self):
        pass

    def render(self, model):
        return "Index of satisfaction: " + str(round(model.total_satisfaction_index, 2))


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.type == 0:
        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
    else:
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"
    return portrayal


happy_element = HappyElement()
index_element = IndexElement()
canvas_element = CanvasGrid(schelling_draw, 20, 20, 500, 500)
happy_chart = ChartModule([
    {"Label": "happy", "Color": "Black"},
])
index_chart = ChartModule([
    {"Label": "total_satisfaction_index", "Color": "Green"},
    {"Label": "red_satisfaction_index", "Color": "Red"},
    {"Label": "blue_satisfaction_index", "Color": "Blue"},
])

model_params = {
    "height": 20,
    "width": 20,
    "density": UserSettableParameter("slider", "Agent density", 0.8, 0.01, 1.0, 0.01),
    "minority_pc": UserSettableParameter(
        "slider", "Fraction minority", 0.2, 0.00, 1.0, 0.01
    ),
    "homophily": UserSettableParameter("slider", "Homophily", 3, 0, 8, 1),
    
    # medo pode ser ajustado pela interface
    "fear": UserSettableParameter("slider", "Fear tolerance", 0.8, 0, 1, 0.01),
}

server = ModularServer(
    Schelling, [canvas_element, happy_element, happy_chart, index_element, index_chart], "Schelling", model_params
)
