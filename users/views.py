import requests
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from users.models import CustomUser
from .models import Invitation
from .serializers import InvitationSerializer
from django.core.mail import send_mail
from django.conf import settings
import secrets
from django.utils import timezone
from datetime import timedelta
from .permissions import IsOwnerOrManager, IsVerified, IsSelf
from rest_framework import permissions
from .serializers import CustomUserDetailsSerializer
# Create your views here.


# For admins, owners and managers only.
class ListAccounts(generics.ListAPIView):
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsVerified, IsOwnerOrManager]

    def get_queryset(self):
        user = self.request.user
        if user.position == 'owner':
            return CustomUser.objects.filter(company=user.company)
        elif user.position == 'manager':
            return CustomUser.objects.filter(company=user.company)


class DetailAccount(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsVerified, IsSelf]


class CustomEmailConfirmView(APIView):

    def get(self, request, key):
        verify_email_url = 'http://localhost:8000/api/dj-rest-auth/registration/verify-email/'

        # make a POST request to the verify-email endpoint with the key
        response = requests.post(verify_email_url, {'key': key})
        if response.status_code == 200:
            # Update the user's verified status in the database
            user = CustomUser.objects.get(email=request.user.email)
            user.verified = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email verification failed'}, status=status.HTTP_400_BAD_REQUEST)


# Send invitation from a company manager to a user to be a new employee.
class InviteUserView(generics.CreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsVerified, IsOwnerOrManager]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = CustomUser.objects.get(
                    email=serializer.validated_data.get('recipient_email'))
            except CustomUser.DoesNotExist:
                return Response({'error': 'Invalid recipient email'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.validated_data['sender'] = request.user
            invitation = serializer.save()
            # Generate a unique token for the invitation
            token = secrets.token_urlsafe(32)
            invitation.token = token
            invitation.save()

            # Send invitation email to the recipient with the token in the acceptance link
            subject = 'Invitation to join our company'
            message = f'You have been invited to join our company by {invitation.sender}. Click the link to accept the invitation: http://127.0.0.1:8000/api/invite/{token}/accept \n Note that the link expires in 2 days'
            recipient_email = serializer.validated_data.get('recipient_email')

            send_mail(subject, message, invitation.sender.email,
                      [recipient_email])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptInvitationView(APIView):
    def get(self, request, token):
        try:
            invitation = Invitation.objects.get(token=token)
        except Invitation.DoesNotExist:
            return Response({'message': 'Invitation not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        try:
            if invitation.recipient_email == user.email:
                if invitation.accepted:
                    return Response({'message': 'Invitation already accepted'}, status=status.HTTP_400_BAD_REQUEST)

                created_time = invitation.created_at
                current_time = timezone.now()
                time_difference = current_time - created_time

                if time_difference.days >= 2:
                    return Response({'message': 'Cannot accept the invitation after 2 days.\nAsk the manager/owner to resend the invitation.'}, status=status.HTTP_400_BAD_REQUEST)
                invitation.accepted = True
                invitation.save()
                if invitation.sender.company:
                    user.company = invitation.sender.company
                    user.manager = invitation.sender
                    user.save()

                    company = invitation.sender.company
                    company.employee_count += 1
                    company.save()
                    return Response({'message': 'Invitation accepted successfully'}, status=status.HTTP_200_OK)

                return Response({'message': 'Something went wrong! Maybe the sender is not a manager in a company yet.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message': 'Invalid token for accepting the invitation'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


# User = get_user_model()


# class NewEmailConfirmation(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         user = get_object_or_404(User, email=request.data['email'])
#         emailAddress = EmailAddress.objects.filter(
#             user=user, verified=True).exists()

#         if emailAddress:
#             return Response({'message': 'This email is already verified'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             try:
#                 send_email_confirmation(request, user=user)
#                 return Response({'message': 'Email confirmation sent'}, status=status.HTTP_201_CREATED)
#             except APIException:
#                 return Response({'message': 'This email does not exist, please create a new account'}, status=status.HTTP_403_FORBIDDEN)

    # def perform_create(self, serializer):
    #     try:
    #         user = CustomUser.objects.get(
    #             email=serializer.validated_data.get('recipient_email'))
    #     except CustomUser.DoesNotExist:
    #         print("I AM ERROR ##############")
    #         return Response({'message': 'Invalid recipient email'}, status=status.HTTP_404_NOT_FOUND)
    #     invitation = serializer.save()

    #     # Generate a unique token for the invitation
    #     token = secrets.token_urlsafe(32)
    #     invitation.token = token
    #     invitation.save()

    #     # Send invitation email to the recipient with the token in the acceptance link
    #     subject = 'Invitation to join our company'
    #     message = f'You have been invited to join our company by {invitation.sender}. Click the link to accept the invitation: http://127.0.0.1:8000/api/invite/{token}/accept \n Note that the link expires in 2 days'
    #     recipient_email = serializer.validated_data.get('recipient_email')

    #     send_mail(subject, message, invitation.sender.email, [recipient_email])
