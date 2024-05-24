# Blackjack API
path('regist/', RegistrationAPIView.as_view()),
path('user/', UserRetriveUpdateView.as_view()),
path('users/login/', LoginAPIView.as_view()),
path('user/balance', UserBalanceView.as_view())
## API Routing
### Authentication 
    GET
        auth/users/
    
    ### POST