"""SauceDemo practice personas (public demo credentials, by design).

The personas are a built-in feature of the target app: each one exhibits a
different behavior — normal, locked out, visually broken, or slow. Testing
against them lets this lab exercise failure modes, not just happy paths.
"""

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
PERFORMANCE_GLITCH_USER = "performance_glitch_user"  # documented, not exercised in CI (latency)
PASSWORD = "secret_sauce"

INVALID_USERNAME = "not_a_real_user"
INVALID_PASSWORD = "wrong_password"

LOCKED_OUT_ERROR = "Sorry, this user has been locked out."
INVALID_CREDENTIALS_ERROR = "Username and password do not match any user in this service"
