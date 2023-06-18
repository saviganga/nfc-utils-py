class JWTResponses:

    def jwtauthsuccess(self, data):

        return {
            "status": "SUCCESS",
            "message": "Login successful",
            "data": data,
        }

    def jwtautherror(self):

        return {
            "status": "FAILED",
            "message": "Incorrect login credentials, please check username and password and try again.",
        }






xauth_responses = JWTResponses()
        