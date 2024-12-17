from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from .models import Service, AboutUs, Portfolio,Counts, Team, Testimonial, News, Contact,Client,ServiceDetail,HomeDetail,portfolioDetail,newsDetail,QuoteRequest,ContactUs
from django.shortcuts import get_object_or_404
import os

from django.utils.text import slugify

@csrf_exempt
def super_admin_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            return JsonResponse({
                'status':200 ,
                
                'message': 'Login successful!',
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }, status=200)
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid credentials or not a super admin.'
            }, status=404)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid method, only POST is allowed.'
        }, status=405)
        

def super_admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if super admin data is passed in the header
        try:
            super_admin_data = json.loads(request.headers.get('X-Super-Admin'))
            if not super_admin_data or 'username' not in super_admin_data:
                return JsonResponse({'status': 'error', 'message': 'data missing or invalid.'}, status=403)
            
            user = User.objects.get(username=super_admin_data['username'])

            # Check if the user is a super admin
            if not user.is_superuser:
                return JsonResponse({'status': 'error', 'message': 'You must be logged in as a super admin to perform this action.'}, status=403)
        
        except (json.JSONDecodeError, User.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Super admin data invalid or user not found.'}, status=403)

        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
            
# @super_admin_required     
# def add_service(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         try:
#             service = Service.objects.create(
#                 title=data['title'],
#                 description=data['description'],
#                 image=data['image'],  # Assuming you send the image as a URL or handle file uploads separately
#                 detailed_description=data['detailed_description']
#             )
#             return JsonResponse({'status': 'success', 'message': 'Service added successfully!'}, status=201)
#         except KeyError:
#             return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=200)
#     return JsonResponse({'status': 'error', 'message': 'Invalid method. Only POST allowed.'}, status=405)

@csrf_exempt
@super_admin_required
def add_service(request):
    if request.method == 'POST':
        # Check for form data and file uploads
        title = request.POST.get('title')
        slug = slugify(title)

        description = request.POST.get('description')
        image = request.FILES.get('image')  # Retrieve uploaded image from the request
        detailed_description = request.POST.get('detailedDescription')

        if not title or not description or not image or not detailed_description:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=404)
        
        try:
            service = Service.objects.create(
                title=title,
                slug=slug,
                description=description,
                image=image,  # Save the image file
                detailed_description=detailed_description
            )
            return JsonResponse({'status': 'success', 'message': 'Service added successfully!'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only POST allowed.'}, status=405)
@csrf_exempt
@super_admin_required
def add_about_us(request):
    if request.method == 'POST':
        try:
            # Check if there is an existing "About Us" entry (assuming there's only one)
            about_us = AboutUs.objects.first()
            
            if about_us:
                # If an entry exists, update it
                about_us.heading = request.POST.get('heading', about_us.heading)
                about_us.description = request.POST.get('description', about_us.description)
                about_us.first_title = request.POST.get('firstTitle', about_us.first_title)
                about_us.second_title = request.POST.get('secondTitle', about_us.second_title)
                about_us.first_description = request.POST.get('firstDescription', about_us.first_description)
                about_us.second_description = request.POST.get('secondDescription', about_us.second_description)
                
                # Only update the image if provided
                if 'image' in request.FILES:
                    about_us.image = request.FILES['image']
                
                about_us.save()

                return JsonResponse({'status': 'success', 'message': 'About Us updated successfully!'}, status=200)
            else:
                heading=request.POST.get('heading')
                description = request.POST.get('description')
                first_title = request.POST.get('firstTitle')
                second_title = request.POST.get('secondTitle')
                first_description = request.POST.get('firstDescription')
                second_description = request.POST.get('secondDescription')
                if 'image' in request.FILES:
                    image=request.FILES['image']
                about = AboutUs.objects.create(
                heading=heading,
                description=description,
                first_title=first_title,
                second_title=second_title,  # Save the image file
                first_description=first_description,
                second_description=second_description,
                image=image
            )
            return JsonResponse({'status': 'success', 'message': 'Service added successfully!'}, status=200)
                    
                

                
                
                
                
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only POST allowed.'}, status=405)
@csrf_exempt
@super_admin_required
def add_portfolio(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
             image=request.FILES['image']
        data = request.POST
        try:
            portfolio = Portfolio.objects.create(
                title=data.get('title'),
                slug =slugify(data.get('title')),
                description=data.get('description'),

                image=image,  # Assuming image is sent as URL or handled in file upload
                heading=data.get('heading'),
                text_button=data.get('text_button'),
                link=data.get('link')
            )
            return JsonResponse({'status': 'success', 'message': 'Portfolio added successfully!'}, status=201)
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only POST allowed.'}, status=405)
@csrf_exempt
@super_admin_required
def add_team(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image=request.FILES['image']
        data = request.POST
        try:
            team = Team.objects.create(
                name=data.get('name'),
                slug = slugify(data.get('name')),
                description=data.get('description'),

                title=data.get('title'),
                image=image
            )
            return JsonResponse({'status': 'success', 'message': 'Team member added successfully!'}, status=201)
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only POST allowed.'}, status=405)

@csrf_exempt
@super_admin_required
def add_testimonial(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image=request.FILES['image']
        data = request.POST

        try:
            testimonial = Testimonial.objects.create(
                name=data.get('name'),

                title=data.get('title'),
                slug = slugify(data.get('title')),

                image=image,
            )
            return JsonResponse({'status': 'success', 'message': 'Testimonial added successfully!'}, status=201)
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only POST allowed.'}, status=405)
@csrf_exempt
@super_admin_required
def add_news(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image=request.FILES['image']
        data = request.POST

        try:
            news = News.objects.create(
                title=data.get('title'),
                slug = slugify(data.get('title')),
                description=data.get('description'),


                content=data.get('name'),
                image=image
            )
            return JsonResponse({'status': 'success', 'message': 'News article added successfully!'}, status=201)
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=00)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only POST allowed.'}, status=405)
@csrf_exempt
@super_admin_required
def add_contact(request):
    if request.method == 'POST':
        contactimage = None
        client_images = []
        slug=request.POST.get("title")
        heading=request.POST.get('heading')
        heading3=request.POST.get('heading3')

        
        # Handle the contact image
        if 'contactimage' in request.FILES:
            contactimage = request.FILES['contactimage']
        
        # Handle multiple client images
        if 'clientimage' in request.FILES:
            client_images = request.FILES.getlist('clientimage')
        
        # Handle form data
        print('clientimage' in request.FILES)
        try:
            # Check if a contact already exists
            contact = Contact.objects.first()  # Only one contact allowed
            
            if contact:
                # If contact exists, update it
                contact.contact_image = contactimage or contact.contact_image  # If new contact image is provided, update it
                contact.slug=slug or contact.slug
                contact.heading=heading or contact.heading
                contact.heading3=heading3 or contact.heading3

                contact.save()
            else:
                # If no contact exists, create a new one
                contact = Contact.objects.create(
                    contact_image=contactimage,
                    slug=slug,
                    heading=heading,
                    heading3=heading3
                )
            
            # Associate client images with the contact (only if they exist)
            for client_image in client_images:
                Client.objects.create(client_image=client_image)
            
            return JsonResponse({'status': 'success', 'message': 'Contact info added/updated successfully!'}, status=201)
        
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only POST allowed.'}, status=405)

@csrf_exempt
def get_services(request):
    if request.method == 'GET':
        services = Service.objects.all()
        data = []
        for service in services:
            data.append({
                'id': service.id,
                'title': service.title,
                'slug':service.slug,
                'description': service.description,
                'detailed_description': service.detailed_description,
                'image': service.image.url if service.image else None
            })
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)

@csrf_exempt
def get_about_us(request):
    if request.method == 'GET':
        about_us = AboutUs.objects.first()  # Assuming there's only one AboutUs entry
        if about_us:
            data = {
                'heading': about_us.heading,
                'description': about_us.description,
                'firstTitle': about_us.first_title,
                'secondTitle': about_us.second_title,
                'firstDescription': about_us.first_description,
                'secondDescription': about_us.second_description,
                'image': about_us.image.url if about_us.image else None
            }
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        return JsonResponse({'status': 'error', 'message': 'About Us data not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)
@csrf_exempt
def get_portfoli(request):
    if request.method == 'GET':
        about_us = Portfolio.objects.all()  # Assuming there's only one AboutUs entry
        data = []
        for about_us in about_us:
            data.append({
                'id':about_us.id,
                'heading': about_us.heading,
                'title': about_us.title,
                'slug':about_us.slug,
                'link': about_us.link,
                'description':about_us.description,

                'buttonText': about_us.text_button ,
                
                'image': about_us.image.url if about_us.image else None
            })
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)

@csrf_exempt
def get_team(request):
    if request.method == 'GET':
        team_members =Team.objects.all()
       
        data = []
        for member in team_members:
            data.append({
                'id': member.id,
                'name': member.name,
                'title': member.title,
                'description':member.description,

                'image': member.image.url if member.image else None
            })
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)

@csrf_exempt
def get_news(request):
    if request.method == 'GET':
        news_articles = News.objects.all()
        data = []
        for article in news_articles:
            data.append({
                'id': article.id,
                'title': article.title,
                'slug':article.slug,
                'content': article.content,
                'description':article.description,

                'image': article.image.url if article.image else None
            })
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)

@csrf_exempt
def get_testimonials(request):
    if request.method == 'GET':
        testimonials = Testimonial.objects.all()
        data = []
        for testimonial in testimonials:
            data.append({
                'id': testimonial.id,
                'title': testimonial.title,
                'name': testimonial.name,

                'content': testimonial.content,
                'image': testimonial.image.url if testimonial.image else None
            })
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)

@csrf_exempt
def get_contact(request):
    if request.method == 'GET':
        contact = Contact.objects.first()  # Assuming there's only one contact record
        if contact:
            data = {
                'contact_image': contact.contact_image.url if contact.contact_image else None,
                'title':contact.slug,
                'heading':contact.heading,
                'heading3':contact.heading3,

                
            }
            return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)
@csrf_exempt
def get_clients(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        print(clients)
        

        data = []
        for client in clients:
            data.append({
                'client_id': client.id,  # Include the client_id

                'image': client.client_image.url if client.client_image else None
            })
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)


@csrf_exempt
@super_admin_required  # Ensure the user is a super admin
def delete_service(request):
    if request.method == 'POST':
        ids=request.POST.get('id')
        print(ids)
        try:
            # Retrieve the service object by its ID
            service = Service.objects.get(id=ids)
            # Delete the service
            service.delete()
            return JsonResponse({'status': 'success', 'message': 'Service deleted successfully!'}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Service not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only DELETE allowed.'}, status=405)
@csrf_exempt
@super_admin_required
def get_service(request):
    service_id=request.POST.get('id')
    if request.method == 'POST':
        try:
            service = Service.objects.get(id=service_id)
            service_data = {
                'id': service.id,
                'title': service.title,
                'description': service.description,
                'detailedDescription': service.detailed_description,
                'image': service.image.url if service.image else None,
            }
            return JsonResponse({'status': 'success', 'data': service_data}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Service not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)

@csrf_exempt
@super_admin_required  # Ensure only super admin can access this endpoint
def update_service(request):
    service_id=request.POST.get('id')
    if request.method == 'POST':
        try:
            # Get the service to update
            service = Service.objects.get(id=service_id)
            
            # Parse the JSON data from the request body
            data = request.POST
            image=request.FILES.get('image')

            # Update the service fields
            service.title = data.get('title', service.title)
            service.slug=   slugify(service.title)
            service.description = data.get('description', service.description)
            service.detailed_description = data.get('detailed_description', service.detailed_description)

            # Update image if provided
            if image:
                service.image =image  # Assuming image is passed as a URL or file URL

            # Save the updated service
            service.save()

            return JsonResponse({'status': 'success', 'message': 'Service updated successfully!'}, status=200)

        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Service not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=404)
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only PUT allowed.'}, status=405)

@csrf_exempt
@super_admin_required  # Ensure the user is a super admin
def delete_portfolio(request):
    if request.method == 'POST':
        ids=request.POST.get('id')
        print(ids)
        try:
            # Retrieve the service object by its ID
            service = Portfolio.objects.get(id=ids)
            # Delete the service
            service.delete()
            return JsonResponse({'status': 'success', 'message': 'Portfolio deleted successfully!'}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'portfolio not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only DELETE allowed.'}, status=405)

