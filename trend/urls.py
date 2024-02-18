from django.contrib import admin
from django.urls import path, include

from core.api import api_views as core_views
import core

from account.api import api_views as account_views

from game.api import api_views as game_views

from post.api import api_views as post_views

from product.api import api_views as product_views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('account/', include('account.urls', namespace='account')),
    path('game/', include('game.urls', namespace='game')),
    path('post/', include('post.urls', namespace='post')),
    path('product/', include('product.urls', namespace='product')),
    path('reward/', include('reward.urls', namespace='reward')),

    
    path('password-reset/', auth_views.PasswordResetView.as_view(
        form_class = core.forms.CustomPasswordResetForm,
        template_name='core/password_reset.html',
        html_email_template_name = 'core/password_reset_html_email.html',
        subject_template_name = 'core/password_reset_subject.txt',
        from_email = 'support@trend.com'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html',
    ), name='password_reset_confirm'),

    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'core/password_reset_complete.html'
    ), name='password_reset_complete'),

]

# API Endpoints

urlpatterns += [
	path('api/v1/login/', account_views.LoginView.as_view()),
    path('api/v1/logout/', account_views.LogoutView.as_view()),
    path('api/v1/register/', account_views.RegisterView.as_view()),
    path('api/v1/fbregister/', account_views.FacebookRegisterView.as_view()),
    path('api/v1/apple-register/', account_views.AppleRegisterAPIView.as_view()),
    path('api/v1/getverified/', account_views.GetVerifiedAPIView.as_view()),
    path('api/v1/forgotpassword/', account_views.ForgotPasswordAPIView.as_view()),
    path('api/v1/codeverification/', account_views.CodeVerificationAPIView.as_view()),
    path('api/v1/newpassword/', account_views.NewPasswordAPIView.as_view()),
    path('api/v1/updatepassword/', account_views.UpdatePasswordAPIView.as_view()),

    path('api/v1/profile/', core_views.ProfileAPIView.as_view()),
    path('api/v1/profile/follow/', core_views.FollowAPIView.as_view()),
    path('api/v1/profile/followings/', core_views.FollowingsAPIView.as_view()),
    path('api/v1/profile/dp/', core_views.ProfielDPAPIView.as_view()),
    path('api/v1/profile/update/', core_views.ProfileUpdateAPIView.as_view()),
    path('api/v1/getlist/', core_views.GetListAPIView.as_view()),
    path('api/v1/invite/', core_views.InviteAPIView.as_view()),
    path('api/v1/privacy/', core_views.PrivacyAPIView.as_view()),
    path('api/v1/conditions/', core_views.ConditionsAPIView.as_view()),
    path('api/v1/credits/', core_views.CreditsAPIView.as_view()),
    path('api/v1/completed-tours/', core_views.CompletedToursAPIView.as_view()),
    path('api/v1/ongoing-tours/', core_views.RunningToursAPIView.as_view()),

    path('api/v1/classic/', game_views.GameClassicAPIView.as_view()),
    path('api/v1/games/', game_views.GameClassicAPIView.as_view()),
    path('api/v1/event/', game_views.GameEventAPIView.as_view()),
    path('api/v1/game/single/', game_views.GameDetailAPIView),
    path('api/v1/game/join/', game_views.GameJoinAPIView),
    path('api/v1/challenge/', game_views.ChallengeDetailAPIView.as_view()),
    path('api/v1/joinevent/', game_views.JoinEventAPIView.as_view()),
    path('api/v1/submitchallenge/', game_views.SubmitChallengeAPIView.as_view()),
    path('api/v1/ranking/', game_views.RankingAPIView.as_view()),

    path('api/v1/product/', product_views.ProductAPIView.as_view()),
    path('api/v1/product/single/', product_views.ProductDetailView.as_view()),
    path('api/v1/product/buy/', product_views.ProductBuyView.as_view()),

    path('api/v1/post/', post_views.PostView.as_view()),
    path('api/v1/post/single/', post_views.PostDetailView.as_view()),
    path('api/v1/post/user/', post_views.UserPostAPIView),
    path('api/v1/post/create/', post_views.create_post),
    path('api/v1/post/edit/', post_views.edit_post),
    path('api/v1/comment/create/', post_views.create_comment),
    path('api/v1/comment/delete/', post_views.delete_comment),
    path('api/v1/like/', post_views.add_like),
]



handler404 = core.views.handle404
handler500 = core.views.handle500

# For media files like images
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
