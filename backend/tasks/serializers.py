from rest_framework import serializers

class TaskInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField()
    due_date = serializers.DateField()
    estimated_hours = serializers.FloatField()
    importance = serializers.IntegerField()
    dependencies = serializers.ListField(child=serializers.IntegerField(), required=False)

class AnalyzeResponseSerializer(serializers.Serializer):
    sorted_tasks = serializers.ListField()
