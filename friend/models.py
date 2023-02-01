from django.db import models
from accounts.models import CustomUser,Profile


class Friend(models.Model):
    follower = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='follower')
    followed = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='followed')
    create_date = models.DateTimeField(auto_now_add=True,editable=False)
    delete_date = models.DateTimeField(blank=True,null=True,editable=False)

    def __str__(self):
        return f"{self.follower} -> {self.followed}"

class Room(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='room_messages')
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender')
    msg = models.TextField(blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return self.msg

class Group(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='group_room')
    num = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=120,blank=True,null=True)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='member')
    create_date = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return f"{self.room} in {self.user}"

class Posts(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='post_user')
    posts = models.TextField(max_length=255,blank=True,null=True)
    photo = models.ImageField(upload_to='photo',blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return self.user.nickname