@csrf_exempt
@super_admin_required
def get_portfolio(request):
    portfolio_id=request.POST.get('id')
    
    if request.method == 'POST':
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
            teams=Portfolio.objects.first()
            portfolio_data = {
                'id': portfolio.id,
                'title': portfolio.title,
                'text': portfolio.link,
                'description':portfolio.description,
                'des':teams.description,
                'portfolioid':teams.id,
                'heading': portfolio.heading,
                'buttonText':portfolio.text_button ,
                'image':portfolio.image.url if portfolio.image else None,
            }
            return JsonResponse({'status': 'success', 'data': portfolio_data}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'portfolio not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)

@csrf_exempt
@super_admin_required  # Ensure only super admin can access this endpoint
def update_portfolio(request):
    portfolio_id=request.POST.get('id')
    if request.method == 'POST':
        try:
            # Get the service to update
            portfolio = Portfolio.objects.get(id=portfolio_id)
            
            # Parse the JSON data from the request body
            data = request.POST
            image=request.FILES.get('image')

            
            # Update the service fields
            portfolio.title = data.get('title', portfolio.title)
            portfolio.slug=slugify(portfolio.title)
            portfolio.description = data.get('description', portfolio.description)
            portfolio.heading = data.get('heading', portfolio.heading)
            portfolio.text_button = data.get('text_button', portfolio.text_button)
            portfolio.link = data.get('link', portfolio.link)

            # Update image if provided
            if image:
                portfolio.image = image # Assuming image is passed as a URL or file URL

            # Save the updated service
            portfolio.save()

            return JsonResponse({'status': 'success', 'message': 'portfolio updated successfully!'}, status=200)

        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'portfolio not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=404)
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only PUT allowed.'}, status=405)


@csrf_exempt
@super_admin_required
def get_teams(request):
    team_id=request.POST.get('id')
    if request.method == 'POST':
        try:
            team = Team.objects.get(id=team_id)
            teams=Team.objects.first()
            team_data = {
                'id': team.id,
                'name': team.name,
                'description':team.description,
                'title': team.title,
                'image':team.image.url if team.image else None,
                'des':teams.description,
                'teamid':teams.id
            }
            return JsonResponse({'status': 'success', 'data': team_data}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'team not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)

@csrf_exempt
def get_new_testimonials(request):
    test_id=request.POST.get('id')
    if request.method == 'POST':
        testimonials = Testimonial.objects.get(id=test_id)
        data={
            'id': testimonials.id,
            'title': testimonials.title,
            'name': testimonials.name,

            'content': testimonials.content,
            'image': testimonials.image.url if testimonials.image else None
        }
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)

@csrf_exempt
def get__new_news(request):
    new_id=request.POST.get('id')

    if request.method == 'POST':
       article = News.objects.get(id=new_id)
       articles = News.objects.first()

       data={
            'id': article.id,
            'title': article.title,
            'name': article.content,
            'description':article.description,
            'des':articles.description,
            'newsid':articles.id,
            'image': article.image.url if article.image else None
        }
       return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)



