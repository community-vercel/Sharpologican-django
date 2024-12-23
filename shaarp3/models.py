from django.db import models

# Create your models here.
class Service(models.Model):
    title = models.CharField(max_length=655)
    slug = models.CharField(max_length=655)

    description = models.TextField()
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    detailed_description = models.TextField()
    image2 = models.ImageField(upload_to='services/', blank=True, null=True)


class ServiceDetail(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='details')
    image_1 = models.ImageField(upload_to='service_details/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='service_details/', blank=True, null=True)
    moretitle = models.TextField()
    detail = models.TextField()
    detail2 = models.TextField()
    metaname=models.CharField(max_length=777,null=True)
    metadescription=models.CharField(max_length=787,null=True)
    keywords=models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Details for {self.service.title}"
    
class AboutUs(models.Model):
    heading = models.CharField(max_length=3255)
    slug = models.CharField(max_length=655)
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    description = models.TextField()
    first_title = models.CharField(max_length=3255)
    second_title = models.CharField(max_length=3255)
    first_description = models.TextField()
    second_description = models.TextField()

    def __str__(self):
        return self.heading
class Portfolio(models.Model):
    title = models.CharField(max_length=3255)
    slug = models.CharField(max_length=655)
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    heading = models.CharField(max_length=3255)
    text_button = models.CharField(max_length=100)
    link = models.URLField(max_length=3255)
    description=models.TextField( blank=True, null=True)
    image2 = models.ImageField(upload_to='portfolio/', blank=True, null=True)

    def __str__(self):
        return self.title

class portfolioDetail(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='details')
    heading = models.CharField(max_length=655)
    title=models.CharField(max_length=9955, blank=True, null=True)
    branch = models.CharField(max_length=655)
    types = models.CharField(max_length=655)
    progam = models.CharField(max_length=655)
    facebook = models.URLField(max_length=3255, blank=True, null=True)
    linkedin = models.URLField(max_length=3255, blank=True, null=True)
    instagram = models.URLField(max_length=3255, blank=True, null=True)
    x = models.URLField(max_length=3255, blank=True, null=True)
    detail = models.TextField()
    metaname=models.CharField(max_length=777,null=True)
    metadescription=models.CharField(max_length=777,null=True)
    keywords=models.TextField(blank=True, null=True)
    def __str__(self):
        return f"Details for {self.portfolio.title}"
    
class Team(models.Model):
    name = models.CharField(max_length=3255)
    slug = models.CharField(max_length=655)
    description=models.TextField( blank=True, null=True)
    title = models.CharField(max_length=3255)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    index = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Testimonial(models.Model):
    name = models.CharField(max_length=3255)
    slug = models.CharField(max_length=655)
    metaname=models.CharField(max_length=777,null=True)
    metadescription=models.CharField(max_length=777,null=True)
    keywords=models.TextField(blank=True, null=True)
    
    title = models.CharField(max_length=3255)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return self.name
class News(models.Model):
    title = models.CharField(max_length=7955)
    slug = models.CharField(max_length=655)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    description=models.TextField( blank=True, null=True)
    image2 = models.ImageField(upload_to='news/', blank=True, null=True)


    def __str__(self):
        return self.title

class newsDetail(models.Model):
    metaname=models.CharField(max_length=777,null=True)
    metadescription=models.CharField(max_length=787,null=True)
    keywords=models.TextField(blank=True, null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='details')
    detail = models.TextField()
    author = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"Details for {self.news.title}"
    
class Contact(models.Model):
    slug = models.CharField(max_length=655)
    contact_image = models.ImageField(upload_to='contact/', blank=True, null=True)
    client_image = models.ImageField(upload_to='contact/', blank=True, null=True)
    heading=models.TextField( blank=True, null=True)
    heading3=models.TextField( blank=True, null=True)

    def __str__(self):
        return self.slug
class Client(models.Model):
    slug = models.CharField(max_length=655)
    client_image = models.ImageField(upload_to='client/', blank=True, null=True)


    def __str__(self):
        return self.slug
    
class QuoteRequest(models.Model):
    
    first_name = models.CharField(max_length=2255)
    last_name = models.CharField(max_length=2355)
    area_code = models.CharField(max_length=5, blank=True, null=True)
    phone_number = models.CharField(max_length=85)
    email = models.EmailField()
    company_name = models.CharField(max_length=2255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    services_required = models.JSONField(default=list)  # To store selected services as a list
    project_overview = models.TextField(blank=True, null=True)
    budget = models.CharField(max_length=2655, blank=True, null=True)
    ready_to_start = models.CharField(max_length=2055, blank=True, null=True)

    def __str__(self):
        return f"Quote request from {self.first_name} {self.last_name}"
    
class ContactUs(models.Model):
    metaname=models.CharField(max_length=777,null=True)
    metadescription=models.CharField(max_length=777,null=True)
    keywords=models.TextField(blank=True, null=True)
 
    detail = models.TextField()
    detail2 = models.TextField()
    detail3= models.TextField()

class Counts(models.Model):
   
    title = models.TextField()
    num = models.TextField()
    description= models.TextField()
    
    
class HomeDetail(models.Model):
    metaname = models.CharField(max_length=777, null=True)
    metadescription = models.CharField(max_length=787, null=True)
    keywords = models.TextField(blank=True, null=True)
    metanamecontact = models.CharField(max_length=777, null=True)
    metadescriptioncontact = models.CharField(max_length=787, null=True)
    keywordscontact = models.TextField(blank=True, null=True)
    metanamequote = models.CharField(max_length=777, null=True)
    metadescriptionquote = models.CharField(max_length=787, null=True)
    keywordsquote = models.TextField(blank=True, null=True)
    heading = models.TextField()
    detail = models.TextField()
    footeremail = models.TextField()
    footeremail2 = models.TextField()

    def __str__(self):
        return self.metaname if self.metaname else 'Home Detail'


    