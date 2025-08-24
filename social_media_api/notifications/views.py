from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .models import Notification
from .serializers import NotificationSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class NotificationListView(generics.ListAPIView):
    """
    API view to retrieve notifications for the authenticated user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    def get_queryset(self):
        """
        Return notifications for the authenticated user, ordered by timestamp (newest first).
        """
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
    
    def list(self, request, *args, **kwargs):
        """
        Override list method to provide additional context about unread notifications.
        """
        queryset = self.get_queryset()
        unread_count = queryset.filter(read=False).count()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'unread_count': unread_count,
                'notifications': serializer.data
            })
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'unread_count': unread_count,
            'notifications': serializer.data
        })


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_as_read(request, notification_id):
    """
    Mark a specific notification as read.
    """
    try:
        notification = Notification.objects.get(
            id=notification_id, 
            recipient=request.user
        )
        notification.read = True
        notification.save()
        
        return Response({
            'message': 'Notification marked as read',
            'notification_id': notification_id
        }, status=status.HTTP_200_OK)
        
    except Notification.DoesNotExist:
        return Response({
            'error': 'Notification not found'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_as_read(request):
    """
    Mark all notifications for the authenticated user as read.
    """
    updated_count = Notification.objects.filter(
        recipient=request.user,
        read=False
    ).update(read=True)
    
    return Response({
        'message': f'{updated_count} notifications marked as read',
        'updated_count': updated_count
    }, status=status.HTTP_200_OK)