@csrf_exempt
@super_admin_required  # Ensure only super admin can access this endpoint
def update_team(request):
    team_id=request.POST.get('id')
    if request.method == 'POST':
        try:
            # Get the service to update
            team = Team.objects.get(id=team_id)
            
            # Parse the JSON data from the request body
            data = request.POST
            image=request.FILES.get('image')

            
            # Update the service fields
            team.title = data.get('title', team.title)
            team.description=data.get('description')
            team.name = data.get('name', team.name)
          
            # Update image if provided
            if image:
                team.image =image  # Assuming image is passed as a URL or file URL

            # Save the updated service
            team.save()

            return JsonResponse({'status': 'success', 'message': 'team updated successfully!'}, status=200)

        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'team not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=404)
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only PUT allowed.'}, status=405)

@csrf_exempt
@super_admin_required  # Ensure only super admin can access this endpoint
def update_test(request):
    test_id=request.POST.get('id')
    if request.method == 'POST':
        try:
            # Get the service to update
            test = Testimonial.objects.get(id=test_id)
            
            # Parse the JSON data from the request body
            data = request.POST
            image=request.FILES.get('image')
         
            
            # Update the service fields
            test.title = data.get('title', test.title)
            test.name = data.get('name', test.name)
          
            # Update image if provided
            if image:
                test.image =image  # Assuming image is passed as a URL or file URL

            # Save the updated service
            test.save()

            return JsonResponse({'status': 'success', 'message': 'tst updated successfully!'}, status=200)

        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=404)
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only PUT allowed.'}, status=405)

