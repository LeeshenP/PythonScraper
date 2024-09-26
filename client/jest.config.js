module.exports = {
    transform: {
      '^.+\\.[tj]sx?$': 'babel-jest',
    },
    transformIgnorePatterns: [
      '/node_modules/(?!axios)/', // Make sure Jest transforms axios
    ],
    testEnvironment: 'jsdom',  // For testing React apps
  };
  