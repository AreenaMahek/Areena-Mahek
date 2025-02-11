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


# ----------------------------------------------------------------------------- 
# Table Creation 
# -----------------------------------------------------------------------------

if not hasattr(state, "table_items") or state.table_items is None:
    state.table_items = []


state.table_headers = [
{"text": "Values", "value": "values"},
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

# ----------------------------------------------------------------------------- 
# Add values in Table
# -----------------------------------------------------------------------------

def increase_values():
    
    # Increment values by 1
    new_value = int(state.table_items[-1]["values"]) + 1 if state.table_items else 1

    # Append new row
    state.table_items.append(
        {
            "values": new_value,
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
# Scatter Plot with MPL
# ----------------------------------------------------------------------------- 

def ScatterPlot():
    plt.close("all")
    fig, ax = plt.subplots(**figure_size())
    np.random.seed(0)
    ax.plot(
        np.random.normal(size=100), np.random.normal(size=100), "or", ms=10, alpha=0.3
    )
    ax.plot(
        np.random.normal(size=100), np.random.normal(size=100), "ob", ms=20, alpha=0.1
    )

    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_title("Matplotlib ScatterPlot", size=14)
    ax.grid(color="lightgray", alpha=0.7)

    return fig

# ----------------------------------------------------------------------------- 
# Line Plot with MPL
# -----------------------------------------------------------------------------

def LinePlot():
    plt.close("all")
    fig, ax = plt.subplots(**figure_size())
    ax.plot(
        np.random.rand(20),
        "-o",
        alpha=0.5,
        color="black",
        linewidth=5,
        markerfacecolor="green",
        markeredgecolor="lightgreen",
        markersize=20,
        markeredgewidth=10,
    )
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_title("Matplotlib LinePlot", size=14)
    ax.grid(True, color="#EEEEEE", linestyle="solid")
    ax.set_xlim(-2, 22)
    ax.set_ylim(-0.1, 1.1)

    return fig

# -----------------------------------------------------------------------------
# Switch Charts
# -----------------------------------------------------------------------------

@state.change("active_figure", "figure_size")
def update_chart(active_figure, **kwargs):
    ctrl.update_figure(globals()[active_figure]())

# -----------------------------------------------------------------------------
# Remove Item from Table
# -----------------------------------------------------------------------------

def remove_item(value):
    for i in state.table_items:
        if i["values"] == value:
            state.table_items.remove(i)
            server.state.dirty("table_items")
            break


# ----------------------------------------------------------------------------- 
# UI Layout
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
                                        vuetify.VIcon("mdi-delete", color="red", click=(remove_item, "[item.values]"))
                    
                with vuetify.VCol(cols=7):
                    html_figure = matplotlib.Figure(style="position: absolute,padding-top: 30px",)
                    ctrl.update_figure = html_figure.update
                
                                                    
# ----------------------------------------------------------------------------- 
# Start the Application 
# ----------------------------------------------------------------------------- 

if __name__ == "__main__":
    server.start()
