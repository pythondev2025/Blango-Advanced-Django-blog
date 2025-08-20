from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Tag(models.Model):
  value = models.TextField(max_length=100)

  def __str__(self):
    return self.value
  

class Comment(models.Model):
  creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  content = models.TextField()
  
  # post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
  # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
  
  """
    inspite of these 2 we would write the generic foreign key relation which would be used to relate the any 
    model or class we wanna relate it to, rather than to one specific model, and above had also defect that 
    both can be null and comment would not be related to any model, or either both be filled which is weird.
    So, we use the GFK in order to relate to any model we want. We will just store the cotent object while 
    storing instance in the database and it it will automatically go for the methods of 
    "django.contrib.contenttypes.fields.GenericForeignKey" and store content type by stuff like 
      content_type = ContentType.objects.get_for_model(Post) and object_id = post.id
      GFK is one which is not stored in the database coloumns but ContentType object is stored and object id 
      is stored and when we extract from the database then django will do like:
      "content_type.model_class().objects.get(pk=object_id)"
      or 
      "content_type.get_object_for_this_type(pk=object_id)" 
      and desired object/instance would be returned to us
  """
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField(db_index=True)    # db_index field is added for DB optimization
  # and database queries over this column rather than scanning the whole table
  content_object = GenericForeignKey("content_type", "object_id")

  # add the "created at" and "modified at" fields for Comment as well
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True) 


class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)
  published_at = models.DateTimeField(null=True, blank=True, db_index=True)
  title = models.TextField(max_length=100)
  slug = models.SlugField(unique=True)
  summary = models.TextField(max_length=1500)
  content = models.TextField()
  tags = models.ManyToManyField(Tag, related_name="posts")
  comments = GenericRelation(Comment)

  def __str__(self):
    return self.title


class AuthorProfile(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
  bio = models.TextField()

  def __str__(self):
    return f"{self.user}'s {self.__class__.__name__}"