@csrf_exempt
@super_admin_required  # Ensure only super admin can access this endpoint
def update_news(request):
    test_id=request.POST.get('id')
    if request.method == 'POST':
        try:
            # Get the service to update
            test = News.objects.get(id=test_id)
            
            # Parse the JSON data from the request body
            data = request.POST
            image=request.FILES.get('image')
         
            
            # Update the service fields
            test.title = data.get('title', test.title)
            test.description = data.get('description', test.description)

            test.slug=slugify(test.title)
            test.content= data.get('name', test.content)
          
            # Update image if provided
            if image:
                test.image =image  # Assuming image is passed as a URL or file URL

            # Save the updated service
            test.save()

            return JsonResponse({'status': 'success', 'message': 'News updated successfully!'}, status=200)

        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'tst not found.'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=404)
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only PUT allowed.'}, status=405)



@csrf_exempt
@super_admin_required  # Ensure the user is a super admin
def delete_test(request):
    if request.method == 'POST':
        ids=request.POST.get('id')
        print(ids)
        try:
            # Retrieve the service object by its ID
            test = Testimonial.objects.get(id=ids)
            # Delete the service
            test.delete()
            return JsonResponse({'status': 'success', 'message': 'Test deleted successfully!'}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'team not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only DELETE allowed.'}, status=405)


@csrf_exempt
@super_admin_required  # Ensure the user is a super admin
def delete_team(request):
    if request.method == 'POST':
        ids=request.POST.get('id')
        print(ids)
        try:
            # Retrieve the service object by its ID
            team = Team.objects.get(id=ids)
            # Delete the service
            team.delete()
            return JsonResponse({'status': 'success', 'message': 'Team deleted successfully!'}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'team not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only DELETE allowed.'}, status=405)

@csrf_exempt
@super_admin_required  # Ensure the user is a super admin
def delete_news(request):
    if request.method == 'POST':
        ids=request.POST.get('id')
        print(ids)
        try:
            # Retrieve the service object by its ID
            news =News.objects.get(id=ids)
            # Delete the service
            news.delete()
            return JsonResponse({'status': 'success', 'message': 'news deleted successfully!'}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'news not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only DELETE allowed.'}, status=405)


