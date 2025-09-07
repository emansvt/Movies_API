from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrotling(UserRateThrottle):
    scope = 'review-create'

class ReviewListThrottling(UserRateThrottle):
    scope = 'review-list'