"""
Serializers for recipe API 
"""
from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','name']
        read_only_fields = ['id']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id','name']
        read_only_fields = ['id']

class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id','image']
        read_only_fields = ['id']   
        extra_kwargs = {'image':{'required':'True'}}     

class RecipeSerializer(serializers.ModelSerializer):
    """ Serializers for recipe """
    
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    def _get_or_create_tags(self, tags, recipe):
        """ Handle getting or create tags """
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user = auth_user,  **tag)
            recipe.tags.add(tag_obj)                
    
    def _get_or_create_ingredients(self, ingredients, recipe):
        """ Handle getting or create ingredients """
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            tag_obj, created = Ingredient.objects.get_or_create(user = auth_user,  **ingredient)
            recipe.tags.add(tag_obj)                
    

    def create(self, validated_data):
        """ Create recipe """
        tags = validated_data.pop('tags',[])
        ingredients = validated_data.pop('ingredients',[])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)
        
        return recipe    
    
    def update(self, instance, validated_data):
        """ Update Recipe """
        tags = validated_data.pop('tags', None)
        ingredients = validated_data.pop('ingredient', None)

        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)
        
        if ingredients is not None:
            instance.ingredients.clear()
            self._get_or_create_ingredients(ingredients, instance)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance 

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags', 'ingredients']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """ Serializers for recipe details view """

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

