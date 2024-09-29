
import graphene
from graphene_django import DjangoObjectType
from .models import Post

class PostType(DjangoObjectType):
    class Meta:
        model = Post


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType,id=graphene.Int())

    def resolve_all_posts(self,info):
        return Post.objects.all()
    
    def resolve_post(self,info,id):
        return Post.objects.get(pk=id)
    


# myapp/schema.py

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, title, content):
        post = Post(title=title, content=content)
        post.save()
        return CreatePost(post=post)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()


# myapp/schema.py

schema = graphene.Schema(query=Query, mutation=Mutation)
