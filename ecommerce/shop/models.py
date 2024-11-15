from django.db import models

class Categories(models.Model):
    name=models.CharField(max_length=20)
    description=models.TextField()
    image=models.ImageField(upload_to='image')

    def __str__(self):
        return self.name

class product(models.Model):
    name=models.CharField(max_length=20)
    desc=models.TextField()
    image=models.ImageField(upload_to="product")
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    available=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)  #one time
    updated=models.DateTimeField(auto_now=True)      #change every time we update record
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
