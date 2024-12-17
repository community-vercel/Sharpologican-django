from django.urls import path
from . import views

urlpatterns = [
    path('super-admin-login/', views.super_admin_login, name='super-admin-login'),
    path('add-service/', views.add_service, name='add-service'),
    path('add-about-us/', views.add_about_us, name='add-about-us'),
    path('add-portfolio/', views.add_portfolio, name='add-portfolio'),
    path('add-team/', views.add_team, name='add-team'),
    path('add-testimonial/', views.add_testimonial, name='add-testimonial'),
    path('add-news/', views.add_news, name='add-news'),
    path('add-contact/', views.add_contact, name='add-contact'),
    path('services/', views.get_services, name='get_services'),
    path('about-us/', views.get_about_us, name='get_about_us'),
    path('portfolio/', views.get_portfoli, name='get_folio'),
    path('get-portfolio/', views.get_portfolio, name='get portfolio'),
    path('update-portfolio/', views.update_portfolio, name='update_portfolio'),
    path('add-portfoliodetails/', views.add_portfolio_detail, name='add portfolio'),
    path('get-portfoliodetails/', views.get_portfolio_detail, name='get portfolio'),
    path('update-portfoliodetails/', views.update_portfolio_detail, name='get portfolio'),

    path('team/', views.get_team, name='get_team'),
    path('get-team/', views.get_teams, name='get team'),
    path('update-team/', views.update_team, name='updats_team'),
    path('delete-team/', views.delete_team, name='delete_team'),

    path('news/', views.get_news, name='get_news'),
    path('delete-news/', views.delete_news, name='delete_news'),
    path('get-news/', views.get__new_news, name='get_news'),
    path('update-news/', views.update_news, name='update_news'),
    path('add-newsdetails/', views.add_news_detail, name='get_news'),
    path('get-newsdetails/', views.get_news_detail, name='get_news'),
    path('update-newsdetails/', views.update_news_detail, name='get_news'),

    path('testimonials/', views.get_testimonials, name='get_testimonials'),
    path('get-test/', views.get_new_testimonials, name='get_test'),
    path('update-test/', views.update_test, name='updats_test'),

    path('delete-test/', views.delete_test, name='delete_test'),
    path('add-servicedetails/', views.add_service_detail, name='add_services'),
    path('get-servicedetails/', views.get_service_detail, name='add_services'),
    path('update-servicedetails/', views.update_service_detail, name='add_services'),

    
    
    path('contact/', views.get_contact, name='get_contact'),
    path('clients/', views.get_clients, name='get_clients'),
    path('delete-service/', views.delete_service, name='delete_service'),
    path('get-service/', views.get_service, name='delete_service'),
    path('update-service/', views.update_service, name='update_service'),
    path('delete-portfolio/', views.delete_portfolio, name='delete_portfolio'),
    path('delete-image/<int:client_id>/', views.delete_client_image, name='delete_client_image'),

    path('submit-quote/', views.submit_quote, name='get_contact'),
    path('quote-requests/', views.get_quote_requests, name='get_quote_requests'),
    path('add-contactus/', views.add_contact_us, name='get_contact'),
    path('get-contactus/', views.get_contact_us, name='get_contact'),
    path('add-count/', views.add_count, name='get_contact'),
    path('get-count/', views.get_counts, name='get_count'),
    path('get-counts/', views.get_counts_data, name='get_count'),

    path('delete-counts/', views.delete_counts, name='get_count'),
    path('add-home-detail/', views.add_home_detail, name='add-home-detail'),
    path('get-home-detail/', views.get_home_detail, name='get-home-detail'),


   
]