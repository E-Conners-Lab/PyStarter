from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class PasswordResetThrottle(AnonRateThrottle):
    rate = "5/hour"


class CodeExecutionThrottle(UserRateThrottle):
    rate = "60/minute"
