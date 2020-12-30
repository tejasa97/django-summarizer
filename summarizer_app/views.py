from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from .models import Summary


class NewSummarizationTask(APIView):

    class InputSerializer(serializers.Serializer):
        text = serializers.CharField()
        website_icon_url = serializers.CharField(required=False, default='')
        page_url = serializers.CharField(required=False, default='')
        webpage_title = serializers.CharField(required=False, default='')

    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            summary_id = Summary.create_new_summarization(
                **serializer.validated_data)
        except Exception as e:
            print(e)
            return Response({"error": "Internal server error"}, status=500)

        return Response({"summary_id": summary_id})


class GetSummary(APIView):

    def get(self, request, summary_id):

        try:
            summary_obj = Summary.objects.get(summary_id=summary_id)
        except Summary.DoesNotExist:
            return Response({"error": "invalid summary id"}, status=400)

        if summary_obj.summary_available() is False:
            response = {"summary_status": "pending"}
        else:
            response = summary_obj.serialize()

        return Response(response, status=200)


class SaveSummary(APIView):

    class InputSerializer(serializers.Serializer):
        user_email = serializers.CharField()

    def post(self, request, summary_id):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            Summary.save_summary_for_user(
                user_email=serializer.validated_data['user_email'], summary_id=summary_id)
        except Summary.DoesNotExist:
            return Response({"error": "invalid summary id"}, status=400)

        return Response({"success": "saved"})


class GetSummaries(APIView):

    class InputSerializer(serializers.Serializer):
        user_email = serializers.CharField()

    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            summaries = Summary.get_all_summaries_of_user(serializer.validated_data['user_email'])
        except Summary.DoesNotExist:
            return Response({"error": "no summaries found"}, status=400)

        return Response(summaries)
