import { NextRequest, NextResponse } from 'next/server';

// Middleware to handle authentication and 401 responses
export function middleware(request: NextRequest) {
  // Check if this is an API route that requires authentication
  if (request.nextUrl.pathname.startsWith('/api/protected')) {
    // Get the authorization header from the request
    const authHeader = request.headers.get('authorization');

    // If no auth header, redirect to sign-in
    if (!authHeader) {
      // For API routes, return a 401 response instead of redirecting
      if (request.nextUrl.pathname.startsWith('/api/')) {
        return new NextResponse(
          JSON.stringify({ error: 'Unauthorized: Missing authentication token' }),
          { status: 401, headers: { 'content-type': 'application/json' } }
        );
      }

      // For non-API routes, redirect to sign-in page
      return NextResponse.redirect(new URL('/signin', request.url));
    }

    // If auth header exists but doesn't start with 'Bearer ', it's malformed
    if (!authHeader.startsWith('Bearer ')) {
      if (request.nextUrl.pathname.startsWith('/api/')) {
        return new NextResponse(
          JSON.stringify({ error: 'Unauthorized: Invalid token format' }),
          { status: 401, headers: { 'content-type': 'application/json' } }
        );
      }

      return NextResponse.redirect(new URL('/signin', request.url));
    }

    // Extract the token
    const token = authHeader.substring(7); // Remove 'Bearer ' prefix

    // In a real implementation, you'd validate the JWT here
    // For now, we'll just check if it exists
    if (!token) {
      if (request.nextUrl.pathname.startsWith('/api/')) {
        return new NextResponse(
          JSON.stringify({ error: 'Unauthorized: Invalid token' }),
          { status: 401, headers: { 'content-type': 'application/json' } }
        );
      }

      return NextResponse.redirect(new URL('/signin', request.url));
    }
  }

  // Allow the request to continue for non-protected routes
  return NextResponse.next();
}

// Define which paths the middleware should run on
export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
    '/api/protected/:path*',  // Apply to protected API routes
  ],
};