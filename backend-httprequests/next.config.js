/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'standalone',
  async rewrites() {
    return [
      {
        source: "/api/activity",
        destination: "http://localhost:6071/api/activity",
      },
    ];
  }
}

module.exports = nextConfig

