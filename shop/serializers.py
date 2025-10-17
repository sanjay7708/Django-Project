from rest_framework import serializers
from . models import (Category,Product,Variation,ProductImage,Cart,cartItem,
                      Address,Order,OrderItem,ContactForm)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'


class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Variation
        fields='__all__'


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields='__all__'


class ProductSerializer(serializers.ModelSerializer):
    variations=VariationSerializer(many=True,read_only=True)
    images=ProductImageSerializers(many=True,read_only=True)
    category=CategorySerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields='__all__'
class CartItemSerializer(serializers.ModelSerializer):
    # For writes → expect just IDs
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    variation = serializers.PrimaryKeyRelatedField(
        queryset=Variation.objects.all(),
        required=False,
        allow_null=True
    )

    # For reads → return full nested info
    product_detail = ProductSerializer(source="product", read_only=True)
    variation_detail = VariationSerializer(source="variation", read_only=True)

    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = cartItem
        fields = [
            "id",
            "product",         # input only (ID)
            "variation",       # input only (ID)
            "product_detail",  # output only (full object)
            "variation_detail",# output only (full object)
            "quantity",
            "subtotal",
        ]
    def create(self, validated_data):
        """Ensure we always save and return an actual instance (not dict)."""
        return cartItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Allow updating quantity/variation etc."""
        
        
        
        instance.product = validated_data.get("product", instance.product)
        instance.variation = validated_data.get("variation", instance.variation)
        instance.quantity=validated_data.get("quantity", instance.quantity)
        instance.save()
        return instance

    def get_subtotal(self, obj):
        price = obj.variation.price if obj.variation else obj.product.base_price
        return obj.quantity * float(price)

class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    total=serializers.SerializerMethodField()
    total_items=serializers.SerializerMethodField()
    class Meta:
        model=Cart
        fields = ['id', 'user', 'items', 'total', 'total_items', 'created_at']

    def get_total(self, obj):
        return obj.total
    def get_total_items(self,obj):
        return obj.total_items
    

class AddressSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')

    class Meta:
        model=Address
        fields='__all__'
        

class OrderItemSerializer(serializers.ModelSerializer):
    variation_type=serializers.CharField(source='variation.variation_type',read_only=True)
    variation_value=serializers.CharField(source='variation.value',read_only=True)
    product_image=ProductImageSerializers(source='product.images',many=True,read_only=True)
    product_slug=serializers.ReadOnlyField(source='product.slug')
    variation = serializers.PrimaryKeyRelatedField( queryset=Variation.objects.all(), required=False, allow_null=True )
    class Meta: 
        model=OrderItem
        fields=['id',"product_slug","variation","variation_value","variation_type","status",'quantity',"price","product_image"] 
        read_only_fields=["variation_value","variation_type",'product_image']
    

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True,read_only=True)
    items_input=serializers.ListField(child=serializers.DictField(),write_only=True)
    address_id=serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(),write_only=True,required=False)
    address=AddressSerializer(read_only=True)
    class Meta:
        model=Order
        fields=["id","user","created_at","total_price","items","items_input","address_id",'address']
        read_only_fields=["id","user","created_at","total_price","items",'address']

    def create(self, validated_data):
        items_data = validated_data.pop('items_input')
        address = validated_data.pop("address_id", None)
        user = self.context['request'].user
        validated_data.pop("user", None)
    
        # address handling
        if not address:
            address = Address.objects.filter(user=user, is_default=True).first()
    
        if not address:
            raise serializers.ValidationError("No delivery Address available")
    
        # create order
        order = Order.objects.create(user=user, address=address, **validated_data)
    
        # create order items
        for item in items_data:
            product = Product.objects.get(id=item["product"])
            quantity = item.get("quantity", 1)
    
            variation = None
            price = product.base_price  # fallback to product price
    
            if "variation" in item and item["variation"]:
                variation = Variation.objects.get(id=item["variation"])
                if variation.price:  # use variation price if it exists
                    price = variation.price
    
            OrderItem.objects.create(
                order=order,
                product=product,
                variation=variation,
                quantity=quantity,
                price=price
            )
    
        order.calculated_total()
        return order
    
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model=ContactForm
        fields='__all__'