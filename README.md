# Blackjack API

## API Routing
### Authentication 
 
    api/auth/registration - Registrating a new user.
        Allowed methods: POST 
        ----------------------
        POST
            Permission:
                AllowAny

            Payload template:
                    "user": {

                        "email": <user_email>,
                        "username": <username>,
                        "password": <password>,

                    }
            
    api/auth/login - Authenticating a user, get JWT key.
        Allowed methods: POST 
        ----------------------
        POST
            Permission:
                AllowAny

            Payload template:
             "user": {
                    "email": <email>,
                    "password": <password>,
                }

### Users
    api/user/ - Getting a specific user or updating their information.
    Allowed methods: GET, PUT
    -------------------------
    GET 
        Permission:
            IsAuthenticated

        Required Header:
            Authorization: Token <jwt_refresh-token>

        Resopnse Example:
            "user": {
                "email": <user_email>,
                "username": <username>,
                "token": <new_token>,
                "balance": <user_current_balance>
            }

    api/user/balance - Getting or updating the balance of a user.
    GET 
        Permission:
            IsAdminUser

        Required Header:
            Authorization: Token <jwt_refresh-token>

        Resopnse Example:
            "user": {
                "balance": <user_current_balance>
            }
    PUT
        Permission:
            IsAdminUser

        Required Header:
            Authorization: Token <jwt_refresh-token>
        
        Required Params: 
            balance=<new_balance>

        Payload template:
            {
                username: <username>
            }

    api/user/confirm_otp - An endpoint for the one-time password confirmation
    Allowed methods: POST
    ---------------------
    POST
        Permission:
            AllowAny
        Payload template:
            {
                "otp":515819
            }