@csrf_exempt
def delete_client_image(request, client_id):
    if request.method == 'DELETE':
        # Get the client object by ID
        client = get_object_or_404(Client, id=client_id)

        # Check if the client has an image
        if client.client_image:
            # Delete the image file from storage if it exists
            image_path = client.client_image.path
            if os.path.exists(image_path):
                os.remove(image_path)

        # Delete the entire client record from the database
        client.delete()

        return JsonResponse({'message': 'Client and associated image deleted successfully.'}, status=200)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt  # Allow POST requests without CSRF token (for testing purposes)
@super_admin_required  # Ensure only super admin can access this endpoint
def add_service_detail(request):
    if request.method == "POST":
        print('hi')
        # Get service ID from request
        slug = request.POST.get('slug')
        print(slug)
        try:
            service = Service.objects.get(slug=slug)
        except Service.DoesNotExist:
            return JsonResponse({"error": "Service not found"}, status=404)

        detail = request.POST.get('detail')
        detail2 = request.POST.get('detail2')

        # Get the image files from the request
        image_1 = request.FILES.get('image1')
        image_2 = request.FILES.get('image2')
        metaname= request.POST.get('metaname')
        metades= request.POST.get('metades')
        keywords= request.POST.get('keywords')
        # Create a new ServiceDetail object
        service_detail =ServiceDetail(
            service=service,
            detail=detail,
            detail2=detail2,
            image_1=image_1,
            image_2=image_2,
            metaname=metaname,
            metadescription=metades,
            keywords=keywords

        )
        service_detail.save()

        return JsonResponse({
            "message": "Service detail created successfully",
            "service_detail_id": service_detail.id
        }, status=201)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)

@csrf_exempt 
def get_service_detail(request):
    slug=request.POST.get('slug')
    try:
        # Retrieve the ServiceDetail by ID
        service = Service.objects.get(slug=slug)
        service_detail = ServiceDetail.objects.get(service=service)

        # Prepare the response data
        response_data = {
            "service_id": service_detail.service.id,
            "service_title": service_detail.service.title,
            "detail": service_detail.detail,
            "detail2": service_detail.detail2,
            'metaname':service_detail.metaname,
            'metades':service_detail.metadescription,
            'keywords':service_detail.keywords,
            "image1": service_detail.image_1.url if service_detail.image_1 else None,
            "image2": service_detail.image_2.url if service_detail.image_2 else None
        }

        return JsonResponse(response_data, status=200)

    except ServiceDetail.DoesNotExist:
        return JsonResponse({"error": "Service detail not found"}, status=400)
@csrf_exempt  # Allow PUT request without CSRF token for testing purposes
@super_admin_required  # Ensure only super admin can access this endpoint

