class OverloadError(Exception):
    """Raised when system resources are overloaded and operation cannot proceed safely."""
    def __init__(self, message="System overload detected - operation cancelled for safety", resource_type=None, current_value=None, threshold=None):
        self.resource_type = resource_type
        self.current_value = current_value
        self.threshold = threshold
        super().__init__(message)
