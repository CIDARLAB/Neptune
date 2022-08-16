module.exports = {
  root: false,
  env: {
    node: true,
  },
  extends: 'vuetify',
  rules: {
    "no-console": "off",
    // 'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
  },
  parserOptions: {
    parser: 'babel-eslint',
  }
}