def update_service_detail(request):
    slug=request.POST.get('slug')
    print(slug)

    try:
        # Retrieve the existing Service by slug
        service_detail = Service.objects.get(slug=slug)
        print(service_detail)
        service=ServiceDetail.objects.get(service=service_detail)
        image_1 =request.FILES.get('image1')
        image_2 =request.FILES.get('image2')  
        # Parse the incoming JSON data from the request body
        updated_data = request.POST

        # Update the fields if they are provided in the request
  
        if 'detail' in updated_data:
            service.detail = updated_data.get('detail')
        if 'detail2' in updated_data:
            service.detail2 = updated_data.get('detail2')
        if image_1:
            service.image_1 =image_1  # Update image if provided (for file handling, use request.FILES)
        if image_2:
            service.image_2 =image_2  # Update image if provided (for file handling, use request.FILES)
        if 'metaname' in updated_data:
            service_detail.metaname= updated_data.get('metaname')
        if 'metades' in updated_data:
            service_detail.metadescription =updated_data.get('metades')
        if 'keywords' in updated_data:
            service_detail.keywords =updated_data.get('keywords')

        # Save the updated Service
        service.save()

        return JsonResponse({
            "message": "Service updated successfully",
            "service_id": service.id,
        }, status=200)

    except Service.DoesNotExist:
        return JsonResponse({"error": "Service not found"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=404)
    
@csrf_exempt  # Allow POST requests without CSRF token (for testing purposes)
@super_admin_required  # Ensure only super admin can access this endpoint
def add_portfolio_detail(request):
    if request.method == "POST":
        # Get service ID from request
        slug = request.POST.get('slug')
        try:
            portfolio = Portfolio.objects.get(slug=slug)
        except Service.DoesNotExist:
            return JsonResponse({"error": "Service not found"}, status=400)

        # Get the text fields from the request
        heading = request.POST.get('heading')
        branch = request.POST.get('branch')
        types = request.POST.get('types')
        progam = request.POST.get('progam')
        # Get the image files from the request
        facebook = request.POST.get('facebook','')
        instagram = request.POST.get('instagram','')
        linkedin = request.POST.get('linkedin','')
        x = request.POST.get('x','')
        detail=  request.POST.get('detail')
        metaname=request.POST.get('metaname')
        metades=request.POST.get('metades')
        keywords=request.POST.get('keywords')

        # Create a new ServiceDetail object
        portfolio_detail =portfolioDetail(
            portfolio=portfolio,
            detail=detail,
            heading=heading,
            branch=branch,
            types=types,
            progam=progam,
            facebook=facebook,
            instagram=instagram,
            linkedin=linkedin,
            x=x,
            metaname=metaname,
            metadescription=metades,
            keywords=keywords
            
        )
        portfolio_detail.save()

        return JsonResponse({
            "message": "portfoli detail created successfully",
            "service_detail_id": portfolio_detail.id
        }, status=201)

    return JsonResponse({"error": "Invalid HTTP method"}, status=405)

@csrf_exempt 
def get_portfolio_detail(request):
    slug=request.POST.get('slug')
    try:
        # Retrieve the ServiceDetail by ID
        service = Portfolio.objects.get(slug=slug)
        service_detail = portfolioDetail.objects.get(portfolio=service)

        # Prepare the response data
        response_data = {
            "id": service_detail.portfolio_id,
            'title':service_detail.portfolio.title,
            'header':service_detail.portfolio.heading,

            "detail": service_detail.detail,
            "heading": service_detail.heading,
            "branch": service_detail.branch,
            "types": service_detail.types,
            "progam": service_detail.progam,
            "facebook": service_detail.facebook,
            "instagram": service_detail.instagram,
            "linkedin": service_detail.linkedin,
            'metaname':service_detail.metaname,
            'metades':service_detail.metadescription,
            'keywords':service_detail.keywords,

            "x": service_detail.x,
            
        }

        return JsonResponse(response_data, status=200)

    except ServiceDetail.DoesNotExist:
        return JsonResponse({"error": "Service detail not found"}, status=400)
@csrf_exempt  # Allow PATCH/PUT without CSRF token for testing purposes
@super_admin_required  # Ensure only super admin can access this endpoint

def update_portfolio_detail(request):
    detail_id=request.POST.get('id')
    slug=request.POST.get('slug')

    try:
        # Retrieve the PortfolioDetail object by ID
        
        
        portfolio=Portfolio.objects.get(slug=slug)
        portfolio_detail = portfolioDetail.objects.get(portfolio=portfolio)

        # Parse incoming JSON data
        try:
            updated_data = request.POST
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=404)

        # Update the fields if they are provided in the request
        if 'heading' in updated_data:
            portfolio_detail.heading = updated_data.get('heading')
        if 'branch' in updated_data:
            portfolio_detail.branch = updated_data.get('branch')
        if 'types' in updated_data:
            portfolio_detail.types = updated_data.get('types')
        if 'progam' in updated_data:
            portfolio_detail.progam = updated_data.get('progam')
        if 'facebook' in updated_data:
            portfolio_detail.facebook = updated_data.get('facebook')
        if 'linkedin' in updated_data:
            portfolio_detail.linkedin = updated_data.get('linkedin')
        if 'instagram' in updated_data:
            portfolio_detail.instagram = updated_data.get('instagram')
        if 'x' in updated_data:
            portfolio_detail.x = updated_data.get('x')
        if 'detail' in updated_data:
            portfolio_detail.detail = updated_data.get('detail')
        if 'metaname' in updated_data:
            portfolio_detail.metaname= updated_data.get('metaname')
        if 'metades' in updated_data:
            portfolio_detail.metadescription = updated_data.get('metades')
        if 'keywords' in updated_data:
            portfolio_detail.keywords = updated_data.get('keywords')

        # Save the updated PortfolioDetail object
        portfolio_detail.save()

        return JsonResponse({
            "message": "Portfolio detail updated successfully",
            "portfolio_detail_id": portfolio_detail.id
        }, status=200)

    except portfolioDetail.DoesNotExist:
        return JsonResponse({"error": "Portfolio detail not found"}, status=400)
