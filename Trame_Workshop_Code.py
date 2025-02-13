import numpy as np
import matplotlib.pyplot as plt

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vuetify, trame, matplotlib

# ----------------------------------------------------------------------------- 
# Trame setup 
# ----------------------------------------------------------------------------- 

server = get_server(client_type="vue2")
state, ctrl = server.state, server.controller

if not hasattr(state, "table_items") or state.table_items is None:
    state.table_items = []


state.table_headers = [
{"text": "X Value", "value": "values1"},
{"text": "Y Value", "value": "values2"},
{"text": "Actions", "value": "actions"},
]


table = {
"headers": ("table_headers", state.table_headers),
"items": ("table_items", []),
"classes": "elevation-1 ma-4",
"multi_sort": True,
"dense": True,
"items_per_page": 5,
}

def increase_values():
    
    # Increment values by 1
    new_value1 = int(state.table_items[-1]["values1"]) + 1 if state.table_items else 1
    new_value2 = int(state.table_items[-1]["values2"]) * -1.5 if state.table_items else 1

    # Append new row
    state.table_items.append(
        {
            "values1": new_value1,
            "values2": new_value2,
            "actions": "Remove",
        }
    )
    
    #Refresh the tbale items
    server.state.dirty("table_items")  

# ----------------------------------------------------------------------------- 
# Define Figure Size 
# ----------------------------------------------------------------------------- 

def figure_size():
        return {"figsize": (10, 6), "dpi": 80}

# ----------------------------------------------------------------------------- 
# Scatter Plot View 
# ----------------------------------------------------------------------------- 

def ScatterPlot():
    plt.close("all")
    fig, ax = plt.subplots(**figure_size())
    #np.random.seed(0)

    if state.table_items:
        # Extract all X and Y values from table_items
        x_values = [item["values1"] for item in state.table_items]
        y_values = [item["values2"] for item in state.table_items]
    
        ax.plot(x_values, y_values, "or", ms=20, alpha=0.3)
        
        ax.plot(np.random.normal(size=100), np.random.normal(size=100), "ob", ms=20, alpha=0.1)

    ax.set_xlabel("X axis", size=14)
    ax.set_ylabel("Y axis", size=14)
    ax.set_title("Matplotlib ScatterPlot", size=18)
    ax.grid(color="lightgray", alpha=0.7)

    return fig


def LinePlot():
    plt.close("all")
    fig, ax = plt.subplots(**figure_size())
    
    if state.table_items:
        # Extract all X and Y values from table_items
        x_values = [item["values1"] for item in state.table_items]
        y_values = [item["values2"] for item in state.table_items]
        
        ax.plot(x_values, y_values, "-o", 
        color="black", 
        linewidth=5,
        markerfacecolor="green",
        markeredgecolor="lightgreen",
        markersize=20,
        markeredgewidth=10,)
    
    ax.set_xlabel("X axis", size=14)
    ax.set_ylabel("Y axis", size=14)
    ax.set_title("Matplotlib LinePlot", size=18)
    ax.grid(True, color="#EEEEEE", linestyle="solid")
    #ax.set_xlim(0,10)
    #ax.set_ylim(0,20)
    

    return fig

# -----------------------------------------------------------------------------
# Change Charts 
# -----------------------------------------------------------------------------

@state.change("active_figure", "figure_size", "table_items")
def update_chart(active_figure, **kwargs):
    ctrl.update_figure(globals()[active_figure]())

# -----------------------------------------------------------------------------
# Remove Item
# -----------------------------------------------------------------------------

def remove_item(value1, value2):
    for i in state.table_items:
        if i["values1"] == value1:
            if i["values2"] == value2:
                state.table_items.remove(i)
                server.state.dirty("table_items")
                break


# ----------------------------------------------------------------------------- 
# UI 
# ----------------------------------------------------------------------------- 

state.trame__title = "Trame with Matplotlib"

with SinglePageLayout(server) as layout:
    layout.title.set_text("Trame Application with Matplotlib Figures")

    with layout.toolbar:
        vuetify.VSpacer()
        vuetify.VSpacer()
        vuetify.VSelect(
            v_model=("active_figure", "ScatterPlot"),
            items=(
                "figures",
                [
                    {"text": "Scatter Plot", "value": "ScatterPlot"},
                    {"text": "Line Plot", "value": "LinePlot"},
                    
                ],
            ),
            hide_details=True,
            dense=True,
        )

    with layout.content:
        #100% width with fully responsive
        with vuetify.VContainer(fluid=True):    
            with vuetify.VRow(classes="justify-center"):
                vuetify.VSubheader("Welcome to the Trame Dashboard",
                            style="font-size: 30px;font-weight: bold;color: rgb(0, 71, 171); padding-top: 20px")
            
            
            with vuetify.VRow(classes="justify-center"):
                with vuetify.VCol(cols=5):
                    with vuetify.VRow(classes="justify-center"):
                        
                        vuetify.VBtn("Update Table", 
                            style="margin-top: 30px", 
                            color="pink", 
                            click=increase_values, 
                            classes="d-flex align-center justify-center",)
                        
                    with vuetify.VRow(classes="justify-center"):
                            
                            with vuetify.VDataTable(**table, 
                                style="margin-top: 15px"):
                                    
                                    with vuetify.Template(actions="{ item }",__properties=[("actions", "v-slot:item.actions")],):
                                        vuetify.VIcon("mdi-window-close", color="red", click=(remove_item, "[item.values1, item.values2]"),)
                    
                with vuetify.VCol(cols=7):
                    html_figure = matplotlib.Figure(style="position: absolute,padding-top: 30px",)
                    ctrl.update_figure = html_figure.update
                
                                                    
# ----------------------------------------------------------------------------- 
# Start the Application 
# ----------------------------------------------------------------------------- 

if __name__ == "__main__":
    server.start()
