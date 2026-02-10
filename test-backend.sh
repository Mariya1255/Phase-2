#!/bin/bash

echo "========================================"
echo " TESTING BACKEND AFTER FIX"
echo "========================================"
echo ""

echo "Test 1: Check if backend is running..."
response=$(curl -s http://localhost:8000/)
if echo "$response" | grep -q "Todo API"; then
    echo "✓ PASS: Todo API is running"
    echo "  Response: $response"
else
    echo "✗ FAIL: Wrong server or not running"
    echo "  Response: $response"
    exit 1
fi

echo ""
echo "Test 2: Check /docs endpoint..."
docs=$(curl -s http://localhost:8000/docs | head -20)
if echo "$docs" | grep -q "Todo API"; then
    echo "✓ PASS: Swagger docs accessible"
else
    echo "✗ FAIL: Swagger docs not showing Todo API"
    exit 1
fi

echo ""
echo "Test 3: Check /health endpoint..."
health=$(curl -s http://localhost:8000/health)
if echo "$health" | grep -q "healthy"; then
    echo "✓ PASS: Health check working"
    echo "  Response: $health"
else
    echo "✗ FAIL: Health check failed"
    exit 1
fi

echo ""
echo "Test 4: Verify auth routes exist..."
openapi=$(curl -s http://localhost:8000/openapi.json)
if echo "$openapi" | grep -q "/api/auth/signup"; then
    echo "✓ PASS: Auth signup route exists"
else
    echo "✗ FAIL: Auth signup route missing"
    exit 1
fi

if echo "$openapi" | grep -q "/api/auth/signin"; then
    echo "✓ PASS: Auth signin route exists"
else
    echo "✗ FAIL: Auth signin route missing"
    exit 1
fi

echo ""
echo "Test 5: Verify todos routes exist..."
if echo "$openapi" | grep -q "/api/todos"; then
    echo "✓ PASS: Todos routes exist"
else
    echo "✗ FAIL: Todos routes missing"
    exit 1
fi

echo ""
echo "========================================"
echo " ALL TESTS PASSED!"
echo "========================================"
echo ""
echo "Backend is ready. You can now:"
echo "1. Open http://localhost:8000/docs to see API documentation"
echo "2. Test signup: http://localhost:3000/signup"
echo "3. Test signin: http://localhost:3000/signin"
