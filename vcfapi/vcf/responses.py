class VCFUserInformationResponses():

    def get_user_information_success(self, data):

         return {
                "status": "SUCCESS",
                "message": "Successully fetched user information",
                "data": data
            }
    
    def get_user_information_error(self, data, message=None):
        try:
            return {
                "status": "FAILED",
                "message": "Unable to get user information",
                "data": data
            }
        except Exception:
            if message:
                return {
                    "status": "FAILED",
                    "message": message
                }
            else:
                return {
                    "status": "FAILED",
                    "message": "Unable to get user information",
                }
            
    def create_user_information_success(self, data):

         return {
                "status": "SUCCESS",
                "message": "Successully created user information",
                "data": data
            }
    
    def create_user_information_error(self, data, message=None):
        try:
            return {
                "status": "FAILED",
                "message": "Unable to create user information",
                "data": data
            }
        except Exception:
            if message:
                return {
                    "status": "FAILED",
                    "message": message
                }
            else:
                return {
                    "status": "FAILED",
                    "message": "Unable to create user information",
                }


