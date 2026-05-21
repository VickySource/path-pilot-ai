from app.graph.state import CareerState


def should_critique(state: CareerState) -> str:
    return "critique" if state.get("steps") else "end"
