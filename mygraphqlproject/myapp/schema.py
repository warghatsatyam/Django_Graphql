
import graphene
from graphene_django import DjangoObjectType
from .models import Post,Comment

class PostType(DjangoObjectType):
    class Meta:
        model = Post


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType,id=graphene.Int())
    all_comments = graphene.List(CommentType)

    def resolve_all_posts(self,info):
        return Post.objects.all()
    
    def resolve_post(self,info,id):
        return Post.objects.get(pk=id)
    
    def resolve_all_comments(self,info):
        return Comment.objects.all()
    


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
    

class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required    = True)
        author  = graphene.String(required = True)
        content = graphene.String(required = True)

    comment = graphene.Field(CommentType)

    def mutate(self,info,post_id,author,content):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Exception("Post with the given id is not not available")
        comment = Comment(post=post,author=author,content=content)
        comment.save()
        return CreateComment(comment = comment)

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()


# myapp/schema.py

schema = graphene.Schema(query=Query, mutation=Mutation)
