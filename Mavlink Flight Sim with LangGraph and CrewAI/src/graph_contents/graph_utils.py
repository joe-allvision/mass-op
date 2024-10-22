from IPython.display import display, Image
from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod

def display_and_save_graph(app, filename="workflow_graph.png"):
    # Create the graph image
    graph_image = app.get_graph().draw_mermaid_png(
        curve_style=CurveStyle.LINEAR,
        wrap_label_n_words=9,
        draw_method=MermaidDrawMethod.API,
        background_color="white",
        padding=10,
    )

    # Display the graph
    display(Image(
        filename='workflow_graph.png',
        width=800,
        height=600,
    ))

    # Save the PNG to a file
    with open(filename, "wb") as f:
        f.write(graph_image)
    
    print(f"Workflow graph saved as {filename}")
