"""
Workflow Graph Visualization
Creates interactive Plotly graphs showing agent execution flow.
"""

import plotly.graph_objects as go
from typing import Dict, List, Tuple
from utils.workflow_graph_config import AGENT_NODES, AGENT_EDGES


def create_agent_workflow_graph(agent_stats: Dict[str, Dict]) -> go.Figure:
    """
    Create hub-and-spoke workflow graph focused on agents.

    Args:
        agent_stats: Agent execution statistics from backend

    Returns:
        Plotly figure with interactive agent nodes
    """

    # Define positions (hub-and-spoke layout)
    # Router in center, specialists around it
    positions = {
        "start": (0, 2),
        "router": (2, 2),  # Center hub
        "data_gatherer": (4, 3.5),  # Top right
        "action_orchestrator": (4, 2),  # Middle right (swapped with DecisionMaker)
        "decision_maker": (4, 0.5),    # Bottom right (swapped with ActionOrchestrator)
        "hitl": (6, 2),  # Far right
        "end": (8, 2)
    }

    # Create edges
    edge_traces = []

    for source, target in AGENT_EDGES:
        x0, y0 = positions[source]
        x1, y1 = positions[target]

        # Check if this is a bidirectional edge (agent ↔ router)
        is_bidirectional = (target, source) in AGENT_EDGES

        if is_bidirectional and source > target:
            # Skip reverse edge (already drawn)
            continue

        edge_trace = go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(
                width=2,
                color='#888'
            ),
            hoverinfo='none',
            showlegend=False
        )
        edge_traces.append(edge_trace)

    # Create node traces
    node_data = {
        'x': [],
        'y': [],
        'text': [],
        'marker_color': [],
        'marker_size': [],
        'hover_text': [],
        'customdata': []
    }

    for node_id, node_config in AGENT_NODES.items():
        x, y = positions[node_id]
        stats = agent_stats.get(node_id, {"execution_count": 0, "status": "pending"})

        node_data['x'].append(x)
        node_data['y'].append(y)

        # Node label
        icon = node_config.get('icon', '🤖')
        label = node_config.get('label', node_id)
        count = stats.get('execution_count', 0)

        if count > 0:
            text = f"{icon}<br>{label}<br>({count})"
        else:
            text = f"{icon}<br>{label}"

        node_data['text'].append(text)

        # Color by status
        status = stats.get('status', 'pending')
        if status == 'completed':
            color = '#4CAF50'  # Green
        elif status == 'in_progress':
            color = '#FFC107'  # Amber/Yellow
        else:
            color = '#E0E0E0'  # Gray

        node_data['marker_color'].append(color)

        # Size by execution count (for agents)
        node_type = node_config.get('type', 'agent')
        if node_type == 'agent' or node_type == 'hub':
            size = max(40, min(80, 40 + count * 5))
        else:
            size = 30

        node_data['marker_size'].append(size)

        # Hover text
        description = node_config.get('description', '')
        last_action = stats.get('last_action') or stats.get('last_decision', '')

        hover = f"<b>{label}</b><br>{description}<br><br>"
        hover += f"Executions: {count}<br>"
        hover += f"Status: {status}<br>"
        if last_action:
            hover += f"Last action: {last_action}"

        node_data['hover_text'].append(hover)
        node_data['customdata'].append(node_id)

    # Create node scatter trace
    node_trace = go.Scatter(
        x=node_data['x'],
        y=node_data['y'],
        mode='markers+text',
        text=node_data['text'],
        textposition='bottom center',
        marker=dict(
            size=node_data['marker_size'],
            color=node_data['marker_color'],
            line=dict(width=2, color='white')
        ),
        hovertext=node_data['hover_text'],
        hoverinfo='text',
        customdata=node_data['customdata'],
        showlegend=False
    )

    # Combine all traces
    fig = go.Figure(data=edge_traces + [node_trace])

    # Layout
    fig.update_layout(
        showlegend=False,
        hovermode='closest',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.5, 8.5]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.5, 4]  # Extended range to accommodate bottom labels
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=450,  # Increased from 400 to 450
        margin=dict(l=0, r=0, t=10, b=80)  # Increased bottom margin from 70 to 80
    )

    return fig
