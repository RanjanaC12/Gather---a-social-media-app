from django.db import models

class Users_table(models.Model):
  username = models.CharField(max_length=255,unique=True)
  email = models.CharField(max_length=255,unique=True,null=False,primary_key=True)
  password=models.CharField(max_length=255,null=False)
  college = models.CharField(max_length=255)
  course = models.CharField(max_length=255)
  date = models.DateField()
  gender = models.CharField(max_length=255) 
  images = models.ImageField(upload_to='images',null=False)
  phone = models.CharField(max_length=15,unique=True)
class Posts(models.Model):
  post_id = models.AutoField(primary_key=True)
  email = models.ForeignKey(Users_table,on_delete=models.CASCADE)
  username=models.CharField(null=False,max_length=255)
  date = models.DateField()
  posts = models.FileField(upload_to='posts')
  caption = models.CharField(null=True,max_length=255)
  total_likes = models.BigIntegerField(default=0)
  
class Friends(models.Model):
  fid = models.AutoField(primary_key=True)
  email1=models.ForeignKey(Users_table,on_delete=models.CASCADE)
  email2=models.CharField(max_length=255,null=False)
class Requests(models.Model):
  rid = models.AutoField(primary_key=True)
  email1=models.ForeignKey(Users_table,on_delete=models.CASCADE)
  email2=models.CharField(max_length=255,null=False)
  status=models.CharField(max_length=255,null=False,default='unconfirmed')
class Comments(models.Model):
  cid = models.AutoField(primary_key=True)
  category = models.CharField(max_length=255,null=False)
  comment =models.CharField(max_length=255,null=True)
  post_id=models.ForeignKey(Posts,on_delete=models.CASCADE)
  email=models.ForeignKey(Users_table,on_delete=models.CASCADE)
  date=models.DateField(null=True)


  



