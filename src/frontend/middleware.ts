import { NextRequest, NextResponse } from "next/server";

const TOKEN_COOKIE = "pathpilot.token";
const PROTECTED = ["/dashboard", "/skills", "/roadmap", "/upload", "/chat", "/analytics"];
const AUTH_PAGES = ["/login", "/register"];

export function middleware(req: NextRequest) {
  const { pathname } = req.nextUrl;
  // We mirror the localStorage token into a cookie via client effect (see AuthProvider),
  // so middleware can perform a hard redirect on first paint.
  const token = req.cookies.get(TOKEN_COOKIE)?.value;

  if (PROTECTED.some((p) => pathname === p || pathname.startsWith(p + "/")) && !token) {
    const url = req.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("next", pathname);
    return NextResponse.redirect(url);
  }

  if (AUTH_PAGES.includes(pathname) && token) {
    const url = req.nextUrl.clone();
    url.pathname = "/dashboard";
    return NextResponse.redirect(url);
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/skills/:path*", "/roadmap/:path*", "/upload/:path*", "/chat/:path*", "/analytics/:path*", "/login", "/register"],
};