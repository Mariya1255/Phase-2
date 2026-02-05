import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Get the backend API URL from environment variables
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    // Get the request body
    const body = await request.json();

    // Forward the request to the backend
    const response = await fetch(`${backendUrl}/api/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    // Get the response data
    const data = await response.json();

    // Return the response with the same status code
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error('Signup proxy error:', error);
    return NextResponse.json(
      { error: 'Failed to connect to authentication service' },
      { status: 500 }
    );
  }
}