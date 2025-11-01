from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product, Category, Review
from product.serializers import ProductModelSerializer, CategoryModelSerializer, ReviewSerializer
from django.db.models import Count
from rest_framework import status
from django.views import View
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from product.product_filter import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from product.pagination import DefaultPagination


# This is call "FUNCTION VIEW"
@api_view()
def view_specific_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return Response(ProductModelSerializer(product).data)

# This is call "FUNCTION VIEW"
@api_view(['GET', 'POST'])
def product_view(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        serializer = ProductModelSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductModelSerializer(data=request.data) # This line call "Deserializer"
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'path not found'}, status=status.HTTP_404_NOT_FOUND)


# This is call "FUNCTION VIEW"
@api_view(['GET', 'PUT', 'DELETE'])
def category_view(request, pk):
    if request.method == 'GET':
        category = get_object_or_404(Category, pk=pk)
        serializer = CategoryModelSerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        category = get_object_or_404(Category, pk=pk)
        serializer = CategoryModelSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message':'No category found'}, status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'DELETE':
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response({'message:':'Category deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    else:
        return Response({'message':'Path not found'}, status=status.HTTP_404_NOT_FOUND)


# This is call "FUNCTION VIEW"
@api_view(['GET', 'POST'])
def categories_view(request):
    if request.method == 'GET':
        categories = Category.objects.annotate(product_count=Count('product')).all()
        serializer = CategoryModelSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CategoryModelSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response({'message':'Unexpacted error occurrence 😥'})

    

# This is call "CLASS VIEW"
@method_decorator(api_view(['GET', 'POST']), name='dispatch')
class Categories_view(View):
    def get(self, request):
        categories = Category.objects.annotate(product_count=Count('product')).all()
        serializer = CategoryModelSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CategoryModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


# This is call "API VIEW"
class CategoryView(APIView):

    def get_category(self,  pk):
        category = get_object_or_404(Category, pk=pk)
        return category

    def get(self, request, pk):
        category = self.get_category(pk=pk)
        serializer = CategoryModelSerializer(category)
        return Response(serializer.data)
    
    def patch(self, request, pk):
        category = self.get_category(pk=pk)
        serializer = CategoryModelSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        category = self.get_category(pk=pk)
        category.delete()
        return Response({'message':'Category deleted successfully'}, status=status.HTTP_200_OK)
    


# This is call Mixin / Generic view this method work for only 'GET' and 'CREATE'
class GenericProductView (ListCreateAPIView):
    def get_queryset(self):
        productsQueryset = Product.objects.select_related('category').all()
        return productsQueryset
    
    def get_serializer_class(self):
        return ProductModelSerializer
    


# This is call ViewSet VIEWSET GIVES US VERIOUS METHOD LIKE: 
# list ( WHICH IS HELP TO GET ALL THE PRODUCTS INTO LIST WORK LIKE GET METHOD)
# create (HELP TO CREATE PRODUCT WORK LIKE POST METHOD)
# retrieve (HELP TO GET SPECIFIC PRODUCT WORK LIKE GET METHOD  ) 
# update (WHICH IS UPDATE SPECIFIC PRODUCT WORK LIKE PUT METHOD) 
# partial_update (WHICH IS WORK LIKE PATCH METHOD)
# destroy  (WHICH IS DELETE SPECIFIC PRODUCT WORK LIKE DELETE METHOD)
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductModelSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price']



    




class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.select_related('product').all()

    def get_queryset(self):
        return self.queryset.filter(product_id=self.kwargs.get('product_pk'))
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs.get('product_pk')}