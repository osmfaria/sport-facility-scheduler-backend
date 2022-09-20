from rest_framework.exceptions import ValidationError
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from reviews.permissions import ReviewCustomPermission
from reviews.serializers import ReviewSerializer
from reviews.models import Review
from courts.models import Court


class ReviewView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [ReviewCustomPermission]

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    lookup_url_kwarg = ["court_id", "review_id"]


    def get_queryset(self):
        court = Court.objects.get(id=self.kwargs['court_id'])
        return court.reviews
    

    def perform_create(self, serializer):
        court = Court.objects.get(id=self.kwargs['court_id'])
        review_validator = Review.objects.filter(court=court, user=self.request.user)
        if review_validator:
            raise ValidationError({"detail": "User already reviewed that court"})
        serializer.save(user=self.request.user, court=court)
    
    
    def get_object(self):
        review = Review.objects.get(id=self.kwargs['review_id'])
        self.check_object_permissions(self.request, review)
        return review
