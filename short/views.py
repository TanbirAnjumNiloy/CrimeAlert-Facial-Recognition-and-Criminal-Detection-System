from django.shortcuts import render, redirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from .models import ImageUpload
from io import BytesIO
import numpy as np
import face_recognition
from django.http import JsonResponse
import json
import base64
import cv2
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')

def success(request):
    return render(request, 'success.html')

def upload_img(request):
    if request.method == 'POST':
        uploaded_image = request.FILES.get('image', None)
        name = request.POST.get('name', '').strip()
        details = request.POST.get('details', '').strip()

        if uploaded_image and name and details:
            image_data = uploaded_image.read()
            uploaded_image.seek(0)
            image_np = face_recognition.load_image_file(BytesIO(image_data))

            uploaded_image_encodings = face_recognition.face_encodings(image_np)
            
            if not uploaded_image_encodings:
                return HttpResponse("No faces found in the image.")

            for img_obj in ImageUpload.objects.all():
                existing_image_encodings = img_obj.get_face_encodings()
                
                if existing_image_encodings:
                    for uploaded_encoding in uploaded_image_encodings:
                        results = face_recognition.compare_faces(existing_image_encodings, uploaded_encoding, tolerance=0.6)
                        if True in results:
                            return HttpResponse("A similar face already exists in the database.")
            
            fs = FileSystemStorage()
            filename = fs.save(uploaded_image.name, uploaded_image)
            new_upload = ImageUpload(name=name, image=uploaded_image, details=details)
            new_upload.save_face_encodings(uploaded_image_encodings[0])
            new_upload.save()
            return redirect('success')
        else:
            return HttpResponse("Please fill out all fields.")
    return render(request, 'uploadimg.html')

@csrf_exempt
def process_frame(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        np_array = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_encodings = face_recognition.face_encodings(rgb_frame)

        if not frame_encodings:
            return JsonResponse({'match': False})

        for frame_encoding in frame_encodings:
            for img_obj in ImageUpload.objects.all():
                existing_image_encodings = img_obj.get_face_encodings()
                
                if existing_image_encodings:
                    results = face_recognition.compare_faces(existing_image_encodings, frame_encoding, tolerance=0.6)
                    if True in results:
                        return JsonResponse({
                            'match': True,
                            'name': img_obj.name,
                            'details': img_obj.details
                        })
        
        return JsonResponse({'match': False})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def display_your_camera(request):
    return render(request, 'displayyourcamera.html')
