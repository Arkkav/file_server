from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from .models import File
from django.shortcuts import get_object_or_404
from django.http import FileResponse


class FileStorage(APIView):
	parser_class = (FileUploadParser,)
	queryset = File.objects.all()
	serializer_class = FileSerializer

	def post(self, request, *args, **kwargs):
		file_serializer = self.serializer_class(data=request.data)
		if file_serializer.is_valid():
			file_serializer.save()
			file_hash = file_serializer.data['hash']
			return Response({'hash': file_hash}, status=status.HTTP_201_CREATED)
		else:
			return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def get(self, request, *args, **kwargs):
		hash = kwargs.get('hash')
		file_object = get_object_or_404(self.queryset, hash=hash)
		return FileResponse(file_object.file)

	def delete(self, request, *args, **kwargs):
		hash = kwargs.get('hash')
		file_object = get_object_or_404(self.queryset, hash=hash)
		file_object.delete()
		file_object.file.delete(save=False)
		return Response(status=status.HTTP_204_NO_CONTENT)