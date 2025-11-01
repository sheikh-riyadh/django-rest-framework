from rest_framework import serializers
from decimal import Decimal
from product.models import Category,Product,Review


# This is called "Serializer"
class CategoriesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()



# This is called "Serializer"
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    stock = serializers.IntegerField()
    image = serializers.ImageField()
    price_with_tax = serializers.SerializerMethodField(method_name='calculate')

    # If we want to show all the properties of category we can use "Custom CategorySerializer which is applied in the below"
    category = CategoriesSerializer()

    #If we want to show only name we should use "serializers.StringRelatedField" this method
    category_name_only = serializers.StringRelatedField(source='category')

    # If we want to show related primary key we should use "serializers.PrimaryKeyRelatedField"

    category_primary_key = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all(), source='category')
    
    category_link = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(),
        view_name='category',
        source = 'category'
    )




    def calculate(self, product):
        return round(product.price * Decimal(1.1))



# This is called "Model Serializer"
class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']

    product_count = serializers.IntegerField(read_only=True)


# This is called "Model Serializer"
class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'stock']
   
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    def validate_price(self, price): # This is call "Field validation"
        if price < 0:
            raise serializers.ValidationError('Price could not negative number')
        else:
            return price



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
            
        except Product.DoesNotExist:
            raise serializers.ValidationError('Invalid product ID')
        
        return Review.objects.create(product=product **validated_data)
            
