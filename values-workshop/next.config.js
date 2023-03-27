/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: "/api/activity",
        destination: "http://localhost:8080/api/activity",
      },
    ];
  }
}

module.exports = nextConfig