@csrf_exempt
@super_admin_required  # Ensure only super admin can access this endpoint
def add_news_detail(request):
    try:
        data = request.POST

        # Validate and fetch required fields
        slug = data.get('slug')
        detail = data.get('detail')
        metaname=data.get('metaname')
        metades=data.get('metades')
        keywords=data.get('keywords')

    
        # Retrieve the News object
        news = News.objects.get(slug=slug)

        # Create the NewsDetail object
        news_detail = newsDetail.objects.create(news=news,detail=detail,metaname=metaname,metadescription=metades,keywords=keywords)

        return JsonResponse({
            "message": "News detail added successfully",
            "news_detail_id": news_detail.id
        }, status=201)

    except News.DoesNotExist:
        return JsonResponse({"error": "News not found"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=404)
@csrf_exempt
def get_news_detail(request):
    slug = request.POST.get('slug')

    try:
        news = News.objects.get(slug=slug)

        # Retrieve the NewsDetail object
        news_detail = newsDetail.objects.get(news=news)

        # Prepare the response data
        response_data = {
            "news_id": news_detail.news.id,
            "news_title": news_detail.news.title,
            "published_date":news_detail.news.published_date,
            "detail": news_detail.detail,
            'metaname':news_detail.metaname,
            'metades':news_detail.metadescription,
            'keywords':news_detail.keywords
        }

        return JsonResponse(response_data, status=200)

    except newsDetail.DoesNotExist:
        return JsonResponse({"error": "News detail not found"}, status=400)
    
@csrf_exempt
@super_admin_required  # Ensure only super admin can access this endpoint
def update_news_detail(request):
    slug = request.POST.get('slug')

    try:
        news = News.objects.get(slug=slug)

        data = request.POST

        # Retrieve the NewsDetail object
        news_detail = newsDetail.objects.get(news=news)

        # Update the fields if they are provided
        if 'detail' in data:
            news_detail.detail = data.get('detail')
        if 'metaname' in data:
            news_detail.metaname= data.get('metaname')
        if 'metades' in data:
            news_detail.metadescription = data.get('metades')
        if 'keywords' in data:
            news_detail.keywords = data.get('keywords')

        # Save the updated NewsDetail
        news_detail.save()

        return JsonResponse({
            "message": "News detail updated successfully",
            "news_detail_id": news_detail.id
        }, status=200)

    except newsDetail.DoesNotExist:
        return JsonResponse({"error": "News detail not found"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=404)
    
@csrf_exempt  # Only use this for testing, or add proper CSRF handling for production
def submit_quote(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body.decode('utf-8'))

            # Get data from the incoming request
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            area_code = data.get('areaCode', '')
            phone_number = data.get('phoneNumber')
            email = data.get('email')
            company_name = data.get('companyName', '')
            website = data.get('website', '')
            services_required = data.get('servicesRequired', [])
            project_overview = data.get('projectOverview', '')
            budget = data.get('budget', '')
            ready_to_start = data.get('readyToStart', '')

            # Perform some basic validation (optional)
            if not first_name or not last_name or not phone_number or not email:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Save the data to the database
            quote_request = QuoteRequest(
                first_name=first_name,
                last_name=last_name,
                area_code=area_code,
                phone_number=phone_number,
                email=email,
                company_name=company_name,
                website=website,
                services_required=services_required,
                project_overview=project_overview,
                budget=budget,
                ready_to_start=ready_to_start
            )
            quote_request.save()

            # Return success response
            return JsonResponse({'message': 'Quote request submitted successfully!'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Invalid method, use POST"}, status=405)

@csrf_exempt
@super_admin_required 
def get_quote_requests(request):
    try:
        # Fetch all QuoteRequest objects
        quote_requests = QuoteRequest.objects.all()

        # Prepare the data to send in response
        data = []
        for quote in quote_requests:
            data.append({
                "id": quote.id,
                "first_name": quote.first_name,
                "last_name": quote.last_name,
                "area_code": quote.area_code,
                "phone_number": quote.phone_number,
                "email": quote.email,
                "company_name": quote.company_name,
                "website": quote.website,
                "services_required": quote.services_required,
                "project_overview": quote.project_overview,
                "budget": quote.budget,
                "ready_to_start": quote.ready_to_start,
            })

        return JsonResponse({"quote_requests": data}, status=200)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
@super_admin_required 

def add_contact_us(request):
    if request.method == 'POST':
        try:
            # Check if there is already an entry in the ContactUs model
            
            # Parse the incoming JSON data
            data = request.POST
            about_us = ContactUs.objects.first()
            
            if about_us:
                # If an entry exists, update it
                about_us.detail = data.get('detail', about_us.detail)
                about_us.detail2 = data.get('detail2', about_us.detail2)
                about_us.detail3 = data.get('detail3', about_us.detail3)
                about_us.save()
                
            else:
                detail = data.get('detail')
                detail2 = data.get('detail2')
                detail3 = data.get('detail3')

                contact_us = ContactUs.objects.create(
                    detail=detail,
                    detail2=detail2,
                    detail3=detail3
                )

            return JsonResponse({'message': 'Contact Us details added successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
@csrf_exempt

def get_contact_us(request):
    try:
        # Retrieve the first (and only) ContactUs instance
        contact_us = ContactUs.objects.first()

        if contact_us:
            # Prepare the response data
            response_data = {
                "detail": contact_us.detail,
                "detail2": contact_us.detail2,
                "detail3": contact_us.detail3
            }
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'error': 'Invalid JSON data'}, status=404)

    except ContactUs.DoesNotExist:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

@csrf_exempt
@super_admin_required
def add_count(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        try:
            if not id:
                title = request.POST.get('title')
                num = request.POST.get('num')
                description = request.POST.get('description')
                
                count = Counts.objects.create(
                    title=title,
                    num=num,
                    description=description
                )
                

                return JsonResponse({'status': 'success', 'message': 'About Us updated successfully!'}, status=200)
            else:
                about_us = Counts.objects.get(id=id)
                if about_us:
                    
                    about_us.title = request.POST.get('title', about_us.title)
                    about_us.num = request.POST.get('num', about_us.num)
                    about_us.description = request.POST.get('description', about_us.description)
                
                    about_us.save()
                return JsonResponse({'message': 'Count Us details added successfully'}, status=201)

            
                

                
                
          
               
        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only POST allowed.'}, status=405)

@csrf_exempt
def get_counts(request):
    if request.method == 'GET':
        about_u = Counts.objects.all()  # Assuming there's only one AboutUs entry
        data = []
        for about_us in about_u :
            data.append({
                'id':about_us.id,
                'description': about_us.description,
                'title': about_us.title,
                'num': about_us.num,
            })
        
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'About Us data not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)

@csrf_exempt
@super_admin_required
def get_counts_data(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        count = Counts.objects.get(id=id)
        
        data={
       
            'id': count.id,
            'title': count.title,
            'description': count.description,
            'num': count.num,

        
        }
        return JsonResponse({'status': 'success', 'data': data}, status=200)
    return JsonResponse({'status': 'error', 'message': 'About Us data not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only GET allowed.'}, status=405)


@csrf_exempt
@super_admin_required  # Ensure the user is a super admin
def delete_counts(request):
    if request.method == 'POST':
        ids=request.POST.get('id')
        print(ids)
        try:
            # Retrieve the service object by its ID
            team = Counts.objects.get(id=ids)
            # Delete the service
            team.delete()
            return JsonResponse({'status': 'success', 'message': 'Count deleted successfully!'}, status=200)
        except Service.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'team not found.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid method. Only DELETE allowed.'}, status=405)


@csrf_exempt
def add_home_detail(request):
    if request.method in ['POST', 'PUT']:
        data = json.loads(request.body)
        
        # Check if there's already a record in the database
        home_detail, created = HomeDetail.objects.get_or_create(id=1)  # Assume there's only one record

        # Update the record if it already exists, otherwise create a new one
        home_detail.metaname = data.get('metaname', home_detail.metaname)
        home_detail.metadescription = data.get('metadescription', home_detail.metadescription)
        home_detail.keywords = data.get('keywords', home_detail.keywords)
        home_detail.metanamecontact = data.get('metanamecontact', home_detail.metanamecontact)
        home_detail.metadescriptioncontact = data.get('metadescriptioncontact', home_detail.metadescriptioncontact)
        home_detail.keywordscontact = data.get('keywordscontact', home_detail.keywordscontact)
        home_detail.metanamequote = data.get('metanamequote', home_detail.metanamequote)
        home_detail.metadescriptionquote = data.get('metadescriptionquote', home_detail.metadescriptionquote)
        home_detail.keywordsquote = data.get('keywordsquote', home_detail.keywordsquote)
        home_detail.heading = data.get('heading', home_detail.heading)
        home_detail.detail = data.get('detail', home_detail.detail)
        home_detail.footeremail = data.get('footeremail', home_detail.footeremail)
        home_detail.footeremail2 = data.get('footeremail2', home_detail.footeremail2)

        # Save the updated or created record
        home_detail.save()

        # Return appropriate response
        if created:
            return JsonResponse({'message': 'Home Detail added successfully!'}, status=201)
        else:
            return JsonResponse({'message': 'Home Detail updated successfully!'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid method'}, status=405)
    
@csrf_exempt

def get_home_detail(request):
    if request.method == 'GET':
        try:
            home_detail = HomeDetail.objects.all().first()  # We assume only one record exists.
            if home_detail:
                return JsonResponse({
                    'metaname': home_detail.metaname,
                    'metadescription': home_detail.metadescription,
                    'keywords': home_detail.keywords,
                    'metanamecontact': home_detail.metanamecontact,
                    'metadescriptioncontact': home_detail.metadescriptioncontact,
                    'keywordscontact': home_detail.keywordscontact,
                    'metanamequote': home_detail.metanamequote,
                    'metadescriptionquote': home_detail.metadescriptionquote,
                    'keywordsquote': home_detail.keywordsquote,
                    'heading': home_detail.heading,
                    'detail': home_detail.detail,
                    'footeremail': home_detail.footeremail,
                    'footeremail2': home_detail.footeremail2,
                }, status=200)
            else:
                return JsonResponse({'message': 'No data found'}, status=404)
        except HomeDetail.DoesNotExist:
            return JsonResponse({'message': 'Home Detail not found!'}, status=400)