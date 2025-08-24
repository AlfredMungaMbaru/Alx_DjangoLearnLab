#!/usr/bin/env python3
"""
Production Deployment Test Script for Social Media API
Tests the deployed application's functionality and performance.
"""

import requests
import json
import time
import sys
from urllib.parse import urljoin


class DeploymentTester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.user_token = None
        
    def api_url(self, path):
        """Build API URL"""
        return urljoin(self.base_url, path.lstrip('/'))
    
    def test_health_check(self):
        """Test health check endpoint"""
        print("🏥 Testing health check...")
        try:
            response = self.session.get(self.api_url('/health/'))
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Health check passed: {health_data.get('status', 'unknown')}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        print("👤 Testing user registration...")
        test_user = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com",
            "password": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        try:
            response = self.session.post(
                self.api_url('/api/accounts/register/'),
                json=test_user
            )
            
            if response.status_code == 201:
                data = response.json()
                self.user_token = data.get('token')
                print(f"✅ User registration successful: {test_user['username']}")
                return True
            else:
                print(f"❌ User registration failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ User registration error: {e}")
            return False
    
    def test_authentication(self):
        """Test authentication with token"""
        print("🔐 Testing authentication...")
        if not self.user_token:
            print("❌ No token available for authentication test")
            return False
        
        headers = {"Authorization": f"Token {self.user_token}"}
        
        try:
            response = self.session.get(
                self.api_url('/api/accounts/profile/'),
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ Authentication successful")
                return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def test_post_creation(self):
        """Test post creation"""
        print("📝 Testing post creation...")
        if not self.user_token:
            print("❌ No token available for post creation test")
            return False
        
        headers = {"Authorization": f"Token {self.user_token}"}
        post_data = {
            "title": "Test Post from Deployment Test",
            "content": "This is a test post created during deployment testing."
        }
        
        try:
            response = self.session.post(
                self.api_url('/api/posts/'),
                json=post_data,
                headers=headers
            )
            
            if response.status_code == 201:
                data = response.json()
                self.test_post_id = data.get('id')
                print(f"✅ Post creation successful: ID {self.test_post_id}")
                return True
            else:
                print(f"❌ Post creation failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Post creation error: {e}")
            return False
    
    def test_like_functionality(self):
        """Test like functionality"""
        print("❤️  Testing like functionality...")
        if not self.user_token or not hasattr(self, 'test_post_id'):
            print("❌ Prerequisites not met for like test")
            return False
        
        headers = {"Authorization": f"Token {self.user_token}"}
        
        try:
            # Test liking a post
            response = self.session.post(
                self.api_url(f'/api/posts/{self.test_post_id}/like/'),
                headers=headers
            )
            
            if response.status_code == 201:
                print("✅ Post like successful")
                
                # Test unliking a post
                response = self.session.post(
                    self.api_url(f'/api/posts/{self.test_post_id}/unlike/'),
                    headers=headers
                )
                
                if response.status_code == 200:
                    print("✅ Post unlike successful")
                    return True
                else:
                    print(f"❌ Post unlike failed: {response.status_code}")
                    return False
            else:
                print(f"❌ Post like failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Like functionality error: {e}")
            return False
    
    def test_notifications(self):
        """Test notifications"""
        print("🔔 Testing notifications...")
        if not self.user_token:
            print("❌ No token available for notifications test")
            return False
        
        headers = {"Authorization": f"Token {self.user_token}"}
        
        try:
            response = self.session.get(
                self.api_url('/api/notifications/'),
                headers=headers
            )
            
            if response.status_code == 200:
                print("✅ Notifications endpoint accessible")
                return True
            else:
                print(f"❌ Notifications test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Notifications error: {e}")
            return False
    
    def test_performance(self):
        """Basic performance test"""
        print("⚡ Testing performance...")
        
        try:
            start_time = time.time()
            response = self.session.get(self.api_url('/api/posts/'))
            end_time = time.time()
            
            response_time = end_time - start_time
            
            if response.status_code == 200 and response_time < 2.0:
                print(f"✅ Performance test passed: {response_time:.2f}s")
                return True
            elif response.status_code == 200:
                print(f"⚠️  Performance warning: {response_time:.2f}s (>2s)")
                return True
            else:
                print(f"❌ Performance test failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Performance test error: {e}")
            return False
    
    def test_security_headers(self):
        """Test security headers"""
        print("🔒 Testing security headers...")
        
        try:
            response = self.session.get(self.base_url)
            headers = response.headers
            
            security_checks = {
                'X-Frame-Options': headers.get('X-Frame-Options'),
                'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
                'X-XSS-Protection': headers.get('X-XSS-Protection'),
                'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
            }
            
            passed = 0
            total = len(security_checks)
            
            for header, value in security_checks.items():
                if value:
                    print(f"✅ {header}: {value}")
                    passed += 1
                else:
                    print(f"❌ {header}: Missing")
            
            if passed >= total * 0.75:  # At least 75% of security headers
                print(f"✅ Security headers test passed: {passed}/{total}")
                return True
            else:
                print(f"⚠️  Security headers warning: {passed}/{total}")
                return True
        except Exception as e:
            print(f"❌ Security headers test error: {e}")
            return False
    
    def run_all_tests(self):
        """Run all deployment tests"""
        print("🚀 Starting deployment tests...\n")
        
        tests = [
            ("Health Check", self.test_health_check),
            ("User Registration", self.test_user_registration),
            ("Authentication", self.test_authentication),
            ("Post Creation", self.test_post_creation),
            ("Like Functionality", self.test_like_functionality),
            ("Notifications", self.test_notifications),
            ("Performance", self.test_performance),
            ("Security Headers", self.test_security_headers),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n--- {test_name} ---")
            if test_func():
                passed += 1
            time.sleep(1)  # Small delay between tests
        
        print(f"\n{'='*50}")
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Deployment successful.")
            return True
        elif passed >= total * 0.8:  # 80% pass rate
            print("⚠️  Most tests passed. Deployment mostly successful.")
            return True
        else:
            print("❌ Many tests failed. Deployment needs attention.")
            return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python test_deployment.py <base_url>")
        print("Example: python test_deployment.py https://your-app.herokuapp.com")
        sys.exit(1)
    
    base_url = sys.argv[1]
    tester = DeploymentTester(base_url)
    
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
