// Replace your-framework with the framework you are using (e.g., react-webpack5, vue3-vite)
// import { StorybookConfig } from '@storybook/react';

const config = {
  // Required
  framework: '@storybook/react-webpack5',
  stories: ['../stories/**/*.mdx', '../stories/**/*.stories.@(js|jsx|ts|tsx)'],
  // Optional
  addons: ['@storybook/addon-essentials', '@storybook/addon-actions', "storybook-addon-react-router-v6"],
  docs: {
    autodocs: 'tag',
  },
  staticDirs: [],
  core: { disableTelemetry: true, }
};

export default config;