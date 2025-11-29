from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TaskInputSerializer
from .scoring import calculate_score, detect_cycle
from datetime import datetime

@api_view(["POST"])
def analyze_tasks(request):
    tasks = request.data.get("tasks", [])
    strategy = request.data.get("strategy", "smart")

    serializer = TaskInputSerializer(data=tasks, many=True)
    serializer.is_valid(raise_exception=True)
    tasks = serializer.validated_data

    # Convert dates
    for t in tasks:
        t["due_date"] = datetime.strptime(str(t["due_date"]), "%Y-%m-%d").date()

    # Convert into dict for cycle detection
    task_map = {t["id"]: t for t in tasks if "id" in t}

    if detect_cycle(task_map):
        return Response({"error": "Circular dependency detected"}, status=400)

    # Count how many tasks depend on each task
    dependency_count = {t["id"]: 0 for t in tasks if "id" in t}
    for t in tasks:
        for d in t.get("dependencies", []):
            if d in dependency_count:
                dependency_count[d] += 1

    # Scoring
    output = []
    for t in tasks:
        score, explanation = calculate_score(t, strategy, dependency_count.get(t.get("id"), 0))
        output.append({**t, "score": round(score, 2), "explanation": explanation})

    # Sort
    output = sorted(output, key=lambda x: x["score"], reverse=True)

    return Response({"sorted_tasks": output})


@api_view(["GET"])
def suggest_tasks(request):
    return Response({
        "message": "Your backend is working! Add logic if needed."
    })
