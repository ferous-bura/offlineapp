from basesdk.resource import List, Find, Create, Post, Update, Replace, Resource

class SOCIAL_LOGIN(List, Find, Create, Post, Replace):

    path = 'social-login/'

    def auth_user(self):
        pass

class SOCIAL_REGISTRATION(List, Find, Create, Post, Replace):
    path = 'social-register/'
    # redirect to the super website
    pass

# redirect to oauth social site, 
# login
# approve the 3rd party to access own info
# send access token to the 3rd party
# then using the token the 3rd party fetches users info
# then it logs in or register the user using the infos

# next time user comes back it will use the token to sign the user in or what ever
