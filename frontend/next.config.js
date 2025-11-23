/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",

  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY || "",   // Prevent missing-key error
  },

  async headers() {
    return [
      {
        source: "/api/:path*",
        headers: [
          { key: "Access-Control-Allow-Origin", value: "*" },
          { key: "Access-Control-Allow-Methods", value: "GET, POST, PUT, DELETE, OPTIONS" },
          { key: "Access-Control-Allow-Headers", value: "Content-Type, Authorization" },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
