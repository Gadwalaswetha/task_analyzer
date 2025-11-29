from datetime import date

def detect_cycle(tasks_dict):
    visited = set()
    rec_stack = set()

    def visit(task_id):
        if task_id in rec_stack:
            return True
        if task_id in visited:
            return False

        visited.add(task_id)
        rec_stack.add(task_id)

        for dep in tasks_dict[task_id]["dependencies"]:
            if dep in tasks_dict and visit(dep):
                return True

        rec_stack.remove(task_id)
        return False

    for t in tasks_dict:
        if visit(t):
            return True

    return False


def calculate_score(task, strategy, dep_count):
    today = date.today()

    # Urgency
    days_left = (task["due_date"] - today).days
    if days_left < 0:
        urgency = 100
    else:
        urgency = max(0, 100 - days_left * 3)

    importance = task["importance"] * 10
    effort = max(1, 20 - task["estimated_hours"])
    dependency_bonus = dep_count * 5

    # Strategy switch
    if strategy == "fast":
        return effort, f"Fastest Wins: Low-effort prioritized."

    if strategy == "impact":
        return importance, "High Impact: Importance valued most."

    if strategy == "deadline":
        return urgency, "Deadline Driven: Due date urgency prioritized."

    # SMART BALANCE
    score = urgency * 0.35 + importance * 0.45 + effort * 0.15 + dependency_bonus * 0.05
    explanation = (
        f"Smart Balance: urgency={urgency}, importance={importance}, "
        f"effort={effort}, dependencies={dependency_bonus}"
    )

    return score, explanation
