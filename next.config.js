/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',  // Enable static exports
  distDir: 'out',    // Change the output directory to 'out'
  trailingSlash: true, // Add trailing slashes for better static file serving
  images: {
    unoptimized: true, // For static export
  },
}

module.exports = nextConfig 