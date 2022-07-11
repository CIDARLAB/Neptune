const MonacoEditorPlugin = require('monaco-editor-webpack-plugin')

module.exports = {
  lintOnSave: true,
  plugins: [
    new MonacoEditorPlugin({
      // https://github.com/Microsoft/monaco-editor-webpack-plugin#options
      // Include a subset of languages support
      // Some language extensions like typescript are so huge that may impact build performance
      // e.g. Build full languages support with webpack 4.0 takes over 80 seconds
      // Languages are loaded on demand at runtime
      languages: ['verilog', 'css', 'html', 'typescript']
    })
  ],
  rules: [
    {
      test: /\.vue$/,
      exclude: /node_modules/,
      loader: "eslint-loader",
      options: {
        emitWarning: true,
        failOnError: false
      }
    }
  ]
}