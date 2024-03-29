from rest_framework import serializers




# To be used to as a subclass for fields that will need the 
# following fields data: User as a subclass for the CustomUser
class AbstractSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, 
                               format='hex')
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)


